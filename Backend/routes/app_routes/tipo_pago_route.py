from fastapi import APIRouter, Response
from starlette.status import *
from typing import List
from bd_con.conexion import PsqlConnection
from psycopg2.extras import RealDictCursor
from middlewares.verifica_ruta_token import VerificaRutaToken
from models.app_models.tipo_pago_model import TipoPagoGet

router = APIRouter(route_class=VerificaRutaToken)


@router.get('/all', response_model=List[TipoPagoGet])
async def get_alltipo_pago(response: Response):
    conn = PsqlConnection().conn
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute(
        """SELECT cod_tipo_pago, desc_tipo_pago FROM tipo_pago"""
    )
    tipos_pago = cursor.fetchall()
    conn.close()
    response.status_code = HTTP_200_OK
    return tipos_pago



