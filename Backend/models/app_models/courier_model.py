from typing import Optional, List

from pydantic import BaseModel


class CourierGet(BaseModel):
    cod_courier: int
    desc_courier: str
    link_courier: str
    path_imagen: Optional[str] = None


class CourierCreate(BaseModel):
    desc_courier: str
    link_courier: str
    path_imagen: Optional[str] = None


class CourierDelete(BaseModel):
    cod_courier: int


class PrestadorCod(BaseModel):
    cod_usuario: int


class CourierAsociado(BaseModel):
    cod_usuario_courier: int
    desc_usuario_courier: str
    cod_usuario: int
    cod_courier: int
    desc_courier: str
    link_courier: str
    path_imagen: str


class CourierList(BaseModel):
    cod_courier: int


class CourierAsociar(BaseModel):
    cod_usuario: int
    couriers: List[CourierList]
