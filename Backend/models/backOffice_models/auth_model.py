from typing import List, Union, Optional
from pydantic import BaseModel


class Login(BaseModel):
    login_personal: str
    contrasena: str


class RegistUser(BaseModel):
    desc_personal: str
    login_personal: str
    contrasena: str
    cod_tipo_personal: int


class PermisoCod(BaseModel):
    cod_permiso: int


class TipoPCod(BaseModel):
    cod_tipo_personal: int


class TipoPersonal(BaseModel):
    cod_tipo_personal: int
    desc_tipo_personal: str
    permisos: Optional[List[PermisoCod]]


class Permiso(BaseModel):
    cod_permiso: int
    desc_permiso: str


class CreateTipoPersonal(BaseModel):
    desc_tipo_personal: str


class PermisosPersonal(BaseModel):
    cod_tipo_personal: int
    desc_tipo_personal: str
    permisos: Optional[List[Permiso]]
