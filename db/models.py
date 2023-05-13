from datetime import date
from sqlalchemy import Date, Column, Integer, MetaData, String, ForeignKey
from sqlalchemy.orm import relationship, backref

from .base import Base

metadata = MetaData()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, unique=True)
    user_name = Column(String(50))


class FishingTrip(Base):
    __tablename__ = 'fishingtrip'
    id = Column(Integer, primary_key=True)
    fishing_date = Column(Date, default=date.today, unique=True)
    user_id = Column(Integer, ForeignKey('user.user_id'))
    user = relationship('User', backref=backref('fishingtrips', lazy=True))


class Fish(Base):
    __tablename__ = 'fish'
    id = Column(Integer, primary_key=True)
    fish_name = Column(String(50))
    fish_count = Column(Integer)
    fishing_date = Column(Date, ForeignKey('fishingtrip.fishing_date'))
    user_id = Column(Integer, ForeignKey('user.user_id'))
    fishingtrip = relationship('FishingTrip', backref=backref('fish', lazy=True))
    user = relationship('User', backref=backref('fish', lazy=True))









