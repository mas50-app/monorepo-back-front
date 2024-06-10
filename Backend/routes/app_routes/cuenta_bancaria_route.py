from fastapi import APIRouter, Response, Header
from starlette.status import *
from bd_con.conexion import PsqlConnection
from psycopg2.extras import RealDictCursor
from dev_tools.json_web_token import validar_token
from middlewares.verifica_ruta_token import VerificaRutaToken
from models.app_models.cuenta_bancaria_model import Cuenta_bancariaCreate, Cuenta_bancariaUpdate, \
    Cuenta_bancariaGet, CuentaBancCod

router = APIRouter(route_class=VerificaRutaToken)


@router.get('/all', response_model=Cuenta_bancariaGet)
async def get_by_cod_cuenta_bancaria(response: Response, Authorization: str = Header(None)):
    token = Authorization.split(" ")[1]
    token_info = validar_token(token, output=True)
    conn = PsqlConnection().conn
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = """SELECT * FROM cuenta_bancaria WHERE cod_usuario=%s and cod_activa = 'S'"""
    cursor.execute(
        query,
        (
            token_info.get("cod_usuario"),
        )
    )
    cuenta_usuario = cursor.fetchone()
    response.status_code = HTTP_200_OK
    conn.close()
    return cuenta_usuario


@router.post('/crear')
async def create_cuenta_bancaria(response: Response, cuenta: Cuenta_bancariaCreate, Authorization: str = Header(None)):
    token = Authorization.split(" ")[1]
    token_info = validar_token(token, output=True)
    conn = PsqlConnection().conn
    conn.autocommit = True
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = """SELECT * FROM cuenta_bancaria WHERE cod_usuario=%s AND cod_activa = 'S'"""
    cursor.execute(
        query,
        (
            token_info.get("cod_usuario"),
        )
    )
    cuenta_usuario = cursor.fetchone()
    if cuenta_usuario:
        response.status_code = HTTP_226_IM_USED
        conn.close()
        return {"mensaje": f"el usuario ya tiene una cuenta asociada activa, intente actualizarla"}
    query = """INSERT INTO cuenta_bancaria (desc_cuenta_bancaria, nro_cuenta_bancaria, user_id, cod_usuario, cod_banco, cod_tipo_cuenta_bancaria)
                VALUES (%s,%s,%s,%s,%s,%s) returning cod_cuenta_bancaria"""
    cursor.execute(
        query,
        (
            f" ",
            cuenta.nro_cuenta_bancaria,
            token_info.get('desc_usuario'),
            token_info.get("cod_usuario"),
            cuenta.cod_banco,
            cuenta.cod_tipo_cuenta_bancaria
        )
    )
    cod_cuenta_bancaria = cursor.fetchone().get('cod_cuenta_bancaria')

    # Se cambia cod_es_prestador a S aquí ya que es el último paso de registro y se asigna la comisión por defecto
    query = """SELECT comision_mas_50_default FROM app"""
    cursor.execute(query)
    comision = cursor.fetchone()
    query = """UPDATE usuario SET cod_es_prestador = 'S', user_id = %s, comision = %s WHERE cod_usuario = %s"""
    cursor.execute(
        query,
        (
            token_info.get("desc_usuario"),
            comision.get("comision_mas_50_default"),
            token_info.get('cod_usuario')
        )
    )
    print(f"Cambiado usuario {token_info.get('desc_usuario')} de normal a prestador exitosamente")
    conn.close()
    response.status_code = HTTP_201_CREATED
    return {"mensaje": f"cuenta bancaria cod: {cod_cuenta_bancaria} asociada al usuario cod: {token_info.get('cod_usuario')} exitosamente"}


@router.put('/actualizar')
async def update_cuenta_bancaria(response: Response, cuenta: Cuenta_bancariaUpdate, Authorization: str = Header(None)):
    token = Authorization.split(" ")[1]
    token_info = validar_token(token, output=True)
    conn = PsqlConnection().conn
    conn.autocommit = True
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = """UPDATE cuenta_bancaria SET 
                    nro_cuenta_bancaria = %s,
                    cod_banco = %s,
                    cod_tipo_cuenta_bancaria = %s,
                    user_id = %s
               WHERE cod_cuenta_bancaria = %s"""
    cursor.execute(
        query,
        (
            cuenta.nro_cuenta_bancaria,
            cuenta.cod_banco,
            cuenta.cod_tipo_cuenta_bancaria,
            token_info.get('desc_usuario'),
            cuenta.cod_cuenta_bancaria
        )
    )
    conn.close()
    response.status_code = HTTP_200_OK
    return {"mensaje": f"cuenta_bancaria con cod: {cuenta.cod_cuenta_bancaria} acutalizada exitosamente"}


@router.post('/inactivar')
async def inactivar_cuenta_bancaria(response: Response, cuenta: CuentaBancCod):
    conn = PsqlConnection().conn
    conn.autocommit = True
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = """UPDATE cuenta_bancaria SET cod_activa = 'N' WHERE cod_cuenta_bancaria = %s"""
    cursor.execute(
        query,
        (
            cuenta.cod_cuenta_bancaria,
        )
    )
    conn.close()
    response.status_code = HTTP_200_OK
    return {"mensaje": f"cuenta_bancaria con cod: {cuenta.cod_cuenta_bancaria} inactivada exitosamente"}
