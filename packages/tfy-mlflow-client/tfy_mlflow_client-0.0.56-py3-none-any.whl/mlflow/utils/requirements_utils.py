"""
This module provides a set of utilities for interpreting and creating requirements files
(e.g. pip's `requirements.txt`), which is useful for managing ML software environments.
"""

import logging
import os
import re
import subprocess
from collections import namedtuple
from itertools import chain, filterfalse

import importlib_metadata
import pkg_resources
from packaging.version import InvalidVersion, Version

from mlflow.exceptions import MlflowException

_logger = logging.getLogger(__name__)


def _is_comment(line):
    return line.startswith("#")


def _is_empty(line):
    return line == ""


def _strip_inline_comment(line):
    return line[: line.find(" #")].rstrip() if " #" in line else line


def _is_requirements_file(line):
    return line.startswith("-r ") or line.startswith("--requirement ")


def _is_constraints_file(line):
    return line.startswith("-c ") or line.startswith("--constraint ")


def _join_continued_lines(lines):
    """
    Joins lines ending with '\\'.

    >>> _join_continued_lines["a\\", "b\\", "c"]
    >>> 'abc'
    """
    continued_lines = []

    for line in lines:
        if line.endswith("\\"):
            continued_lines.append(line.rstrip("\\"))
        else:
            continued_lines.append(line)
            yield "".join(continued_lines)
            continued_lines.clear()

    # The last line ends with '\'
    if continued_lines:
        yield "".join(continued_lines)


# Represents a pip requirement.
#
# :param req_str: A requirement string (e.g. "scikit-learn == 0.24.2").
# :param is_constraint: A boolean indicating whether this requirement is a constraint.
_Requirement = namedtuple("_Requirement", ["req_str", "is_constraint"])


def _parse_requirements(requirements, is_constraint):
    """
    A simplified version of `pip._internal.req.parse_requirements` which performs the following
    operations on the given requirements file and yields the parsed requirements.

    - Remove comments and blank lines
    - Join continued lines
    - Resolve requirements file references (e.g. '-r requirements.txt')
    - Resolve constraints file references (e.g. '-c constraints.txt')

    :param requirements: A string path to a requirements file on the local filesystem or
                         an iterable of pip requirement strings.
    :param is_constraint: Indicates the parsed requirements file is a constraint file.
    :return: A list of ``_Requirement`` instances.

    References:
    - `pip._internal.req.parse_requirements`:
      https://github.com/pypa/pip/blob/7a77484a492c8f1e1f5ef24eaf71a43df9ea47eb/src/pip/_internal/req/req_file.py#L118
    - Requirements File Format:
      https://pip.pypa.io/en/stable/cli/pip_install/#requirements-file-format
    - Constraints Files:
      https://pip.pypa.io/en/stable/user_guide/#constraints-files
    """
    if isinstance(requirements, str):
        base_dir = os.path.dirname(requirements)
        with open(requirements) as f:
            requirements = f.read().splitlines()
    else:
        base_dir = os.getcwd()

    lines = map(str.strip, requirements)
    lines = map(_strip_inline_comment, lines)
    lines = _join_continued_lines(lines)
    lines = filterfalse(_is_comment, lines)
    lines = filterfalse(_is_empty, lines)

    for line in lines:
        if _is_requirements_file(line):
            req_file = line.split(maxsplit=1)[1]
            # If `req_file` is an absolute path, `os.path.join` returns `req_file`:
            # https://docs.python.org/3/library/os.path.html#os.path.join
            abs_path = os.path.join(base_dir, req_file)
            yield from _parse_requirements(abs_path, is_constraint=False)
        elif _is_constraints_file(line):
            req_file = line.split(maxsplit=1)[1]
            abs_path = os.path.join(base_dir, req_file)
            yield from _parse_requirements(abs_path, is_constraint=True)
        else:
            yield _Requirement(line, is_constraint)


def _flatten(iterable):
    return chain.from_iterable(iterable)


_NORMALIZE_REGEX = re.compile(r"[-_.]+")


def _normalize_package_name(pkg_name):
    """
    Normalizes a package name using the rule defined in PEP 503:
    https://www.python.org/dev/peps/pep-0503/#normalized-names
    """
    return _NORMALIZE_REGEX.sub("-", pkg_name).lower()


def _get_requires_recursive(pkg_name, top_pkg_name=None) -> set:
    """
    Recursively yields both direct and transitive dependencies of the specified
    package.
    The `top_pkg_name` argument will track what's the top-level dependency for
    which we want to list all sub-dependencies.
    This ensures that we don't fall into recursive loops for packages with are
    dependant on each other.
    """
    if top_pkg_name is None:
        # Assume the top package
        top_pkg_name = pkg_name

    pkg_name = _normalize_package_name(pkg_name)
    if pkg_name not in pkg_resources.working_set.by_key:
        return

    package = pkg_resources.working_set.by_key[pkg_name]
    reqs = package.requires()
    if len(reqs) == 0:
        return

    for req in reqs:
        req_name = _normalize_package_name(req.name)
        if req_name == top_pkg_name:
            # If the top package ends up providing himself again through a
            # recursive dependency, we don't want to consider it as a
            # dependency
            continue

        yield req_name
        yield from _get_requires_recursive(req.name, top_pkg_name)


def _prune_packages(packages):
    """
    Prunes packages required by other packages. For example, `["scikit-learn", "numpy"]` is pruned
    to `["scikit-learn"]`.
    """
    packages = set(packages)
    requires = set(_flatten(map(_get_requires_recursive, packages)))
    return packages - requires


def _run_command(cmd):
    """
    Runs the specified command. If it exits with non-zero status, `MlflowException` is raised.
    """
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate()
    stdout = stdout.decode("utf-8")
    stderr = stderr.decode("utf-8")
    if proc.returncode != 0:
        msg = "\n".join(
            [
                f"Encountered an unexpected error while running {cmd}",
                f"exit status: {proc.returncode}",
                f"stdout: {stdout}",
                f"stderr: {stderr}",
            ]
        )
        raise MlflowException(msg)


def _get_installed_version(package, module=None):
    """
    Obtains the installed package version using `importlib_metadata.version`. If it fails, use
    `__import__(module or package).__version__`.
    """
    try:
        version = importlib_metadata.version(package)
    except importlib_metadata.PackageNotFoundError:
        # Note `importlib_metadata.version(package)` is not necessarily equal to
        # `__import__(package).__version__`. See the example for pytorch below.
        #
        # Example
        # -------
        # $ pip install torch==1.9.0
        # $ python -c "import torch; print(torch.__version__)"
        # 1.9.0+cu102
        # $ python -c "import importlib_metadata; print(importlib_metadata.version('torch'))"
        # 1.9.0
        version = __import__(module or package).__version__

    return version


_MODULES_TO_PACKAGES = None

# Represents the PyPI package index at a particular date
# :param date: The YYYY-MM-DD formatted string date on which the index was fetched.
# :param package_names: The set of package names in the index.
_PyPIPackageIndex = namedtuple("_PyPIPackageIndex", ["date", "package_names"])


def _get_local_version_label(version):
    """
    Extracts a local version label from `version`.

    :param version: A version string.
    """
    try:
        return Version(version).local
    except InvalidVersion:
        return None


def _strip_local_version_label(version):
    """
    Strips a local version label in `version`.

    Local version identifiers:
    https://www.python.org/dev/peps/pep-0440/#local-version-identifiers

    :param version: A version string to strip.
    """

    class IgnoreLocal(Version):
        @property
        def local(self):
            return None

    try:
        return str(IgnoreLocal(version))
    except InvalidVersion:
        return version


def _get_pinned_requirement(package, version=None, module=None):
    """
    Returns a string representing a pinned pip requirement to install the specified package and
    version (e.g. 'mlflow==1.2.3').

    :param package: The name of the package.
    :param version: The version of the package. If None, defaults to the installed version.
    :param module: The name of the top-level module provided by the package . For example,
                   if `package` is 'scikit-learn', `module` should be 'sklearn'. If None, defaults
                   to `package`.
    """
    if version is None:
        version_raw = _get_installed_version(package, module)
        local_version_label = _get_local_version_label(version_raw)
        if local_version_label:
            version = _strip_local_version_label(version_raw)
            msg = (
                "Found {package} version ({version_raw}) contains a local version label "
                "(+{local_version_label}). MLflow logged a pip requirement for this package as "
                "'{package}=={version_logged}' without the local version label to make it "
                "installable from PyPI. To specify pip requirements containing local version "
                "labels, please use `conda_env` or `pip_requirements`."
            ).format(
                package=package,
                version_raw=version_raw,
                version_logged=version,
                local_version_label=local_version_label,
            )
            _logger.warning(msg)

        else:
            version = version_raw

    return f"{package}=={version}"
