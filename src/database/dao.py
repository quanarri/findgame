from pstats import Stats
from create_bot import logger

from sqlalchemy import  select
from typing import List, Dict, Any, Optional
from sqlalchemy.exc import SQLAlchemyError
from uuid import uuid4, UUID as PythonUUID

from database.base import connection
from database.models import Game, Region, Request, User




@connection
async def init_data(session):
    region = await session.scalar(select(Region).filter_by(name="Крым"))
    if not region:
        new_region = Region(name="Крым")
        session.add(new_region)

    game = await session.scalar(select(Game).filter_by(name="Дота"))
    if not game:
        new_game = Game(name="Дота")
        session.add(new_game)
        await session.commit()



@connection
async def set_user(session, tg_id: int) -> Optional[User]:
    try:
        user = await session.scalar(select(User).filter_by(id=tg_id))

        if not user:
            new_user = User(id=tg_id)
            session.add(new_user)
            await session.commit()
            logger.info(f"Зарегистрировал пользователя с ID {tg_id}!")
            return None
        else:
            logger.info(f"Пользователь с ID {tg_id} найден!")
            return user
    except SQLAlchemyError as e:
        logger.error(f"Ошибка при добавлении пользователя: {e}")
        await session.rollback()



@connection
async def get_regions(session) -> List[Dict[str, Any]]:
    try:
        result = await session.execute(select(Region))
        regions = result.scalars().all()

        if not regions:
            logger.info(f"Регионы не найдены")
            return []

        region_list = [
            {
                'id': region.id,
                'name': region.name,
            } for region in regions
        ]


        return region_list
    except SQLAlchemyError as e:
        logger.error(f"Ошибка при получении регионов: {e}")
        return []
    

@connection
async def get_games(session) -> List[Dict[str, Any]]:
    try:
        result = await session.execute(select(Game))
        games = result.scalars().all()

        if not games:
            logger.info(f"Игры не найдены")
            return []

        region_list = [
            {
                'id': game.id,
                'name': game.name,
            } for game in games
        ]


        return region_list
    except SQLAlchemyError as e:
        logger.error(f"Ошибка при получении игр: {e}")
        return []
    
@connection
async def get_my_requests(session) -> List[Dict[str, Any]]:
    try:
        result = await session.execute(select(Request))
        requests = result.scalars().all()

        if not requests:
            logger.info(f"Запросы не найдены")
            return []

        requests_list = [
            {
                'id': request.id,
            } for request in requests
        ]

        return requests_list
    except SQLAlchemyError as e:
        logger.error(f"Ошибка при получении запросов: {e}")
        return []
    
@connection
async def get_all_requests(session) -> List[Dict[str, Any]]:
    try:
        result = await session.execute(select(Game))
        games = result.scalars().all()

        if not games:
            logger.info(f"Игры не найдены")
            return []

        region_list = [
            {
                'id': game.id,
                'name': game.name,
            } for game in games
        ]


        return region_list
    except SQLAlchemyError as e:
        logger.error(f"Ошибка при получении запросов: {e}")
        return []
    

@connection
async def add_request(session, user_id: str, region: PythonUUID, game: PythonUUID) -> Optional[User]:
    try:
        request = await session.scalar(select(Request).filter_by(region_id=region, game_id=game))

        if not request:
            new_request = Request(user_id=user_id, region_id=region, game_id=game)
            session.add(new_request)
            await session.commit()
            logger.info(f"Создана новая заявки")
            return None
        else:
            logger.info(f"Заявка в регионе {region} по игре {game} уже существует!")
            return new_request
    except SQLAlchemyError as e:
        logger.error(f"Ошибка при добавлении запрос: {e}")
        await session.rollback()
