from datetime import date, datetime
from typing import List, Optional, Union
from pydantic import BaseModel, validator

from models.app_models.documento_model import Usuario


class DetalleLiquidacion(BaseModel):
    desc_detalle_liquidacion: Optional[str] = ""
    cod_documento: int
    monto_documento: float


class LiquidacionCreate(BaseModel):
    cod_usuario: int
    comision: float
    desc_liquidacion: str = ""
    monto_liquidacion: float = 500.00
    monto_venta: float = 500.00
    detalles: List[DetalleLiquidacion]


class UsuarioPendiente(BaseModel):
    cod_usuario: int
    desc_usuario: str
    nombre_usuario: str
    apellido1_usuario: str
    rut_usuario: str
    mail_usuario: str
    comision: float
    pendientes: int
    monto_total: float


class UsuarioCod(BaseModel):
    cod_usuario: int


class DocPendiente(BaseModel):
    cod_documento: int
    desc_documento: str
    cod_usuario_vendedor: int
    cod_usuario_comprador: int
    monto_documento: float
    comision: float
    monto_comision_bruto: float
    monto_comision_neto: float
    monto_iva: float
    monto_liquidacion: float
    fecha_documento: date
    cod_estado_documento: int
    desc_estado_documento: str
    cod_retiro: str
    cod_domicilio: str
    desc_estado_documento: str


class ResumenPorLiquidar(BaseModel):
    monto_total_ventas: Union[float, None]
    monto_total_comision: Union[float, None]
    monto_total_liquidacion: Union[float, None]
    docs: List[DocPendiente] = []


class Detalle(BaseModel):
    cod_detalle_liquidacion: int
    desc_detalle_liquidacion: str
    cod_liquidacion: int
    cod_documento: int
    monto_documento: int
    desc_documento: str
    fecha_documento: date
    cod_retiro: str


class Liquidacion(BaseModel):
    # Usuario Info Start
    cod_usuario: int
    desc_usuario: Optional[str]
    nombre_usuario: Optional[str]
    apellido1_usuario: Optional[str]
    rut_usuario: str
    mail_usuario: str
    cod_es_prestador: str
    cod_activo: str
    cod_comuna: str
    desc_comuna: Optional[str]
    # Usuario Info End
    monto_venta: float
    comision: float
    monto_liquidacion: float
    monto_comision: Optional[float]
    fecha_liquidacion: Union[str, datetime]
    cod_liquidacion: int
    desc_liquidacion: str
    detalles: Optional[List[Detalle]] = []

    @validator("monto_liquidacion", "monto_comision", "comision", "monto_venta")
    def format_monto(cls, value):
        return '{:,.0f}'.format(value).replace(',', '.')


class LiquidAll(BaseModel):
    length: int
    liquidaciones: List[Liquidacion]


class LiquidacionCod(BaseModel):
    cod_liquidacion: int


class DetalleLiq(BaseModel):
    cod_detalle_liquidacion: int
    desc_detalle_liquidacion: Optional[str]
    cod_documento: int
    monto_documento: float


class LiquidacionPDF(BaseModel):
    cod_liquidacion: int
    desc_liquidacion: str
    fecha_liquidacion: date
    monto_liquidacion: float
    monto_venta: float
    cod_usuario: int
    nombre_usuario: str
    rut_usuario: str
    mail_usuario: str
    cod_comuna: int
    desc_comuna: str
    detalles: List[DetalleLiq]
