from collections.abc import Iterator
from datetime import datetime
from typing import Any, ClassVar

from sqlalchemy import DateTime, MetaData, create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker
from sqlalchemy.types import TypeEngine

from backend.config import settings

# Deterministic constraint names, so migrations and their downgrades can refer
# to constraints by name instead of relying on names Postgres generates.
NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


class Base(DeclarativeBase):
    metadata = MetaData(naming_convention=NAMING_CONVENTION)
    # Ensure timezone aware by default
    type_annotation_map: ClassVar[dict[Any, TypeEngine[Any]]] = {
        datetime: DateTime(timezone=True)
    }


engine = create_engine(settings.database_url)

# expire_on_commit=False: expired attributes would otherwise be lazily
# refreshed with a hidden SELECT on next access after a commit.
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)


def get_session() -> Iterator[Session]:
    with SessionLocal() as session:
        yield session
