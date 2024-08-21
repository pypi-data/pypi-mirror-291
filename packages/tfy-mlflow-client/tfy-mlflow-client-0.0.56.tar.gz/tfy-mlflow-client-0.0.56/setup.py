import logging
import os
from importlib.machinery import SourceFileLoader

from setuptools import find_packages, setup

_MLFLOW_SKINNY_ENV_VAR = "MLFLOW_SKINNY"
_MLFLOW_FOR_SERVER_ENV_VAR = "MLFLOW_FOR_SERVER"

version = (
    SourceFileLoader("mlflow.version", os.path.join("mlflow", "version.py")).load_module().VERSION
)


# Get a list of all files in the JS directory to include in our module
def package_files(directory):
    paths = []
    for path, _, filenames in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join("..", path, filename))
    return paths


# Prints out a set of paths (relative to the mlflow/ directory) of files in mlflow/server/js/build
# to include in the wheel
alembic_files = [
    "../mlflow/store/db_migrations/alembic.ini",
    "../mlflow/temporary_db_migrations_for_pre_1_users/alembic.ini",
]
extra_files = []

"""
Minimal requirements for the skinny MLflow client which provides a limited
subset of functionality such as: RESTful client functionality for Tracking and
Model Registry, as well as support for Project execution against local backends
and Databricks.
"""
SKINNY_REQUIREMENTS = [
    "setuptools",
    "click>=7.0",
    "entrypoints",
    "GitPython>=2.1.0",
    "PyYAML>=5.1",
    "protobuf>=3.12,<6.0",
    "pytz",
    "requests>=2.17.3",
    "packaging",
    # Automated dependency detection in MLflow Models relies on
    # `importlib_metadata.packages_distributions` to resolve a module name to its package name
    # (e.g. 'sklearn' -> 'scikit-learn'). importlib_metadata 3.7.0 or newer supports this function:
    # https://github.com/python/importlib_metadata/blob/main/CHANGES.rst#v370
    "importlib_metadata>=3.7.0,!=4.7.0",
    "sqlparse>=0.5.0",
    "pydantic>=1.8.2,<3.0.0",
    "tabulate>=0.7.7",
    "oauthlib>=3.1.0",
]

"""
These are the core requirements for the complete MLflow platform, which augments
the skinny client functionality with support for running the MLflow Tracking
Server & UI. It also adds project backends such as Docker among
other capabilities.
"""
CORE_REQUIREMENTS = SKINNY_REQUIREMENTS + [
    "alembic<=1.4.1",
    # Required
    "docker>=4.0.0",
    "fastapi",
    "gunicorn; platform_system != 'Windows'",
    "numpy",
    "scipy",
    "pandas",
    "querystring_parser",
    # Required to run the MLflow server against SQL-backed storage
    "sqlalchemy<2.0.0",
    "waitress; platform_system == 'Windows'",
]

_is_mlflow_skinny = bool(os.environ.get(_MLFLOW_SKINNY_ENV_VAR))
logging.debug("{} env var is set: {}".format(_MLFLOW_SKINNY_ENV_VAR, _is_mlflow_skinny))
_is_for_server = bool(int(os.environ.get(_MLFLOW_FOR_SERVER_ENV_VAR, "0")))
logging.info("{} env var is set: {}".format(_MLFLOW_FOR_SERVER_ENV_VAR, _is_for_server))

if not _is_for_server:
    setup(
        name="tfy-mlflow-client",
        version=version,
        packages=find_packages(
            exclude=[
                "tests",
                "tests.*",
                "mlflow.server",
                "mlflow.server.*",
                "mlflow.store.tracking.sqlalchemy_store",
                "mlflow.store.tracking.dbmodels",
                "mlflow.store.db_migrations",
                "mlflow.store.db_migrations.*",
            ]
        ),
        install_requires=SKINNY_REQUIREMENTS,
        package_data={"mlflow": extra_files},
        zip_safe=False,
    )
else:
    setup(
        name="mlflow" if not _is_mlflow_skinny else "mlflow-skinny",
        version=version,
        packages=find_packages(exclude=["tests", "tests.*"]),
        package_data=({"mlflow": alembic_files + extra_files}),
        install_requires=CORE_REQUIREMENTS if not _is_mlflow_skinny else SKINNY_REQUIREMENTS,
        extras_require={
            "extras": [
                "scikit-learn",
                # Required to log artifacts and models to HDFS artifact locations
                "pyarrow",
                # Required to log artifacts and models to AWS S3 artifact locations
                "boto3",
                # Required to log artifacts and models to GCS artifact locations
                "google-cloud-storage",
                "azureml-core>=1.2.0",
                # Required to serve models through MLServer
                "mlserver>=0.5.3",
                "mlserver-mlflow>=0.5.3",
            ],
            "sqlserver": ["mlflow-dbstore"],
            "aliyun-oss": ["aliyunstoreplugin"],
        },
        entry_points="""
            [console_scripts]
            mlflow=mlflow.cli:cli
        """,
        zip_safe=False,
        author="TrueFoundry",
        description="mloundry-server: TrueFoundry's Experiment Tracking Backend",
        long_description="mloundry-server: TrueFoundry's Experiment Tracking Backend",
        long_description_content_type="text/x-rst",
        license="Apache License 2.0",
        classifiers=["Intended Audience :: Developers", "Programming Language :: Python :: 3.6"],
        keywords="ml ai databricks",
        url="https://mlflow.org/",
        python_requires=">=3.6",
        project_urls={
            "Bug Tracker": "https://github.com/mlflow/mlflow/issues",
            "Documentation": "https://mlflow.org/docs/latest/index.html",
            "Source Code": "https://github.com/mlflow/mlflow",
        },
    )
