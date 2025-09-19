from typing import Optional
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.testing.schema import mapped_column

from app.models.base import Base
from app.models.mixin import DateTimeMixin


class User(Base, DateTimeMixin):
  __tablename__ = 'user'
  id: Mapped[int] = mapped_column(primary_key=True, auto_increment=True)
  username: Mapped[str] = mapped_column(
    String(64),
    index=True,
    unique=True,
    nullable=False
  )
  password_hash: Mapped[Optional[str]] = mapped_column(String(256))

  def __repr__(self) -> str:
    return f"<User(id={self.id}, username='{self.username}')>"

