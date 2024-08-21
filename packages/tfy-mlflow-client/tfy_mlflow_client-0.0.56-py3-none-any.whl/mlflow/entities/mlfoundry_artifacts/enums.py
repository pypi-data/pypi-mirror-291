import enum
from typing import Any, List

from mlflow.dto import mlfoundry_artifacts_dto as mlfa_dto
from mlflow.exceptions import MlflowException
from mlflow.protos.databricks_pb2 import BAD_REQUEST


class BaseEnum(enum.Enum):
    @classmethod
    def values(cls) -> List:
        return [member.value for member in cls]

    @classmethod
    def _missing_(cls, value: Any):
        raise MlflowException(
            f"Unknown value for type {cls.__name__}: {value}", error_code=BAD_REQUEST
        )

    def to_dto(self) -> int:
        dto_cls = getattr(mlfa_dto, self.__class__.__name__ + "Dto")
        return dto_cls.Value(self.value)


@enum.unique
class ArtifactType(str, BaseEnum):
    # kept lowercase values because they will be part of fqn
    ARTIFACT = "artifact"
    MODEL = "model"
    PLOT = "plot"
    IMAGE = "image"
    CHAT_PROMPT = "chat_prompt"


SPECIAL_ARTIFACT_TYPES = {ArtifactType.MODEL}
OTHER_ARTIFACT_TYPES = [at for at in ArtifactType if at not in SPECIAL_ARTIFACT_TYPES]


@enum.unique
class ArtifactVersionTransitStatus(str, BaseEnum):
    CREATED = "CREATED"
    FAILED = "FAILED"


@enum.unique
class ArtifactVersionStatus(str, BaseEnum):
    COMMITTED = "COMMITTED"
    DELETED = "DELETED"
    HARD_DELETED = "HARD_DELETED"


@enum.unique
class EventType(str, BaseEnum):
    INPUT = "INPUT"
    OUTPUT = "OUTPUT"


@enum.unique
class PredictionType(str, BaseEnum):
    CATEGORICAL = "categorical"
    NUMERIC = "numeric"


@enum.unique
class FeatureValueType(str, BaseEnum):
    INT = "int"
    FLOAT = "float"
    STRING = "string"


@enum.unique
class CustomMetricValueType(str, BaseEnum):
    FLOAT = "float"


@enum.unique
class CustomMetricType(str, BaseEnum):
    METRIC = "metric"
    PROJECTION = "projection"


@enum.unique
class MultiPartUploadStorageProvider(str, enum.Enum):
    S3_COMPATIBLE = "S3_COMPATIBLE"
    AZURE_BLOB = "AZURE_BLOB"
