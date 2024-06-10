from datetime import datetime
import requests
from fastapi import APIRouter, Response, Header
from starlette.status import *
from bd_con.conexion import PsqlConnection
from psycopg2.extras import RealDictCursor
from dev_tools.json_web_token import validar_token, generar_token
from models.app_models.auth_model import Login, VerificaMail
from models.app_models.usuario_model import UsuarioCreate


router = APIRouter()


@router.post('/login')
async def login(response: Response, userLogin: Login):
    conn = PsqlConnection().conn
    conn.autocommit = True
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = """SELECT 
                    u.cod_usuario,
                    desc_usuario,
                    nombre_usuario,
                    apellido1_usuario,
                    apellido2_usuario,
                    rut_usuario,
                    mail_usuario,
                    cod_es_prestador,
                    cod_comuna,
                    cod_pausado,
                    cod_revisado,
                    coalesce(path_imagen, '') as url_foto_perfil
                FROM usuario u
                WHERE uuid = %s AND cod_activo = 'S' AND cod_eliminado = 'N'"""

    cursor.execute(
        query,
        (userLogin.uuid,)
    )

    usuario = cursor.fetchone()

    if usuario:
        # Actualizamos la última sesión abierta
        query = """UPDATE usuario SET last_login = %s WHERE cod_usuario = %s"""
        cursor.execute(
            query,
            (
                datetime.now(),
                usuario.get("cod_usuario")
            )
        )

        # Aqui se buscan los tokens que tiene el usuario y se revisa que el token no este utilizado en otro usuario diferente
        query = """SELECT cod_usuario, token 
                    FROM firebase_token_usuario 
                    WHERE cod_usuario = %s and token = %s"""

        cursor.execute(
            query,
            (
                usuario.get("cod_usuario"),
                userLogin.token
            )
        )
        token = cursor.fetchone()

        if not token:
            query = """INSERT INTO firebase_token_usuario (desc_firebase_token_usuario, user_id, cod_usuario, token) 
                    VALUES (%s,%s,%s,%s) returning cod_firebase_token_usuario"""
            cursor.execute(
                query,
                (
                    f"Token de {usuario.get('desc_usuario')}",
                    usuario.get('desc_usuario'),
                    usuario.get('cod_usuario'),
                    userLogin.token
                )
            )
            cod_firebase_token_usuario = cursor.fetchone().get('cod_firebase_token_usuario')
            print(f"Token regisrado con cod {cod_firebase_token_usuario}")

        # Aqui se elinmina el token que estuviera asociado a otro usuario para evitar notificaciones erroneas
        query = """DELETE FROM firebase_token_usuario WHERE cod_usuario != %s and token = %s returning token"""
        cursor.execute(
            query,
            (
                usuario.get('cod_usuario'),
                userLogin.token
            )
        )
        token = cursor.fetchone()
        if token:
            print(f"------------ Se Eliminan registro de token: {token} ------------")

        # Validacion de estados de activacion de compra y venta en la aplicacion
        query = """SELECT cod_compra_activa, cod_venta_activa FROM app"""
        cursor.execute(query)
        usuario["estados_app"] = cursor.fetchone()
        conn.close()
        response.status_code = HTTP_200_OK
        return {"token": generar_token(usuario)}
    conn.close()
    response.status_code = HTTP_401_UNAUTHORIZED
    return {"mensaje": "usuario no registrado"}


@router.get('/verifica-token')
def verificar_token(Authorization: str = Header(None)):
    token = Authorization.split(" ")[1]
    token_info = validar_token(token, output=True)
    # Retorna si es valido la info del token y si no un JsonResponse 401
    return token_info


@router.post('/registrar')
async def create_usuario(response: Response, usuario: UsuarioCreate):
    usuario = usuario.dict(exclude_none=True)
    if usuario.get("desc_usuario") in ("", None):
        usuario["desc_usuario"] = usuario.get("nombre_usuario")
    conn = PsqlConnection().conn
    conn.autocommit = True
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute(
        """SELECT * FROM usuario WHERE uuid = %s""",
        (usuario.get('uuid'), )
    )
    usuario_exist = cursor.fetchone()
    if usuario_exist:
        response.status_code = HTTP_226_IM_USED
        return {"mensaje": "usuario ya está registrado"}
    valores = [datetime.now()]
    query = """INSERT INTO usuario (fecha_registro,"""
    for u in usuario.keys():
        valores.append(usuario.get(u))
        query += f"{u}, "
    query = query[:-2]
    query += f") VALUES ({','.join('%s' for i in range(valores.__len__()))}) returning cod_usuario"
    cursor.execute(
        query,
        valores
    )
    response.status_code = HTTP_201_CREATED
    cod_us = cursor.fetchone().get('cod_usuario')
    conn.close()
    return {"mensaje": f"usuario creado cod: {cod_us} exitosamente"}


@router.post("/verifica_mail")
async def verifica_mail(response: Response, mail: VerificaMail):
    verify_email_resp = requests.get(
        f"https://api.hunter.io/v2/email-verifier?email={mail.mail}&api_key=7d505d6a7a8628a23b9cc50994ad37a58e6d3e05"
    )
    is_valid = verify_email_resp.json().get("data").get("status")
    if is_valid == "invalid":
        response.status_code = HTTP_406_NOT_ACCEPTABLE
        return {"mensaje": f"Mail Ínvalido"}
    response.status_code = HTTP_200_OK
    return {"mensaje": f"Mail Válido"}
