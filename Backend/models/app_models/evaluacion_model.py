from datetime import date
from typing import List
from pydantic import BaseModel, validator
from dev_tools.rut import validateRut
from starlette.responses import JSONResponse
from starlette.status import *


class Evaluacion(BaseModel):
    cod_evaluacion: int
    desc_evaluacion: str
    cod_usuario_evaluador: int
    desc_usuario_evaluador: str
    cod_usuario_evaluado: int
    desc_usuario_evaluado: str
    valor: int
    fecha_evaluacion: date


class EvaluacionGetAll(BaseModel):
    prom_evaluacion: float
    evaluaciones: List[Evaluacion]


class EvaluacionCreate(BaseModel):
    desc_evaluacion: str
    cod_usuario_evaluado: int
    valor: int
    fecha_evaluacion: date = date.today()
    cod_documento: int


class EvaluacionUpdate(BaseModel):
    cod_evaluacion: int
    desc_evaluacion: str
    user_id: str
    cod_usuario_evaluado: int
    cod_usuario_evaluador: int
    valor: int
    fecha: date
    cod_documento: int


class EvalCod(BaseModel):
    cod_evaluacion: int

