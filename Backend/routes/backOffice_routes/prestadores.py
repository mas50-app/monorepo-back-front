import os
from asyncio import sleep
from typing import List, Union
from fastapi import APIRouter, Response, Header
from psycopg2.extras import RealDictCursor
from starlette.background import BackgroundTasks
from starlette.responses import FileResponse
from starlette.status import *
from bd_con.conexion import PsqlConnection
from dev_tools.json_web_token import validar_token
from dev_tools.notifications.app_notification import create_notification
from dev_tools.pdf_generator import pdf_cartola_prestador
from middlewares.verifica_ruta_token import VerificaRutaToken
from models.backOffice_models.documentos_model import DocumentoPDF
from models.backOffice_models.prestadores_model import Prestador, PrestadorUpdate, TopPrestador, PrestadorFichaUpdate, \
    Filtros

router = APIRouter(
    route_class=VerificaRutaToken
)


def set_filtros(filtros: Filtros) -> str:
    condiciones = []

    if filtros.cod_prestador:
        condiciones.append(f"d.cod_usuario_vendedor = {filtros.cod_prestador}")

    if filtros.desde:
        condiciones.append(f"d.fecha_documento >= '{filtros.desde}'")

    if filtros.hasta:
        condiciones.append(f"d.fecha_documento <= '{filtros.hasta}'")

    where_clause = " AND ".join(condiciones)
    return f"WHERE {where_clause}" if where_clause else ""


@router.get("/all", response_model=List[Prestador])
async def get_prestadores(response: Response):
    conn = PsqlConnection().conn
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = """SELECT u.*, c.desc_comuna FROM usuario u 
                JOIN comuna c on u.cod_comuna = c.cod_comuna
                WHERE cod_es_prestador = 'S'
                ORDER BY u.cod_usuario"""
    cursor.execute(query)
    prestadores = cursor.fetchall()
    conn.close()
    response.status_code = HTTP_200_OK
    return prestadores


@router.get("/pendientes", response_model=Union[List[Prestador], None])
async def get_prestadores_pendientes(response: Response):
    conn = PsqlConnection().conn
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = """SELECT u.*, c.desc_comuna FROM usuario u 
                JOIN comuna c on u.cod_comuna = c.cod_comuna
                WHERE cod_es_prestador = 'S' AND cod_revisado = 'N' and cod_eliminado = 'N'
                ORDER BY u.cod_usuario"""
    cursor.execute(query)
    pendientes = cursor.fetchall()
    conn.close()
    response.status_code = HTTP_200_OK
    return pendientes


@router.put("/cambiar_estado_revisado")
async def set_revisado(response: Response, prestador: PrestadorUpdate, Authorization: str = Header(None)):
    token = Authorization.split(" ")[1]
    token_info = validar_token(token, output=True)
    conn = PsqlConnection().conn
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    conn.autocommit = True
    query = """UPDATE usuario SET cod_revisado = 'S', user_id = %s WHERE cod_usuario = %s returning cod_usuario"""
    cursor.execute(
        query,
        (
            token_info.get('desc_personal'),
            prestador.cod_usuario
        )
    )
    create_notification(
        "Cuenta de Usuario Verificada",
        "Tus antecedentes han sido validados de forma exitosa. Ya puedes disfrutar y ofrecer tus productos o servicios.",
        token_info.get('desc_personal'),
        prestador.cod_usuario
    )
    conn.close()
    response.status_code = HTTP_200_OK
    return {"mensaje": f"Prestador con cod: {prestador.cod_usuario} modificado a revisado exitosamente"}


@router.put("/cambiar_estado_activo")
async def pivot_cod_activo(response: Response, prestador: PrestadorUpdate, Authorization: str = Header(None)):
    token = Authorization.split(" ")[1]
    token_info = validar_token(token, output=True)
    conn = PsqlConnection().conn
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    conn.autocommit = True
    query = """UPDATE usuario SET cod_activo = %s, user_id = %s WHERE cod_usuario = %s returning cod_usuario"""
    cursor.execute(
        query,
        (
            prestador.enum_str,
            token_info.get('desc_personal'),
            prestador.cod_usuario
        )
    )
    mensaje_activacion = "Su cuenta ha sido reactivada de exitosamente."
    mensaje_inactivacion = "Su cuenta a sido Inactivada, ya que no cumple con " \
                           "los términos y condiciones de nuestra aplicación. Si quiere" \
                           " saber más detalles contactenos al correo contacto@mas50.cl."
    create_notification(
        "Cuenta de Usuario inactivado" if prestador.enum_str == 'N' else 'Cuenta de Usuario activada',
        mensaje_inactivacion if prestador.enum_str == 'N' else mensaje_activacion,
        token_info.get("desc_personal"),
        prestador.cod_usuario
    )
    conn.close()
    response.status_code = HTTP_200_OK
    return {
        "mensaje": f"Prestador cambiado de {'activo' if prestador.enum_str == 'N' else 'inactivo'} a "
                   f"{'inactivo' if prestador.enum_str == 'N' else 'activo'} exitosamente"
    }


@router.put("/cambiar_estado_pausado")
async def pivot_cod_pausado(response: Response, prestador: PrestadorUpdate, Authorization: str = Header(None)):
    token = Authorization.split(" ")[1]
    token_info = validar_token(token, output=True)
    conn = PsqlConnection().conn
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    conn.autocommit = True
    query = """UPDATE usuario SET cod_pausado = %s, user_id = %s WHERE cod_usuario = %s returning cod_usuario"""
    cursor.execute(
        query,
        (
            prestador.enum_str,
            token_info.get('desc_personal'),
            prestador.cod_usuario
        )
    )
    conn.close()
    response.status_code = HTTP_200_OK
    return {
        "mensaje": f"Prestador cambiado de {'pausado' if prestador.enum_str == 'N' else 'reanudar'} a "
                   f"{'reanudar' if prestador.enum_str == 'N' else 'pausado'} exitosamente"
    }


@router.get("/top_prestadores", response_model=Union[List[TopPrestador], None])
async def get_top_prestadores(response: Response):
    conn = PsqlConnection().conn
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = """SELECT u.*,
                       Count(d.cod_documento) ventas
                FROM   usuario u
                       LEFT JOIN documento d
                              ON d.cod_usuario_vendedor = u.cod_usuario AND u.cod_es_prestador = 'S' AND u.cod_revisado = 'S' AND u.cod_activo = 'S'
                GROUP  BY u.cod_usuario
                ORDER  BY ventas DESC
                LIMIT  5 """
    cursor.execute(
        query
    )
    top_prestadores = cursor.fetchall()
    conn.close()
    response.status_code = HTTP_200_OK
    return top_prestadores


@router.put("/update")
async def update_prestador(response: Response, prestador: PrestadorFichaUpdate, Authorization: str = Header(None)):
    token = Authorization.split(" ")[1]
    token_info = validar_token(token, output=True)
    conn = PsqlConnection().conn
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    conn.autocommit = True
    query = """UPDATE usuario SET
                    user_id = %s,
                    desc_usuario = %s,
                    nombre_usuario = %s,
                    apellido1_usuario = %s,
                    rut_usuario = %s,
                    mail_usuario = %s,
                    cod_comuna = %s,
                    comision = %s
                WHERE cod_usuario = %s"""
    cursor.execute(
        query,
        (
            token_info.get('desc_personal'),
            prestador.desc_usuario,
            prestador.nombre_usuario,
            prestador.apellido1_usuario,
            prestador.rut_usuario,
            prestador.mail_usuario,
            prestador.cod_comuna,
            prestador.comision,
            prestador.cod_usuario
        )
    )
    query = """UPDATE cuenta_bancaria SET 
                        user_id = %s,
                        cod_banco = %s,
                        cod_tipo_cuenta_bancaria = %s,
                        nro_cuenta_bancaria = %s
                WHERE cod_usuario = %s"""
    cursor.execute(
        query,
        (
            token_info.get("desc_personal"),
            prestador.cod_banco,
            prestador.cod_tipo_cuenta_bancaria,
            prestador.nro_cuenta_bancaria,
            prestador.cod_usuario
        )
    )

    conn.close()
    response.status_code = HTTP_200_OK
    return {
        "mensaje": f"Prestador actualizado exitosamente"
    }


@router.post("/download-pdf")
async def download_pdf(response: Response, filtros: Filtros, background_tasks: BackgroundTasks):
    conn = PsqlConnection().conn
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = """SELECT d.*, ed.desc_estado_documento, To_json(vendedor) vendedor, To_json(comprador) comprador
                    FROM   documento d
                           JOIN pago pa on d.cod_documento = pa.cod_documento
                           JOIN (SELECT comp.*, comuna.desc_comuna FROM usuario comp join comuna on comp.cod_comuna = comuna.cod_comuna) comprador
                             ON d.cod_usuario_comprador = comprador.cod_usuario
                           JOIN (SELECT vend.*, comuna.desc_comuna FROM usuario vend join comuna on vend.cod_comuna = comuna.cod_comuna) vendedor
                             ON d.cod_usuario_vendedor = vendedor.cod_usuario
                           join estado_documento ed on d.cod_estado_documento = ed.cod_estado_documento %s
                           ORDER by d.fecha_documento asc""" % (set_filtros(filtros))
    cursor.execute(
        query
    )
    documentos = cursor.fetchall()
    conn.close()
    if not documentos:
        response.status_code = HTTP_206_PARTIAL_CONTENT
        return {"mensaje": "No posee ventas"}
    pdf_temp = pdf_cartola_prestador([DocumentoPDF(**doc) for doc in documentos])

    # Eliminar el archivo temporal después de enviar la respuesta
    async def eliminar_archivo_temporal():
        await sleep(1)
        os.remove(pdf_temp)
        print("------- PDF temporal removed -------")
    background_tasks.add_task(eliminar_archivo_temporal)
    response.status_code = HTTP_200_OK
    return FileResponse(pdf_temp)
