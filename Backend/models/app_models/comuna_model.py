from pydantic import BaseModel, validator
from dev_tools.rut import validateRut
from starlette.responses import JSONResponse
from starlette.status import *


class CiudadGet(BaseModel):
    cod_ciudad: int
    desc_ciudad: str
    cod_comuna: int
    desc_comuna: str
    cod_region: int
    desc_region: str
