from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Annotated
from sqlalchemy.orm import Session
from database import Base, SessionLocal, engine
from models import Pokemon, Favorites

#Create the database tables 
Base.metadata.create_all(bind=engine)

app = FastAPI()

class PokemonSchema(BaseModel):
    id: int
    name : str
    sprite_url: str

class FavoritesSchema(BaseModel): 
    id : int
    pokemon_id : int


class FavoriteCreate(BaseModel): 
    pokemon_id : int

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
#Get pokemon by name
@app.get("/pokemon/name/{name}", response_model= PokemonSchema)
def get_pokemon_by_name(name: str, db: Session = Depends(get_db)):
    return db.query(Pokemon).filter(Pokemon.name == name).first()

#Get pokemon by id 
@app.get("/pokemon/id/{id}", response_model=PokemonSchema)
def get_pokemon_by_id(id: int, db: Session = Depends(get_db)):
    return db.query(Pokemon).filter(Pokemon.id == id).first()



###API endpoints to retrive pokemon from database

# API to get all the pokemon in the favorites
@app.get("/favorites", response_model=List[PokemonSchema])
def get_favorites(db:Session = Depends(get_db)):
        favorites = db.query(Favorites).all()
        pokemon_ids = [fav.pokemon_id for fav in favorites]
        return db.query(Pokemon).filter(Pokemon.id.in_(pokemon_ids)).all()

# Api to add a pokemon to the favorites
@app.post("/favorites")
def add_to_favorite(fav: FavoriteCreate, db: Session = Depends(get_db)):
    existing = db.query(Favorites).filter(Favorites.pokemon_id == fav.pokemon_id).first()

    if existing:
        return {"message": "Already in favorites"}

    new_fav = Favorites(pokemon_id=fav.pokemon_id)
    db.add(new_fav)
    db.commit()

    return {"message": "Added to favorites"}

# Api to remove a pokemon from the favorites
@app.delete("/favorites/{pokemon_id}", response_model=FavoritesSchema)
def remove_from_favorites(pokemon_id: int, db: Session = Depends(get_db)):
    favorite = db.query(Favorites).filter(Favorites.pokemon_id == pokemon_id).first()
    if not favorite:
        raise HTTPException(status_code=404, detail="Favorite not found")
    db.delete(favorite)
    db.commit()
    return {"message": "Removed from favorites"}