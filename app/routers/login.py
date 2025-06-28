from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import json

router = APIRouter()

# Modelo que valida los datos de entrada
class LoginData(BaseModel):
    usuario: str
    contrasena: str

@router.post("/login")
def login(data: LoginData):
    try:
        with open("app/data/usuarios.json", "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Archivo de usuarios no encontrado")

    for user in datos.get("usuarios", []):
        if user["usuario"].lower() == data.usuario.lower() and user["contrasena"] == data.contrasena:
            return {
                "mensaje": f"Bienvenida/o {user['nombre']}",
                "rol": user["rol"],
                "terminal": user["terminal_id"]
            }

    raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos")
