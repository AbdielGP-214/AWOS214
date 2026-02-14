#Zona de Importaciones
from fastapi import FastAPI,status,HTTPException
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
@app.get("/v1/parametroOb/{id}",tags=['Parametro Obligatorio'])
async def consultaUno(id:int):
    return {"Se encontro usuario" : id}

#PARAMETRO OPCIONAL
@app.get("/v1/parametroOp/",tags=['Parametro Opcional'])
async def consultaTodos(id:Optional [int]=None):
    if id is not None:
        for usuario in usuarios:
            if usuario["id"] == id:
                return {"mensaje": "Usuario Encontrado", "usuario":usuario}
        return  {"mensaje": "Usuario no Encontrado", "usuario":id}
    else:
        return  {"mensaje": "No se proporciono id"}
    
#get
@app.get("/v1/usuarios/",tags=['CRUD HTTP'])
async def leer_usuarios():
    return{
        "status":"200",
        "total": len(usuarios),
        "usuarios": usuarios
    }

#post
@app.post("/v1/usuarios/",tags=['CRUD HTTP'],status_code=status.HTTP_201_CREATED)
async def crear_usuario(usuario:dict):
    for usr in usuarios:
        if usr["id"] == usuario.get("id"):
            raise HTTPException(
                status_code=400,
                detail="El id ya existe"
            )
    usuarios.append(usuario)
    return{
        "mensaje":"Usuario Agregado",
        "Usuario":usuario
    }

#put
@app.put("/v1/usuarios/{id}", tags=['CRUD HTTP'])
async def actualizar_usuario(id: int, usuario_actualizado: dict):
    for index, usr in enumerate(usuarios):
        if usr["id"] == id:
            usuarios[index] = usuario_actualizado
            return {
                "mensaje": "Usuario Actualizado",
                "Usuario": usuario_actualizado
            }
    raise HTTPException(
        status_code=404,
        detail="El usuario no existe"
    )


#delete
@app.delete("/V1/usuarios/", tags=['CRUD HTTP'], status_code=status.HTTP_200)
async def eliminar_usuario(id:int):
    for usuario in usuarios:
        if usuario["id"] == id:
            usuarios.remove(usuario)
            return{
                "mensaje": "Usuario eliminado correctamente",
                "usuario": usuario
            }
    raise HTTPException(
        status_code=400, 
        detail="Usuario no encontrado"
    )



    
    
