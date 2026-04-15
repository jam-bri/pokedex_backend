from sqlalchemy import Column, Integer, String, Boolean

from database import Base

class Pokemon(Base): 
    __tablename__ = "pokemon"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index = True)
    sprite_url = Column(String)