from fastapi import Depends,HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets


#Seguridad HTTP Basic

security= HTTPBasic()

def verificar_Peticion(credenciales:HTTPBasicCredentials=Depends(security)):
    userAuth = secrets.compare_digest(credenciales.username,"abdielGP")
    passAuth = secrets.compare_digest(credenciales.password,"123456")

    if not(userAuth and passAuth):
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail= "Credenciales no Autorizadas"
        )
    
    return credenciales.username