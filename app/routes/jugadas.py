from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def listar_jugadas():
    return {"jugadas": []}

@router.post("/")
def registrar_jugada():
    return {"message": "Jugada registrada"}