from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, validator


class FiltroMes(BaseModel):
    mes: date
