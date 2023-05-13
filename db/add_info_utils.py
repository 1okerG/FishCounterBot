from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from datetime import date

from .models import *


async def get_or_create_user(session, user_id, user_name):
    try:
        user = await session.execute(select(User).filter_by(user_id=user_id))
        user = user.scalar_one_or_none()
        if not user:
            user = User(user_id=user_id, user_name=user_name)
            session.add(user)
            await session.commit()
    except SQLAlchemyError:
        await session.rollback()
        raise
    return user

async def get_or_create_fishing_trip(session, user_id, fishing_date=date.today()):
    try:
        fishtrip = await session.execute(select(FishingTrip).filter_by(user_id=user_id, fishing_date=fishing_date))
        fishtrip = fishtrip.scalar_one_or_none()

        already_fishing = True
        
        if not fishtrip:
            already_fishing = False
            fishtrip = FishingTrip(user_id=user_id, fishing_date=fishing_date)
            session.add(fishtrip)
            await session.commit()
    except SQLAlchemyError:
        await session.rollback()
        raise
    return already_fishing

async def create_or_update_fish(session, user_id, fish_name, fish_count, fishing_date=date.today()):
    try:
        fish = await session.execute(select(Fish).filter_by(user_id=user_id, fishing_date=fishing_date, fish_name=fish_name))
        fish = fish.scalar_one_or_none()
        
        if fish:
            fish.fish_count += fish_count
            await session.commit()
        elif not fish:
            fish = Fish(user_id=user_id, fishing_date=fishing_date, fish_name=fish_name, fish_count=fish_count)
            session.add(fish)
            await session.commit()
    except SQLAlchemyError:
        await session.rollback()
        raise
    return fish



