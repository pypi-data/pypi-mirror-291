"""
Utilities for dealing with artifacts in the context of a Run.
"""

import os
import posixpath
import urllib.parse

from mlflow.exceptions import MlflowException
from mlflow.protos.databricks_pb2 import INVALID_PARAMETER_VALUE
from mlflow.store.artifact.artifact_repository_registry import get_artifact_repository
from mlflow.tracking._tracking_service.utils import _get_store
from mlflow.utils.file_utils import path_to_local_file_uri
from mlflow.utils.uri import append_to_uri_path


def get_artifact_uri(run_id, artifact_path=None, tracking_uri=None):
    """
    Get the absolute URI of the specified artifact in the specified run. If `path` is not specified,
    the artifact root URI of the specified run will be returned; calls to ``log_artifact``
    and ``log_artifacts`` write artifact(s) to subdirectories of the artifact root URI.

    :param run_id: The ID of the run for which to obtain an absolute artifact URI.
    :param artifact_path: The run-relative artifact path. For example,
                          ``path/to/artifact``. If unspecified, the artifact root URI for the
                          specified run will be returned.
    :param tracking_uri: The tracking URI from which to get the run and its artifact location. If
                         not given, the current default tracking URI is used.
    :return: An *absolute* URI referring to the specified artifact or the specified run's artifact
             root. For example, if an artifact path is provided and the specified run uses an
             S3-backed  store, this may be a uri of the form
             ``s3://<bucket_name>/path/to/artifact/root/path/to/artifact``. If an artifact path
             is not provided and the specified run uses an S3-backed store, this may be a URI of
             the form ``s3://<bucket_name>/path/to/artifact/root``.
    """
    if not run_id:
        raise MlflowException(
            message="A run_id must be specified in order to obtain an artifact uri!",
            error_code=INVALID_PARAMETER_VALUE,
        )

    store = _get_store(tracking_uri)
    run = store.get_run(run_id)
    assert urllib.parse.urlparse(run.info.artifact_uri).scheme != "runs"  # avoid an infinite loop
    if artifact_path is None:
        return run.info.artifact_uri
    else:
        return append_to_uri_path(run.info.artifact_uri, artifact_path)


# TODO: This would be much simpler if artifact_repo.download_artifacts could take the absolute path
# or no path.
def _download_artifact_from_uri(artifact_uri, output_path=None):
    """
    :param artifact_uri: The *absolute* URI of the artifact to download.
    :param output_path: The local filesystem path to which to download the artifact. If unspecified,
                        a local output path will be created.
    """
    if os.path.exists(artifact_uri):
        if os.name != "nt":
            # If we're dealing with local files, just reference the direct pathing.
            # non-nt-based file systems can directly reference path information, while nt-based
            # systems need to url-encode special characters in directory listings to be able to
            # resolve them (i.e., spaces converted to %20 within a file name or path listing)
            root_uri = os.path.dirname(artifact_uri)
            artifact_path = os.path.basename(artifact_uri)
            return get_artifact_repository(artifact_uri=root_uri).download_artifacts(
                artifact_path=artifact_path, dst_path=output_path
            )
        else:  # if we're dealing with nt-based systems, we need to utilize pathname2url to encode.
            artifact_uri = path_to_local_file_uri(artifact_uri)

    parsed_uri = urllib.parse.urlparse(str(artifact_uri))
    prefix = ""
    if parsed_uri.scheme and not parsed_uri.path.startswith("/"):
        # relative path is a special case, urllib does not reconstruct it properly
        prefix = parsed_uri.scheme + ":"
        parsed_uri = parsed_uri._replace(scheme="")

    # For models:/ URIs, it doesn't make sense to initialize a ModelsArtifactRepository with only
    # the model name portion of the URI, then call download_artifacts with the version info.
    if urllib.parse.urlparse(artifact_uri).scheme == "models":
        raise NotImplemented("This implementation was removed!")
    else:
        artifact_path = posixpath.basename(parsed_uri.path)
        parsed_uri = parsed_uri._replace(path=posixpath.dirname(parsed_uri.path))
        root_uri = prefix + urllib.parse.urlunparse(parsed_uri)

    return get_artifact_repository(artifact_uri=root_uri).download_artifacts(
        artifact_path=artifact_path, dst_path=output_path
    )
