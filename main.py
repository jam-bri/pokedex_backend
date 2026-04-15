from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Annotated
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Pokemon


app = FastAPI()

class Pokemon(BaseModel):
    id: int
    name : str
    sprite_url: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/pokemon")
def get_pokemon(db: Session = Depends(get_db)):
    return db.query(Pokemon).all()

@app.get("/pokemon/{id}")
def get_pokemon_by_id(id: int, db: Session = Depends(get_db)):
    return db.query(Pokemon).filter(Pokemon.id == id).first()