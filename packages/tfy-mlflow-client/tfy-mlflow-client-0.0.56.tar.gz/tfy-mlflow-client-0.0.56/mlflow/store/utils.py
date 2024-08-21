import functools
from typing import Optional, List, Callable, Type, TypeVar
from sqlalchemy.orm import Query
from sqlalchemy import func

from mlflow.exceptions import MlflowException
from mlflow.store.entities.paged_list import PagedList
from mlflow.utils.search_utils import SearchUtils
from mlflow.protos.databricks_pb2 import RESOURCE_DOES_NOT_EXIST
from mlflow.pydantic_v1 import BaseModel


_ET = TypeVar("_ET", bound=BaseModel)


def paginate_query(
    query: Query,
    count_field: Optional[str] = None,
    order_by_clauses: Optional[List[Type[func]]] = None,
    max_results: Optional[int] = None,
    page_token: Optional[str] = None
) -> PagedList:
    """
    Paginate the results of a SQLAlchemy query.

    Args:
        query (Query): The SQLAlchemy query to paginate.
        count_field (Optional[str]): Field to count for pagination. If None, use COUNT(*).
        order_by_clauses (Optional[List[Type[func]]]): List of order_by clauses.
        max_results (Optional[int]): Maximum number of results per page.
        page_token (Optional[str]): Token for the next page.

    Returns:
        PagedList: A PagedList object containing the paginated results.
    """
    if count_field:
        total = query.with_entities(func.count(count_field)).scalar()
    else:
        total = query.count()

    if order_by_clauses:
        query = query.order_by(*order_by_clauses)

    if max_results is not None:
        max_results_for_query = max_results + 1
        offset = SearchUtils.parse_start_offset_from_page_token(page_token)
        instances = query.offset(offset).limit(max_results_for_query).all()
        next_token = None
        if max_results_for_query == len(instances):
            final_offset = offset + max_results
            next_token = SearchUtils.create_page_token(final_offset)
        instances = instances[:max_results]
    else:
        instances = query.all()
        next_token = None

    return PagedList(instances, next_token, total=total)


def err_if_not_exist_wrapper(entity_name):
    def wrapper(fn: Callable[..., Optional[_ET]]) -> Callable[..., Optional[_ET]]:
        @functools.wraps(fn)
        def inner(*args, err_if_not_exist=False, **kwargs) -> Optional[_ET]:
            entity = fn(*args, **kwargs)
            if err_if_not_exist and not entity:
                raise MlflowException(
                    f"No {entity_name} found with given arguments: {args[1:]!s}, {kwargs!s}",
                    error_code=RESOURCE_DOES_NOT_EXIST,
                )
            return entity

        return inner

    return wrapper
