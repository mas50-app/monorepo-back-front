from datetime import date, datetime
from typing import List, Optional
from pydantic import BaseModel, validator


class DevolucionCreate(BaseModel):
    desc_devolucion: str = ""
    cod_documento: int
    monto_devolucion: int
    cod_manual: str = "N"


class DevolucionCod(BaseModel):
    cod_devolucion: int


class Devolucion(BaseModel):
    cod_devolucion: int
    desc_devolucion: str
    cod_documento: int
    monto_devolucion: int
    cod_es_manual: str
    flow_token: Optional[str] = None
    flow_orden_devolucion: Optional[int] = None
    fecha_devolucion: Optional[datetime] = None
    flow_fee_devolucion: Optional[int] = None
    flow_status: Optional[str] = None


class Usuario(BaseModel):
    cod_usuario: int
    desc_usuario: Optional[str] = ""
    nombre_usuario: Optional[str] = ""
    apellido1_usuario: Optional[str] = ""
    apellido2_usuario: Optional[str] = ""
    rut_usuario: Optional[str] = ""
    mail_usuario: Optional[str] = ""
    cod_es_prestador: str
    uuid: str
    cod_activo: str
    cod_comuna: str
    desc_comuna: Optional[str] = ""
    desc_talento_usuario: Optional[str] = ""
    cod_revisado: str
    cod_pausado: str
    path_imagen: Optional[str] = ""
    last_login: Optional[datetime] = None
    cod_eliminado: str


class DocDevols(BaseModel):
    cod_documento: int
    vendedor: Usuario
    comprador: Usuario
    desc_documento: str
    cod_usuario_vendedor: int
    cod_usuario_comprador: int
    monto_documento: int
    fecha_documento: date
    cod_estado_documento: int
    flow_token: str
    flow_order: int
    cod_retiro: str
    cod_domicilio: str
    cod_direccion_usuario_comprador: Optional[int] = None

    @validator("fecha_documento")
    def format_date(cls, value):
        return value.strftime('%d-%m-%Y')


class DocCod(BaseModel):
    cod_documento: int


class DevolByCodPrestador(BaseModel):
    cod_usuario: int


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

    @validator("fecha_agenda")
    def format_date(cls, value):
        return value.strftime('%d-%m-%Y')


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
    detalles: List[Detalle]

    @validator("fecha_documento")
    def format_date(cls, value):
        return value.strftime('%d-%m-%Y')


class DevolucionGet(BaseModel):
    cod_devolucion: int
    desc_devolucion: str
    fecha_devolucion: datetime
    monto_devolucion: int
    cod_es_manual: str

    @validator("fecha_devolucion")
    def format_date(cls, value):
        return value.strftime('%d-%m-%Y')


class DevolucionElem(BaseModel):
    cod_devolucion: int
    desc_devolucion: str
    fecha_devolucion: datetime
    monto_devolucion: int
    cod_es_manual: str
    personal: str
    cod_usuario: int
    desc_usuario: str

    @validator("fecha_devolucion")
    def format_date(cls, value):
        return value.strftime('%d-%m-%Y')

    @validator("monto_devolucion")
    def format_monto(cls, value):
        return '{:,.0f}'.format(value).replace(',', '.')
