from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, condecimal
from typing import Optional, List
from datetime import date
from ..db import get_db
from ..models import Publicacion, Foto, ProductoBase, Usuario
from sqlalchemy.exc import IntegrityError, DataError, ProgrammingError, OperationalError

router = APIRouter(tags=["publicaciones"])

# ---- Schemas ----
class FotoIn(BaseModel):
    url: str
    orden_foto: int

class PublicacionCreate(BaseModel):
    id_usuario: int
    id_producto: int
    titulo: str
    descripcion: Optional[str] = None
    precio: condecimal(max_digits=10, decimal_places=2)
    moneda: str
    condicion: Optional[str] = None
    autenticidad: Optional[str] = None
    talle: Optional[str] = None
    stock: int
    estado: str
    fecha_publicacion: date
    fotos: List[FotoIn] = []

class PublicacionOut(BaseModel):
    id_publicacion: int
    titulo: str
    precio: condecimal(max_digits=10, decimal_places=2)
    moneda: str
    stock: int
    estado: str
    class Config: from_attributes = True

# ---- Endpoints ----
@router.post("/publicaciones", response_model=PublicacionOut, status_code=status.HTTP_201_CREATED)
def crear_publicacion(body: PublicacionCreate, db: Session = Depends(get_db)):
    if not db.get(Usuario, body.id_usuario):
        raise HTTPException(400, "id_usuario inexistente")
    if not db.get(ProductoBase, body.id_producto):
        raise HTTPException(400, "id_producto inexistente")

    pub = Publicacion(
        id_usuario=body.id_usuario,
        id_producto=body.id_producto,
        titulo=body.titulo,
        descripcion=body.descripcion,
        precio=body.precio,
        moneda=body.moneda,
        condicion=body.condicion,
        autenticidad=body.autenticidad,
        talle=body.talle,
        stock=body.stock,
        estado=body.estado,
        fecha_publicacion=body.fecha_publicacion,
    )

    try:
        db.add(pub)
        db.flush()  # ya tengo pub.id_publicacion

        for f in body.fotos:
            db.add(Foto(
                id_publicacion=pub.id_publicacion,
                url=f.url,
                orden_foto=f.orden_foto
            ))

        db.commit()
        db.refresh(pub)
        return pub

    except (IntegrityError, DataError, ProgrammingError, OperationalError) as e:
        db.rollback()
        # mensaje claro desde Postgres (FK/UNIQUE/CHECK/NOT NULL/etc.)
        raise HTTPException(status_code=400, detail=str(e.orig))
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/publicacion", response_model=List[PublicacionOut])
def listar_publicaciones(db: Session = Depends(get_db)):
    return db.query(Publicacion).order_by(Publicacion.id_publicacion.desc()).all()
