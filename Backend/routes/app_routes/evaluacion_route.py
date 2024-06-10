from fastapi import APIRouter, Response, Header
from starlette.status import *
from typing import Union, Dict
from bd_con.conexion import PsqlConnection
from psycopg2.extras import RealDictCursor
from dev_tools.json_web_token import validar_token
from middlewares.verifica_ruta_token import VerificaRutaToken
from models.app_models.evaluacion_model import EvaluacionGetAll, EvaluacionCreate, Evaluacion, EvalCod

router = APIRouter(route_class=VerificaRutaToken)


@router.get('/all', response_model=Union[EvaluacionGetAll, Dict])
async def get_allevaluacion(response: Response, Authorization: str = Header(None)):
    token = Authorization.split(" ")[1]
    token_info = validar_token(token, output=True)
    conn = PsqlConnection().conn
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = """SELECT u.cod_usuario,
                       Avg(e.valor) AS prom_evaluacion,
                       Json_agg((SELECT x
                                 FROM   (SELECT e.cod_evaluacion,
                                                e.desc_evaluacion,
                                                e.cod_usuario_evaluador,
                                                u.desc_usuario AS desc_usuario_evaluador,
                                                e.cod_usuario_evaluado,
                                                u1.desc_usuario AS desc_usuario_evaluado,
                                                e.valor,
                                                e.fecha_evaluacion) AS x)) AS evaluaciones
                FROM   evaluacion e
                       JOIN usuario u
                         ON u.cod_usuario = e.cod_usuario_evaluador
                       JOIN usuario u1
                         ON u1.cod_usuario = e.cod_usuario_evaluador 
                WHERE  cod_usuario_evaluado = %s
                GROUP  BY 1 """
    cursor.execute(
        query,
        (
            token_info.get('cod_usuario'),
        )
    )
    evaluaciones = cursor.fetchone()
    conn.close()

    if evaluaciones:
        response.status_code = HTTP_200_OK
        return evaluaciones
    else:
        response.status_code = HTTP_206_PARTIAL_CONTENT
        return {"mensaje": "no tiene evaluaciones"}


@router.post('/por_cod', response_model=Evaluacion)
async def get_by_cod_evaluacion(response: Response, eval: EvalCod):
    conn = PsqlConnection().conn
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = """SELECT 
                    e.*,
                    u.desc_usuario as desc_usuario_evaluado,
                    u1.desc_usuario as desc_usuario_evaluador  
                FROM evaluacion e
                JOIN usuario u on e.cod_usuario_evaluado = u.cod_usuario
                JOIN usuario u1 on e.cod_usuario_evaluador = u1.cod_usuario
                WHERE cod_evaluacion = %s"""
    cursor.execute(
        query,
        (
            eval.cod_evaluacion,
        )
    )
    evaluacion = cursor.fetchone()
    response.status_code = HTTP_200_OK
    conn.close()
    return evaluacion


@router.post('/crear')
async def create_evaluacion(response: Response, eval: EvaluacionCreate, Authorization: str = Header(None)):
    token = Authorization.split(" ")[1]
    token_info = validar_token(token, output=True)
    cod_usuario_evaluador = token_info.get('cod_usuario')
    conn = PsqlConnection().conn
    conn.autocommit = True
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = """INSERT INTO evaluacion (desc_evaluacion, user_id, cod_usuario_evaluado,
                                        cod_usuario_evaluador, valor, fecha_evaluacion, 
                                        cod_documento) 
                        VALUES (%s,%s,%s,%s,%s,%s,%s) returning cod_evaluacion"""
    cursor.execute(
        query,
        (
            eval.desc_evaluacion,
            token_info.get('desc_usuario'),
            eval.cod_usuario_evaluado,
            cod_usuario_evaluador,
            eval.valor,
            eval.fecha_evaluacion,
            eval.cod_documento
        )
    )
    evaluacion = cursor.fetchone().get('cod_evaluacion')
    response.status_code = HTTP_201_CREATED
    conn.close()
    return {"mensaje": f"evaluacion con cod: {evaluacion} exitosamente"}
