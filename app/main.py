from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from routers import login  # Asegúrate que 'routers/login.py' existe y contiene 'router'

app = FastAPI()

# Permitir peticiones CORS (ajusta los orígenes si necesitas seguridad más estricta)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cambia "*" por dominios específicos si quieres restringir
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Montar carpeta static para servir archivos como favicon
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Ruta raíz (para prueba de funcionamiento)
@app.get("/", include_in_schema=False)
@app.head("/", include_in_schema=False)
def root():
    return {"mensaje": "BoliBank System API está funcionando correctamente."}

# Ruta del favicon para evitar error 404
@app.get("/favicon.ico")
async def favicon():
    return FileResponse("app/static/favicon.ico")

# Incluir rutas del login (si usas más routers, agrégalos también)
app.include_router(login.router, prefix="/auth", tags=["auth"])
