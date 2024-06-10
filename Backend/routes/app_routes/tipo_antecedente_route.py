from fastapi import APIRouter, Response
from psycopg2.extras import RealDictCursor
from starlette.status import HTTP_200_OK, HTTP_201_CREATED
from bd_con.conexion import PsqlConnection
from middlewares.verifica_ruta_token import VerificaRutaToken
from models.app_models.tipo_antecedente_model import TipoAntecedentePost

router = APIRouter(route_class=VerificaRutaToken)


@router.get('/all')
async def get_tipo_documento(response: Response):
    conn = PsqlConnection().conn
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = """SELECT cod_tipo_antecedente, desc_tipo_antecedente FROM tipo_antecedente"""
    cursor.execute(query)
    response.status_code = HTTP_200_OK
    tipos_documento = cursor.fetchall()
    conn.close()
    return tipos_documento


@router.post('/crear')
async def crear_tipo_documento(response: Response, tipo_antecedente: TipoAntecedentePost):
    conn = PsqlConnection().conn
    conn.autocommit = True
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = """INSERT INTO tipo_antecedente (desc_tipo_antecedente) VALUES (%s) returning cod_tipo_antecedente"""
    cursor.execute(
        query,
        (
            tipo_antecedente.desc_tipo_antecedente,
        )
    )
    cod_tipo_antecedente = cursor.fetchone().get('cod_tipo_antecedente')
    response.status_code = HTTP_201_CREATED
    conn.close()
    return {"mensaje": f"tipo_antecedente creado con cod: {cod_tipo_antecedente} exitosamente"}

