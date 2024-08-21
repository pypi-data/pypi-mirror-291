import logging
import sys

import click
from click import UsageError

import mlflow.db
import mlflow.experiments
import mlflow.runs
from mlflow.entities.lifecycle_stage import LifecycleStage
from mlflow.exceptions import MlflowException
from mlflow.server.handler_utils import ensure_dir
from mlflow.store.artifact.artifact_repository_registry import get_artifact_repository
from mlflow.store.tracking import (
    DEFAULT_ARTIFACTS_URI,
    DEFAULT_LOCAL_FILE_AND_ARTIFACT_PATH,
)
from mlflow.tracking import _get_store
from mlflow.utils import cli_args
from mlflow.utils.annotations import experimental
from mlflow.utils.logging_utils import eprint
from mlflow.utils.process import ShellCommandException
from mlflow.utils.uri import resolve_default_artifact_root

_logger = logging.getLogger(__name__)


@click.group()
@click.version_option()
def cli():
    pass


def _validate_server_args(gunicorn_opts=None, workers=None, waitress_opts=None):
    if sys.platform == "win32":
        if gunicorn_opts is not None or workers is not None:
            raise NotImplementedError(
                "waitress replaces gunicorn on Windows, "
                "cannot specify --gunicorn-opts or --workers"
            )
    else:
        if waitress_opts is not None:
            raise NotImplementedError(
                "gunicorn replaces waitress on non-Windows platforms, "
                "cannot specify --waitress-opts"
            )


@cli.command()
@click.option(
    "--backend-store-uri",
    metavar="PATH",
    default=DEFAULT_LOCAL_FILE_AND_ARTIFACT_PATH,
    help="URI to which to persist experiment and run data. Acceptable URIs are "
    "SQLAlchemy-compatible database connection strings "
    "(e.g. 'sqlite:///path/to/file.db') or local filesystem URIs "
    "(e.g. 'file:///absolute/path/to/directory'). By default, data will be logged "
    f"to {DEFAULT_LOCAL_FILE_AND_ARTIFACT_PATH}",
)
@click.option(
    "--default-artifact-root",
    metavar="URI",
    default=None,
    help="Directory in which to store artifacts for any new experiments created. For tracking "
    "server backends that rely on SQL, this option is required in order to store artifacts. "
    "Note that this flag does not impact already-created experiments with any previous "
    "configuration of an MLflow server instance. "
    "If the --serve-artifacts option is specified, the default artifact root is "
    f"{DEFAULT_ARTIFACTS_URI}. Otherwise, the default artifact root is "
    f"{DEFAULT_LOCAL_FILE_AND_ARTIFACT_PATH}.",
)
@cli_args.SERVE_ARTIFACTS
@cli_args.ARTIFACTS_DESTINATION
@cli_args.PORT
@cli_args.HOST
def ui(
    backend_store_uri, default_artifact_root, serve_artifacts, artifacts_destination, port, host
):
    """
    Launch the MLflow tracking UI for local viewing of run results. To launch a production
    server, use the "mlflow server" command instead.

    The UI will be visible at http://localhost:5000 by default, and only accept connections
    from the local machine. To let the UI server accept connections from other machines, you will
    need to pass ``--host 0.0.0.0`` to listen on all network interfaces (or a specific interface
    address).
    """
    from mlflow.server import _run_server
    from mlflow.server.stores import initialize_backend_stores

    # Ensure that both backend_store_uri and default_artifact_uri are set correctly.
    if not backend_store_uri:
        backend_store_uri = DEFAULT_LOCAL_FILE_AND_ARTIFACT_PATH

    default_artifact_root = resolve_default_artifact_root(
        serve_artifacts, default_artifact_root, backend_store_uri, resolve_to_local=True
    )

    try:
        initialize_backend_stores(backend_store_uri, default_artifact_root)
    except Exception as e:
        _logger.error("Error initializing backend store")
        _logger.exception(e)
        sys.exit(1)

    # TODO: We eventually want to disable the write path in this version of the server.
    try:
        _run_server(
            backend_store_uri,
            default_artifact_root,
            serve_artifacts,
            False,
            artifacts_destination,
            host,
            port,
            None,
            1,
        )
    except ShellCommandException:
        eprint("Running the mlflow server failed. Please see the logs above for details.")
        sys.exit(1)


def _validate_static_prefix(ctx, param, value):  # pylint: disable=unused-argument
    """
    Validate that the static_prefix option starts with a "/" and does not end in a "/".
    Conforms to the callback interface of click documented at
    http://click.pocoo.org/5/options/#callbacks-for-validation.
    """
    if value is not None:
        if not value.startswith("/"):
            raise UsageError("--static-prefix must begin with a '/'.")
        if value.endswith("/"):
            raise UsageError("--static-prefix should not end with a '/'.")
    return value


@cli.command()
@click.option(
    "--backend-store-uri",
    metavar="PATH",
    default=DEFAULT_LOCAL_FILE_AND_ARTIFACT_PATH,
    help="URI to which to persist experiment and run data. Acceptable URIs are "
    "SQLAlchemy-compatible database connection strings "
    "(e.g. 'sqlite:///path/to/file.db') or local filesystem URIs "
    "(e.g. 'file:///absolute/path/to/directory'). By default, data will be logged "
    "to the ./mlruns directory.",
)
@cli_args.SERVE_ARTIFACTS
@click.option(
    "--artifacts-only",
    is_flag=True,
    default=False,
    help="If specified, configures the mlflow server to be used only for proxied artifact serving. "
    "With this mode enabled, functionality of the mlflow tracking service (e.g. run creation, "
    "metric logging, and parameter logging) is disabled. The server will only expose "
    "endpoints for uploading, downloading, and listing artifacts. "
    "Default: False",
)
@cli_args.ARTIFACTS_DESTINATION
@cli_args.HOST
@cli_args.PORT
@cli_args.WORKERS
@click.option(
    "--static-prefix",
    default=None,
    callback=_validate_static_prefix,
    help="A prefix which will be prepended to the path of all static paths.",
)
@click.option(
    "--gunicorn-opts",
    default=None,
    help="Additional command line options forwarded to gunicorn processes.",
)
@click.option(
    "--waitress-opts", default=None, help="Additional command line options for waitress-serve."
)
@click.option(
    "--expose-prometheus",
    default=None,
    help="Path to the directory where metrics will be stored. If the directory "
    "doesn't exist, it will be created. "
    "Activate prometheus exporter to expose metrics on /metrics endpoint.",
)
def server(
    backend_store_uri,
    serve_artifacts,
    artifacts_only,
    artifacts_destination,
    host,
    port,
    workers,
    static_prefix,
    gunicorn_opts,
    waitress_opts,
    expose_prometheus,
):
    """
    Run the MLflow tracking server.

    The server which listen on http://localhost:5000 by default, and only accept connections
    from the local machine. To let the server accept connections from other machines, you will need
    to pass ``--host 0.0.0.0`` to listen on all network interfaces
    (or a specific interface address).
    """
    from mlflow.server import _run_server
    from mlflow.server.stores import initialize_backend_stores

    _validate_server_args(gunicorn_opts=gunicorn_opts, workers=workers, waitress_opts=waitress_opts)

    # Ensure that both backend_store_uri and default_artifact_uri are set correctly.
    if not backend_store_uri:
        backend_store_uri = DEFAULT_LOCAL_FILE_AND_ARTIFACT_PATH

    # No need of default artifact root env var going forward
    default_artifact_root = "file:/tmp/mlruns"
    # default_artifact_root = resolve_default_artifact_root(
    #     serve_artifacts, default_artifact_root, backend_store_uri
    # )

    try:
        initialize_backend_stores(backend_store_uri, default_artifact_root)
    except Exception as e:
        _logger.error("Error initializing backend store")
        _logger.exception(e)
        sys.exit(1)

    try:
        _run_server(
            backend_store_uri,
            default_artifact_root,
            serve_artifacts,
            artifacts_only,
            artifacts_destination,
            host,
            port,
            static_prefix,
            workers,
            gunicorn_opts,
            waitress_opts,
            expose_prometheus,
        )
    except ShellCommandException:
        eprint("Running the mlflow server failed. Please see the logs above for details.")
        sys.exit(1)


@cli.command(short_help="Permanently delete runs in the `deleted` lifecycle stage.")
@click.option(
    "--backend-store-uri",
    metavar="PATH",
    default=DEFAULT_LOCAL_FILE_AND_ARTIFACT_PATH,
    help="URI of the backend store from which to delete runs. Acceptable URIs are "
    "SQLAlchemy-compatible database connection strings "
    "(e.g. 'sqlite:///path/to/file.db') or local filesystem URIs "
    "(e.g. 'file:///absolute/path/to/directory'). By default, data will be deleted "
    "from the ./mlruns directory.",
)
@click.option(
    "--run-ids",
    default=None,
    help="Optional comma separated list of runs to be permanently deleted. If run ids"
    " are not specified, data is removed for all runs in the `deleted`"
    " lifecycle stage.",
)
@experimental
def gc(backend_store_uri, run_ids):
    """
    Permanently delete runs in the `deleted` lifecycle stage from the specified backend store.
    This command deletes all artifacts and metadata associated with the specified runs.
    """
    backend_store = _get_store(backend_store_uri, None)
    if not hasattr(backend_store, "hard_delete_run"):
        raise MlflowException(
            "This cli can only be used with a backend that allows hard-deleting runs"
        )
    if not run_ids:
        run_ids = backend_store._get_deleted_runs()
    else:
        run_ids = run_ids.split(",")

    for run_id in run_ids:
        run = backend_store.get_run(run_id)
        if run.info.lifecycle_stage != LifecycleStage.DELETED:
            raise MlflowException(
                "Run % is not in `deleted` lifecycle stage. Only runs in "
                "`deleted` lifecycle stage can be deleted." % run_id
            )
        # TODO (chiragjn): ensure_dir is a temporary hack. Better to migrate paths in db
        artifact_repo = get_artifact_repository(ensure_dir(run.info.artifact_uri))
        artifact_repo.delete_artifacts()
        backend_store.hard_delete_run(run_id)
        print("Run with ID %s has been permanently deleted." % str(run_id))


cli.add_command(mlflow.experiments.commands)
cli.add_command(mlflow.runs.commands)
cli.add_command(mlflow.db.commands)

if __name__ == "__main__":
    cli()
