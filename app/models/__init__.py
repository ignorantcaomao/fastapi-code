# 导入 Base，它是所有模型的基础
from .base import Base
# 导入你所有的模型，确保它们被 Base.metadata 识别
from .user import User
from .heros import Hero


# 可选：使用 __all__ 来明确声明这个包对外暴露的接口
# 这是一种良好的编程习惯
__all__ = ["Base","User", "Hero"]