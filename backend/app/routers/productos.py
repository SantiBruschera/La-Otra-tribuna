from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
from ..db import get_db
from ..models import ProductoBase

router = APIRouter(tags=["productos"])

class ProductoCreate(BaseModel):
    equipo: Optional[str] = None
    liga: Optional[str] = None
    marca: Optional[str] = None
    temporada: Optional[str] = None
    version: Optional[str] = None
    categoria: Optional[str] = None

class ProductoOut(BaseModel):
    id_producto: int
    equipo: Optional[str]
    liga: Optional[str]
    marca: Optional[str]
    temporada: Optional[str]
    version: Optional[str]
    categoria: Optional[str]
    class Config: from_attributes = True

@router.post("/productos-base", response_model=ProductoOut, status_code=status.HTTP_201_CREATED)
def crear_producto(body: ProductoCreate, db: Session = Depends(get_db)):
    prod = ProductoBase(**body.model_dump())
    db.add(prod)
    db.commit()
    db.refresh(prod)
    return prod

@router.get("/productos-base", response_model=List[ProductoOut])
def listar_productos(db: Session = Depends(get_db)):
    return db.query(ProductoBase).order_by(ProductoBase.id_producto.desc()).all()
