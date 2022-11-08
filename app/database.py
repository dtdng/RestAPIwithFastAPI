from importlib.metadata import metadata
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import sqlalchemy
import databases

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

database = databases.Database(SQLALCHEMY_DATABASE_URL)

metadata = sqlalchemy.MetaData()

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

metadata.create_all(engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

#Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
    