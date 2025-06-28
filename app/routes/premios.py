from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def consultar_premios():
    return {"premios": []}

@router.post("/")
def registrar_premio():
    return {"message": "Premio registrado"}