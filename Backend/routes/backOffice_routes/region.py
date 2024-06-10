from typing import List
from starlette.status import *
from bd_con.conexion import PsqlConnection
from psycopg2.extras import RealDictCursor
from fastapi import APIRouter, Response


router = APIRouter()


@router.get('/all')
async def get_regiones(response: Response):
    conn = PsqlConnection().conn
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = """SELECT cod_region, desc_region FROM region ORDER BY cod_region"""
    cursor.execute(query)
    regiones = cursor.fetchall()
    conn.close()
    response.status_code = HTTP_200_OK
    return regiones
