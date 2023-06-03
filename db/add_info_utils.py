from sqlalchemy import and_, select
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
        fish = await session.execute(
            select(Fish).join(FishingTrip).filter(
                and_(
                    FishingTrip.user_id == user_id,
                    FishingTrip.fishing_date == fishing_date,
                    Fish.fish_name == fish_name
                )
            )
        )
        fish = fish.scalar_one_or_none()

        if fish:
            fish.fish_count += fish_count
            await session.commit()
        elif not fish:
            fishing_trip = await session.execute(
                select(FishingTrip).filter(
                    and_(
                        FishingTrip.user_id == user_id,
                        FishingTrip.fishing_date == fishing_date
                    )
                )
            )
            fishing_trip = fishing_trip.scalar_one_or_none()

            if fishing_trip:
                fish = Fish(user_id=user_id, fishingtrip_id=fishing_trip.id, fish_name=fish_name, fish_count=fish_count)
                session.add(fish)
                await session.commit()
            else:
                # Handle the case when there is no FishingTrip for the given user and date
                # You may choose to raise an exception or handle it in a different way
                pass
    except SQLAlchemyError:
        await session.rollback()
        raise
    return fish



