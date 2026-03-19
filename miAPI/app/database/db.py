from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

#1. Definimos la URL de la BD
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://postgres:123456@localhost:5434/DB_miapi"
)

#2. Creamos el motor de conexión a la BD
engine = create_engine(DATABASE_URL)

#3. Creamos gestionador de sesiones
SessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine)
Base = declarative_base()