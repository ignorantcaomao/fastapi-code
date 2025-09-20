from pydantic import BaseModel
from typing import Text

from app.models import Hero


class HeroBase(BaseModel):
    name: str
    alias: str
    powers: Text

class HeroCreate(HeroBase):
  pass

class HeroUpdate(HeroBase):
  alias: str | None = None
  name: str | None = None
  powers: Text | None = None

class HeroResponse(HeroBase):
    id: int
    powers: Text | None = None

    class Config:
      from_attributes = True  # 关键配置！允许模型从ORM对象的属性中读取数据


class HeroStoryResponse(HeroResponse):
  """
      继承自 HeroResponse，并增加一个 story 字段
      """
  story: str

# 1. 分页信息模型
class Pagination(BaseModel):
  currentPage: int
  totalPages: int
  totalItems: int
  limit: int
  hasMore: bool
  previousPage: int | None  # 可能没有上一页
  nextPage: int | None  # 可能没有下一页


# 2. 排序信息模型
class Sort(BaseModel):
  field: str
  direction: str # "asc" 或 "desc"

# 3. 过滤信息模型
class Filter(BaseModel):
  search: str | None

# 4. 最终的、集大成的列表响应模型
class HeroListResponse(BaseModel):
  # 数据本身是一个 HeroResponse 列表
  data: list[HeroResponse]
  # 嵌套 Pagination 模型
  pagination: Pagination
  # 嵌套 Sort 模型
  sort: Sort
  # 嵌套 Filters 模型
  filter: Filter


