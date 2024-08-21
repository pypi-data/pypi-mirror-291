from typing import List, Optional

from mlflow.pydantic_v1 import BaseModel, Field


# Metric associated with a run, represented as a key-value pair.
class MetricDto(BaseModel):
    key: str
    value: Optional[float]
    timestamp: Optional[int]
    step: Optional[int] = 0


class GetMetricHistoryResponse(BaseModel):
    metrics: List[MetricDto]


class MetricCollectionDto(BaseModel):
    key: Optional[str]
    metrics: Optional[List[MetricDto]] = Field(default_factory=list)


class ListMetricHistoryRequestDto(BaseModel):
    run_id: str
    metric_keys: Optional[List[str]] = Field(default_factory=list)


class ListMetricHistoryResponseDto(BaseModel):
    metric_collections: List[MetricCollectionDto]
