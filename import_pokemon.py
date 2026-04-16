from database import engine
from models import Base
import time
import requests
from database import SessionLocal
from models import Pokemon


#importing pokemon data from pokeapi.co if not in database
db = SessionLocal()

for i in range(1, 152):
    url = f"https://pokeapi.co/api/v2/pokemon/{i}"
    data = requests.get(url).json()

    existing = db.query(Pokemon).filter(Pokemon.id == data["id"]).first()

    if not existing:
        pokemon = Pokemon(
            id=data["id"],
            name=data["name"],
            sprite_url=data["sprites"]["other"]["dream_world"]["front_default"]
        )
        db.add(pokemon)
        db.commit()

    print(f"Imported {data['name']}") 
    time.sleep(0.3) # to avoid surcharing the server

db.close()