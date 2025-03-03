import os
import sys
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship
from sqlalchemy import create_engine, String, ForeignKey
from eralchemy2 import render_er

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    firstname: Mapped[str] = mapped_column(nullable=False)
    lastname: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    
    favorites = relationship("Favorite", back_populates="user")

class Character(Base):
    __tablename__ = 'character'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    birthday: Mapped[str] = mapped_column()
    gender: Mapped[str] = mapped_column()
    height: Mapped[str] = mapped_column()
    weight: Mapped[str] = mapped_column()
    hair_color: Mapped[str] = mapped_column()
    eye_color: Mapped[str] = mapped_column()
    
    favorites = relationship("Favorite", back_populates="character")

class Planet(Base):
    __tablename__ = 'planet'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    weather: Mapped[str] = mapped_column()
    population: Mapped[str] = mapped_column()
    gravity: Mapped[str] = mapped_column()
    size: Mapped[str] = mapped_column()
    
    favorites = relationship("Favorite", back_populates="planet")

class Favorite(Base):
    __tablename__ = 'favorite'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    character_id: Mapped[int] = mapped_column(ForeignKey('character.id'), nullable=True)
    planet_id: Mapped[int] = mapped_column(ForeignKey('planet.id'), nullable=True)
    
    user = relationship("User", back_populates="favorites")
    character = relationship("Character", back_populates="favorites")
    planet = relationship("Planet", back_populates="favorites")


    def to_dict(self):
        return {}