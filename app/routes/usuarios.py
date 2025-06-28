from fastapi import APIRouter

router = APIRouter()

@router.post("/login")
def login():
    return {"message": "Login exitoso"}

@router.post("/register")
def register():
    return {"message": "Usuario registrado"}