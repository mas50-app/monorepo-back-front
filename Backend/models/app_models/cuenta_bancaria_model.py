from pydantic import BaseModel, validator
from dev_tools.rut import validateRut
from starlette.responses import JSONResponse
from starlette.status import *


class Cuenta_bancariaGet(BaseModel):
    cod_cuenta_bancaria: int
    nro_cuenta_bancaria: str
    cod_banco: int
    cod_tipo_cuenta_bancaria: int


class Cuenta_bancariaCreate(BaseModel):
    nro_cuenta_bancaria: str
    cod_banco: int
    cod_tipo_cuenta_bancaria: int


class CuentaBancCod(BaseModel):
    cod_cuenta_bancaria: int


class Cuenta_bancariaUpdate(BaseModel):
    cod_cuenta_bancaria: int
    nro_cuenta_bancaria: str
    cod_banco: int
    cod_tipo_cuenta_bancaria: int

