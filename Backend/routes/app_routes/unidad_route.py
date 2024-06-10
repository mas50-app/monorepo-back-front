from fastapi import APIRouter, Response
from starlette.status import *
from typing import List
from bd_con.conexion import PsqlConnection
from psycopg2.extras import RealDictCursor
from middlewares.verifica_ruta_token import VerificaRutaToken
from models.app_models.unidad_model import Unidad

router = APIRouter()


@router.get('/all', response_model=List[Unidad])
async def get_allunidad(response: Response):
    conn = PsqlConnection().conn
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = """SELECT * FROM unidad"""
    cursor.execute(query)
    unidades = cursor.fetchall()
    response.status_code = HTTP_200_OK
    return unidades
