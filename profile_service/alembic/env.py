from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool, MetaData
from alembic import context
import os
import sys

# Добавляем путь к проекту в PYTHONPATH
sys.path.append(os.getcwd())

from models import Base  # Импортируем Base из models.py

# Настройка Alembic
config = context.config
fileConfig(config.config_file_name)

# Функция для исключения таблицы `users` из автосоздания
def include_object(object, name, type_, reflected, compare_to):
    if type_ == "table" and name == "users":
        return False  # Исключаем таблицу `users` из автосоздания
    return True

def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=Base.metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        include_object=include_object,
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
        # Отражение таблицы `users`
        metadata = MetaData()
        metadata.reflect(bind=connection, only=["users"])

        # Объединяем метаданные
        Base.metadata.reflect(bind=connection)

        context.configure(
            connection=connection,
            target_metadata=Base.metadata,
            include_object=include_object,
        )
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()