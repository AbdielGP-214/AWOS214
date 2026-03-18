#Zona de Importaciones
from fastapi import FastAPI
from app.routers import usuarios,varios





#Zona de Instancias del servidor
app = FastAPI(title="MI PRIMER API",
              description="Abdiel Gonzalez Paulin",
              version="1.0.0"
              ) 

app.include_router(usuarios.router)
app.include_router(varios.router)









    




    
    
