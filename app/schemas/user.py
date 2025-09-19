from pydantic import BaseModel

# 基础模型，包含所有用户共有的字段
class UserBase(BaseModel):
  username: str

class UserCreate(UserBase):
  password: str

class UserResponse(BaseModel):
  id: int
  # Pydantic V2 的新配置方式
  class Config:
    from_attributes = True  # 告诉 Pydantic 模型可以从 ORM 对象属性中读取数据
