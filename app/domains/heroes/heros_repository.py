from sqlite3 import IntegrityError

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import AlreadyExistsException, NotFoundException
from app.models.heros import Hero
from app.schemas.heros import HeroCreate, HeroUpdate
from sqlalchemy import select


class HeroRepository:
  """Repository for handling hero database operations."""

  def __init__(self, session: AsyncSession):
    self.session = session

  async def create(self, hero_data: HeroCreate) -> Hero:
    """Create a new hero."""
    hero = Hero(**hero_data.model_dump())
    try:
      self.session.add(hero)
      await self.session.commit()
      await self.session.refresh(hero)
      return hero
    except IntegrityError:
      await self.session.rollback()
      raise AlreadyExistsException(
        f"Hero with alias {hero_data.alias} already exists"
      )

  async def get_by_id(self, hero_id: int) -> Hero:
    """Get a hero by its id."""
    hero = await self.session.get(Hero, hero_id)
    if not hero:
      raise NotFoundException(f"Hero with alias {hero_id} not found")
    return hero

  async def get_all(self) -> list[Hero]:
    """Get all heroes."""
    query = select(Hero)
    result = await self.session.scalars(query)
    return list(result.all())

  async def update(self, hero_id: int, hero_data: HeroUpdate) -> Hero:
    """Update a hero."""
    # 复用了 get_by_id 逻辑
    hero = await self.get_by_id(hero_id)

    update_data = hero_data.model_dump(exclude_unset=True)

    if not update_data:
      raise ValueError("no fields to update")

    for key, value in update_data.items():
      setattr(hero, key, value)

    await self.session.commit()
    await self.session.refresh(hero)
    return hero

  async def delete(self, hero_id: int) -> None:
    """Delete a hero."""
    hero = await self.get_by_id(hero_id)

    await self.session.delete(hero)
    await self.session.commit()


