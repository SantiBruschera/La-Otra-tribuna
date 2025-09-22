from fastapi import FastAPI
from .db import Base, engine
from .routers import publicacion, usuarios, productos  


# crea las tablas en Postgres si no existen (temporal; luego migraciones)
# Base.metadata.create_all(bind=engine)

app = FastAPI(title="La Otra Tribuna API")

@app.get("/health")
def health():
    return {"status": "ok", "service": "la-otra-tribuna"}

app.include_router(usuarios.router, prefix="/api")
app.include_router(productos.router, prefix="/api")
app.include_router(publicacion.router, prefix="/api")

