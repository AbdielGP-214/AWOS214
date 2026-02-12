#Zona de Importaciones
from fastapi import FastAPI
import asyncio
from typing import Optional

#Zona de Instancias del servidor
app = FastAPI(title="MI PRIMER API",
              description="Abdiel Gonzalez Paulin",
              version="1.0.0"
              ) 

#BD ficticia
usuarios=[
    {"id":1,"nombre":"Fidel","edad":22},
    {"id":2,"nombre":"Israel","edad":20},
    {"id":3,"nombre":"Sofi","edad":21},
]

#Zona de Endpoints
@app.get("/",tags=['Inicio'])
async def bienvenida():
    return {"mensaje": "!Bienvenido a mi API!"}

@app.get("/HolaMundo",tags=['Bienvenida Asincrona'])
async def hola():
    await asyncio.sleep(4) #simulacion de una peticion
    return {
        "mensaje": "!Hola Mundo FastAPI!",
        "estatus":"200"
        }

#PARAMETRO OBLIGATORIO
@app.get("/v1/usuario/{id}",tags=['Parametro Obligatorio'])
async def consultaUno(id:int):
    return {"Se encontro usuario" : id}

#PARAMETRO OPCIONAL
@app.get("/v1/usuario/",tags=['Parametro Opcional'])
async def consultaTodos(id:Optional [int]=None):
    if id is not None:
        for usuario in usuarios:
            if usuario["id"] == id:
                return {"mensaje": "Usuario Encontrado", "usuario":usuario}
        return  {"mensaje": "Usuario no Encontrado", "usuario":id}
    else:
        return  {"mensaje": "No se proporciono id"}



    
    
