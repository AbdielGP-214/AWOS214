from fastapi import FastAPI, status, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, EmailStr
from typing import List, Literal
from datetime import datetime

app = FastAPI(
    title="API Biblioteca Digital",
    description="Abdiel Gonzalez Paulin",
    version="1.0.0"
)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": "Faltan datos o el nombre del libro no es válido."}
    )

# BD ficticia
libros = []
prestamos = []

#Modelos de validacion Pydantic

anio_actual = datetime.now().year

class Usuario(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100, description="Nombre del usuario")
    correo: EmailStr = Field(..., description="Correo válido del usuario")

class Libro(BaseModel):
    id: int = Field(..., gt=0, description="ID del libro")
    nombre: str = Field(..., min_length=2, max_length=100, description="Nombre del libro")
    anio_libro: int = Field(..., gt=1450, le=anio_actual, description="Año de publicación")
    paginas: int = Field(..., gt=1, description="Número de páginas")
    estado: Literal["disponible", "prestado"] = "disponible"

class Prestamo(BaseModel):
    id_prestamo: int = Field(..., gt=0)
    id_libro: int = Field(..., gt=0)
    usuario: Usuario


# Zona de Endpoints

# a. Registrar un libro
@app.post("/v1/libros/", tags=['Libros'], status_code=status.HTTP_201_CREATED)
async def registrar_libro(libro_nuevo: Libro):
    
    for lib in libros:
        if lib.id == libro_nuevo.id:
            raise HTTPException(status_code=400, detail="El ID del libro ya existe")
            
    libros.append(libro_nuevo)
    return {
        "mensaje": "Libro registrado exitosamente",
        "libro": libro_nuevo
    }

# b. Listar todos los libros disponibles
@app.get("/v1/libros/disponibles", tags=['Libros'])
async def listar_disponibles():
    libros_disponibles = []
    for lib in libros:
        if lib.estado == "disponible":
            libros_disponibles.append(lib)
            
    return {
        "status": "200",
        "total": len(libros_disponibles),
        "libros": libros_disponibles
    }

# c. Buscar un libro por su nombre
@app.get("/v1/libros/buscar/{nombre}", tags=['Libros'])
async def buscar_libro(nombre: str):
    libros_encontrados = []
    for lib in libros:
        
        if nombre.lower() in lib.nombre.lower():
            libros_encontrados.append(lib)
            
    if len(libros_encontrados) == 0:
        raise HTTPException(status_code=400, detail="Libro no encontrado")
        
    return {"mensaje": "Libros encontrados", "libros": libros_encontrados}

# d. Registrar el préstamo de un libro a un usuario
@app.post("/v1/prestamos/", tags=['Préstamos'], status_code=status.HTTP_201_CREATED)
async def registrar_prestamo(nuevo_prestamo: Prestamo):
    libro_encontrado = None
    
    
    for lib in libros:
        if lib.id == nuevo_prestamo.id_libro:
            libro_encontrado = lib
            break
            
    if libro_encontrado is None:
        raise HTTPException(status_code=400, detail="El libro no existe")
        
    if libro_encontrado.estado == "prestado":
        raise HTTPException(status_code=409, detail="El libro ya está prestado")
        
    
    libro_encontrado.estado = "prestado"
    prestamos.append(nuevo_prestamo)
    
    return {"mensaje": "Préstamo registrado correctamente"}

# e. Marcar un libro como devuelto
@app.put("/v1/libros/{id_libro}/devolver", tags=['Libros'], status_code=status.HTTP_200_OK)
async def devolver_libro(id_libro: int):
    for lib in libros:
        if lib.id == id_libro:
            if lib.estado == "disponible":
                raise HTTPException(status_code=400, detail="El libro ya estaba disponible")
                
            lib.estado = "disponible"
            return {"mensaje": "Libro devuelto con éxito", "libro": lib}
            
    raise HTTPException(status_code=400, detail="El libro no existe")

# f. Eliminar el registro de un préstamo
@app.delete("/v1/prestamos/{id_prestamo}", tags=['Préstamos'], status_code=status.HTTP_200_OK)
async def eliminar_prestamo(id_prestamo: int):
    for prestamo in prestamos:
        if prestamo.id_prestamo == id_prestamo:
            prestamos.remove(prestamo)
            return {"mensaje": "Registro de préstamo eliminado"}
            
    
    raise HTTPException(status_code=409, detail="El registro de préstamo ya no existe")