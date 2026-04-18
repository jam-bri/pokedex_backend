from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql://USER:PASSWORD@localhost:5432/pokedex_db" # Update with your actual database credentials

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit =False, autoflush=False, bind=engine)
Base = declarative_base()