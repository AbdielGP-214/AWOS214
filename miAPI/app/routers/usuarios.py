
from fastapi import Depends,HTTPException, status, APIRouter
from app.models.usuario import usuario_create
from app.database.database import usuarios
from app.security.auth import verificar_Peticion

from sqlalchemy.orm import Session
from app.database.db import get_db
from app.database.usuario import Usuario as usuarioDB

router = APIRouter(
    prefix= "/v1/usuarios", tags=["CRUD HTTP"]
)


#get
@router.get("/")
async def leer_usuarios(db: Session = Depends(get_db)):
    queryUsers= db.query(usuarioDB).all()
    return{
        "status":"200",
        "total": len(queryUsers),
        "usuarios": queryUsers
    }

#post
@router.post("/",status_code=status.HTTP_201_CREATED)
async def crear_usuario(usuarioP:usuario_create, db: Session = Depends(get_db)):
    
    nuevoUsuario = usuarioDB(
        nombre=usuarioP.nombre,
        edad=usuarioP.edad
    )
    
    db.add(nuevoUsuario)
    db.commit()
    db.refresh(nuevoUsuario)
    
    return{
        "mensaje":"Usuario Agregado",
        "Usuario":usuarioP
    }

#put
@router.put("/{id}",status_code=status.HTTP_200_OK)
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
@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def eliminar_usuario(id:int, userAuth:str= Depends(verificar_Peticion)):
    for usuario in usuarios:
        if usuario["id"] == id:
            usuarios.remove(usuario)
            return{
                "mensaje": f"Usuario eliminado correctamente por :{userAuth}",
                "usuario": usuario
            }
    raise HTTPException(
        status_code=400, 
        detail="Usuario no encontrado"
    )