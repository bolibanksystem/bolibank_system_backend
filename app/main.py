from fastapi import FastAPI
from routers import login

app = FastAPI()

app.include_router(login.router)

@app.get("/")
def root():
    return {"mensaje": "BoliBank SYSTEM backend funcionando."}
