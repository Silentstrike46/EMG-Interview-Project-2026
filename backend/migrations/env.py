from logging.config import fileConfig

from alembic import context
from sqlalchemy import create_engine, pool

from backend.config import settings
from backend.db import Base

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# TODO: import the models package here once it exists, so every table is
# registered on Base.metadata before autogenerate compares against it.
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Emit migration SQL to stdout without connecting (`alembic upgrade --sql`)."""
    context.configure(
        url=settings.database_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    # NullPool: a migration run is a one-off process, so pooling buys nothing.
    engine = create_engine(settings.database_url, poolclass=pool.NullPool)

    with engine.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
