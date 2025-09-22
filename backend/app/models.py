from sqlalchemy import Column, Integer, String, Text, DECIMAL, Date, ForeignKey, UniqueConstraint, CheckConstraint
from sqlalchemy.orm import relationship
from .db import Base

class Usuario(Base):
    __tablename__ = "usuario"
    id_usuario = Column(Integer, primary_key=True, autoincrement=True, index=True)
    nombre = Column(String(30), nullable=False)
    apellido = Column(String(30), nullable=False)
    email = Column(String(50), unique=True, nullable=False, index=True)
    contrasena = Column(String(100), nullable=False)
    fecha_alta = Column(Date, nullable=False)

class ProductoBase(Base):
    __tablename__ = "producto_base"
    id_producto = Column(Integer, primary_key=True, autoincrement=True)
    equipo = Column(String(50))
    liga = Column(String(50))
    marca = Column(String(30))
    temporada = Column(String(20))
    version = Column(String(20))
    categoria = Column(String(20))
    publicaciones = relationship("Publicacion", back_populates="producto")

class Publicacion(Base):
    __tablename__ = "publicacion"
    id_publicacion = Column(Integer, primary_key=True, autoincrement=True)
    # 👇 sin "public."
    id_usuario  = Column(Integer, ForeignKey("usuario.id_usuario"), nullable=False, index=True)
    id_producto = Column(Integer, ForeignKey("producto_base.id_producto"), nullable=False, index=True)
    titulo = Column(String(100), nullable=False)
    descripcion = Column(Text)
    precio = Column(DECIMAL(10, 2), nullable=False)
    moneda = Column(String(10), nullable=False)
    condicion = Column(String(20))
    autenticidad = Column(String(20))
    talle = Column(String(10))
    stock = Column(Integer, nullable=False)
    estado = Column(String(20), nullable=False)
    fecha_publicacion = Column(Date, nullable=False)
    producto = relationship("ProductoBase", back_populates="publicaciones")
    fotos = relationship("Foto", back_populates="publicacion", cascade="all, delete-orphan")

class Foto(Base):
    __tablename__ = "foto"
    __table_args__ = (
        UniqueConstraint("id_publicacion", "orden_foto"),
        CheckConstraint("orden_foto >= 1"),
    )
    id_foto = Column(Integer, primary_key=True, autoincrement=True)
    # 👇 sin "public."
    id_publicacion = Column(Integer, ForeignKey("publicacion.id_publicacion"), nullable=False, index=True)
    url = Column(String(200), nullable=False)
    orden_foto = Column(Integer, nullable=False)
    publicacion = relationship("Publicacion", back_populates="fotos")



