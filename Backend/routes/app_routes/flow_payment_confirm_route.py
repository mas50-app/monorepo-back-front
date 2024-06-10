import datetime

from fastapi import APIRouter, Response, Request
from psycopg2.extras import RealDictCursor
from starlette.status import *
from bd_con.conexion import PsqlConnection
from dev_tools.notifications.app_notification import create_notification

router = APIRouter()


@router.post('/crear')
async def create_pago(response: Response, request: Request):
    conn = PsqlConnection().conn
    conn.autocommit = True
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    req_body = await request.body()
    token = str(req_body).split("=")[1].replace("'", "")

    query = """SELECT documento.*, json_agg(s) servicios FROM documento  
                JOIN detalle_documento dd on documento.cod_documento = dd.cod_documento
                JOIN item_servicio i on dd.cod_item_servicio = i.cod_item_servicio
                JOIN servicio s on i.cod_servicio = s.cod_servicio
                WHERE flow_token = %s
                GROUP BY documento.cod_documento"""
    cursor.execute(
        query,
        (token,)
    )
    documento = cursor.fetchone()

    # Cambiando estado a pagado
    query = """UPDATE documento SET cod_estado_documento = %s WHERE cod_documento = %s"""
    cursor.execute(
        query,
        (
            2,
            documento.get('cod_documento')
        )
    )

    query = """INSERT INTO pago (desc_pago, cod_documento, cod_tipo_pago, monto_pago, fecha_pago, user_id) 
                    VALUES (%s,%s,%s,%s,%s,%s) returning cod_pago"""
    cursor.execute(
        query,
        (
            f"Pago Test Cod Documento: {documento.get('cod_documento')}",
            documento.get('cod_documento'),
            1,
            documento.get("monto_documento"),
            documento.get("fecha_documento"),
            documento.get("")
        )
    )

    pago = cursor.fetchone()

    query = """SELECT * FROM usuario u WHERE cod_usuario = %s"""
    cursor.execute(
        query,
        (
            documento.get("cod_usuario_comprador"),
        )
    )
    comprador = cursor.fetchone()

    query = """INSERT INTO historial_estado_documento (desc_historial_estado_documento, user_id, cod_documento, cod_estado_documento, fecha_cambio_estado) 
                    VALUES (%s,%s,%s,%s,%s)"""

    cursor.execute(
        query,
        (
            "",
            comprador.get("desc_usuario"),
            documento.get("cod_documento"),
            2,
            datetime.datetime.now()
        )
    )

    query = """SELECT * FROM usuario u WHERE cod_usuario = %s"""
    cursor.execute(
        query,
        (
            documento.get("cod_usuario_vendedor"),
        )
    )
    vendedor = cursor.fetchone()

    # Notificacion vendedor
    create_notification(
        "Venta Completada",
        f"{vendedor.get('desc_usuario')} has recibido un pago de {comprador.get('desc_usuario')} "
        f"de forma exitosa por un monto de CLP {'${:,.0f}'.format(int(documento.get('monto_documento')))} por el servicio"
        f" {documento.get('servicios', [])[0].get('nom_servicio', '')}",
        comprador.get("desc_usuario"),
        # token_info.get('cod_usuario')
        documento.get("cod_usuario_vendedor")
    )
    # Notificacion comprador
    create_notification(
        "Compra Completada",
        f"{comprador.get('desc_usuario').capitalize()} se ha realizado un pago exitosamente a {vendedor.get('desc_usuario').capitalize()}. Por un monto de CLP {'${:,.0f}'.format(int(documento.get('monto_documento')))}.",
        comprador.get("desc_usuario"),
        # token_info.get('cod_usuario')
        documento.get("cod_usuario_comprador")
    )
    conn.close()
    response.status_code = HTTP_200_OK
    return pago
