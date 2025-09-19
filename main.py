from fastapi import FastAPI, Depends

from app.core.config import get_settings, get_project_version, settings, Settings




async def lifespan(app: FastAPI):
  get_settings()
  yield

app = FastAPI(
  title=settings.APP_NAME,
  version=get_project_version(),
  lifespan=lifespan,
)


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
