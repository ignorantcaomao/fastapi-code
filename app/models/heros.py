from app.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer


class Hero(Base):
    __tablename__ = 'heros'

    # 一个英雄的表，包含了名字以及称号两个字段
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    alias: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)

    def __repr__(self) -> str:
      return f"<Hero(id={self.id!r}, name={self.name!r}, alias={self.alias!r})>"