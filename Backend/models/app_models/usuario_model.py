from datetime import time
from pydantic import BaseModel, validator
from typing import Optional, List
from models.app_models.sn_model import Sn


class UsuarioGet(BaseModel):
    cod_usuario: int
    desc_usuario: str
    nombre_usuario: str
    apellido1_usuario: str
    apellido2_usuario: Optional[str]
    rut_usuario: Optional[str]
    mail_usuario: Optional[str]
    path_imagen: Optional[str]
    cod_es_prestador: str
    cod_comuna: str
    cod_activo: str
    comision: Optional[float] = None


class UsuarioCreate(BaseModel):
    desc_usuario: str
    nombre_usuario: str
    apellido1_usuario: str
    apellido2_usuario: Optional[str] = None
    rut_usuario: Optional[str]
    uuid: str
    mail_usuario: Optional[str] = None
    # url_foto_perfil: Optional[str] = None
    cod_es_prestador: Sn = "N"
    cod_comuna: str
    cod_activo: Sn = "S"

    @validator("uuid")
    def uuid_validator(cls, value):
        if value.__len__() == 0:
            raise ValueError('uuid length must be greater than 1')
        return value


class UsuarioUpdate(BaseModel):
    desc_usuario: Optional[str] = None
    nombre_usuario: Optional[str] = None
    apellido1_usuario: Optional[str] = None
    apellido2_usuario: Optional[str] = None
    rut_usuario: Optional[str] = None
    mail_usuario: Optional[str] = None
    # cod_es_prestador: Optional[Sn] = None
    cod_comuna: Optional[str] = None
    cod_activo: str = "S"


class SubirDocs(BaseModel):
    uuid: str
    cod_es_prestador: str = "S"


class Dia(BaseModel):
    cod_dia_horario_usuario: Optional[int]
    cod_dia: int


class Horario(BaseModel):
    desde: time
    hasta: time
    dias: List[Dia]


class HorarioGet(BaseModel):
    cod_horario_usuario: int
    desde: time
    hasta: time
    dias: List[Dia]


class HorarioUsuario(BaseModel):
    cod_horario_usuario: int
