#Zona de Importaciones
from fastapi import FastAPI
from app.routers import usuarios,varios
from app.database.db import engine
from app.database import usuario 

usuario.Base.metadata.create_all(bind=engine)



#Zona de Instancias del servidor
app = FastAPI(title="MI PRIMER API",
              description="Abdiel Gonzalez Paulin",
              version="1.0.0"
              ) 

app.include_router(usuarios.router)
app.include_router(varios.router)









    




    
    
