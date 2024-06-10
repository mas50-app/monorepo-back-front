from datetime import date
from pydantic import BaseModel


class Notificacion(BaseModel):
    cod_notificacion: int


class NotificacionAll(BaseModel):
    cod_notificacion: int
    desc_notificacion: str
    fecha_notificacion: date
    cod_leida: str
    titulo: str
    cuerpo: str


