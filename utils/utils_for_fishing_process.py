from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from datetime import date

from models import *

engine = create_engine('sqlite:///fishing.db', echo=True)
Session = sessionmaker(bind=engine)

async def get_or_create_user(session, user_id, user_name):
    try:
        user = session.query(User).filter_by(user_id=user_id).first()
        if not user:
            user = User(user_id=user_id, user_name=user_name)
            session.add(user)
            session.commit()
    except SQLAlchemyError:
        session.rollback()
        raise
    return user

async def get_or_create_fishing_trip(session, user_id):
    try:
        fishtrip = session.query(FishingTrip).filter_by(
            user_id=user_id, fishing_date=date.today()).first()
        
        already_fishing = True
        
        if not fishtrip:
            already_fishing = False
            fishtrip = FishingTrip(user_id=user_id)
            session.add(fishtrip)
            session.commit()
    except SQLAlchemyError:
        session.rollback()
        raise
    return already_fishing

async def create_or_update_fish(session, user_id, fish_name, fish_count):
    try:
        fish = session.query(Fish).filter_by(
            user_id=user_id, fishing_date=date.today(), fish_name=fish_name).first()
        
        if fish:
            fish.fish_count += fish_count
            session.commit()
        elif not fish:
            fish = Fish(user_id=user_id, fishing_date=date.today(), fish_name=fish_name, fish_count=fish_count)
            session.add(fish)
            session.commit()
    except SQLAlchemyError:
        session.rollback()
        raise
    return fish 



