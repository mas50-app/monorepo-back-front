from typing import List

from fastapi import APIRouter, Response, Header
from psycopg2.extras import RealDictCursor
from starlette.status import HTTP_200_OK
from bd_con.conexion import PsqlConnection
from dev_tools.json_web_token import validar_token
from middlewares.verifica_ruta_token import VerificaRutaToken
from models.app_models.notificacion_model import Notificacion, NotificacionAll

router = APIRouter(
    route_class=VerificaRutaToken
)


@router.put("/set_leida")
async def set_notificacion_leida(response: Response, notificacion: Notificacion):
    conn = PsqlConnection().conn
    conn.autocommit = True
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = """UPDATE notificacion SET cod_leida='S' WHERE cod_notificacion = %s"""
    cursor.execute(
        query,
        (
            notificacion.cod_notificacion,
        )
    )
    conn.close()
    mensaje = f"Notificacion cambiada a leida con cod {notificacion.cod_notificacion} exitosamente"
    print(mensaje)
    response.status_code = HTTP_200_OK
    return mensaje


@router.get("/all", response_model=List[NotificacionAll])
async def get_notificacion_all(response: Response, Authorization: str = Header(None)):
    token = Authorization.split(" ")[1]
    token_info = validar_token(token, output=True)
    conn = PsqlConnection().conn
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = """SELECT 
                cod_notificacion,
                desc_notificacion,
                inserttime as fecha_notificacion,
                cod_leida,
                titulo,
                cuerpo
                FROM notificacion WHERE cod_usuario = %s
                ORDER BY fecha_notificacion desc"""
    cursor.execute(
        query,
        (
            token_info.get("cod_usuario"),
        )
    )
    notificaciones = cursor.fetchall()
    conn.close()
    response.status_code = HTTP_200_OK
    return notificaciones
