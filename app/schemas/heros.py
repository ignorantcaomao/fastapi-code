from pydantic import BaseModel

class HeroBase(BaseModel):
    name: str
    alias: str

class HeroCreate(HeroBase):
  pass

class HeroUpdate(HeroBase):
  alias: str | None = None
  name: str | None = None

class HeroResponse(HeroBase):
    id: int

    class Config:
      from_attributes = True  # 关键配置！允许模型从ORM对象的属性中读取数据


class HeroStoryResponse(HeroResponse):
  """
      继承自 HeroResponse，并增加一个 story 字段
      """
  story: str