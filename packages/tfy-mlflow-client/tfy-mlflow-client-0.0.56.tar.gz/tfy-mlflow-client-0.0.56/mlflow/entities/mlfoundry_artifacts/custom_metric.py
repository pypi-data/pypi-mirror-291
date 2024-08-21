from mlflow.entities.mlfoundry_artifacts.enums import (
    CustomMetricType,
    CustomMetricValueType,
)
from mlflow.pydantic_v1 import BaseModel


class CustomMetric(BaseModel):
    class Config:
        orm_mode = True
        validate_assignment = True
        use_enum_values = True
        allow_mutation = False
        extra = "allow"

    name: str
    value_type: CustomMetricValueType
    type: CustomMetricType
