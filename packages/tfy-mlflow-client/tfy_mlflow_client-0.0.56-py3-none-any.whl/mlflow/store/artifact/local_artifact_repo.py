import os
import shutil
from typing import Optional

from mlflow.entities import FileInfo
from mlflow.store.artifact.artifact_repo import ArtifactRepository, verify_artifact_path
from mlflow.store.entities import PagedList
from mlflow.utils.file_utils import (
    get_file_info,
    list_all,
    local_file_uri_to_path,
    mkdir,
    relative_path_to_artifact_path,
)


class LocalArtifactRepository(ArtifactRepository):
    """Stores artifacts as files in a local directory."""

    def __init__(
        self, artifact_uri, credentials=None, storage_integration_id=None, *args, **kwargs
    ):
        super().__init__(artifact_uri, *args, **kwargs)
        self._artifact_dir = local_file_uri_to_path(self.artifact_uri)

    @property
    def artifact_dir(self):
        return self._artifact_dir

    def log_artifact(self, local_file, artifact_path=None):
        verify_artifact_path(artifact_path)
        # NOTE: The artifact_path is expected to be in posix format.
        # Posix paths work fine on windows but just in case we normalize it here.
        if artifact_path:
            artifact_path = os.path.normpath(artifact_path)

        artifact_dir = (
            os.path.join(self.artifact_dir, artifact_path) if artifact_path else self.artifact_dir
        )
        if not os.path.exists(artifact_dir):
            mkdir(artifact_dir)
        shutil.copyfile(local_file, os.path.join(artifact_dir, os.path.basename(local_file)))

    def _is_directory(self, artifact_path):
        # NOTE: The path is expected to be in posix format.
        # Posix paths work fine on windows but just in case we normalize it here.
        path = os.path.normpath(artifact_path) if artifact_path else ""
        list_dir = os.path.join(self.artifact_dir, path) if path else self.artifact_dir
        return os.path.isdir(list_dir)

    def log_artifacts(self, local_dir, artifact_path=None):
        # TODO (chiragjn): Replace this will shutil.copytree - distutils has been removed circa Python 3.12
        import distutils.dir_util as dir_util

        verify_artifact_path(artifact_path)
        # NOTE: The artifact_path is expected to be in posix format.
        # Posix paths work fine on windows but just in case we normalize it here.
        if artifact_path:
            artifact_path = os.path.normpath(artifact_path)
        artifact_dir = (
            os.path.join(self.artifact_dir, artifact_path) if artifact_path else self.artifact_dir
        )
        if not os.path.exists(artifact_dir):
            mkdir(artifact_dir)
        dir_util.copy_tree(src=local_dir, dst=artifact_dir, preserve_mode=0, preserve_times=0)

    def download_artifacts(self, artifact_path, dst_path=None):
        """
        Artifacts tracked by ``LocalArtifactRepository`` already exist on the local filesystem.
        If ``dst_path`` is ``None``, the absolute filesystem path of the specified artifact is
        returned. If ``dst_path`` is not ``None``, the local artifact is copied to ``dst_path``.

        :param artifact_path: Relative source path to the desired artifacts.
        :param dst_path: Absolute path of the local filesystem destination directory to which to
                         download the specified artifacts. This directory must already exist. If
                         unspecified, the absolute path of the local artifact will be returned.

        :return: Absolute path of the local filesystem location containing the desired artifacts.
        """
        if dst_path:
            return super().download_artifacts(artifact_path, dst_path)
        # NOTE: The artifact_path is expected to be in posix format.
        # Posix paths work fine on windows but just in case we normalize it here.
        local_artifact_path = os.path.join(self.artifact_dir, os.path.normpath(artifact_path))
        if not os.path.exists(local_artifact_path):
            raise IOError("No such file or directory: '{}'".format(local_artifact_path))
        return os.path.abspath(local_artifact_path)

    def list_artifacts(
        self, path, max_results: Optional[int] = None, page_token: Optional[str] = None
    ) -> PagedList[FileInfo]:
        if max_results is not None or page_token is not None:
            raise ValueError(
                "Pagination is not supported. `max_results` and `page_token` should be None"
            )
        # NOTE: The path is expected to be in posix format.
        # Posix paths work fine on windows but just in case we normalize it here.
        if path:
            path = os.path.normpath(path)
        list_dir = os.path.join(self.artifact_dir, path) if path else self.artifact_dir
        if os.path.isdir(list_dir):
            artifact_files = list_all(list_dir, full_path=True)
            infos = [
                get_file_info(
                    f, relative_path_to_artifact_path(os.path.relpath(f, self.artifact_dir))
                )
                for f in artifact_files
            ]
            return PagedList(sorted(infos, key=lambda f: f.path), token=None)
        else:
            return PagedList([], token=None)

    def _download_file(self, remote_file_path, local_path):
        # NOTE: The remote_file_path is expected to be in posix format.
        # Posix paths work fine on windows but just in case we normalize it here.
        remote_file_path = os.path.join(self.artifact_dir, os.path.normpath(remote_file_path))
        shutil.copyfile(remote_file_path, local_path)

    def delete_artifacts(self, artifact_path=None):
        artifact_path = (
            os.path.join(self._artifact_dir, artifact_path) if artifact_path else self._artifact_dir
        )
        shutil.rmtree(local_file_uri_to_path(artifact_path))
