import asyncio
from logging.config import fileConfig

from sqlalchemy import pool, event, Table, DDL
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context

from backend.models import Base
from backend.configs import Settings


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config
config.set_main_option('sqlalchemy.url', str(Settings().db_url))

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def include_name(name, type_, parent_names):
    if type_ == "schema":
        return name == target_metadata.schema
    else:
        return True


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        version_table_schema=target_metadata.schema,
        include_name=include_name,
        include_schemas=True,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """In this scenario we need to create an Engine
    and associate a connection with the context.

    """

    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""

    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()


# triggers = [
#     DDL(
#     'CREATE TRIGGER on_attachments AFTER INSERT OR UPDATE OR DELETE ON waiwaitapota.public."attachments"'
#     "FOR EACH ROW EXECUTE PROCEDURE version_update('attachments');").execute_if(dialect='postgresql'),
#     DDL(
#     'CREATE TRIGGER on_categories AFTER INSERT OR UPDATE OR DELETE ON waiwaitapota.public."categories"'
#     "FOR EACH ROW EXECUTE PROCEDURE version_update('categories');"),
#     DDL(
#     'CREATE TRIGGER on_words AFTER INSERT OR UPDATE OR DELETE ON waiwaitapota.public."words"'
#     "FOR EACH ROW EXECUTE PROCEDURE version_update('words');"),
#     DDL(
#     'CREATE TRIGGER on_users AFTER INSERT OR UPDATE OR DELETE ON waiwaitapota.public."users"'
#     "FOR EACH ROW EXECUTE PROCEDURE version_update('users');"),
#     DDL(
#     'CREATE TRIGGER on_references AFTER INSERT OR UPDATE OR DELETE ON waiwaitapota.public."references"'
#     "FOR EACH ROW EXECUTE PROCEDURE version_update('references');"),
#     DDL(
#     'CREATE TRIGGER on_meanings AFTER INSERT OR UPDATE OR DELETE ON waiwaitapota.public."meanings"'
#     "FOR EACH ROW EXECUTE PROCEDURE version_update('meanings');")]
#
# for trigger in triggers:
#     event.listens_for(Table, 'after_create', trigger=trigger.execute_if(dialect='postgresql'))

# event.listen(Table, 'after_create', update_function)