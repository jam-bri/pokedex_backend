from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# DATABASE_URL = "postgresql://pokedex_user:password@localhost:5432/pokedex_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit =False, autoflush=False, bind=engine)
Base = declarative_base()