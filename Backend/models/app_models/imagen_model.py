from typing import List, Any, Optional

from pydantic import BaseModel


class Item(BaseModel):
    cod_item_servicio: int
    desc_item_servicio: str
    cod_servicio: int
    cod_unidad: int
    valor_unidad: int
    cod_activo: str
    imagenes: List[Any]


class Servicio(BaseModel):
    cod_servicio: int
    desc_servicio: str
    cod_usuario: int
    direccion: str
    cod_retiro: str
    cod_domicilio: str
    cod_es_articulo: str
    nom_servicio: str
    desc_domicilio: str
    cod_activo: str
    cod_pausado: str
    dias_antelacion: int
    cod_revisado: str
    items: List[Item]
    path_imagen: Optional[str]


class Imagenes(BaseModel):
    servicios: List[Servicio]


class ImagePath(BaseModel):
    path: str
