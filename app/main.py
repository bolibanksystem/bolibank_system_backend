from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from routers import login  # importa login.py

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # o restringe a tu dominio
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.api_route("/", methods=["GET", "HEAD"])
def root():
    return {"mensaje": "BoliBank System API está funcionando correctamente."}

@app.get("/favicon.ico")
async def favicon():
    return FileResponse("app/static/favicon.ico")

# Aquí incluimos el router
app.include_router(login.router, prefix="/auth", tags=["auth"])
