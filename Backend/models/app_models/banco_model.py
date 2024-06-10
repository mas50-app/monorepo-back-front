from pydantic import BaseModel, validator
from dev_tools.rut import validateRut
from starlette.responses import JSONResponse
from starlette.status import *


class BancoGet(BaseModel):
    cod_banco: int
    desc_banco: str

    # @validator('desc_banco')
    # def upper_str(cls, value):
    #     return value.upper()


class BancoCreate(BaseModel):
    desc_banco: str


class BancoUpdate(BaseModel):
    cod_banco: int
    desc_banco: str

class BancoDelete(BaseModel):
    cod_banco: int
