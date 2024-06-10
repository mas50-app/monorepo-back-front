from datetime import time
from typing import List, Optional, Any, Union
from pydantic import BaseModel, validator


class Comuna(BaseModel):
    desc_comuna: str
    cod_comuna: str
    cod_provincia: str


class Categoria(BaseModel):
    cod_categoria: int
    desc_categoria: str


class Item(BaseModel):
    cod_item_servicio: int
    desc_item_servicio: str
    cod_servicio: Optional[int]
    cod_unidad: int
    valor_unidad: int


class Servicio(BaseModel):
    cod_servicio: Optional[int] = None
    desc_servicio: Optional[str] = None
    nom_servicio: Optional[str] = None
    direccion: Optional[str] = None
    cod_retiro: Optional[str] = None
    cod_domicilio: Optional[str] = None
    cod_es_articulo: Optional[str] = None
    desc_domicilio: Optional[str] = None
    cod_activo: Optional[str] = None
    cod_pausado: Optional[str] = None
    dias_antelacion: Optional[int] = None
    favorito: Optional[bool] = None
    cod_es_nacional: str = 'N'
    comunas: Optional[List[Union[str, None]]] = None
    categorias: Optional[List[int]] = None
    path_imagen: Optional[str] = None
    items: Optional[List[Item]] = None

    @validator("path_imagen")
    def str_null_manage(cls, value):
        if not value:
            return ""
        return value

    @validator("items")
    def list_null_manage(cls, value):
        if not value:
            return []
        return value




class Dia(BaseModel):
    cod_dia: int
    desc_dia: str


class Horario(BaseModel):
    cod_horario_usuario: int
    desde: time
    hasta: time
    dias: List[Dia]


class RespPorCod(BaseModel):
    servicio: Servicio
    horarios: List[Horario]


class Imagen(BaseModel):
    file: str


class ItemCrear(BaseModel):
    cod_item_servicio: Optional[int] = None
    desc_item_servicio: str
    cod_unidad: int
    valor_unidad: float


class ServicioVerificador(BaseModel):
    cod_usuario: int


class ServicioBuscador(BaseModel):
    filtro: str
    cod_comuna: Optional[str] = None


class ServicioCod(BaseModel):
    cod_servicio: int
    cod_usuario: int


class ComuCod(BaseModel):
    cod_comuna: str


class CategCod(BaseModel):
    cod_categoria: int

