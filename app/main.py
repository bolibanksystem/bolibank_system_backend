from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from routers import login  # Esto importa bien el archivo login.py

app = FastAPI()

# Middleware para CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Archivos estáticos
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/")
def root():
    return {"mensaje": "BoliBank System API está funcionando correctamente."}

@app.get("/favicon.ico")
async def favicon():
    return FileResponse("app/static/favicon.ico")

# Aquí incluimos el router
app.include_router(login.router, prefix="/auth", tags=["auth"])
