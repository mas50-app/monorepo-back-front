from datetime import date, datetime
from typing import List, Optional, Union, Any
from pydantic import BaseModel, validator
from models.backOffice_models.devoluciones import Usuario, Devolucion


class DocumentoSimple(BaseModel):
    cod_documento: int
    desc_documento: str
    cod_usuario_vendedor: int
    cod_usuario_comprador: int
    monto_documento: float
    monto_venta: float
    monto_comision_bruto: float
    comision: float
    fecha_documento: date
    cod_estado_documento: int
    desc_estado_documento: str
    flow_token: str
    flow_order: int
    cod_retiro: str
    cod_domicilio: str
    cod_direccion_usuario_comprador: Optional[int] = None
    cod_vendedor: int
    nombre_vendedor: str
    # vendedor: Usuario
    cod_comprador: int
    nombre_comprador: str

    @validator("fecha_documento")
    def format_date(cls, value):
        return value.strftime('%d-%m-%Y')

    @validator("monto_documento", "monto_venta", "monto_comision_bruto")
    def format_monto(cls, value):
        return '{:,.0f}'.format(value).replace(',', '.')


class DocCod(BaseModel):
    cod_documento: int


class Detalle(BaseModel):
    cod_detalle_documento: int
    desc_detalle_documento: Optional[str] = ""
    cod_documento: int
    cantidad: int
    subtotal: int
    cod_item_servicio: int
    fecha_agenda: date
    desc_item_servicio: Optional[str] = ""
    cod_servicio: int
    cod_unidad: int
    desc_unidad: str
    valor_unidad: int
    cod_activo: str
    desc_servicio: str
    cod_usuario: int
    direccion: str
    cod_retiro: str
    cod_domicilio: str
    cod_es_articulo: str
    nom_servicio: str
    desc_domicilio: str
    cod_pausado: str
    dias_antelacion: int
    cod_revisado: str
    path_imagen: str
    cod_es_nacional: str


class DocumentoDetalle(BaseModel):
    cod_documento: int
    desc_documento: str
    cod_usuario_vendedor: int
    cod_usuario_comprador: int
    monto_documento: int
    fecha_documento: date
    cod_estado_documento: int
    desc_estado_documento: str
    flow_token: str
    flow_order: int
    cod_retiro: str
    cod_domicilio: str
    cod_direccion_usuario_comprador: Optional[int] = None
    desc_direccion_usuario: Optional[str] = ""
    vendedor: Usuario
    comprador: Usuario
    devoluciones: List[Devolucion]
    evaluaciones: List[Any]
    detalles: List[Detalle]


class Filtro(BaseModel):
    mes: str


class DocumentoPDF(BaseModel):
    cod_documento: int
    desc_documento: str
    cod_usuario_vendedor: int
    cod_usuario_comprador: int
    monto_documento: float
    monto_venta: float
    monto_comision_bruto: float
    comision: float
    fecha_documento: date
    cod_estado_documento: int
    desc_estado_documento: str
    flow_token: str
    flow_order: int
    cod_retiro: str
    cod_domicilio: str
    vendedor: Usuario
    comprador: Usuario
    # devoluciones: List[Devolucion]
    # evaluaciones: List[Any]
    # detalles: List[Detalle]

    @validator("fecha_documento")
    def format_date(cls, value):
        return value.strftime('%d-%m-%Y')

    @validator("monto_documento", "monto_venta", "monto_comision_bruto")
    def format_monto(cls, value):
        return '{:,.0f}'.format(value).replace(',', '.')
