from __future__ import with_statement
from alembic import context
from sqlalchemy import engine_from_config, pool
from logging.config import fileConfig
from sqlalchemy import text

from backend.models import Base
from backend.configs import Settings

config = context.config
config.set_main_option('sqlalchemy.url', str(Settings().db_url))

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

"""
Load models metadata. We should define schema in this class firstly, 
or set schema implicit with `__table_args__ = {'schema' : 'test'}` in model class
"""
target_metadata = Base.metadata


def include_name(name, type_, parent_names):
    # https://alembic.sqlalchemy.org/en/latest/autogenerate.html#omitting-schema-names-from-the-autogenerate-process
    if type_ == "schema":
        # this **will* include the default schema
        return name in [None, "schema_one", "schema_two"]
    else:
        return True


def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True)

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix='sqlalchemy.',
        poolclass=pool.NullPool)
    current_tenant = context.get_x_argument(as_dictionary=True).get("tenant")
    with connectable.connect() as connection:
        # set search path on the connection, which ensures that
        # PostgreSQL will emit all CREATE / ALTER / DROP statements
        # in terms of this schema by default
        connection.execute(text('set search_path to "%s"' % current_tenant))
        # in SQLAlchemy v2+ the search path change needs to be committed
        connection.commit()

        # make use of non-supported SQLAlchemy attribute to ensure
        # the dialect reflects tables in terms of the current tenant name
        connection.dialect.default_schema_name = current_tenant

        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            version_table_schema=target_metadata.schema,
            include_schemas=True,
            include_name=include_name
        )

        with context.begin_transaction():
            """
            By default search_path is setted to "$user",public 
            that why alembic can't create foreign keys correctly
            """
            context.execute('SET search_path TO public')
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()