from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import json
import os

router = APIRouter()

# Modelo para los datos de entrada (login)
class LoginData(BaseModel):
    usuario: str
    contrasena: str

# Modelo para la respuesta del login
class LoginResponse(BaseModel):
    mensaje: str
    rol: str
    terminal: str

@router.post("/login", response_model=LoginResponse)
def login(data: LoginData):
    path = os.path.join("data", "usuarios.json")
    try:
        with open(path, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Archivo de usuarios no encontrado")

    for user in datos.get("usuarios", []):
        if user["usuario"].lower() == data.usuario.lower() and user["contrasena"] == data.contrasena:
            return LoginResponse(
                mensaje=f"Bienvenida/o {user['nombre']}",
                rol=user["rol"],
                terminal=user["terminal_id"]
            )
    raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos")
