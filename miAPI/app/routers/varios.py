from typing import Optional
import asyncio
from app.database.database import usuarios
from fastapi import APIRouter

router= APIRouter(tags=['Varios'])


#Zona de Endpoints
@router.get("/")
async def bienvenida():
    return {"mensaje": "!Bienvenido a mi API!"}

@router.get("/HolaMundo",tags=['Bienvenida Asincrona'])
async def hola():
    await asyncio.sleep(4) #simulacion de una peticion
    return {
        "mensaje": "!Hola Mundo FastAPI!",
        "estatus":"200"
        }

#PARAMETRO OBLIGATORIO
@router.get("/v1/parametroOb/{id}",tags=['Parametro Obligatorio'])
async def consultaUno(id:int):
    return {"Se encontro usuario" : id}

#PARAMETRO OPCIONAL
@router.get("/v1/parametroOp/",tags=['Parametro Opcional'])
async def consultaTodos(id:Optional [int]=None):
    if id is not None:
        for usuario in usuarios:
            if usuario["id"] == id:
                return {"mensaje": "Usuario Encontrado", "usuario":usuario}
        return  {"mensaje": "Usuario no Encontrado", "usuario":id}
    else:
        return  {"mensaje": "No se proporciono id"}