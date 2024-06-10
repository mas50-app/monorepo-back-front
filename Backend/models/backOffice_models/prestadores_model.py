from datetime import datetime, date
from typing import Optional
from pydantic import BaseModel, validator
from dev_tools.null_safety import null_str


class Prestador(BaseModel):
    cod_usuario: int
    desc_usuario: str
    nombre_usuario: str
    apellido1_usuario: str
    apellido2_usuario: Optional[str]
    rut_usuario: Optional[str]
    mail_usuario: str
    path_imagen: Optional[str] = ""
    cod_es_prestador: str
    cod_revisado: str
    cod_activo: str
    cod_comuna: str
    desc_comuna: str
    desc_talento_usuario: Optional[str]
    cod_pausado: str
    cod_eliminado: str
    comision: float
    last_login: Optional[datetime] = None
    fecha_registro: Optional[datetime] = None

    @validator("desc_talento_usuario", "apellido2_usuario")
    def null_safety(cls, value):
        return null_str(value)

    @validator("last_login", "fecha_registro")
    def format_date(cls, value):
        if value:
            return value.strftime('%H:%M:%S | %d-%m-%Y')
        return ""


class PrestadorUpdate(BaseModel):
    cod_usuario: int
    enum_str: Optional[str]


class TopPrestador(BaseModel):
    cod_usuario: int
    desc_usuario: str
    nombre_usuario: str
    apellido1_usuario: str
    apellido2_usuario: Optional[str]
    rut_usuario: str
    mail_usuario: str
    path_imagen: Optional[str]
    cod_es_prestador: str
    cod_activo: str
    cod_comuna: str
    desc_talento_usuario: Optional[str]
    cod_revisado: str
    ventas: int

    @validator("desc_talento_usuario", "apellido2_usuario")
    def null_safety(cls, value):
        return null_str(value)


class PrestadorFichaUpdate(BaseModel):
    cod_usuario: int
    desc_usuario: str
    nombre_usuario: str
    apellido1_usuario: str
    rut_usuario: str
    mail_usuario: str
    cod_comuna: str
    comision: float
    cod_banco: int
    cod_tipo_cuenta_bancaria: int
    nro_cuenta_bancaria: str


class Filtros(BaseModel):
    cod_prestador: int
    desde: Optional[date]
    hasta: Optional[date]
