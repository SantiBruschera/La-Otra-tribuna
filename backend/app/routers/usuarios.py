from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from datetime import date
from ..db import get_db
from ..models import Usuario

router = APIRouter(tags=["usuarios"])

class UsuarioCreate(BaseModel):
    nombre: str
    apellido: str
    email: EmailStr
    contrasena: str
    fecha_alta: date

class UsuarioOut(BaseModel):
    id_usuario: int
    nombre: str
    apellido: str
    email: EmailStr
    class Config:
        from_attributes = True

@router.post("/usuarios", response_model=UsuarioOut, status_code=status.HTTP_201_CREATED)
def crear_usuario(body: UsuarioCreate, db: Session = Depends(get_db)):
    if db.query(Usuario).filter(Usuario.email == body.email).first():
        raise HTTPException(status_code=400, detail="Email ya registrado")
    u = Usuario(**body.model_dump())
    db.add(u)
    db.commit()
    db.refresh(u)
    return u

@router.get("/usuarios", response_model=list[UsuarioOut])
def listar_usuarios(db: Session = Depends(get_db)):
    return db.query(Usuario).order_by(Usuario.id_usuario.desc()).all()
