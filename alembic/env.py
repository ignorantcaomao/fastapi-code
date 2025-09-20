import asyncio
import os
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context

from pathlib import Path
import sys
# ----------------- 我们改造的起点 -----------------
# 步骤1：将项目根目录加入 Python 的模块搜索路径
# 这确保了 Alembic 能找到我们 app 目录下的代码
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

# 步骤2：动态加载 .env 文件，让配置与环境同步
# 这让我们可以用类似 `ENVIRONMENT=prod alembic upgrade head` 的方式来操作不同数据库
ENV = os.getenv("ENVIRONMENT", "dev")
dotenv_file = project_root / f".env.{ENV}"

from dotenv import load_dotenv
load_dotenv(dotenv_path=dotenv_file)

# 步骤3：导入我们的配置和模型定义的 Base
# 这是最关键的一步，让 Alembic 知道我们的数据库在哪，以及我们的模型长什么样
from app.core.config import Settings
# 这会触发 app/models/__init__.py, 进而加载所有模型
from app.models import Base
# 实例化我们的配置
settings = Settings()
# ----------------- 我们改造的终点 -----------------

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# ----------------- 注入数据库 URL -----------------
# 用我们从 settings 中读取的 URL 覆盖 alembic.ini 中的默认值
config.set_main_option("sqlalchemy.url", settings.DB.DATABASE_URL)

# Interpret the config file for Python logging.
# This line sets up loggers basically.
# 从配置文件中解释日志配置。
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
# ----------------- 设置目标元数据 -----------------
# 这是 Alembic 进行比对的“最终蓝图”
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


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
