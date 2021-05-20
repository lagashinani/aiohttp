from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
from db.schema import Base
from api.app import app_config

driver = app_config['postgres']['driver']
database = app_config['postgres']['database']
user = app_config['postgres']['user']
password = app_config['postgres']['password']
host = app_config['postgres']['host']
port = app_config['postgres']['port']

db_url = f'{driver}://{user}:{password}@{host}/{database}'

config = context.config
config.set_main_option('sqlalchemy.url', db_url)
fileConfig(config.config_file_name)
target_metadata = Base.metadata

def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
