from typing import List
from fastapi import APIRouter, Response
from psycopg2.extras import RealDictCursor
from starlette.status import HTTP_200_OK
from bd_con.conexion import PsqlConnection
from middlewares.verifica_ruta_token import VerificaRutaToken
from models.app_models.estado_documento import EstadoDocumento

router = APIRouter(route_class=VerificaRutaToken)


@router.get('/all', response_model=List[EstadoDocumento])
async def get_tipos_estados_documentos(response: Response):
    conn = PsqlConnection().conn
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = """SELECT * FROM estado_documento"""
    cursor.execute(query)
    estados = cursor.fetchall()
    conn.close()
    response.status_code = HTTP_200_OK
    return estados
