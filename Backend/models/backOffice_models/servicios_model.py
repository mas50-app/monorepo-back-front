from datetime import datetime, date
from typing import List, Optional, Union
from pydantic import BaseModel, validator


class Item(BaseModel):
    cod_item_servicio: int
    desc_item_servicio: str
    cod_servicio: int
    cod_unidad: int
    valor_unidad: int
    desc_unidad: str
    cod_activo: str


class Comuna(BaseModel):
    cod_comuna: int
    desc_comuna: str


class Categoria(BaseModel):
    cod_categoria: int
    desc_categoria: str


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
    path_imagen: Optional[str] = ""
    cod_activo: str
    cod_pausado: str
    dias_antelacion: int
    cod_revisado: str
    nombre_usuario: str
    desc_usuario: str
    desc_talento_usuario: Optional[str]
    comunas: List[Comuna]
    categorias: List[Categoria]
    # items: List[Item]


class TopPrestacion(BaseModel):
    cod_servicio: int
    nom_servicio: str
    cod_usuario: int
    desc_usuario: str
    nombre_usuario: str
    ventas: int


class Filtros(BaseModel):
    cantidad: int
    desde: Optional[date] = None
    hasta: date


class ServicioCodUsuario(BaseModel):
    cod_usuario: int


class ServicioCod(BaseModel):
    cod_servicio: int
    enum_str: Optional[str]


class ItemServicioCod(BaseModel):
    cod_item_servicio: int
    enum_str: Optional[str]


class ServicioD(BaseModel):
    cod_servicio: int
    desc_servicio: str
    nom_servicio: str
    direccion: str
    cod_retiro: str
    cod_domicilio: str
    cod_es_articulo: str
    desc_domicilio: str
    dias_antelacion: int
    path_imagen: Optional[str]
    items: List[Item]


class Doc(BaseModel):
    cod_antecedente: int
    desc_antecedente: str
    cod_tipo_antecedente: int
    desc_tipo_antecedente: str
    path_imagen: Optional[str] = ""


class Courier(BaseModel):
    cod_courier: int
    desc_courier: str
    path_imagen: str


class DetalleServicio(BaseModel):
    cod_usuario: int
    nombre_usuario: str
    apellido1_usuario: str
    apellido2_usuario: Optional[str]
    desc_usuario: str
    rut_usuario: str
    mail_usuario: str
    path_imagen: Optional[str]
    cod_activo: str
    cod_revisado: str
    cod_pausado: str
    desc_talento_usuario: Optional[str]
    cod_comuna: str
    comision: float
    desc_comuna: str
    cod_provincia: str
    desc_provincia: str
    cod_cuenta_bancaria: int
    desc_cuenta_bancaria: Optional[str]
    cod_tipo_cuenta_bancaria: int
    desc_tipo_cuenta_bancaria: str
    nro_cuenta_bancaria: int
    cod_banco: int
    desc_banco: str
    valoraciones: Optional[int] = 0
    valoracion_media: Optional[float] = 0.0
    docs: List[Union[Doc, None]]
    servicios: Union[List[ServicioD], None]
    couriers: List[Courier]


class Evaluacion(BaseModel):
    cod_evaluacion: int
    desc_evaluacion: str
    cod_usuario_evaluado: int
    cod_usuario_evaluador: int
    nombre_usuario: str
    valor: int
    fecha_evaluacion: date
    cod_documento: int
    desc_usuario: str

    @validator("fecha_evaluacion")
    def format_date(cls, value):
        return value.strftime('%d-%m-%Y')


class Valoraciones(BaseModel):
    valoracion_media: float
    evaluaciones: List[Evaluacion]


class DetalleVista(BaseModel):
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
    path_imagen: str
    cod_es_nacional: str
    nombre_usuario: str
    desc_usuario: str
    rut_usuario: str
    mail_usuario: str
    desc_talento_usuario: str
    items: List[Item]
    valoraciones: Optional[Valoraciones] = {}


class UpdateDetalleVista(BaseModel):
    cod_servicio: int
    desc_servicio: str
    direccion: str
    cod_retiro: str
    cod_domicilio: str
    cod_es_articulo: str
    nom_servicio: str
    desc_domicilio: str
    dias_antelacion: int
    cod_es_nacional: str
    cod_usuario: int
    nombre_usuario: str
    desc_usuario: str
    rut_usuario: str
    mail_usuario: str
