import posixpath
import uuid
from typing import Dict, List, Optional, Sequence, Tuple, Union

# SQLAlchemy imports
from sqlalchemy.engine.row import Row
from sqlalchemy import Integer, or_, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, joinedload, load_only
from sqlalchemy.dialects.postgresql import ARRAY

from mlflow.pydantic_v1 import BaseModel

# Entities imports
from mlflow.entities.mlfoundry_artifacts.artifact_version_in_transit import (
    ArtifactVersionInTransit,
)
from mlflow.entities.mlfoundry_artifacts.enums import (
    ArtifactType,
    ArtifactVersionStatus,
    ArtifactVersionTransitStatus,
    EventType,
)
from mlflow.entities.lifecycle_stage import LifecycleStage
from mlflow.entities.view_type import ViewType
from mlflow.entities.mlfoundry_artifacts.artifact import Artifact, ArtifactVersion

from mlflow.exceptions import (
    MlflowException,
    INVALID_PARAMETER_VALUE,
    RESOURCE_DOES_NOT_EXIST,
    INTERNAL_ERROR,
    BAD_REQUEST,
)
# Store imports
from mlflow.store.db.base_sql_achemy_store import BaseSqlAlchemyStore
from mlflow.store.mlfoundry_artifacts.dbmodels.models import (
    SqlArtifact,
    SqlArtifactVersion,
    SqlArtifactMaxVersion,
    SqlArtifactVersionInTransit,
    SqlEvent,
    SqlExperiment,
    ArtifactsRootSequence,
)
from mlflow.store.entities.paged_list import PagedList
from mlflow.store.utils import paginate_query, err_if_not_exist_wrapper
from mlflow.utils.time_utils import now_utc
from mlflow.utils.uri import append_to_uri_path


class SqlAlchemyArtifactStore(BaseSqlAlchemyStore):
    """ SQLAlchemy store for MLFoundry artifacts """

    def _create_artifact_max_version(self, session: Session, artifact_id: uuid.UUID) -> None:
        artifact_max_version = SqlArtifactMaxVersion(artifact_id=artifact_id, max_version=0)
        session.add(artifact_max_version)

    # Artifact CRUDs
    def create_artifact(self, artifact: Artifact) -> Artifact:
        """Create an artifact"""
        with self.ManagedSessionMaker() as session:
            sql_artifact = SqlArtifact(
                id=artifact.id,
                experiment_id=artifact.experiment_id,
                type=artifact.type,
                name=artifact.name,
                fqn=artifact.fqn,
                description=artifact.description,
                artifact_storage_root=artifact.artifact_storage_root,
                created_by=artifact.created_by,
            )
            session.add(sql_artifact)

            # Add the artifact to the artifact_max_version table
            self._create_artifact_max_version(session=session, artifact_id=artifact.id)

            session.flush()
            return sql_artifact.to_entity()

    def _get_artifacts_with_latest_version_query(
        self,
        session: Session,
        filters: Sequence = (),
        latest_version_subquery_filters: Sequence = (),
        join_artifact_in_latest_version_subquery: bool = False,
        join_experiments: bool = False,
        include_entries_without_versions: bool = True,
        return_steps: bool = False,
        view_type: ViewType = ViewType.ACTIVE_ONLY,
    ):
        """
        Get the artifacts with the latest version

        # TODO: When we remodle the artifact versioning for models, we need to update this function
        Note: version_model_cls is removed from the function signature as it is used for only SqlModelVersion
        Removed all SqlModelVersion related code
        """
        version_model_cls = SqlArtifactVersion

        # modify the filters with view_type
        stages = LifecycleStage.view_type_to_stages(view_type)
        filters = [*filters, SqlArtifact.lifecycle_stage.in_(stages)]

        if return_steps:
            latest_versions = session.query(
                version_model_cls.artifact_id,
                func.max(version_model_cls.version).label("latest_version"),
                func.array_agg(version_model_cls.step, type_=ARRAY(Integer)).label(
                    "steps_"
                ),
            )
        else:
            latest_versions = session.query(
                version_model_cls.artifact_id,
                func.max(version_model_cls.version).label("latest_version"),
            )

        if join_artifact_in_latest_version_subquery:
            latest_versions = latest_versions.join(SqlArtifact)

        latest_versions = (
            latest_versions.filter(*latest_version_subquery_filters)
            .group_by(version_model_cls.artifact_id)
            .subquery("latest_versions")
        )
        if return_steps:
            query = session.query(
                SqlArtifact, version_model_cls, latest_versions.c.steps_
            )
        else:
            query = session.query(SqlArtifact, version_model_cls)
        if join_experiments:
            query = query.join(
                SqlExperiment,
                SqlArtifact.experiment_id == SqlExperiment.experiment_id,
                isouter=False,
            )
        query = query.join(
            latest_versions,
            latest_versions.c.artifact_id == SqlArtifact.id,
            isouter=include_entries_without_versions,
        ).join(
            version_model_cls,
            (version_model_cls.artifact_id == latest_versions.c.artifact_id)
            & (version_model_cls.version == latest_versions.c.latest_version),
            isouter=True,
        )
        query = query.filter(*filters)
        return query

    def _get_artifact(
        self,
        artifact_type: Optional[ArtifactType] = None,
        experiment_id: Optional[int] = None,
        artifact_id: Optional[uuid.UUID] = None,
        name: Optional[str] = None,
        fqn: Optional[str] = None,
        view_type: ViewType = ViewType.ACTIVE_ONLY,
    ) -> Optional[Artifact]:
        """Get the artifact"""

        # Assert that the required filters are provided
        if not any([fqn, artifact_id, (experiment_id and name and artifact_type)]):
            raise MlflowException(
                "To get the artifact, exactly one of the following filter must be provided :"
                "fqn OR artifact_id OR (experiment_id, name, and artifact_type)",
                error_code=INVALID_PARAMETER_VALUE,
            )

        with self.ManagedSessionMaker() as session:
            if fqn:
                filters = [SqlArtifact.fqn == fqn]
                latest_version_subquery_filters = [
                    SqlArtifactVersion.status == ArtifactVersionStatus.COMMITTED.value,
                    SqlArtifact.fqn == fqn,
                ]
            else:
                filters = [
                    or_(SqlArtifact.name == name, SqlArtifact.id == artifact_id),
                ]
                latest_version_subquery_filters = [
                    SqlArtifactVersion.status == ArtifactVersionStatus.COMMITTED.value,
                    SqlArtifact.id == artifact_id,
                ]

            if artifact_type:
                filters += [SqlArtifact.type == artifact_type.value]

            if experiment_id:
                filters += [SqlArtifact.experiment_id == experiment_id]

            query = self._get_artifacts_with_latest_version_query(
                session=session,
                filters=filters,
                latest_version_subquery_filters=latest_version_subquery_filters,
                join_artifact_in_latest_version_subquery=True,
                join_experiments=False,
                include_entries_without_versions=True,
                return_steps=False,
                view_type=view_type,
            )

            instance: Optional[Tuple[SqlArtifact, SqlArtifactVersion]] = (
                query.one_or_none()
            )
            if instance:
                artifact_instance, latest_version_instance = instance
                return artifact_instance.to_entity(
                    latest_version=latest_version_instance
                )

    @err_if_not_exist_wrapper("artifact")
    def get_artifact_by_id(
        self,
        artifact_id: uuid.UUID,
        view_type: ViewType = ViewType.ACTIVE_ONLY,
    ) -> Optional[Artifact]:
        """Get the artifact by ID"""
        return self._get_artifact(
            artifact_id=artifact_id,
            view_type=view_type,
        )

    @err_if_not_exist_wrapper("artifact")
    def get_artifact_by_fqn(
        self,
        fqn: str,
        view_type: ViewType = ViewType.ACTIVE_ONLY,
    ) -> Optional[Artifact]:
        """Get the artifact by FQN"""
        return self._get_artifact(
            fqn=fqn,
            view_type=view_type,
        )

    @err_if_not_exist_wrapper("artifact")
    def get_artifact_by_name(
        self,
        experiment_id: int,
        artifact_type: ArtifactType,
        name: str,
        view_type: ViewType = ViewType.ACTIVE_ONLY,
    ) -> Optional[Artifact]:
        """Get the artifact by name"""
        return self._get_artifact(
            artifact_type=artifact_type,
            experiment_id=experiment_id,
            name=name,
            view_type=view_type,
        )

    def _update_artifact(self, session: Session, artifact_id: uuid.UUID) -> Artifact:
        updated = (
            session.query(SqlArtifact)
            .filter(SqlArtifact.id == artifact_id)
            .update({"updated_at": now_utc()})
        )

        if updated == 0:
            raise MlflowException(
                f"No artifact with ID {artifact_id} found",
                error_code=RESOURCE_DOES_NOT_EXIST,
            )
        elif updated > 1:
            raise MlflowException(
                "More than one row updated when expected one",
                error_code=INTERNAL_ERROR,
            )

    # Artifact Versions In Transit CRUDs
    def create_artifact_version_in_transit(
        self,
        artifact: Artifact,
    ) -> ArtifactVersionInTransit:
        """Create an artifact version in transit"""
        with self.ManagedSessionMaker() as session:
            id_ = str(session.query(ArtifactsRootSequence.next_value()).scalar())
            artifact_storage_root = append_to_uri_path(
                artifact.artifact_storage_root, id_, posixpath.sep
            )
            instance = SqlArtifactVersionInTransit(
                artifact_id=artifact.id,
                artifact_storage_root=artifact_storage_root,
                status=ArtifactVersionTransitStatus.CREATED.value,
            )
            session.add(instance)
            session.flush()

            return instance.to_entity()

    @err_if_not_exist_wrapper("artifact version in transit")
    def get_artifact_version_in_transit(
        self,
        version_id: uuid.UUID,
        status: ArtifactVersionTransitStatus,
    ) -> Optional[ArtifactVersionInTransit]:
        """Get the artifact version in transit"""
        with self.ManagedSessionMaker() as session:
            instance = (
                session.query(SqlArtifactVersionInTransit)
                .options(joinedload(SqlArtifactVersionInTransit.artifact))
                .filter_by(version_id=version_id, status=status.value)
                .one_or_none()
            )
            return instance.to_entity() if instance else None

    def _delete_artifact_version_in_transit(self, session: Session, version_id: uuid.UUID) -> None:
        instance = (
            session.query(SqlArtifactVersionInTransit)
            .filter_by(version_id=version_id)
            .one_or_none()
        )
        if not instance:
            raise MlflowException(
                f"No ArtifactVersionInTransit with version_id={version_id} found",
                error_code=RESOURCE_DOES_NOT_EXIST,
            )
        session.delete(instance)

    def finalize_artifact_version(
        self,
        artifact: Artifact,
        artifact_version: ArtifactVersion,
    ) -> ArtifactVersion:
        """Finalize an artifact version"""
        artifact_metadata = artifact_version.artifact_metadata or {}
        internal_metadata = artifact_version.internal_metadata or {}
        internal_metadata_dict = (
            internal_metadata.dict()
            if isinstance(internal_metadata, BaseModel)
            else internal_metadata
        )

        with self.ManagedSessionMaker() as session:
            artifact_id = artifact_version.artifact_id
            # select for update (lock)
            artifact_max_version = (
                session.query(SqlArtifactMaxVersion)
                .filter(SqlArtifactMaxVersion.artifact_id == artifact_id)
                .with_for_update()
                .one_or_none()
            )
            if not artifact_max_version:
                raise MlflowException(
                    f"No artifact with ID {artifact_id} found",
                    error_code=RESOURCE_DOES_NOT_EXIST
                )

            # add to main table
            new_version = artifact_max_version.max_version + 1
            sql_artifact_version = SqlArtifactVersion(
                id=artifact_version.id,
                artifact_id=artifact_id,
                artifact_type=artifact.type,
                version=new_version,
                artifact_storage_root=artifact_version.artifact_storage_root,
                status=ArtifactVersionStatus.COMMITTED.value,
                description=artifact_version.description,
                artifact_metadata=artifact_metadata,
                internal_metadata=internal_metadata_dict,
                data_path=artifact_version.data_path,
                step=artifact_version.step if artifact_version.run_id else None,
                artifact_size=artifact_version.artifact_size,
                created_by=artifact_version.created_by,
                run_uuid=artifact_version.run_id if artifact_version.run_id else None,
            )
            try:
                session.add(sql_artifact_version)
                # update the artifact to Update the updated_at field
                self._update_artifact(session=session, artifact_id=artifact_id)
                session.flush()
            except IntegrityError as e:
                raise MlflowException(
                    f"Failed to finalize artifact version with ID {artifact_version.id}",
                    error_code=BAD_REQUEST,
                ) from e

            # Delete from transit table
            self._delete_artifact_version_in_transit(
                session=session, version_id=artifact_version.id
            )
            # Calculate the new max version
            artifact_max_version.max_version = max(
                artifact_max_version.max_version, new_version
            )
            session.flush()

            # create an event
            event = SqlEvent(
                run_uuid=artifact_version.run_id if artifact_version.run_id else None,
                artifact_id=artifact_id,
                artifact_version_id=artifact_version.id,
                type=EventType.OUTPUT.value,
            )
            session.add(event)

            # return ArtifactVersion entity
            # note that to_entity will end up firing a select call for `artifact` relationship
            artifact_version = sql_artifact_version.to_entity()

        return artifact_version

    # Artifact Versions CRUDs
    def create_artifact_version(
        self, artifact: Artifact, artifact_version: ArtifactVersion
    ) -> ArtifactVersion:
        """Create an artifact version"""
        with self.ManagedSessionMaker() as session:
            sql_artifact_version = SqlArtifactVersion(
                artifact_id=artifact_version.artifact_id,
                artifact_type=artifact.type.value,
                version=artifact_version.version,
                artifact_storage_root=artifact_version.artifact_storage_root,
                artifact_metadata=artifact_version.artifact_metadata,
                internal_metadata=artifact_version.internal_metadata,
                data_path=artifact_version.data_path,
                description=artifact_version.description,
                status=artifact_version.status,
                step=artifact_version.step,
                created_by=artifact_version.created_by,
            )
            session.add(sql_artifact_version)
            session.commit()
            return sql_artifact_version.to_entity()

    # Get or List Artifact Versions
    def _get_artifact_version(
        self,
        version_id: Optional[uuid.UUID] = None,
        experiment_id: Optional[int] = None,
        artifact_name: Optional[str] = None,
        version: Optional[int] = None,
        artifact_type: Optional[ArtifactType] = None,
        fqn: Optional[str] = None,
        status: Optional[ArtifactVersionStatus] = None,
    ) -> Optional[ArtifactVersion]:

        # Assert that the required filters are provided
        if not any(
            [fqn, version_id, (experiment_id and artifact_name and artifact_type and version)]
        ):
            raise MlflowException(
                "To get the artifact version, exactly one of the following filter must be provided:"
                "fqn OR version_id OR (experiment_id, artifact_name, version and artifact_type)",
                error_code=INVALID_PARAMETER_VALUE,
            )

        with self.ManagedSessionMaker() as session:
            # Create the base query for SqlArtifactVersion
            query = session.query(SqlArtifactVersion).options(
                joinedload(SqlArtifactVersion.artifact).load_only(
                    SqlArtifact.experiment_id, SqlArtifact.name, SqlArtifact.fqn
                )
            )

            # Apply joins and filters based on provided arguments
            if fqn:
                artifact_fqn, _version = ArtifactVersion.get_artifact_fqn_and_version(
                    fqn
                )
                version = version or _version
                query = (
                    query.add_columns(SqlEvent.run_uuid)
                    .join(SqlArtifact, SqlArtifactVersion.artifact_id == SqlArtifact.id)
                    .join(SqlEvent, SqlEvent.artifact_version_id == SqlArtifactVersion.id)
                    .filter(SqlEvent.type == EventType.OUTPUT, SqlArtifact.fqn == artifact_fqn)
                )
            elif version_id:
                query = (
                    query.add_columns(SqlEvent.run_uuid)
                    .join(SqlEvent, SqlEvent.artifact_version_id == SqlArtifactVersion.id)
                    .filter(SqlEvent.type == EventType.OUTPUT, SqlArtifactVersion.id == version_id)
                )
            else:
                query = query.join(
                    SqlArtifact, SqlArtifactVersion.artifact_id == SqlArtifact.id
                ).filter(
                    SqlArtifact.experiment_id == experiment_id,
                    SqlArtifact.name == artifact_name,
                    SqlArtifact.type == artifact_type.value,
                )

            # Apply additional filters
            if status:
                query = query.filter(SqlArtifactVersion.status == status.value)

            if version is not None and version != -1:
                query = query.filter(SqlArtifactVersion.version == version)

            # Order by version if needed and limit the result to 1
            if version == -1:
                query = query.order_by(SqlArtifactVersion.version.desc()).limit(1)

            # Execute the query and fetch the result
            result = query.one_or_none()

            # Return the entity if the result is not None
            if result:
                instance, run_id = (
                    result if isinstance(result, Row) else (result, result.run_uuid)
                )
                return instance.to_entity(run_id=run_id)
        return None

    @err_if_not_exist_wrapper("artifact version")
    def get_artifact_version_by_id(
        self, version_id: uuid.UUID, status: Optional[ArtifactVersionStatus] = None
    ) -> Optional[ArtifactVersion]:
        """Get the artifact version by ID"""
        return self._get_artifact_version(version_id=version_id, status=status)

    @err_if_not_exist_wrapper("artifact version")
    def get_artifact_version_by_fqn(
        self, fqn: str, status: Optional[ArtifactVersionStatus] = None
    ) -> Optional[ArtifactVersion]:
        """Get the artifact version by FQN"""
        return self._get_artifact_version(fqn=fqn, status=status)

    @err_if_not_exist_wrapper("artifact version")
    def get_artifact_version(
        self,
        experiment_id: int,
        artifact_name: str,
        version: int,
        artifact_type: ArtifactType,
        status: Optional[ArtifactVersionStatus] = None,
    ) -> Optional[ArtifactVersion]:
        """Get the artifact version"""
        return self._get_artifact_version(
            experiment_id=experiment_id,
            artifact_name=artifact_name,
            artifact_type=artifact_type,
            version=version,
            status=status,
        )

    def list_artifact_versions(
        self,
        artifact_id: Optional[uuid.UUID] = None,
        run_ids: Optional[List[str]] = None,
        run_steps: Optional[List[str]] = None,
        experiment_ids: Optional[List[uuid.UUID]] = None,
        artifact_types: Optional[List[ArtifactType]] = None,
        statuses: Optional[Sequence[ArtifactVersionStatus]] = None,
        max_results: Optional[int] = None,
        page_token: Optional[str] = None,
    ) -> PagedList[ArtifactVersion]:

        filters = []

        # Apply filters based on the provided arguments
        if artifact_id:
            filters.append(SqlArtifactVersion.artifact_id == artifact_id)
        elif run_ids:
            filters.append(SqlArtifactVersion.run_uuid.in_(run_ids))
            if run_steps:
                if len(run_ids) != 1:
                    raise MlflowException(
                        "Only one run_id must be passed in `run_ids` when `run_steps` is given",
                        error_code=INVALID_PARAMETER_VALUE
                    )
                filters.append(SqlArtifactVersion.step.in_(run_steps))
        elif experiment_ids:
            filters.append(SqlArtifact.experiment_id.in_(experiment_ids))
        else:
            raise MlflowException(
                "At least one of `artifact_id`, `run_ids`, or `experiment_ids` must be provided",
                error_code=INVALID_PARAMETER_VALUE
            )

        # Apply additional filters
        statuses = statuses or [ArtifactVersionStatus.COMMITTED]
        if statuses:
            filters.append(SqlArtifactVersion.status.in_([s.value for s in statuses]))

        artifact_types = artifact_types or []
        if artifact_types:
            filters.append(
                SqlArtifactVersion.artifact_type.in_((at.value for at in artifact_types))
            )

        # Apply ordering
        if run_ids and len(run_ids) == 1:
            order_by_clauses = [SqlArtifactVersion.step.desc(), SqlArtifactVersion.version.desc()]
        else:
            order_by_clauses = [SqlArtifactVersion.version.desc()]

        with self.ManagedSessionMaker() as session:
            # Create the base query for SqlArtifactVersion
            session_query = session.query(SqlArtifactVersion)

            # Join with SqlArtifact and select only necessary fields
            session_query = session_query.join(
                SqlArtifact, SqlArtifact.id == SqlArtifactVersion.artifact_id
            ).options(
                load_only(SqlArtifact.experiment_id, SqlArtifact.fqn)  # Load only necessary fields
            )

            # Apply the filters to the query
            query = session_query.filter(*filters)

            # Execute the query and fetch paginated results
            instances_paged_list = paginate_query(
                query=query,
                count_field=SqlArtifactVersion.id,
                order_by_clauses=order_by_clauses,
                max_results=max_results,
                page_token=page_token,
            )
            entities_list = [instance.to_entity() for instance in instances_paged_list]
            return PagedList(
                entities_list,
                token=instances_paged_list.token,
                total=instances_paged_list.total,
            )

    def delete_artifact_version(self, version_id: uuid.UUID):
        with self.ManagedSessionMaker() as session:
            instance = (
                session.query(SqlArtifactVersion)
                .filter(
                    SqlArtifactVersion.id == version_id,
                    SqlArtifactVersion.status == ArtifactVersionStatus.HARD_DELETED,
                )
                .one_or_none()
            )
            if not instance:
                raise MlflowException(
                    f"No ArtifactVersion with version_id={version_id} status={ArtifactVersionStatus.HARD_DELETED!r} found",
                    error_code=RESOURCE_DOES_NOT_EXIST,
                )
            session.delete(instance)

    def _update_artifact_version(
        self,
        session: Session,
        version_id: uuid.UUID,
        description: Optional[str] = None,
        artifact_metadata: Optional[Dict[str, Union[str, int, float, bool]]] = None,
    ):
        query = session.query(SqlArtifactVersion).filter_by(
            id=version_id, status=ArtifactVersionStatus.COMMITTED.value
        )
        artifact_version = query.one_or_none()

        if not artifact_version:
            raise MlflowException(
                f"Artifact version with ID {version_id} not found",
                error_code=RESOURCE_DOES_NOT_EXIST,
            )

        if description is not None:
            artifact_version.description = description
        if artifact_metadata is not None:
            artifact_version.artifact_metadata = artifact_metadata

        try:
            self._update_artifact(
                session=session,
                artifact_id=artifact_version.artifact_id,
            )
            session.flush()
        except IntegrityError as e:
            raise MlflowException(
                f"Failed to update artifact version with ID {version_id}",
                error_code=BAD_REQUEST,
            ) from e

    def update_artifact_version(
        self,
        version_id: uuid.UUID,
        description: Optional[str] = None,
        artifact_metadata: Optional[Dict[str, Union[str, int, float, bool]]] = None,
    ) -> ArtifactVersion:
        with self.ManagedSessionMaker() as session:
            self._update_artifact_version(
                session=session,
                version_id=version_id,
                description=description,
                artifact_metadata=artifact_metadata,
            )

            artifact_version = self._get_artifact_version(
                version_id=version_id, status=ArtifactVersionStatus.COMMITTED
            )

            if not artifact_version:
                raise MlflowException(
                    f"Failed to update artifact version with ID {version_id}",
                    error_code=RESOURCE_DOES_NOT_EXIST,
                )

            return artifact_version
