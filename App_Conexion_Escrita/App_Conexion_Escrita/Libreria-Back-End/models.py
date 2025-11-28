"""
Modelos ORM de SQLAlchemy para la aplicación de librería.

Este módulo define:
- Enumeraciones para tipos de punto de venta, roles de usuario y tipos de movimiento.
- Tablas principales:
    - PuntoVenta
    - Usuario
    - Papel
    - Libro
    - InventarioLibro
    - MovimientoLibro

Cada clase mapea una tabla de la base de datos y se usa para interactuar
con la BD a través de SQLAlchemy.
"""

from sqlalchemy import Column, Integer, String, Enum, Text, ForeignKey, DateTime, DECIMAL
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base
import enum


# Definiciones de tipo de punto de venta.
class TipoPuntoVenta(enum.Enum):
    tienda = "tienda"
    metro = "metro"
    online = "online"

# Diferenciar los roles de usuario.
class RolUsuario(enum.Enum):
    admin = "admin"
    vendedor = "vendedor"


# Definicion de tipo de movimiento de inventario.
class TipoMovimiento(enum.Enum):
    entrada = "entrada"
    salida = "salida"
    venta = "venta"
    ajuste = "ajuste"


# Tabla de punto de venta.
class PuntoVenta(Base):
    __tablename__ = "puntos_venta"
    id_punto_venta = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    ubicacion = Column(String(150))
    tipo = Column(Enum(TipoPuntoVenta), nullable=False)
    usuarios = relationship("Usuario", back_populates="punto_venta")

# Tabla de usuarios.
class Usuario(Base):
    __tablename__ = "usuarios"
    id_usuario = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(100), unique=True)
    contrasena = Column(String(255), nullable=False)
    rol = Column(Enum(RolUsuario), nullable=False)
    punto_venta_id = Column(Integer, ForeignKey("puntos_venta.id_punto_venta"))
    punto_venta = relationship("PuntoVenta", back_populates="usuarios")

# Tabla de papel.
class Papel(Base):
    __tablename__ = "papel"
    paginas = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    stock_paginas = Column(Integer, nullable=False)

# Tabla de libros.
class Libro(Base):
    __tablename__ = "libros"
    id_libro = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(150), nullable=False)
    categoria = Column(String(100))
    descripcion = Column(Text)
    precio = Column(DECIMAL(10, 2))
    paginas_por_libro = Column(Integer,nullable=False)

    fecha_creacion = Column(
        DateTime,
        server_default=func.now(),
        nullable=False
    )
# Tabla de inventario de libros.
class InventarioLibro(Base):
    __tablename__ = "inventario_libros"
    id_inventario = Column(Integer, primary_key=True, autoincrement=True)
    libro_id = Column(Integer, ForeignKey("libros.id_libro"), nullable=False)
    stock = Column(Integer, nullable=False, default=0)
    
    updated_at = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

# Tabla de movimientos de libros.
class MovimientoLibro(Base):
    __tablename__ = "movimientos_libros"
    id_mov_libro = Column(Integer, primary_key=True, autoincrement=True)
    inventario_id = Column(Integer, ForeignKey("inventario_libros.id_inventario"), nullable=False)
    tipo = Column(Enum(TipoMovimiento), nullable=False)
    cantidad = Column(Integer, nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuarios.id_usuario"))
    observaciones = Column(Text, nullable=True)
    
    fecha_movimiento = Column(
        DateTime,
        server_default=func.now(),
        nullable=False
    )