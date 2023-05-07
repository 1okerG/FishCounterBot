from datetime import date
from sqlalchemy import Date, create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base


# engine = create_engine('sqlite:///fishing.db', echo=True)


Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    user_id = Column(String(50), unique=True)
    user_name = Column(String(50))


class FishingTrip(Base):
    __tablename__ = 'fishingtrip'
    id = Column(Integer, primary_key=True)
    fishing_date = Column(Date, default=date.today, unique=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User', backref=backref('fishingtrips', lazy=True))


class Fish(Base):
    __tablename__ = 'fish'
    id = Column(Integer, primary_key=True)
    fish_name = Column(String(50))
    fish_count = Column(Integer)
    fishing_date = Column(Date, ForeignKey('fishingtrip.fishing_date'))
    user_id = Column(Integer, ForeignKey('user.id'))
    fishingtrip = relationship('FishingTrip', backref=backref('fish', lazy=True))
    user = relationship('User', backref=backref('fish', lazy=True))


# Base.metadata.create_all(engine)








