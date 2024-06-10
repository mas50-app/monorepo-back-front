from datetime import date
from typing import List, Optional
from pydantic import BaseModel, validator
from dev_tools.null_safety import null_int


class FiltroMes(BaseModel):
    mes: str = date.today().strftime('%m-%d')


class Filtros(BaseModel):
    cod_categoria: Optional[List[int]]
    cod_region: Optional[List[str]]
    desde: Optional[date] = None
    hasta: Optional[date] = None


class ResumenAnual(BaseModel):
    mes: str
    monto: int


class EstadoCuenta(BaseModel):
    promedio_diario: Optional[int] = None
    promedio_semanal: Optional[int] = None
    promedio_mensual: Optional[int] = None
    resumen_anual: List[ResumenAnual]
