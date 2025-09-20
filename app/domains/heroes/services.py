from app.domains.heroes.heros_repository import HeroRepository
from app.models.heros import Hero
from app.schemas.heros import HeroCreate, HeroResponse, HeroUpdate, HeroStoryResponse


class HeroService:
  def __init__(self, repository: HeroRepository):
    self.repository = repository

  async def create_hero(self, data: HeroCreate) -> HeroResponse:
    new_hero = await self.repository.create(data)
    return HeroResponse.model_validate(new_hero)

  async def get_hero(self, hero_id: int) -> HeroResponse:
    hero = await self.repository.get_by_id(hero_id)
    return HeroResponse.model_validate(hero)

  # async def get_heros(self) -> list[HeroResponse]:
  #   heroes = await self.repository.get_all()
  #   return [HeroResponse.model_validate(hero) for hero in heroes]

  async def get_heros(
    self,
    *,
    search: str = None,
    order_by: str,
    direction: str,
    limit: int,
    offset: int,
    ) -> tuple[int, list[HeroResponse]]:
    total, heros_orm = await self.repository.get_all(
      search=search,
      order_by=order_by,
      direction=direction,
      limit=limit,
      offset=offset,
    )
    # 2. 将 ORM 对象列表转换为 Pydantic 模型列表
    heros_schema = [HeroResponse.model_validate(h) for h in heros_orm]
    # 3. 返回元组
    return total, heros_schema

  async def update_hero(self, hero_id: int, data: HeroUpdate) -> HeroResponse:
    hero = await self.repository.update(hero_id, data)
    return HeroResponse.model_validate(hero)

  async def delete_hero(self, hero_id: int) -> None:
    await self.repository.delete(hero_id)

  async def get_hero_with_story(self, hero_id: int) -> HeroStoryResponse:
    """
       获取英雄信息，并动态生成一段背景故事。
       这个方法完美展示了服务层的业务逻辑处理能力。
       """

    hero = await self.repository.get_by_id(hero_id)
    # 2. 在服务层中应用“业务逻辑”
    # 这里的逻辑是：根据英雄的名字和别名，虚构一段故事
    story_template = (
      f"在繁华的都市背后，流传着一个传说……那就是“{hero.alias}”！"
      f"很少有人知道，这位在暗夜中守护光明的英雄，其真实身份是 {hero.name}。"
      f"每一个被TA拯救的人，都会在心中默默记下这个名字。"
    )

    return HeroStoryResponse(
      id=hero.id,
      name=hero.name,
      alias=hero.alias,
      story=story_template
    )
