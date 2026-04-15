from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Annotated
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Pokemon


app = FastAPI()

class PokemonSchema(BaseModel):
    id: int
    name : str
    sprite_url: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


###API endpoints to retrive pokemon from database

#Get all pokemon
@app.get("/pokemon", response_model=List[PokemonSchema])
def get_pokemon(db: Session = Depends(get_db)):
    return db.query(Pokemon).all()
#Get pokemon by id 
@app.get("/pokemon/{id}", response_model=PokemonSchema)
def get_pokemon_by_id(id: int, db: Session = Depends(get_db)):
    return db.query(Pokemon).filter(Pokemon.id == id).first()
#Get pokemon by name
@app.get("/pokemon/{name}", response_model= PokemonSchema)
def get_pokemon_by_name(name: str, db: Session = Depends(get_db)):
    return db.query(Pokemon).filter(Pokemon.name == name).first()