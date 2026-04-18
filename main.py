from fastapi import FastAPI, HTTPException, Depends, Header
from passlib.context import CryptContext
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy.orm import Session
from database import Base, SessionLocal, engine
from models import Pokemon, Favorites, User
from starlette.middleware.cors import CORSMiddleware
import secrets

# Create the database tables(if it doesn't exist yet)
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Simple in-memory token store ---
active_tokens: dict[str, int] = {}  # token -> user_id

# --- Schemas ---

class PokemonSchema(BaseModel):
    id: int
    name: str
    sprite_url: str
    class Config:
        from_attributes = True

class FavoritesSchema(BaseModel):
    id: int
    pokemon_id: int
    user_id: int

class FavoriteCreate(BaseModel):
    pokemon_id: int

class UserCreate(BaseModel):
    username: str
    password: str


# --- Dependencies ---

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(authorization: Optional[str] = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Please log in first")
    token = authorization.split(" ")[1]
    user_id = active_tokens.get(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return user_id

# --- Security ---
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# --- Endpoints: Users ---
@app.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    new_user = User(username=user.username, hashed_password=hash_password(user.password))
    db.add(new_user)
    db.commit()
    return {"message": "User created successfully"}

@app.post("/signin")
def signin(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    token = secrets.token_urlsafe(32)
    active_tokens[token] = db_user.id
    return {
        "message": f"Welcome back, {db_user.username}!",
        "token": token,
        "user_id": db_user.id,
        "username": db_user.username
    }

@app.post("/signout")
def signout(authorization: Optional[str] = Header(None)):
    if authorization and authorization.startswith("Bearer "):
        token = authorization.split(" ")[1]
        active_tokens.pop(token, None)
    return {"message": "Logged out successfully"}

# --- Endpoints: Pokemon ---

@app.get("/pokemon", response_model=List[PokemonSchema])
def get_pokemon(db: Session = Depends(get_db)):
    return db.query(Pokemon).all()

@app.get("/pokemon/name/{name}", response_model=PokemonSchema)
def get_pokemon_by_name(name: str, db: Session = Depends(get_db)):
    return db.query(Pokemon).filter(Pokemon.name == name).first()

@app.get("/pokemon/id/{id}", response_model=PokemonSchema)
def get_pokemon_by_id(id: int, db: Session = Depends(get_db)):
    return db.query(Pokemon).filter(Pokemon.id == id).first()

# --- Endpoints: Favorites ---
@app.get("/favorites", response_model=List[PokemonSchema])
def get_favorites(db: Session = Depends(get_db), user_id: int = Depends(get_current_user)):
    favorites = db.query(Favorites).filter(Favorites.user_id == user_id).all()
    pokemon_ids = [fav.pokemon_id for fav in favorites]
    return db.query(Pokemon).filter(Pokemon.id.in_(pokemon_ids)).all()

@app.post("/favorites")
def add_to_favorite(fav: FavoriteCreate, db: Session = Depends(get_db), user_id: int = Depends(get_current_user)):
    existing = db.query(Favorites).filter(Favorites.pokemon_id == fav.pokemon_id,Favorites.user_id == user_id).first()

    if existing:
        return {"message": "Already in favorites"}

    new_fav = Favorites(pokemon_id=fav.pokemon_id, user_id=user_id)
    db.add(new_fav)
    db.commit()
    return {"message": "Added to favorites"}

@app.delete("/favorites/{pokemon_id}")
def remove_from_favorites(pokemon_id: int, db: Session = Depends(get_db), user_id: int = Depends(get_current_user)):
    favorite = db.query(Favorites).filter(Favorites.pokemon_id == pokemon_id, Favorites.user_id == user_id).first()
    
    if not favorite:
        raise HTTPException(status_code=404, detail="Favorite not found")

    db.delete(favorite)
    db.commit()
    return {"message": "Removed from favorites"}