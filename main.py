from fastapi import FastAPI, Depends
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.core.config import get_settings, get_project_version, settings, Settings
from app.core.exceptions import global_exception_handler
from app.core.session import setup_database_connection, create_db_and_tables, close_database_connection, get_db
from app.domains.heroes.heroes_dependencies import get_hero_service
from app.domains.heroes.services import HeroService
from app.schemas.heros import HeroResponse, HeroCreate


# 使用 lifespan 管理应用生命周期事件
async def lifespan(app: FastAPI):
  # 应用启动时执行
  get_settings()
  await setup_database_connection()
  # [可选] 在开发时创建表
  if settings.ENVIRONMENT == "dev":
    print(settings.ENVIRONMENT)
    await create_db_and_tables()
  logger.info("🚀 应用启动，数据库已连接。")
  yield
  # 应用关闭时执行
  await close_database_connection()
  logger.info("应用关闭，数据库连接已释放。")

app = FastAPI(
  title=settings.APP_NAME,
  version=get_project_version(),
  lifespan=lifespan,
)

# 注册全局异常处理器
# 这会捕获所有类型为 Exception 的异常
app.add_exception_handler(Exception, global_exception_handler)


@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.get("/")
def read_root(
    settings: Settings = Depends(get_settings),
):
  """
      一个示例端点，演示如何访问配置。
      """

  return {
        "message": f"Hello from the {settings.APP_NAME}!",
        "environment": settings.ENVIRONMENT,
        "debug_mode": settings.DEBUG,
        # 演示如何访问嵌套的配置项
        "database_host": settings.DB.HOST,
        # 演示如何使用在模型中动态计算的属性
        "database_url_hidden_password": settings.DB.DATABASE_URL.replace(
            settings.DB.PASSWORD, "****"
        ),
        "app_version": get_project_version()
    }

@app.get("/db-check")
async def db_check(db: AsyncSession = Depends(get_db)):
  """
      一个简单的端点，用于检查数据库连接是否正常工作。
      """
  try:
    result = await db.execute(text("select 1"))
    if result.scalar_one() == 1:
      return {"status": "ok", "message": "数据库连接成功！"}
  except Exception as e:
    return {"status": "error", "message": f"数据库连接失败: {e}"}


@app.post("/hero/", response_model=HeroResponse)
async def create(
    hero_data: HeroCreate,
    service: HeroService = Depends(get_hero_service)
):
  return await service.create_hero(hero_data)