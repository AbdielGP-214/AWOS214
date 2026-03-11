#zona de importaciones
from fastapi import FastAPI,status,HTTPException,Depends
import asyncio
from typing import Optional
from pydantic import BaseModel, Field
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets


#Zona de Instancias del servidor
app = FastAPI(title="SOPORTE TECNICO",)

class ticket_create(BaseModel):
    nombre:str= Field(..., min_length=3,max_length=50,example="sofia")
    descripcion:str= Field(..., min_length=20,max_length=200,example="mi problema es tal...........")
    

#seguridad

security= HTTPBasic()

def verificar_Peticion(credenciales:HTTPBasicCredentials=Depends(security)):
    userAuth = secrets.compare_digest(credenciales.username,"Soporte")
    passAuth = secrets.compare_digest(credenciales.password,"4321")

    if not(userAuth and passAuth):
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail= "Credenciales no Autorizadas"
        )
    
    return credenciales.username


#BD ficticia
ticket=[
    {"id":1,"nombre":"Fidel","descripcion":"Tengo un problema con mi computadora","prioridad":"media","estado":"pendiente"},
    {"id":2,"nombre":"Israel","descripcion":"Mi impresora no funciona","prioridad":"alta","estado":"resuelto"},
    {"id":3,"nombre":"Sofi","descripcion":"Necesito ayuda con mi teléfono","prioridad":"baja","estado":"pendiente"},
]



#zona de endpoints

#crear ticket 
@app.post("/tickets",status_code=status.HTTP_201_CREATED)
async def create_ticket(ticket:ticket_create):
    new_ticket = {
        "id": len(ticket) + 1,
        "nombre": ticket.nombre,
        "descripcion": ticket.descripcion,
        "prioridad": "media",
        "estado": "pendiente"
    }
    ticket.append(new_ticket)
    return new_ticket


#listar tickets
@app.get("/tickets",status_code=status.HTTP_200_OK)
async def get_tickets():
    return ticket

#obtener ticket por id
@app.get("/tickets/{ticket_id}",status_code=status.HTTP_200_OK)
async def get_ticket(ticket_id:int,usuario:str=Depends(verificar_Peticion)):
    for t in ticket:
        if t["id"] == ticket_id:
            return t
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Ticket no encontrado")

#cambiar estado del ticket
@app.put("/tickets/{ticket_id}",status_code=status.HTTP_200_OK)
async def update_ticket(ticket_id:int,estado:str=Field(...,example="resuelto"),usuario:str=Depends(verificar_Peticion)):
    for t in ticket:
        if t["id"] == ticket_id:
            t["estado"] = estado
            return t
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Ticket no encontrado")

#eliminar ticket
@app.delete("/tickets/{ticket_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_ticket(ticket_id:int,usuario:str=Depends(verificar_Peticion)):
    global ticket
    ticket = [t for t in ticket if t["id"] != ticket_id]
    return None

