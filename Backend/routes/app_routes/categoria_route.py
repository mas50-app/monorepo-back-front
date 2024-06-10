from typing import List
from starlette.status import *
from bd_con.conexion import PsqlConnection
from psycopg2.extras import RealDictCursor
from fastapi import APIRouter, Response
from models.app_models.servicio_model import Categoria


router = APIRouter()


@router.get('/all', response_model=List[Categoria])
async def get_allcategoria(response: Response):
    conn = PsqlConnection().conn
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = """SELECT * FROM categoria ORDER BY cod_categoria"""
    cursor.execute(query)
    categorias = cursor.fetchall()
    conn.close()
    response.status_code = HTTP_200_OK
    return categorias
