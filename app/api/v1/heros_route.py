from fastapi import APIRouter, Depends, status
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.session import get_db
from app.domains.heroes.heros_repository import HeroRepository
from app.domains.heroes.services import HeroService
from app.schemas.heros import HeroCreate, HeroResponse, HeroUpdate, HeroStoryResponse

router = APIRouter(prefix="/heroes", tags=["heroes"])


def get_hero_service(session: AsyncSession = Depends(get_db)) -> HeroService:
    repository = HeroRepository(session)
    return HeroService(repository)


@router.post("", response_model=HeroResponse, status_code=status.HTTP_201_CREATED)
async def create_hero(
    data: HeroCreate, service: HeroService = Depends(get_hero_service)
) -> HeroResponse:
  try:
    create_hero = await service.create_hero(data)
    logger.info(f"Created Hero {create_hero.id}")
    return create_hero
  except Exception as e:
    logger.error(f"Failed to create Hero {create_hero.id}")
    raise

@router.get("", response_model=list[HeroResponse])
async def get_All_heros(service: HeroService = Depends(get_hero_service)) -> list[HeroResponse]:
  try:
    heros = await service.get_heros()
    logger.info(f"Found {len(heros)} Heros")
    return heros
  except Exception as e:
    logger.error(f"Failed to fetch all heroes: {e}")
    raise

@router.get("/{hero_id}", response_model=HeroResponse)
async def get_hero(
    hero_id: int, service: HeroService = Depends(get_hero_service)
) -> HeroResponse:
  try:
    hero = await service.get_hero(hero_id)
    logger.info(f"Found Hero {hero.id}")
    return hero
  except Exception as e:
    logger.error(f"Failed to fetch Hero {hero_id}: {e}")
    raise

@router.patch("/{hero_id}", response_model=HeroResponse, status_code=status.HTTP_200_OK)
async def update_hero(hero_id: int, data: HeroUpdate, service: HeroService = Depends(get_hero_service)) -> HeroResponse:
  try:
    updated_hero = await service.update_hero(data=data, hero_id=hero_id)
    logger.info(f"Updated Hero {updated_hero.id}")
    return updated_hero
  except Exception as e:
    logger.error(f"Failed to update Hero {hero_id}: {e}")
    raise

@router.delete("/{hero_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_hero(hero_id: int, service: HeroService = Depends(get_hero_service)) -> None:
  try:
    await service.delete_hero(hero_id)
    logger.info(f"Deleted Hero {hero_id}")
  except Exception as e:
    logger.error(f"Failed to delete Hero {hero_id}: {e}")
    raise

@router.get("/{hero_id}/story", response_model=HeroStoryResponse)
async def generate_hero_story(
    hero_id: int, service: HeroService = Depends(get_hero_service)
) -> HeroStoryResponse:
  try:
    hero = await service.get_hero_with_story(hero_id=hero_id)
    logger.info(f"Generated story for hero {hero.id}")
    return hero
  except Exception as e:
    logger.error(f"Failed to generate story for hero {hero_id}: {e}")
    raise
