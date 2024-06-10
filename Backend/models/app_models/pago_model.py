from datetime import date, time
from typing import List
from pydantic import BaseModel


class FiltroMes(BaseModel):
    mes: str = date.today().strftime('%m-%d')


class Detalle(BaseModel):
    desc_detalle_documento: str
    cod_detalle_documento: int
    cantidad: int
    cod_item_servicio: int
    desc_item_servicio: str
    subtotal: int


class PagoAllElement(BaseModel):
    cod_pago: int
    desc_pago: str
    cod_documento: int
    cod_tipo_pago: int
    monto_pago: int
    fecha_pago: date
    hora_pago: time
    desc_documento: str
    cod_usuario_vendedor: int
    cod_usuario_comprador: int
    monto_documento: int
    fecha_documento: date
    cod_aceptado: str
    cod_anulado: str
    direccion_comprador: str
    cod_comuna_documento: str
    detalles: List[Detalle]


class PagoToken(BaseModel):
    token: str
