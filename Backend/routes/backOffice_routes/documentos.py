import datetime
import os
from asyncio import sleep
from typing import List
from fastapi import APIRouter, Response, Request, Header, BackgroundTasks
from psycopg2.extras import RealDictCursor
from fastapi.responses import FileResponse
from starlette.status import *
from bd_con.conexion import PsqlConnection
from dev_tools.json_web_token import validar_token
from dev_tools.notifications.app_notification import create_notification
from dev_tools.pdf_generator import pdf_documento
from middlewares.verifica_ruta_token import VerificaRutaToken
from models.app_models.documento_model import DocumentoCod
from models.backOffice_models.devoluciones import DocCod, DocumentoDetalle
from models.backOffice_models.documentos_model import DocumentoSimple, Filtro

router = APIRouter(
    # route_class=VerificaRutaToken
)


@router.post("/all", response_model=List[DocumentoSimple])
async def get_all_documentos(response: Response, filtro: Filtro):
    conn = PsqlConnection().conn
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = f"""SELECT d.*, ed.desc_estado_documento,
                        vendedor.cod_usuario cod_vendedor,
                        vendedor.nombre_usuario nombre_vendedor,
                        comprador.cod_usuario cod_comprador,
                        comprador.nombre_usuario nombre_comprador
                FROM   documento d
                        join usuario vendedor on d.cod_usuario_vendedor = vendedor.cod_usuario
                        join usuario comprador on d.cod_usuario_comprador = comprador.cod_usuario
                        join estado_documento ed using(cod_estado_documento)
                       left join devolucion d2 USING(cod_documento)
                WHERE to_char(fecha_documento, 'YYYY-MM') = %s and cod_estado_documento > 1
                GROUP  BY d.cod_documento, vendedor.cod_usuario, comprador.cod_usuario, ed.desc_estado_documento
                ORDER BY d.cod_documento desc """

    cursor.execute(
        query,
        (
            filtro.mes,
        )
    )
    documentos = cursor.fetchall()
    for documento in documentos:
        if documento.get("devoluciones"):
            documento["devolucion"] = "S"
        else:
            documento["devolucion"] = "N"
    conn.close()
    response.status_code = HTTP_200_OK
    return documentos


@router.post("/by_cod_doc", response_model=DocumentoDetalle)
async def get_detalle_documento(response: Response, documento: DocCod):
    conn = PsqlConnection().conn
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = """SELECT d.*, ed.desc_estado_documento,
                       du.desc_direccion_usuario,
                       To_json(vendedor)                  vendedor,
                       To_json(comprador)                 comprador,
                        COALESCE(json_agg(d2) FILTER (WHERE d2.cod_devolucion IS NOT NULL), '[]') devoluciones,
                        COALESCE(json_agg(e) FILTER (WHERE e.cod_evaluacion IS NOT NULL), '[]') evaluaciones,
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
                       left JOIN devolucion d2 on d.cod_documento = d2.cod_documento
                       left join evaluacion e on d.cod_documento = e.cod_documento
                       join estado_documento ed on d.cod_estado_documento = ed.cod_estado_documento
                       JOIN detalle_documento dd on d.cod_documento = dd.cod_documento
                       JOIN item_servicio is2 using(cod_item_servicio)
                       JOIN unidad un on is2.cod_unidad = un.cod_unidad
                       JOIN servicio s using(cod_servicio)
                       LEFT JOIN direccion_usuario du
                              ON d.cod_direccion_usuario_comprador = du.cod_direccion_usuario
                WHERE  d.cod_documento = %s
                GROUP  BY d.cod_documento,
                          du.desc_direccion_usuario,
                          vendedor.cod_usuario,
                          comprador.cod_usuario,
                          ed.desc_estado_documento"""
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


@router.post("/download-pdf")
async def download_pdf(response: Response, documento: DocCod, background_tasks: BackgroundTasks):
    conn = PsqlConnection().conn
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = """SELECT d.*, ed.desc_estado_documento,
                           du.desc_direccion_usuario,
                           To_json(vendedor)                  vendedor,
                           To_json(comprador)                 comprador,
                            COALESCE(json_agg(d2) FILTER (WHERE d2.cod_devolucion IS NOT NULL), '[]') devoluciones,
                            COALESCE(json_agg(e) FILTER (WHERE e.cod_evaluacion IS NOT NULL), '[]') evaluaciones,
                           Json_agg((SELECT det
                                     FROM   (SELECT dd.*,
                                                    is2.*,
                                                    un.desc_unidad,
                                                    s.*)det)) detalles
                    FROM   documento d
                           JOIN (SELECT comp.*, comuna.desc_comuna FROM usuario comp join comuna on comp.cod_comuna = comuna.cod_comuna) comprador
                             ON d.cod_usuario_comprador = comprador.cod_usuario
                           JOIN (SELECT vend.*, comuna.desc_comuna FROM usuario vend join comuna on vend.cod_comuna = comuna.cod_comuna) vendedor
                             ON d.cod_usuario_vendedor = vendedor.cod_usuario
                           left JOIN devolucion d2 on d.cod_documento = d2.cod_documento
                           left join evaluacion e on d.cod_documento = e.cod_documento
                           join estado_documento ed on d.cod_estado_documento = ed.cod_estado_documento
                           JOIN detalle_documento dd on d.cod_documento = dd.cod_documento
                           JOIN item_servicio is2 using(cod_item_servicio)
                           JOIN unidad un on is2.cod_unidad = un.cod_unidad
                           JOIN servicio s using(cod_servicio)
                           LEFT JOIN direccion_usuario du
                                  ON d.cod_direccion_usuario_comprador = du.cod_direccion_usuario
                    WHERE  d.cod_documento = %s
                    GROUP  BY d.cod_documento,
                              du.desc_direccion_usuario,
                              vendedor.*,
                              comprador.*,
                              ed.desc_estado_documento"""
    cursor.execute(
        query,
        (
            documento.cod_documento,
        )
    )
    documento_detalles = cursor.fetchone()
    conn.close()
    pdf_temp = pdf_documento(DocumentoDetalle(**documento_detalles))

    # Eliminar el archivo temporal después de enviar la respuesta
    async def eliminar_archivo_temporal():
        await sleep(1)
        os.remove(pdf_temp)
        print("------- PDF temporal removed -------")
    background_tasks.add_task(eliminar_archivo_temporal)

    return FileResponse(pdf_temp)


@router.get('/filtro_meses')
async def get_meses_con_movimientos(response: Response):
    conn = PsqlConnection().conn
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = """SELECT 
                    DISTINCT ( To_char(p.fecha_pago, 'YYYY-MM') ) mes,
                    (array['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre'])[to_char(p.fecha_pago,'mm')::int]||' '||to_char(p.fecha_pago,'yyyy') desc_mes
                FROM   pago p
                       JOIN documento d USING(cod_documento)
                       ORDER BY mes desc"""
    cursor.execute(
        query
    )
    meses_con_movimientos = cursor.fetchall()
    conn.close()
    response.status_code = HTTP_200_OK
    return meses_con_movimientos


@router.post('/mapa')
async def get_mapa_estados(response: Response, doc: DocCod):
    conn = PsqlConnection().conn
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = """SELECT ed.cod_historial_estado_documento,
                   ed.user_id,
                   to_char(ed.fecha_cambio_estado, 'HH:MI:SS DD-MM-YYYY') as fecha_cambio_estado,
                   ed.cod_estado_documento,
                   ed2.desc_estado_documento
            FROM   documento d
                   join historial_estado_documento ed USING(cod_documento)
                   join estado_documento ed2
                     ON ed.cod_estado_documento = ed2.cod_estado_documento
            WHERE  cod_documento = %s
                   AND d.cod_estado_documento > 1
            ORDER  BY cod_estado_documento ASC """
    cursor.execute(
        query,
        (
            doc.cod_documento,
        )
    )
    estados = cursor.fetchall()
    conn.close()
    response.status_code = HTTP_200_OK
    print(estados)
    return estados


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
            token_info.get("desc_personal"),
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
        token_info.get('desc_personal'),
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
            token_info.get("desc_personal"),
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
        token_info.get('desc_personal'),
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