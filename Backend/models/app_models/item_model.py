from typing import Optional, List

from pydantic import BaseModel


class Imagen(BaseModel):
    cod_imagen: Optional[int]
    desc_imagen: Optional[str]


class Item(BaseModel):
    cod_item_servicio: Optional[int] = None
    desc_item_servicio: Optional[str] = None
    cod_servicio: int
    cod_unidad: int
    valor_unidad: int
    editable: Optional[bool] = None
    cod_activo: Optional[str] = None


class ItemCodServ(BaseModel):
    cod_servicio: int


class ItemCod(BaseModel):
    cod_item_servicio: int
    editable: bool


class ImagenByCod(BaseModel):
    cod_imagen: int
