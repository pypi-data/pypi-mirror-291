import threading
from typing import Dict
import sqlalchemy

# Store imports
from mlflow.store.db.base_sql_model import Base
from mlflow.store.db.utils import (
    _get_managed_session_maker,
    _verify_schema,
    create_sqlalchemy_engine_with_retry,
)

# Utils imports
from mlflow.utils.uri import extract_db_type_from_uri, is_local_uri
from mlflow.utils.file_utils import local_file_uri_to_path, mkdir

class BaseSqlAlchemyStore:
    """
    Base class for SQLAlchemy store.
    
    This class provides the base implementation for interacting with a SQL database using SQLAlchemy.
    It handles the creation of database engines, sessions, and ensures the database schema is verified.

    :param db_uri: The SQLAlchemy database URI string to connect to the database.
    :param default_artifact_root: Path/URI to location suitable for large data (optional).
    """

    _db_uri_sql_alchemy_engine_map: Dict[str, sqlalchemy.engine.Engine] = {}
    _db_uri_sql_alchemy_engine_map_lock = threading.Lock()

    def __init__(self, db_uri: str, default_artifact_root: str=None):
        """
        Initialize the base SQLAlchemy store.

        :param db_uri: The SQLAlchemy database URI string to connect to the database.
        :param default_artifact_root: Path/URI to location suitable for large data (optional).
        """
        self.db_uri = db_uri
        self.db_type = extract_db_type_from_uri(db_uri)
        self.artifact_root_uri = default_artifact_root
        self.engine = self._initialize_engine()
        Base.metadata.bind = self.engine
        SessionMaker = sqlalchemy.orm.sessionmaker(bind=self.engine)
        self.ManagedSessionMaker = _get_managed_session_maker(SessionMaker, self.db_type)

        if default_artifact_root and is_local_uri(default_artifact_root):
            mkdir(local_file_uri_to_path(default_artifact_root))

        _verify_schema(self.engine)

    def _initialize_engine(self) -> None:
        """Initialize the SQLAlchemy engine for the given database URI."""
        if self.db_uri not in BaseSqlAlchemyStore._db_uri_sql_alchemy_engine_map:
            with BaseSqlAlchemyStore._db_uri_sql_alchemy_engine_map_lock:
                if self.db_uri not in BaseSqlAlchemyStore._db_uri_sql_alchemy_engine_map:
                    BaseSqlAlchemyStore._db_uri_sql_alchemy_engine_map[self.db_uri] = (
                        create_sqlalchemy_engine_with_retry(self.db_uri)
                    )
        return BaseSqlAlchemyStore._db_uri_sql_alchemy_engine_map[self.db_uri]
