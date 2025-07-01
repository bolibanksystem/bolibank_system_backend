from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import json
import os
import random
import re

router = APIRouter()

# Almacenamiento temporal de códigos de verificación
codigos_verificacion = {}

# Modelos para datos recibidos
class LoginData(BaseModel):
    usuario: str
    contrasena: str

class SolicitarCodigo(BaseModel):
    usuario: str

class ConfirmarCodigo(BaseModel):
    usuario: str
    codigo: str
    nueva_contrasena: str

# Ruta para login
@router.post("/login")
def login(data: LoginData):
    path = os.path.join("data", "usuarios.json")
    try:
        with open(path, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Archivo de usuarios no encontrado")

    for user in datos.get("usuarios", []):
        if user["usuario"].lower() == data.usuario.lower() and user["contrasena"] == data.contrasena:
            return {
                "mensaje": f"Bienvenida/o {user['nombre']}",
                "rol": user["rol"],
                "terminal": user.get("terminal_id", "")
            }
    raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos")

# Ruta para solicitar código de recuperación
@router.post("/recuperar-password/solicitar-codigo")
def solicitar_codigo(data: SolicitarCodigo):
    path = os.path.join("data", "usuarios.json")
    try:
        with open(path, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Archivo de usuarios no encontrado")

    # Buscar usuario
    usuario_upper = data.usuario.upper()
    for user in datos.get("usuarios", []):
        if user["usuario"].upper() == usuario_upper:
            # Generar código de 4 dígitos
            codigo = ''.join(random.choices("0123456789", k=4))
            codigos_verificacion[usuario_upper] = codigo
            # En un sistema real, enviar código por email/SMS aquí
            return {"mensaje": f"Código enviado para {data.usuario}", "codigo": codigo}  # Omitir código en producción

    raise HTTPException(status_code=404, detail="Usuario no encontrado")

# Ruta para confirmar código y cambiar contraseña
@router.post("/recuperar-password/confirmar")
def confirmar_codigo(data: ConfirmarCodigo):
    usuario_upper = data.usuario.upper()

    if usuario_upper not in codigos_verificacion:
        raise HTTPException(status_code=400, detail="No se ha solicitado código para este usuario")

    if codigos_verificacion[usuario_upper] != data.codigo:
        raise HTTPException(status_code=400, detail="Código incorrecto")

    # Validar seguridad contraseña
    nueva = data.nueva_contrasena
    if len(nueva) < 8 or not re.search(r"[A-Z]", nueva) or not re.search(r"\d", nueva) or not re.search(r"[!@#\$%\^&\*_\+\-=]", nueva):
        raise HTTPException(status_code=400, detail="Contraseña insegura: mínimo 8, 1 mayúscula, 1 número, 1 símbolo")

    path = os.path.join("data", "usuarios.json")
    try:
        with open(path, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Archivo de usuarios no encontrado")

    # Actualizar contraseña en datos
    actualizado = False
    for user in datos.get("usuarios", []):
        if user["usuario"].upper() == usuario_upper:
            user["contrasena"] = nueva
            actualizado = True
            break

    if not actualizado:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Guardar cambios
    with open(path, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, indent=4, ensure_ascii=False)

    # Borrar código temporal
    del codigos_verificacion[usuario_upper]

    return {"mensaje": "Contraseña actualizada correctamente"}

