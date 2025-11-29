"""
Router para la gestión de usuarios.

Funcionalidades:
- Crear usuarios
- Listar usuarios (con filtro opcional por nombre/email)
- Obtener un usuario por ID
- Actualizar parcialmente un usuario
- Eliminar un usuario

Ademas, define los siguientes esquemas Pydantic:
- UsuarioCreate
- UsuarioUpdate
- UsuarioOut
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field
from database import get_db
from models import Usuario, PuntoVenta
from sqlalchemy import or_
from schemas import UsuarioCreate, UsuarioUpdate, UsuarioOut

# Dependencia para obtener sesión de DB
router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

# Crear un nuevo usuario
@router.post("/", response_model=UsuarioOut, status_code=status.HTTP_201_CREATED)
def crear_usuario(payload: UsuarioCreate, db: Session = Depends(get_db)):

    # Validar email único (si viene)
    if payload.email:
        existente = db.query(Usuario).filter(Usuario.email == payload.email).first()
        if existente:
            raise HTTPException(
                status_code=400,
                detail="El email ya está registrado"
            )

    # Validar punto de venta (si viene)
    if payload.punto_venta_id is not None:
        pv = db.query(PuntoVenta).get(payload.punto_venta_id)
        if not pv:
            raise HTTPException(
                status_code=400,
                detail="El punto de venta especificado no existe"
            )

    # En un entorno real deberías hashear la contraseña
    usuario = Usuario(
        nombre=payload.nombre,
        email=payload.email,
        contrasena=payload.contrasena,  # TODO: aplicar hash
        rol=payload.rol,
        punto_venta_id=payload.punto_venta_id
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario

# Listar usuarios
@router.get("/", response_model=List[UsuarioOut])
def listar_usuarios(
    q: Optional[str] = Query(
        None,
        description="Filtra por nombre o email que contenga este valor"
    ),
    db: Session = Depends(get_db)
):

    query = db.query(Usuario)

    if q:
        like = f"%{q}%"
        query = query.filter(
            or_(
                Usuario.nombre.ilike(like),
                Usuario.email.ilike(like)
            )
        )

    return query.order_by(Usuario.id_usuario.asc()).all()

# Obtener un usuario por ID
@router.get("/{usuario_id}", response_model=UsuarioOut)
def obtener_usuario(usuario_id: int, db: Session = Depends(get_db)):

    usuario = db.query(Usuario).get(usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

# Actualizar parcialmente un usuario
@router.patch("/{usuario_id}", response_model=UsuarioOut)
def actualizar_usuario(
    usuario_id: int,
    payload: UsuarioUpdate,
    db: Session = Depends(get_db)
):

    usuario = db.query(Usuario).get(usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    data = payload.model_dump(exclude_unset=True)

    # Validar email nuevo (si se envía)
    if "email" in data and data["email"] is not None:
        existente = (
            db.query(Usuario)
            .filter(Usuario.email == data["email"], Usuario.id_usuario != usuario_id)
            .first()
        )
        if existente:
            raise HTTPException(
                status_code=400,
                detail="El email ya está registrado por otro usuario"
            )

    # Validar punto de venta nuevo (si se cambia)
    if "punto_venta_id" in data and data["punto_venta_id"] is not None:
        pv = db.query(PuntoVenta).get(data["punto_venta_id"])
        if not pv:
            raise HTTPException(
                status_code=400,
                detail="El punto de venta especificado no existe"
            )

    # Aplicar cambios
    for k, v in data.items():
        setattr(usuario, k, v)

    db.commit()
    db.refresh(usuario)
    return usuario

# Eliminar un usuario
@router.delete("/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_usuario(usuario_id: int, db: Session = Depends(get_db)):

    usuario = db.query(Usuario).get(usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    db.delete(usuario)
    db.commit()
    return  # 204: sin contenido

class LoginRequest(BaseModel):
    email: EmailStr
    contrasena: str

class LoginResponse(BaseModel):
    message: str
    role: str

@router.post("/login", response_model=LoginResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    usuario = (
        db.query(Usuario)
        .filter(
            Usuario.email == payload.email,
            Usuario.contrasena == payload.contrasena  # OJO: plano, sin hash
        )
        .first()
    )
    if not usuario:
        raise HTTPException(status_code=400, detail="Credenciales inválidas")

    return {"message": "Inicio de sesión exitoso", "role": usuario.rol}

class LoginRequest(BaseModel):
    email: EmailStr
    contrasena: str

class LoginResponse(BaseModel):
    message: str
    role: str

#@router.post("/login", response_model=LoginResponse)
#def login(payload: LoginRequest, db: Session = Depends(get_db)):
#    # Buscar usuario por email y contraseña (en texto plano por ahora)
#    usuario = (
#        db.query(Usuario)
#        .filter(
#            Usuario.email == payload.email,
#            Usuario.contrasena == payload.contrasena
#        )
#        .first()
#    )
#
#    if not usuario:
#        raise HTTPException(status_code=400, detail="Credenciales inválidas")
#
#    return {"message": "Inicio de sesión exitoso", "role": usuario.rol}