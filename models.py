from sqlalchemy import Column, ForeignKey, Integer, String, UniqueConstraint
from database import Base

class Pokemon(Base): 
    __tablename__ = "pokemon"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    sprite_url = Column(String)

class Favorites(Base): 
    __tablename__ = "favorites"
    id = Column(Integer, primary_key=True, index=True)
    pokemon_id = Column(Integer, ForeignKey("pokemon.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)

    __table_args__ = (
        UniqueConstraint("pokemon_id", "user_id"),
    )

class User(Base): 
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)