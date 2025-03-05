#models.py
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Profile(Base):
    __tablename__ = 'profiles'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False, unique=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    gender = Column(String, nullable=True)
    date_of_birth = Column(Date, nullable=True)
    country = Column(String, nullable=True)
    city = Column(String, nullable=True)
    profile_picture = Column(String, nullable=True)