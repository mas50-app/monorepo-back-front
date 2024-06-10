from typing import List, Union
from fastapi import APIRouter, Response, Header, Request
from psycopg2.extras import RealDictCursor
from starlette.status import *
from starlette.websockets import WebSocket
from bd_con.conexion import PsqlConnection
from dev_tools.payment_gateway import Payment
from dev_tools.json_web_token import validar_token
from dev_tools.notifications.app_notification import create_notification
from middlewares.verifica_ruta_token import VerificaRutaToken
from models.backOffice_models.devoluciones import DevolucionCreate, DevolucionCod, DocDevols, DocCod, DocumentoDetalle, \
    DevolByCodPrestador, DevolucionGet, DevolucionElem
from models.payment_gateway_models.FlowApi_models import FlowEstadosDevolucion
from models.payment_gateway_models.payment_models import RefundCreate

router = APIRouter(
    route_class=VerificaRutaToken
)

estados = FlowEstadosDevolucion()


@router.post("/crear")
async def create_refund(response: Response, devolucion: DevolucionCreate, request: Request, Authorization: str = Header(None)):
    token = Authorization.split(" ")[1]
    token_info = validar_token(token, output=True)
    conn = PsqlConnection().conn
    conn.autocommit = True
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = """SELECT d.*, u.*, coalesce(sum(d2.monto_devolucion), 0) monto_devoluciones FROM documento d
                LEFT JOIN devolucion d2 on d.cod_documento = d2.cod_documento 
                JOIN usuario u on d.cod_usuario_comprador = u.cod_usuario
                WHERE d.cod_documento = %s
                GROUP BY d.cod_documento, u.cod_usuario"""
    cursor.execute(
        query,
        (
            devolucion.cod_documento,
            # (estados.rejected, estados.refunded, estados.canceled)
        )
    )
    documento = cursor.fetchone()
    if documento.get("monto_devoluciones", 0) + devolucion.monto_devolucion > documento.get("monto_documento"):
        conn.close()
        response.status_code = HTTP_406_NOT_ACCEPTABLE
        return {"mensaje": f"El documento yase encuentra devuelto en su totalidad o la cantidad a devolver es demasiado alta"}

    query = """INSERT INTO devolucion (desc_devolucion, user_id, cod_documento, monto_devolucion, cod_es_manual) 
                VALUES (%s,%s,%s,%s,%s) returning cod_devolucion"""
    cursor.execute(
        query,
        (
            devolucion.desc_devolucion,
            token_info.get("desc_personal"),
            devolucion.cod_documento,
            devolucion.monto_devolucion,
            devolucion.cod_manual
        )
    )
    devol = cursor.fetchone()
    if devol and devolucion.cod_manual == 'N':
        refund = Payment()
        url_confirmation = request.url.scheme + "://" + request.url.netloc + "/api/v1/flow_refund_confirm/crear"
        print("AQUI VA A SER LA CONFIRMACIONNNN-------", url_confirmation)
        refunf_d = {
            "refundCommerceOrder": devol.get("cod_devolucion"),
            "flowTrxId": documento.get("flow_order"),
            "amount": devolucion.monto_devolucion,
            "receiverEmail": documento.get("mail_usuario"),
            "urlCallBack": url_confirmation
        }
        refund_req = refund.create_refund(refund_data=RefundCreate(**refunf_d))
        if refund_req.status_code != 200:
            response.status_code = HTTP_409_CONFLICT
            conn.close()
            return refund_req.json()
        payment_req_json = refund_req.json()
        query = """UPDATE devolucion SET flow_token = %s, flow_orden_devolucion = %s, fecha_devolucion = %s,
                                        flow_fee_devolucion = %s, flow_status = %s 
                    WHERE cod_devolucion = %s"""
        cursor.execute(
            query,
            (
                payment_req_json.get("token"),
                payment_req_json.get("flowRefundOrder"),
                payment_req_json.get("date"),
                payment_req_json.get("fee"),
                estados.created,
                devol.get("cod_devolucion")
            )
        )
    conn.close()
    response.status_code = HTTP_201_CREATED
    return {"mensaje": f"Devolución creada exitosamente con cod {devol.get('cod_devolucion')}"}


@router.put("/cancelar")
async def cancel_refund(response: Response, devolucion: DevolucionCod, Authorization: str = Header(None)):
    token = Authorization.split(" ")[1]
    token_info = validar_token(token, output=True)
    conn = PsqlConnection().conn
    conn.autocommit = True
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = """SELECT flow_token FROM devolucion WHERE cod_devolucion = %s"""
    cursor.execute(
        query,
        (
            devolucion.cod_devolucion,
        )
    )
    flow_token = cursor.fetchone()
    refund = Payment()
    refund_resp = refund.cancel_refund(token=flow_token.get("flow_token"))
    if refund_resp.status_code != 200:
        conn.close()
        response.status_code = HTTP_406_NOT_ACCEPTABLE
        print(refund_resp.json())
        return refund_resp.json()
    query = """UPDATE devolucion SET flow_status = %s, user_id = %s WHERE cod_devolucion = %s"""
    cursor.execute(
        query,
        (
            estados.canceled,
            token_info.get("desc_personal"),
            devolucion.cod_devolucion,
        )
    )
    conn.close()
    response.status_code = HTTP_200_OK
    return {"mensaje": f"Devolución cancelada exitosamente"}


@router.post("/flow_estado")
async def get_flow_estado(response: Response, devolucion: DevolucionCod):
    conn = PsqlConnection().conn
    # conn.autocommit = True
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = """SELECT flow_token FROM devolucion WHERE cod_devolucion = %s"""
    cursor.execute(
        query,
        (
            devolucion.cod_devolucion,
        )
    )
    flow_token = cursor.fetchone()
    refund = Payment()
    refund_resp = refund.get_refund_status(token=flow_token.get("flow_token"))
    conn.close()
    response.status_code = HTTP_200_OK
    return refund_resp.json()


@router.get("/all-docs-rech", response_model=List[DocDevols])
async def get_all_documentos_rechazados_devoluciones(response: Response):
    conn = PsqlConnection().conn
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = f"""SELECT d.*,
                        To_json(vendedor) vendedor,
                       To_json(comprador) comprador
                FROM   documento d
                        join usuario vendedor on d.cod_usuario_vendedor = vendedor.cod_usuario
                        join usuario comprador on d.cod_usuario_comprador = comprador.cod_usuario
                WHERE d.cod_estado_documento = 4
                GROUP  BY d.cod_documento, vendedor.cod_usuario, comprador.cod_usuario
                ORDER BY d.cod_documento desc"""
    cursor.execute(query)
    devols = cursor.fetchall()
    conn.close()
    response.status_code = HTTP_200_OK
    return devols


@router.post("/by_cod_doc", response_model=DocumentoDetalle)
async def get_detalle_by_doc(response: Response, documento: DocCod):
    conn = PsqlConnection().conn
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = """SELECT d.*, ed.desc_estado_documento,
                       du.desc_direccion_usuario,
                       To_json(vendedor)                  vendedor,
                       To_json(comprador)                 comprador,
                       COALESCE(json_agg(d2) FILTER (WHERE d2.cod_devolucion IS NOT NULL), '[]') devoluciones,
                       Json_agg((SELECT det
                                 FROM   (SELECT dd.*,
                                                is2.*,
                                                un.desc_unidad,
                                                s.*)det)) detalles
                FROM   documento d
                       JOIN usuario comprador
                         ON d.cod_usuario_comprador = comprador.cod_usuario
                       JOIN usuario vendedor
                         ON d.cod_usuario_vendedor = vendedor.cod_usuario
                       JOIN devolucion d2 using(cod_documento)
                       JOIN detalle_documento dd using(cod_documento)
                       JOIN item_servicio is2 using(cod_item_servicio)
                       JOIN estado_documento ed on d.cod_estado_documento = ed.cod_estado_documento 
                       JOIN unidad un on is2.cod_unidad = un.cod_unidad
                       JOIN servicio s using(cod_servicio)
                       LEFT JOIN direccion_usuario du
                              ON d.cod_direccion_usuario_comprador = du.cod_direccion_usuario
                WHERE  cod_documento = %s
                GROUP  BY d.cod_documento,
                          ed.desc_estado_documento,
                          du.desc_direccion_usuario,
                          vendedor.cod_usuario,
                          comprador.cod_usuario"""
    cursor.execute(
        query,
        (
            documento.cod_documento,
        )
    )
    documento_detalles = cursor.fetchone()
    conn.close()
    response.status_code = HTTP_200_OK
    return documento_detalles


@router.post("/dev-por-doc", response_model=Union[DevolucionGet, None])
async def get_devolucion_by_doc(response: Response, documento: DocCod):
    conn = PsqlConnection().conn
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = """SELECT * FROM devolucion WHERE cod_documento = %s"""
    cursor.execute(
        query,
        (
            documento.cod_documento,
        )
    )
    devol = cursor.fetchone()
    response.status_code = HTTP_200_OK
    return devol


@router.get("/all", response_model=List[DevolucionElem])
async def get_devoluciones_all():
    conn = PsqlConnection().conn
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = """SELECT de.cod_devolucion, de.desc_devolucion, de.fecha_devolucion, de.monto_devolucion,
                        de.user_id as personal, vend.cod_usuario , vend.desc_usuario, de.cod_es_manual 
                FROM devolucion de
                JOIN documento d on d.cod_documento = de.cod_documento
                JOIN usuario comp on d.cod_usuario_comprador = comp.cod_usuario
                JOIN usuario vend on d.cod_usuario_vendedor = vend.cod_usuario"""
    cursor.execute(query)
    devols = cursor.fetchall()
    return devols


@router.websocket("/ws")
async def wbs(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_json()
        print(data)
        conn = PsqlConnection().conn
        # conn.autocommit = True
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        for cod_devolucion in data.get("devoluciones"):
            query = """SELECT flow_token FROM devolucion WHERE cod_devolucion = %s"""
            cursor.execute(
                query,
                (
                    cod_devolucion,
                )
            )
            flow_token = cursor.fetchone()
            refund = Payment()
            refund_resp = refund.get_refund_status(token=flow_token.get("flow_token"))
            print(refund_resp.json())
            await websocket.send_json(refund_resp.json())
