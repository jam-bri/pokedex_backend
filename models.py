from sqlalchemy import Column, ForeignKey, Integer, String, Boolean

from database import Base

class Pokemon(Base): 
    __tablename__ = "pokemon"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index = True)
    sprite_url = Column(String)

class Favorites(Base): 
    __tablename__ = "favorites"
    id = Column(Integer, primary_key = True, index = True)
    pokemon_id = Column(Integer, ForeignKey("pokemon.id"), unique=True)

