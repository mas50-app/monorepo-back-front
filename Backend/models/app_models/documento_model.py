from datetime import date, datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, validator


class DocumentoGet(BaseModel):
    cod_documento: int
    desc_direccion_comprador: Optional[str]
    desc_comuna_comprador: Optional[str]
    nombre_usuario_comprador: Optional[str]
    desc_usuario_comprador: Optional[str]
    monto_documento: float
    fecha_documento: date
    cod_estado_documento: int
    desc_estado_documento: str
    cod_retiro: Optional[str]
    cod_domicilio: Optional[str]


class DetalleDocumento(BaseModel):
    cantidad: int
    subtotal: float
    fecha_agenda: date = date.today()
    cod_item_servicio: int
    desc_item_servicio: str


class DocumentoCreate(BaseModel):
    cod_usuario_vendedor: int
    nom_vendedor: str
    monto_documento: float
    fecha_documento: date = date.today()
    cod_estado_documento: int = 1
    cod_direccion_comprador: Optional[int]
    cod_retiro: str = 'S'
    cod_domicilio: str = 'N'
    cod_courier: Optional[int] = None
    detalles: List[DetalleDocumento]


class DocumentoCod(BaseModel):
    cod_documento: int


class Usuario(BaseModel):
    cod_usuario: int
    desc_usuario: Optional[str]
    nombre_usuario: Optional[str]
    apellido1_usuario: Optional[str]
    rut_usuario: str
    mail_usuario: str
    cod_es_prestador: str
    cod_activo: str
    cod_comuna: str
    desc_comuna: Optional[str]
    desc_talento_usuario: Optional[str]

    @validator("desc_talento_usuario")
    def return_str(cls, value):
        if value:
            return value
        return ""


class Detalle(BaseModel):
    cod_detalle_documento: int
    desc_detalle_documento: Optional[str]
    cantidad: int
    subtotal: int
    fecha_agenda: Optional[date]
    cod_item_servicio: int
    desc_item_servicio: str
    cod_servicio: int
    cod_unidad: int
    desc_unidad: str
    valor_unidad: int


class Direccion(BaseModel):
    direccion: Optional[str] = ""
    desc_domicilio: Optional[str] = ""
    desc_comuna: Optional[str] = ""


class DireccionComprador(BaseModel):
    cod_direccion_usuario: int
    desc_direccion_usuario: str
    cod_comuna: str
    cod_activa: str
    desc_comuna: str


class DocumentosByEstVEndedor(BaseModel):
    cod_documento: int
    desc_documento: str
    cod_usuario_vendedor: int
    cod_usuario_comprador: int
    monto_documento: int
    fecha_documento: Optional[date]
    fecha_agenda: Optional[date]
    cod_estado_documento: int
    cod_retiro: Optional[str]
    cod_domicilio: Optional[str]
    comprador: Usuario
    direccion: Optional[Any]
    path_imagen_despacho: str
    detalles: List[Detalle]

    @validator("cod_retiro", "cod_domicilio")
    def return_str(cls, value):
        if value:
            return value
        return "N"


class DocumentosByEstComprador(BaseModel):
    cod_documento: int
    desc_documento: str
    cod_usuario_vendedor: int
    cod_usuario_comprador: int
    monto_documento: int
    fecha_documento: Optional[date]
    fecha_agenda: Optional[date]
    cod_estado_documento: int
    cod_retiro: Optional[str]
    cod_domicilio: Optional[str]
    vendedor: Usuario
    direccion: Optional[Direccion] = None
    path_imagen_despacho: str
    detalles: List[Detalle]

    @validator("cod_retiro", "cod_domicilio")
    def return_str(cls, value):
        if value:
            return value
        return "N"


class BasicDoc(BaseModel):
    cod_documento: int
    desc_documento: str
    cod_usuario_vendedor: int
    cod_usuario_comprador: int
    monto_documento: int
    fecha_documento: Optional[date] = None
    fecha_agenda: Optional[date] = None
    cod_estado_documento: int
    cod_retiro: str
    cod_domicilio: str
    cod_direccion_usuario_comprador: Optional[int] = 0
