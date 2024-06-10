from fastapi import APIRouter, Response, Header
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel
from starlette.status import *
from bd_con.conexion import PsqlConnection
from dev_tools.json_web_token import validar_token

router = APIRouter()


class App(BaseModel):
    version: str


class AppConf(BaseModel):
    cod_app: int
    desc_app: str
    cod_venta_activa: str
    cod_compra_activa: str
    version: str
    comision_mas_50_default: float
    terminos_condiciones_url: str
    politicas_privacidad_url: str


@router.get('/version')
async def get_app_version(response: Response):
    conn = PsqlConnection().conn
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = """SELECT version, cod_venta_activa, cod_compra_activa, terminos_condiciones_url, politicas_privacidad_url 
                FROM app WHERE cod_app = 1"""
    cursor.execute(query)
    app = cursor.fetchone()
    conn.close()
    response.status_code = HTTP_200_OK
    return app


@router.get('/update_version')
async def get_app_version(response: Response, app: App):
    conn = PsqlConnection().conn
    conn.autocommit = True
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = """UPDATE app SET version = %s WHERE cod_app = 1"""
    cursor.execute(
        query,
        (
            app.version,
        )
    )
    conn.close()
    response.status_code = HTTP_200_OK
    return {"msensaje": f"Aplicacion actualizada a version: {app.version} exitosamente"}


@router.get("/info", response_model=AppConf)
async def get_app_conf(response: Response):
    conn = PsqlConnection().conn
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("""SELECT * FROM app""")
    app_info = cursor.fetchone()
    conn.close()
    response.status_code = HTTP_200_OK
    return app_info


@router.put("/info")
async def update_app_conf(response: Response, app: AppConf, Authorization: str = Header(None)):
    token = Authorization.split(" ")[1]
    token_info = validar_token(token, output=True)
    conn = PsqlConnection().conn
    conn.autocommit = True
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = """UPDATE app SET 
                    cod_compra_activa = %s,
                    cod_venta_activa = %s,
                    comision_mas_50_default = %s,
                    user_id = %s
                WHERE cod_app = %s"""
    cursor.execute(
        query,
        (
            app.cod_compra_activa,
            app.cod_venta_activa,
            app.comision_mas_50_default,
            token_info.get("desc_personal"),
            app.cod_app
        )
    )
    conn.close()
    response.status_code = HTTP_200_OK
    return {"mensaje": "App Conf actualizada exitosamente"}
