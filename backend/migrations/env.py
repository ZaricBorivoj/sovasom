from alembic import context
from office.accounts import models  # noqa: F401
from office.config import Settings
from office.database import Base
from sqlalchemy import create_engine, pool


def run_migrations():
    database_url = context.config.attributes.get("database_url") or Settings().database_url
    engine = create_engine(database_url, poolclass=pool.NullPool, hide_parameters=True)
    with engine.connect() as connection:
        context.configure(connection=connection, target_metadata=Base.metadata)
        with context.begin_transaction():
            context.run_migrations()


run_migrations()
