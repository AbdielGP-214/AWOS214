# Zona de Importaciones
from fastapi import FastAPI, status, HTTPException, Depends
import asyncio
from typing import Optional
from pydantic import BaseModel, Field


from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from jose import JWTError, jwt

# Zona de Instancias del servidor
app = FastAPI(title="MI PRIMER API JWT",
              description="Abdiel Gonzalez Paulin",
              version="1.0.0"
              ) 

# BD ficticia
usuarios = [
    {"id": 1, "nombre": "Fidel", "edad": 22},
    {"id": 2, "nombre": "Israel", "edad": 20},
    {"id": 3, "nombre": "Sofi", "edad": 21},
]

# Base de datos ficticia para autenticación 
usuarios_db = {
    "abdielGP": {
        "username": "abdielGP",
        "password": "123456" 
    }
}

# Modelo de validación Pydantic
class usuario_create(BaseModel):
    id: int = Field(..., gt=0, description="Identificador de usuario")
    nombre: str = Field(..., min_length=3, max_length=50, example="Juanita")
    edad: int = Field(..., ge=1, le=123, description="Edad valida entre 1 y 123")




SECRET_KEY = "una_clave_secreta_super_segura_para_firmar" 
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales no válidas",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return username

@app.post("/login", tags=['Autenticación'])
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = usuarios_db.get(form_data.username)
    if not user or form_data.password != user["password"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}




# Zona de Endpoints
@app.get("/", tags=['Inicio'])
async def bienvenida():
    return {"mensaje": "!Bienvenido a mi API!"}

@app.get("/HolaMundo", tags=['Bienvenida Asincrona'])
async def hola():
    await asyncio.sleep(4) 
    return {
        "mensaje": "!Hola Mundo FastAPI!",
        "estatus": "200"
        }

@app.get("/v1/parametroOb/{id}", tags=['Parametro Obligatorio'])
async def consultaUno(id: int):
    return {"Se encontro usuario": id}

@app.get("/v1/parametroOp/", tags=['Parametro Opcional'])
async def consultaTodos(id: Optional[int] = None):
    if id is not None:
        for usuario in usuarios:
            if usuario["id"] == id:
                return {"mensaje": "Usuario Encontrado", "usuario": usuario}
        return  {"mensaje": "Usuario no Encontrado", "usuario": id}
    else:
        return  {"mensaje": "No se proporciono id"}
    
@app.get("/v1/usuarios/", tags=['CRUD HTTP'])
async def leer_usuarios():
    return{
        "status": "200",
        "total": len(usuarios),
        "usuarios": usuarios
    }

@app.post("/v1/usuarios/", tags=['CRUD HTTP'], status_code=status.HTTP_201_CREATED)
async def crear_usuario(usuario: usuario_create):
    for usr in usuarios:
        if usr["id"] == usuario.id:
            raise HTTPException(
                status_code=400,
                detail="El id ya existe"
            )
    usuarios.append(usuario.dict())
    return{
        "mensaje": "Usuario Agregado",
        "Usuario": usuario
    }

# PUT PROTEGIDO CON JWT
@app.put("/v1/usuarios/{id}", tags=['CRUD HTTP'])
async def actualizar_usuario(id: int, usuario_actualizado: dict, current_user: str = Depends(get_current_user)):
    for index, usr in enumerate(usuarios):
        if usr["id"] == id:
            usuarios[index] = usuario_actualizado
            return {
                "mensaje": f"Usuario Actualizado correctamente por: {current_user}",
                "Usuario": usuario_actualizado
            }
    raise HTTPException(
        status_code=404,
        detail="El usuario no existe"
    )

# DELETE PROTEGIDO CON JWT
@app.delete("/v1/usuarios/", tags=['CRUD HTTP'], status_code=status.HTTP_200_OK)
async def eliminar_usuario(id: int, current_user: str = Depends(get_current_user)):
    for usuario in usuarios:
        if usuario["id"] == id:
            usuarios.remove(usuario)
            return{
                "mensaje": f"Usuario eliminado correctamente por: {current_user}",
                "usuario": usuario
            }
    raise HTTPException(
        status_code=400, 
        detail="Usuario no encontrado"
    )