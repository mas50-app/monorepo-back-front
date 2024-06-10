import datetime
from fastapi import APIRouter, Response, Header, Request
from starlette.status import *
from typing import List, Union, Dict
from bd_con.conexion import PsqlConnection
from psycopg2.extras import RealDictCursor
from dev_tools.payment_gateway import Payment
from dev_tools.json_web_token import validar_token
from dev_tools.notifications.app_notification import create_notification
from middlewares.verifica_ruta_token import VerificaRutaToken
from models.app_models.documento_model import DocumentoGet, DocumentoCreate, DocumentoCod, DetalleDocumento, \
    DocumentosByEstVEndedor, DocumentosByEstComprador, BasicDoc
from models.payment_gateway_models.payment_models import PaymentCreate

router = APIRouter(
    route_class=VerificaRutaToken
)


@router.get('/all', response_model=Union[List[DocumentoGet], Dict])
async def get_alldocumento(response: Response, Authorization: str = Header(None)):
    token = Authorization.split(" ")[1]
    token_info = validar_token(token, output=True)
    cod_usuario = token_info.get('cod_usuario')
    conn = PsqlConnection().conn
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = """SELECT 
            d.*,
            ed.cod_estado_documento,
            ed.desc_estado_documento,
            du.desc_direccion_usuario as desc_direccion_comprador,
            c.desc_comuna as desc_comuna_comprador,
            u.desc_usuario as desc_usuario_comprador,
            u.apellido1_usuario || ' ' || coalesce(u.apellido2_usuario, '') || ', ' || u.nombre_usuario as nombre_usuario_comprador
            FROM documento d
            LEFT JOIN direccion_usuario du on d.cod_direccion_usuario_comprador = du.cod_direccion_usuario
            LEFT JOIN comuna c on c.cod_comuna = du.cod_comuna
            LEFT JOIN usuario u on u.cod_usuario = d.cod_usuario_comprador
            JOIN estado_documento ed on d.cod_estado_documento = ed.cod_estado_documento
            WHERE cod_usuario_vendedor = %s"""
    # print("VENDEDOOOOOOR", cod_usuario)
    cursor.execute(
        query,
        (
            cod_usuario,
        )
    )
    documentos = cursor.fetchall()
    conn.close()
    if documentos:
        response.status_code = HTTP_200_OK
        return documentos
    else:
        response.status_code = HTTP_206_PARTIAL_CONTENT
        return {"mensaje": "no tiene documentos"}


@router.post('/por_cod', response_model=List[DetalleDocumento])
async def get_by_cod_documento(response: Response, documento: DocumentoCod):
    conn = PsqlConnection().conn
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = """SELECT 
                dd.*,
                it.desc_item_servicio,
                s.nom_servicio 
                FROM detalle_documento dd
                JOIN item_servicio it using(cod_item_servicio)
                JOIN servicio s using(cod_servicio)
                WHERE cod_documento = %s"""
    cursor.execute(
        query,
        (
            documento.cod_documento,
        )
    )
    detalles = cursor.fetchall()
    response.status_code = HTTP_200_OK
    conn.close()

    return detalles


@router.post('/crear')
async def create_documento(
        response: Response,
        request: Request,
        documento: DocumentoCreate,
        Authorization: str = Header(None)
):
    token = Authorization.split(" ")[1]
    token_info = validar_token(token, output=True)
    cod_usuario_comprador = token_info.get('cod_usuario')
    conn = PsqlConnection().conn
    # conn.autocommit = True
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    query = """SELECT s.cod_servicio, desc_servicio, nom_servicio, comision FROM item_servicio 
                JOIN servicio s on item_servicio.cod_servicio = s.cod_servicio
                JOIN usuario u on s.cod_usuario = u.cod_usuario
                WHERE cod_item_servicio = %s"""
    cursor.execute(
        query,
        (
            documento.detalles[0].cod_item_servicio,
        )
    )
    servicio = cursor.fetchone()

    # Cálculo de Comisiones
    comision = servicio.get("comision")
    monto_comision_neto = documento.monto_documento * float(comision) / 100
    monto_iva_comision = monto_comision_neto * 0.19
    monto_comision_bruto = monto_comision_neto + monto_iva_comision
    monto_venta_bruto = documento.monto_documento - monto_comision_bruto

    query = """INSERT INTO documento (desc_documento, cod_usuario_vendedor, cod_usuario_comprador,
                                        monto_documento, fecha_documento, user_id,
                                        cod_estado_documento, cod_direccion_usuario_comprador,
                                        cod_retiro, cod_domicilio, comision, monto_comision_neto,
                                        monto_iva, monto_comision_bruto, monto_venta)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) returning cod_documento"""

    cursor.execute(
        query,
        (
            # f"{documento.nom_vendedor.capitalize()} vende a {token_info.get('desc_usuario').capitalize()} el"
            # f" {documento.fecha_documento} por {documento.monto_documento}",
            f"{servicio.get('nom_servicio')} vende a {token_info.get('desc_usuario')} el"
            f" {documento.fecha_documento.strftime('%d-%m-%Y')} "
            f"por un monto de {'{:,.0f}'.format(documento.monto_documento).replace(',', '.')}",
            documento.cod_usuario_vendedor,
            cod_usuario_comprador,
            documento.monto_documento,
            documento.fecha_documento,
            token_info.get('desc_usuario'),
            documento.cod_estado_documento,
            documento.cod_direccion_comprador if documento.cod_direccion_comprador not in (0, None, '') else None,
            documento.cod_retiro,
            documento.cod_domicilio,
            comision,
            monto_comision_neto,
            monto_iva_comision,
            monto_comision_bruto,
            monto_venta_bruto
        )
    )
    cod_documento = cursor.fetchone().get('cod_documento')

    if not cod_documento:
        conn.rollback()
        conn.close()
        response.status_code = HTTP_409_CONFLICT
        return {"mensaje": "Estructura incorrecta de armado de documento"}

    # Creación de Despacho
    if documento.cod_courier:
        query = """INSERT INTO despacho (desc_despacho, user_id, cod_courier, cod_documento, fecha_despacho) 
                    VALUES (%s,%s,%s,%s,%s)"""
        cursor.execute(
            query,
            (
                "",
                token_info.get("desc_usuario"),
                documento.cod_courier,
                cod_documento,
                documento.detalles[0].fecha_agenda
            )
        )

    # Manejo de Pasarela de Pagos, creación de orden de pago
    url_confirmation = request.url.scheme + "://" + request.url.netloc + "/api/v1/flow_payment_confirm/crear"

    payment = Payment()
    payment_data = {
        "subject": f"Compra a {documento.nom_vendedor}".upper(),
        "commerceOrder": f"Orden {cod_documento}".upper(),
        "amount": int(documento.monto_documento),
        "email": token_info.get("mail_usuario"),
        "urlConfirmation": url_confirmation,
        "urlReturn": "https://www.google.com/"
    }
    payment_req = payment.create_order(payment_data=PaymentCreate(**payment_data))
    payment_req_json = payment_req.json()

    if payment_req.status_code == 200:
        flow_token = payment_req_json.get("token")
        flow_url = payment_req_json.get("url")
        flow_order = payment_req_json.get("flowOrder")

        query = """UPDATE documento SET flow_token = %s, flow_order = %s WHERE cod_documento = %s"""
        cursor.execute(
            query,
            (
                flow_token,
                flow_order,
                cod_documento
            )
        )

        for detalle in documento.detalles:
            query = """INSERT INTO detalle_documento (desc_detalle_documento, user_id, cod_documento, fecha_agenda, 
                                                    cantidad, subtotal, cod_item_servicio) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s)"""
            print("-----------------------", (
                    f"{detalle.desc_item_servicio}",
                    token_info.get('desc_usuario'),
                    cod_documento,
                    detalle.fecha_agenda,
                    detalle.cantidad,
                    detalle.subtotal,
                    detalle.cod_item_servicio
                ))
            cursor.execute(
                query,
                (
                    f"{detalle.desc_item_servicio}",
                    token_info.get('desc_usuario'),
                    cod_documento,
                    detalle.fecha_agenda,
                    detalle.cantidad,
                    detalle.subtotal,
                    detalle.cod_item_servicio
                )
            )
        conn.commit()
        conn.close()
        response.status_code = HTTP_201_CREATED
        redirect_url = f"{flow_url}?token={flow_token}"
        return redirect_url
    else:
        conn.rollback()
        conn.close()
        response.status_code = HTTP_409_CONFLICT
        mensaje = {"mensaje": f"La pasarela de pago devuelve {payment_req_json}"}
        return mensaje


@router.put('/set_aceptado')
async def cambio_estado_documento_aceptado(response: Response, doc: DocumentoCod, Authorization: str = Header(None)):
    token = Authorization.split(" ")[1]
    token_info = validar_token(token, output=True)
    conn = PsqlConnection().conn
    conn.autocommit = True
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = """INSERT INTO historial_estado_documento (desc_historial_estado_documento, user_id, cod_documento, 
                                                cod_estado_documento, fecha_cambio_estado) 
            VALUES (%s,%s,%s,%s,%s)"""
    cursor.execute(
        query,
        (
            "",
            token_info.get("desc_usuario"),
            doc.cod_documento,
            3,
            datetime.datetime.now()
        )
    )
    query = """UPDATE documento SET cod_estado_documento = 3 WHERE cod_documento = %s"""
    cursor.execute(
        query,
        (
            doc.cod_documento,
        )
    )
    query = """SELECT cod_usuario_comprador, u.desc_usuario, d.cod_retiro FROM documento d
                        JOIN usuario u on d.cod_usuario_comprador = u.cod_usuario
                        WHERE cod_documento = %s"""
    cursor.execute(
        query,
        (
            doc.cod_documento,
        )
    )
    comprador = cursor.fetchone()

    # Se envían las notificaciones pertinentes
    create_notification(
        'Pedido Aceptado',
        f"{comprador.get('desc_usuario').capitalize()}, felicidades su pedido ha sido aceptado por "
        f"{token_info.get('desc_usuario').capitalize()}, ahora se está procesando, pronto le tendremos actualizaciones sobre su estado",
        token_info.get('desc_usuario'),
        comprador.get('cod_usuario_comprador')
    )
    response.status_code = HTTP_200_OK
    conn.close()
    return {"mensaje": "estado documento cambiado a aceptado exitosamente"}


@router.put('/set_rechazado')
async def cambio_estado_documento_rechazado(response: Response, doc: DocumentoCod, Authorization: str = Header(None)):
    token = Authorization.split(" ")[1]
    token_info = validar_token(token, output=True)
    conn = PsqlConnection().conn
    conn.autocommit = True
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = """INSERT INTO historial_estado_documento (desc_historial_estado_documento, user_id, cod_documento, 
                                                cod_estado_documento, fecha_cambio_estado) 
            VALUES (%s,%s,%s,%s,%s)"""
    cursor.execute(
        query,
        (
            "",
            token_info.get("desc_usuario"),
            doc.cod_documento,
            4,
            datetime.datetime.now()
        )
    )
    query = """UPDATE documento SET cod_estado_documento = 4 WHERE cod_documento = %s"""
    cursor.execute(
        query,
        (
            doc.cod_documento,
        )
    )
    query = """SELECT cod_usuario_comprador, u.desc_usuario, d.cod_retiro FROM documento d
                    JOIN usuario u on d.cod_usuario_comprador = u.cod_usuario
                    WHERE cod_documento = %s"""
    cursor.execute(
        query,
        (
            doc.cod_documento,
        )
    )
    comprador = cursor.fetchone()

    # Se envían las notificaciones pertinentes
    create_notification(
        'Pedido Rechazado',
        f"{comprador.get('desc_usuario').capitalize()}, lamentablemente su pedido fue rechazado por "
        f"{token_info.get('desc_usuario').capitalize()}"
        f", por falta de disponibilidad y stock. Su pago será reembolsado cuanto antes. Intente nuevamente más tarde.",
        token_info.get('desc_usuario'),
        comprador.get('cod_usuario_comprador')
    )
    response.status_code = HTTP_200_OK
    conn.close()
    return {"mensaje": "estado documento cambiado a rechazado exitosamente"}


@router.put('/set_terminado')
async def cambio_estado_documento_terminado(response: Response, doc: DocumentoCod, Authorization: str = Header(None)):
    token = Authorization.split(" ")[1]
    token_info = validar_token(token, output=True)
    conn = PsqlConnection().conn
    conn.autocommit = True
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    # Se crean el seguimiento de los cambios de estado
    query = """INSERT INTO historial_estado_documento (desc_historial_estado_documento, user_id, cod_documento, 
                                                    cod_estado_documento, fecha_cambio_estado) 
                VALUES (%s,%s,%s,%s,%s)"""
    cursor.execute(
        query,
        (
            "",
            token_info.get("desc_usuario"),
            doc.cod_documento,
            5,
            datetime.datetime.now()
        )
    )

    # Se cambia el estado del documento
    query = """UPDATE documento SET cod_estado_documento = 5 WHERE cod_documento = %s"""
    cursor.execute(
        query,
        (
            doc.cod_documento,
        )
    )
    query = """SELECT cod_usuario_comprador, u.desc_usuario, d.cod_retiro FROM documento d
                JOIN usuario u on d.cod_usuario_comprador = u.cod_usuario
                WHERE cod_documento = %s"""
    cursor.execute(
        query,
        (
            doc.cod_documento,
        )
    )
    comprador = cursor.fetchone()

    # Se envían las notificaciones pertinentes
    create_notification(
        '👌 Su pedido está listo 👌',
        f"Estimada/o {comprador.get('desc_usuario').capitalize()}, su pedido a {token_info.get('desc_usuario').capitalize()} "
        f" {'está listo para ser retirado!!!' if comprador.get('cod_retiro') == 'S' else 'será enviado a la dirección indicada!!!'}",
        token_info.get('desc_usuario'),
        comprador.get('cod_usuario_comprador')
    )
    create_notification(
        'Pedido terminado notificado',
        f"Hemos notificado a {comprador.get('desc_usuario').capitalize()} que su pedido está listo"
        f" {'para su retiro' if comprador.get('cod_retiro') == 'S' else 'y ya va en camino'}.",
        token_info.get('desc_usuario'),
        token_info.get('cod_usuario')
    )
    response.status_code = HTTP_200_OK
    conn.close()
    return {"mensaje": "estado documento cambiado a listo exitosamente"}


@router.put('/set_entregado')
async def cambio_estado_documento_entregado(response: Response, doc: DocumentoCod, Authorization: str = Header(None)):
    token = Authorization.split(" ")[1]
    token_info = validar_token(token, output=True)
    conn = PsqlConnection().conn
    conn.autocommit = True
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    # Se crean el seguimiento de los cambios de estado
    query = """INSERT INTO historial_estado_documento (desc_historial_estado_documento, user_id, cod_documento, 
                                                        cod_estado_documento, fecha_cambio_estado) 
                    VALUES (%s,%s,%s,%s,%s)"""
    cursor.execute(
        query,
        (
            "",
            token_info.get("desc_usuario"),
            doc.cod_documento,
            6,
            datetime.datetime.now()
        )
    )

    # Se Actualiza el estado del despacho
    query = """UPDATE despacho SET fecha_enviado = %s, cod_enviado = 'S' WHERE cod_documento = %s"""
    cursor.execute(
        query,
        (
            datetime.datetime.now(),
            doc.cod_documento
        )
    )

    # Se cambia el estado del documento
    query = """UPDATE documento SET cod_estado_documento = 6 WHERE cod_documento = %s"""
    cursor.execute(
        query,
        (
            doc.cod_documento,
        )
    )
    query = """SELECT cod_usuario_comprador, u.desc_usuario, d.cod_retiro FROM documento d
                    JOIN usuario u on d.cod_usuario_comprador = u.cod_usuario
                    WHERE cod_documento = %s"""
    cursor.execute(
        query,
        (
            doc.cod_documento,
        )
    )
    comprador = cursor.fetchone()

    # Se envían las notificaciones pertinentes
    create_notification(
        'Pedido Recibido',
        f"Estimada/o {comprador.get('desc_usuario').capitalize()}, su pedido a sido entregado"
        f" {'en local' if comprador.get('cod_retiro') == 'S' else 'a la dirección que indicó en la compra'}.",
        token_info.get('desc_usuario'),
        comprador.get('cod_usuario_comprador')
    )
    create_notification(
        'Pedido entregado notificado',
        f"Hemos notificado a {comprador.get('desc_usuario').capitalize()} que su pedido fue"
        f" {'entregado en local' if comprador.get('cod_retiro') == 'S' else 'entregado en domicilio'}.",
        token_info.get('desc_usuario'),
        token_info.get('cod_usuario')
    )
    response.status_code = HTTP_200_OK
    conn.close()
    return {"mensaje": "estado documento cambiado a entregado exitosamente"}


@router.put('/set_evaluado')
async def cambio_estado_documento_evaluado(response: Response, doc: DocumentoCod, Authorization: str = Header(None)):
    token = Authorization.split(" ")[1]
    token_info = validar_token(token, output=True)
    conn = PsqlConnection().conn
    conn.autocommit = True
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    # Se crean el seguimiento de los cambios de estado
    query = """INSERT INTO historial_estado_documento (desc_historial_estado_documento, user_id, cod_documento, 
                                                        cod_estado_documento, fecha_cambio_estado) 
                    VALUES (%s,%s,%s,%s,%s)"""
    cursor.execute(
        query,
        (
            "",
            token_info.get("desc_usuario"),
            doc.cod_documento,
            7,
            datetime.datetime.now()
        )
    )

    # Se cambia el estado del documento
    query = """UPDATE documento SET cod_estado_documento = 7 WHERE cod_documento = %s"""
    cursor.execute(
        query,
        (
            doc.cod_documento,
        )
    )
    query = """SELECT cod_usuario_vendedor, u.desc_usuario, d.cod_retiro 
                    FROM documento d
                    JOIN usuario u on d.cod_usuario_vendedor = u.cod_usuario
                    WHERE cod_documento = %s"""
    cursor.execute(
        query,
        (
            doc.cod_documento,
        )
    )
    vendedor = cursor.fetchone()

    # Se envían las notificaciones pertinentes
    create_notification(
        'Evaluación Emitida',
        f"{token_info.get('desc_usuario').capitalize()}, muchas gracias por su opinión, es muy importante para nosotros.",
        token_info.get('desc_usuario'),
        token_info.get('cod_usuario')
    )
    create_notification(
        'Evaluación Recibida',
        f"{vendedor.get('desc_usuario').capitalize()}, su cliente {token_info.get('desc_usuario').capitalize()} ha evaluado su servicio. Ya puede revisar su comentario.",
        token_info.get('desc_usuario'),
        vendedor.get('cod_usuario_vendedor')
    )
    response.status_code = HTTP_200_OK
    conn.close()
    return {"mensaje": "estado documento cambiado a evaluado exitosamente"}


@router.post('/get_detalle_documento_vendedor', response_model=DocumentosByEstVEndedor)
async def get_detalle_documento_vendedor(response: Response, documento: DocumentoCod):
    conn = PsqlConnection().conn
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = """SELECT d.*, coalesce(de.path_imagen_comprobante, '') path_imagen_despacho,
                        Max(dd.fecha_agenda) as fecha_agenda,
                       To_json(uc)                 comprador,
                       Json_agg(dd)                detalles
                FROM   documento d
                       join usuario uc
                         ON d.cod_usuario_comprador = uc.cod_usuario
                       LEFT JOIN despacho de ON d.cod_documento = de.cod_documento  
                       join (SELECT *
                             FROM   detalle_documento dd1
                                    join item_servicio it
                                      ON dd1.cod_item_servicio = it.cod_item_servicio
                                    join unidad u
                                      ON it.cod_unidad = u.cod_unidad) AS dd
                         ON dd.cod_documento = d.cod_documento
                WHERE  d.cod_documento = %s
                GROUP  BY d.cod_documento,
                          uc.cod_usuario, de.path_imagen_comprobante"""
    cursor.execute(
        query,
        (
            documento.cod_documento,
        )
    )
    document = cursor.fetchone()
    document['direccion'] = {}
    cod_direccion = document.get('cod_direccion_usuario_comprador')
    if cod_direccion:
        query = """SELECT du.cod_direccion_usuario, du.desc_direccion_usuario,
                            du.cod_comuna, c.desc_comuna, du.cod_activa
                    FROM direccion_usuario du
                    JOIN comuna c on du.cod_comuna = c.cod_comuna 
                    WHERE cod_direccion_usuario = %s"""
        cursor.execute(
            query,
            (
                cod_direccion,
            )
        )
        document['direccion'] = cursor.fetchone()
    response.status_code = HTTP_200_OK
    conn.close()
    print(document)
    return document


@router.get('/get_documentos_estados_vendedor', response_model=List[BasicDoc])
async def get_documento_detalle_vendedor(response: Response, Authorization: str = Header(None)):
    token = Authorization.split(" ")[1]
    token_info = validar_token(token, output=True)
    conn = PsqlConnection().conn
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = """SELECT d.cod_documento,
                       desc_documento,
                       cod_usuario_vendedor,
                       cod_usuario_comprador,
                       monto_documento,
                       fecha_documento,
                       Max(dd.fecha_agenda) as fecha_agenda,
                       cod_estado_documento,
                       cod_retiro,
                       cod_domicilio,
                       Coalesce(cod_direccion_usuario_comprador, 0) AS 
                       cod_direccion_usuario_comprador
                FROM   documento d
                       join detalle_documento dd
                         ON d.cod_documento = dd.cod_documento
                WHERE  d.cod_usuario_vendedor = %s
                       AND d.cod_estado_documento IN ( 2, 3, 4, 5, 6, 7 )
                GROUP  BY d.cod_documento """

    cursor.execute(
        query,
        (
            token_info.get("cod_usuario"),
        )
    )
    docuemtos = cursor.fetchall()
    conn.close()
    response.status_code = HTTP_200_OK
    return docuemtos


@router.post('/get_detalle_documento_comprador', response_model=DocumentosByEstComprador)
async def get_detalle_documento_comprador(response: Response, documento: DocumentoCod):
    conn = PsqlConnection().conn
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = """SELECT d.*, coalesce(de.path_imagen_comprobante, '') path_imagen_despacho,
                       To_json(uv)                 vendedor,
                       Max(dd.fecha_agenda) as fecha_agenda,
                       Json_agg(dd)                detalles
                FROM   documento d
                       join usuario uv
                         ON d.cod_usuario_vendedor = uv.cod_usuario
                       LEFT JOIN despacho de ON d.cod_documento = de.cod_documento 
                       join (SELECT *
                             FROM   detalle_documento dd1
                                    join item_servicio it
                                      ON dd1.cod_item_servicio = it.cod_item_servicio
                                    join unidad u
                                      ON it.cod_unidad = u.cod_unidad) AS dd
                         ON dd.cod_documento = d.cod_documento
                WHERE  d.cod_documento = %s
                GROUP  BY d.cod_documento,
                          uv.cod_usuario, de.path_imagen_comprobante"""
    cursor.execute(
        query,
        (
            documento.cod_documento,
        )
    )
    document = cursor.fetchone()

    # document["direccion"] = {}

    if document.get("cod_retiro") == "S":
        cod_servicio = document.get('detalles')[0].get('cod_servicio')

        query = """SELECT direccion, desc_domicilio, desc_comuna FROM servicio s
                    join usuario u on s.cod_usuario = u.cod_usuario
                    join comuna c on u.cod_comuna = c.cod_comuna
                    WHERE s.cod_servicio = %s"""

        cursor.execute(
            query,
            (
                cod_servicio,
            )
        )

        direccion_servicio = cursor.fetchone()

        document['direccion'] = direccion_servicio

    response.status_code = HTTP_200_OK
    conn.close()
    return document


@router.get('/get_documentos_estados_comprador', response_model=List[BasicDoc])
async def get_documento_detalle_comprador(response: Response, Authorization: str = Header(None)):
    token = Authorization.split(" ")[1]
    token_info = validar_token(token, output=True)
    conn = PsqlConnection().conn
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = """SELECT cod_documento,
                       desc_documento,
                       cod_usuario_vendedor,
                       cod_usuario_comprador,
                       monto_documento,
                       fecha_documento,
                       Max(dd.fecha_agenda) as fecha_agenda,
                       cod_estado_documento,
                       cod_retiro,
                       cod_domicilio,
                       Coalesce(cod_direccion_usuario_comprador, 0) AS
                       cod_direccion_usuario_comprador
                FROM   documento d
                       join detalle_documento dd USING(cod_documento)
                WHERE  d.cod_usuario_comprador = %s
                       AND d.cod_estado_documento IN ( 2, 3, 4, 5, 6, 7 )
                GROUP  BY d.cod_documento """
    cursor.execute(
        query,
        (
            token_info.get("cod_usuario"),
        )
    )
    docuemtos = cursor.fetchall()
    conn.close()
    response.status_code = HTTP_200_OK
    return docuemtos
