import time

from sqlalchemy import (
    BigInteger,
    Column,
    ForeignKey,
    ForeignKeyConstraint,
    Integer,
    PrimaryKeyConstraint,
    String,
)
from sqlalchemy.orm import backref, relationship

from mlflow.store.db.base_sql_model import Base


class SqlRegisteredModel(Base):
    __tablename__ = "registered_models"

    name = Column(String(256), unique=True, nullable=False)

    creation_time = Column(BigInteger, default=lambda: int(time.time() * 1000))

    last_updated_time = Column(BigInteger, nullable=True, default=None)

    description = Column(String(5000), nullable=True)

    __table_args__ = (PrimaryKeyConstraint("name", name="registered_model_pk"),)

    def __repr__(self):
        return "<SqlRegisteredModel ({}, {}, {}, {})>".format(
            self.name, self.description, self.creation_time, self.last_updated_time
        )


class SqlModelVersion(Base):
    __tablename__ = "model_versions"

    name = Column(String(256), ForeignKey("registered_models.name", onupdate="cascade"))

    version = Column(Integer, nullable=False)

    creation_time = Column(BigInteger, default=lambda: int(time.time() * 1000))

    last_updated_time = Column(BigInteger, nullable=True, default=None)

    description = Column(String(5000), nullable=True)

    user_id = Column(String(256), nullable=True, default=None)

    current_stage = Column(String(20), default="None")

    source = Column(String(500), nullable=True, default=None)

    run_id = Column(String(32), nullable=True, default=None)

    run_link = Column(String(500), nullable=True, default=None)

    status = Column(String(20), default="READY")

    status_message = Column(String(500), nullable=True, default=None)

    # linked entities
    registered_model = relationship(
        "SqlRegisteredModel", backref=backref("model_versions", cascade="all")
    )

    __table_args__ = (PrimaryKeyConstraint("name", "version", name="model_version_pk"),)


class SqlRegisteredModelTag(Base):
    __tablename__ = "registered_model_tags"

    name = Column(String(256), ForeignKey("registered_models.name", onupdate="cascade"))

    key = Column(String(250), nullable=False)

    value = Column(String(5000), nullable=True)

    # linked entities
    registered_model = relationship(
        "SqlRegisteredModel", backref=backref("registered_model_tags", cascade="all")
    )

    __table_args__ = (PrimaryKeyConstraint("key", "name", name="registered_model_tag_pk"),)

    def __repr__(self):
        return "<SqlRegisteredModelTag ({}, {}, {})>".format(self.name, self.key, self.value)


class SqlModelVersionTag(Base):
    __tablename__ = "model_version_tags"

    name = Column(String(256))

    version = Column(Integer)

    key = Column(String(250), nullable=False)

    value = Column(String(5000), nullable=True)

    # linked entities
    model_version = relationship(
        "mlflow.store.model_registry.dbmodels.models.SqlModelVersion",
        foreign_keys=[name, version],
        backref=backref("model_version_tags", cascade="all"),
    )

    __table_args__ = (
        PrimaryKeyConstraint("key", "name", "version", name="model_version_tag_pk"),
        ForeignKeyConstraint(
            ("name", "version"),
            ("model_versions.name", "model_versions.version"),
            onupdate="cascade",
        ),
    )

    def __repr__(self):
        return "<SqlModelVersionTag ({}, {}, {}, {})>".format(
            self.name, self.version, self.key, self.value
        )
