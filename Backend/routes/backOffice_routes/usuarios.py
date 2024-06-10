import os
from typing import List, Union
from fastapi import APIRouter, Response, Header
from psycopg2.extras import RealDictCursor
from starlette.status import HTTP_200_OK
from bd_con.conexion import PsqlConnection
from dev_tools.json_web_token import validar_token
from dev_tools.notifications.app_notification import create_notification
from middlewares.verifica_ruta_token import VerificaRutaToken
from models.backOffice_models.usuarios_model import Usuario, TopClientes, UsuarioCod

router = APIRouter(route_class=VerificaRutaToken)


DATA_PATH_WIN = "./temporales_desarrollo/imagenes/"
DATA_PATH_LIN = "/app/temporales_desarrollo/imagenes/"


@router.get("/all", response_model=Union[List[Usuario], None])
async def get_usuarios(response: Response):
    conn = PsqlConnection().conn
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = """SELECT u.*, c.desc_comuna FROM usuario u
                JOIN comuna c on u.cod_comuna = c.cod_comuna
                ORDER BY u.cod_usuario"""
    cursor.execute(query)
    usuarios = cursor.fetchall()
    conn.close()
    response.status_code = HTTP_200_OK
    return usuarios


@router.get("/top_clientes", response_model=Union[List[TopClientes], None])
async def get_top_clientes(response: Response):
    conn = PsqlConnection().conn
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = """SELECT u.*,
                       Count(d.cod_documento) compras
                FROM   usuario u
                       LEFT JOIN documento d
                              ON d.cod_usuario_comprador = u.cod_usuario AND u.cod_activo = 'S'
                GROUP  BY u.cod_usuario
                ORDER  BY compras DESC
                LIMIT  5 """
    cursor.execute(
        query
    )
    top_clientes = cursor.fetchall()
    conn.close()
    response.status_code = HTTP_200_OK
    return top_clientes


@router.post("/por_cod")
async def get_perfil_usuario(response: Response, usuario: UsuarioCod):
    conn = PsqlConnection().conn
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = """SELECT * FROM usuario
                JOIN comuna c on usuario.cod_comuna = c.cod_comuna
                """
    cursor.execute(
        query,
        (
            usuario.cod_usuario,
        )
    )
    usuario = cursor.fetchone()
    conn.close()
    response.status_code = HTTP_200_OK
    return usuario


@router.put("/cambiar_estado_activo")
async def pivot_cod_activo(response: Response, usuario: UsuarioCod, Authorization: str = Header(None)):
    token = Authorization.split(" ")[1]
    token_info = validar_token(token, output=True)
    conn = PsqlConnection().conn
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    conn.autocommit = True
    query = """UPDATE usuario SET cod_activo = %s, user_id = %s WHERE cod_usuario = %s returning desc_usuario"""
    cursor.execute(
        query,
        (
            usuario.enum_str,
            token_info.get('desc_personal'),
            usuario.cod_usuario
        )
    )
    mensaje_activacion = "Su cuenta ha sido reactivada de exitosamente."
    mensaje_inactivacion = "Su cuenta a sido Inactivada, ya que no cumple con " \
                           "los términos y condiciones de nuestra aplicación. Si quiere" \
                           " saber más detalles contactenos al correo contacto@mas50.cl."
    create_notification(
        "Cuenta de Usuario inactivado" if usuario.enum_str == 'N' else 'Cuenta de Usuario activada',
        mensaje_inactivacion if usuario.enum_str == 'N' else mensaje_activacion,
        token_info.get("desc_personal"),
        usuario.cod_usuario
    )
    conn.close()
    response.status_code = HTTP_200_OK
    return {
        "mensaje": f"Prestador cambiado de {'activo' if usuario.enum_str == 'N' else 'inactivo'} a "
                   f"{'inactivo' if usuario.enum_str == 'N' else 'activo'} exitosamente"
    }


@router.put("/cambiar_estado_pausado")
async def pivot_cod_pausado(response: Response, usuario: UsuarioCod, Authorization: str = Header(None)):
    token = Authorization.split(" ")[1]
    token_info = validar_token(token, output=True)
    conn = PsqlConnection().conn
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    conn.autocommit = True
    query = """UPDATE usuario SET cod_pausado = %s, user_id = %s WHERE cod_usuario = %s returning cod_usuario"""
    cursor.execute(
        query,
        (
            usuario.enum_str,
            token_info.get('desc_personal'),
            usuario.cod_usuario
        )
    )
    conn.close()
    response.status_code = HTTP_200_OK
    return {
        "mensaje": f"Prestador cambiado de {'pausado' if usuario.enum_str == 'N' else 'reanudar'} a "
                   f"{'reanudar' if usuario.enum_str == 'N' else 'pausado'} exitosamente"
    }


@router.post("/eliminar_antecedentes")
async def elimina_antecedentes(response: Response, usuario: UsuarioCod, Authorization: str = Header(None)):
    token = Authorization.split(" ")[1]
    token_info = validar_token(token, output=True)
    conn = PsqlConnection().conn
    conn.autocommit = True
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = """DELETE FROM antecedente WHERE cod_usuario = %s returning path_imagen"""
    cursor.execute(
        query,
        (
            usuario.cod_usuario,
        )
    )
    image = cursor.fetchone()
    try:
        if os.name == "nt":
            os.remove(os.path.join(DATA_PATH_WIN, image.get("path_imagen")))
        else:
            os.remove(os.path.join(DATA_PATH_LIN, image.get("path_imagen")))
    except:
        print("No se encontró archivo para remover")

    query = """UPDATE usuario SET cod_revisado = 'N' WHERE cod_usuario = %s"""
    cursor.execute(
        query,
        (
            usuario.cod_usuario,
        )
    )
    create_notification(
        "Antecedentes rechazados",
        "Sus antecedentes no fueron validados correctamente. Por favor, vuelva a "
        "subir su fotografía y la de su Cédula de Identidad.",
        token_info.get("desc_personal"),
        usuario.cod_usuario
    )
    conn.close()
    response.status_code = HTTP_200_OK
    return {"mensaje": "Antecedentes eliminados exitosamente"}
