import base64
import os
import tempfile
from typing import List
import weasyprint

from dev_tools.formats import CLP_format
from models.backOffice_models.devoluciones import DocumentoDetalle
from models.backOffice_models.documentos_model import DocumentoPDF
from models.backOffice_models.liquidaciones_model import LiquidacionPDF


def pdf_documento(documento: DocumentoDetalle) -> str:
    # Carga el contenido de la imagen en base64
    with open('./temporales_desarrollo/imagenes/default.jpeg', 'rb') as image_file:
        image_data = base64.b64encode(image_file.read()).decode('utf-8')
    detalle = ""
    for det in documento.detalles:
        detalle += f"""<tr style="height: 18.4px;">
                            <td style="width: 19.9594%; text-align: center; vertical-align: middle; height: 18.4px;"><span style="">{det.desc_item_servicio}</span></td>
                            <td style="width: 19.9594%; text-align: center; vertical-align: middle; height: 18.4px;"><span style="">{det.cantidad}</span></td>
                            <td style="width: 19.9594%; text-align: center; vertical-align: middle; height: 18.4px;"><span style="">{det.desc_unidad}</span></td>
                            <td style="width: 19.9594%; text-align: center; vertical-align: middle; height: 18.4px;"><span style="">{'{:,.0f}'.format(det.valor_unidad).replace(',', '.')}</span></td>
                            <td style="width: 20.044%; text-align: center; vertical-align: middle; height: 18.4px;"><span style="">{'{:,.0f}'.format(det.subtotal).replace(',', '.')}</span></td>
                        </tr>"""
    html_body = f"""
            <html lang="es">
            <head>
                <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
                <style>
                        body {{
                            position: relative;
                        }}
                        body::before {{
                            content: "";
                            position: absolute;
                            top: 0;
                            left: 0;
                            right: 0;
                            bottom: 0;
                            background-image: url("data:image/jpeg;base64,{image_data}");
                            background-size: 98% 70%;
                            background-position: center center;
                            background-repeat: no-repeat;
                            opacity: 0.05;
                            z-index: -1;
                        }}
                        .container {{
                            text-align: center;
                        }}
                        .header-container {{
                            text-align: center;
                        }}
                        h2 {{
                            letter-spacing: 3px;
                        }}
                        table {{
                            width: 100%;
                            border-collapse: collapse;
                            border: 1px solid;
                        }}
                        td, th {{
                            border: 1px solid;
                            padding: 10px;
                            font-size: 14px;
                        }}
                        footer {{
                            padding: 10px;
                            text-align: left;
                        }}
                    </style>
            </head>
            <body>
                <div class="header-container">
                    <table>
                    <tbody>
                        <tr>
                            <td style="width: 20%; border: none;">
                            </td>
                            <td style="width: 60%; border: none;">
                                <h1 style="text-align: center;">
                                    <span>DOCUMENTO N&deg; {documento.cod_documento}</span>
                                </h1>
                            </td>
                            <td style="width: 20%; border: none;">
                                <div style="text-align: center; line-height: 2;">
                                    &nbsp;<span>Fecha Emisi&oacute;n</span>
                                </div>
                                <div style="text-align: center;"><span >{documento.fecha_documento}</span></div>
                            </td>
                        </tr>
                    </tbody>
                </table>
                </div>
                <div class="container">
                    <h2>Datos Comprador</h2>
                    <table style="border-collapse: collapse; width: 100%; margin-left: auto; margin-right: auto;">
                        <tbody>
                            <tr>
                                <td style="width: 24.9657%; text-align: center; vertical-align: middle;"><span>Nombre Completo</span></td>
                                <td style="width: 27.1963%; text-align: center; vertical-align: middle;"><span>Email</span></td>
                                <td style="width: 16.7296%; text-align: center; vertical-align: middle;"><span>Comuna</span></td>
                                <td style="text-align: center; vertical-align: middle; width: 31.057%;"><span>Direcci&oacute;n</span></td>
                            </tr>
                            <tr>
                                <td style="width: 24.9657%; text-align: center; vertical-align: middle;">
                                    <span>{" ".join([documento.comprador.nombre_usuario, documento.comprador.apellido1_usuario])}</span>
                                </td>
                                <td style="width: 27.1963%; text-align: center; vertical-align: middle;"><span>{documento.comprador.mail_usuario}</span></td>
                                <td style="width: 16.7296%; text-align: center; vertical-align: middle; padding: 5px;"><span>{documento.comprador.desc_comuna}</span></td>
                                <td style="text-align: center; vertical-align: middle; width: 31.057%; padding: 5px;"><span>{documento.desc_direccion_usuario}</span></td>
                            </tr>
                        </tbody>
                    </table>
                </div>
                <div class="container">
                    <h2>Datos Vendedor</h2>
                    <table style="border-collapse: collapse; width: 100%; margin-left: auto; margin-right: auto;" border="1" cellpadding="5px">
                    <tbody>
                        <tr>
                            <td style="width: 24.9785%; text-align: center;"><span>Nombre del Negocio</span></td>
                            <td style="width: 27.2278%; text-align: center;"><span>Email</span></td>
                            <td style="text-align: center; width: 16.7039%;">
                                <div><span>Comuna</span></div>
                            </td>
                            <td style="text-align: center; width: 31.0586%;"><span>Direcci&oacute;n</span></td>
                        </tr>
                        <tr>
                            <td style="width: 24.9785%; text-align: center;"><span>{documento.detalles[0].nom_servicio}</span></td>
                            <td style="width: 27.2278%; text-align: center;"><span>{documento.vendedor.mail_usuario}</span></td>
                            <td style="text-align: center; width: 16.7039%;"><span>{documento.vendedor.desc_comuna}</span></td>
                            <td style="text-align: center; width: 31.0586%;"><span>{documento.detalles[0].direccion}</span></td>
                        </tr>
                    </tbody>
                </table>
                </div>
                <div class="container">
                    <h2>Datos Generales</h2>
                    <table style="border-collapse: collapse; width: 100%; margin: 0 auto; padding: 5px;">
                    <tbody>
                        <tr>
                            <td style="width: 24.7506%; padding: 5px; text-align: center;">
                                <div style="text-align: center;"><span>&nbsp;Fecha Agenda</span></div>
                            </td>
                            <td style="width: 24.7506%; padding: 5px; text-align: center;"><span>Tipo Venta&nbsp;</span></td>
                            <td style="width: 24.7506%; padding: 5px; text-align: center;"><span>&nbsp;Estado</span></td>
                            <td style="width: 24.7506%; padding: 5px; text-align: center;">
                                <div style="text-align: center;"><span>&nbsp;<span>Monto Total</span></span></div>
                            </td>
                        </tr>
                        <tr>
                            <td style="width: 24.7506%; padding: 5px; text-align: center;"><span>{documento.detalles[0].fecha_agenda}</span></td>
                            <td style="width: 24.7506%; padding: 5px; text-align: center;"><span>{"Retiro en Tienda" if documento.cod_retiro == "S" else "Delivery"}</span></td>
                            <td style="width: 24.7506%; padding: 5px; text-align: center;">
                                <span>{documento.desc_estado_documento}</span>
                            </td>
                            <td style="width: 24.7506%; padding: 5px; text-align: center;"><span>{'{:,.0f}'.format(documento.monto_documento).replace(',', '.')}</span></td>
                        </tr>
                    </tbody>
                </table>
                </div>
                <div class="container">
                    <h2>Detalle de Compra</h2>
                    <table style="border-collapse: collapse; width: 99.9831%; border-color: #000000; border-style: none; height: 57.6px;">
                    <tbody>
                        <tr style="height: 21px;">
                            <td style="width: 19.9594%; text-align: center; vertical-align: middle; height: 21px;"><span>Item</span></td>
                            <td style="width: 19.9594%; text-align: center; vertical-align: middle; height: 21px;"><span>Cantidad</span></td>
                            <td style="width: 19.9594%; text-align: center; vertical-align: middle; height: 21px;"><span>Unidad</span></td>
                            <td style="width: 19.9594%; text-align: center; vertical-align: middle; height: 21px;"><span>Precio Unitario</span></td>
                            <td style="width: 20.044%; text-align: center; vertical-align: middle; height: 21px;"><span>Subtotal</span></td>
                        </tr>
                        {detalle}
                    </tbody>
                    <tfoot>
                        <tr>
                            <td colspan="4" style="text-align: center;"><span><strong>Total</strong></span></td>
                            <td>
                                <div style="text-align: center;"><span>{'{:,.0f}'.format(documento.monto_documento).replace(',', '.')}</span></div>
                            </td>
                        </tr>
                    </tfoot>
                </table>
                </div>
            </body>
            <footer>
                <p>&copy; 2023 Mas Cincuenta&trade;. Todos los derechos reservados.</p>
            </footer>
            </html>
            """
    temp_html_file = tempfile.NamedTemporaryFile(suffix=".html").name
    with open(temp_html_file, 'w') as archivo:
        archivo.write(html_body)
        archivo.close()

    with open(temp_html_file, 'r') as html_file:
        html_content = html_file.read()
        html_file.close()

    temp_pdf_file = tempfile.NamedTemporaryFile(suffix=".pdf").name
    weasyprint.HTML(string=html_content).write_pdf(temp_pdf_file)

    os.remove(temp_html_file)

    return temp_pdf_file


def pdf_cartola_prestador(documentos: List[DocumentoPDF]) -> str:
    # Carga el contenido de la imagen en base64
    with open('./temporales_desarrollo/imagenes/default.jpeg', 'rb') as image_file:
        image_data = base64.b64encode(image_file.read()).decode('utf-8')
    detalle = ""
    total_monto = 0
    total_sin_com = 0
    total_com = 0
    for doc in documentos:
        detalle += f"""<tr style="height: 18.4px;">
                            <td style="width: 8%; text-align: center; vertical-align: middle; height: 18.4px;"><span style="">{doc.cod_documento}</span></td>
                            <td style="width: 18.4%; text-align: center; vertical-align: middle; height: 18.4px;"><span style="">{doc.fecha_documento}</span></td>
                            <td style="width: 18.4%; text-align: center; vertical-align: middle; height: 18.4px;"><span style="">{doc.desc_estado_documento}</span></td>
                            <td style="width: 18.4%; text-align: center; vertical-align: middle; height: 18.4px;"><span style="">{doc.monto_documento}</span></td>
                            <td style="width: 18.4%; text-align: center; vertical-align: middle; height: 18.4px;"><span style="">{doc.monto_venta}</span></td>
                            <td style="width: 18.4%; text-align: center; vertical-align: middle; height: 18.4px;"><span style="">{doc.monto_comision_bruto}</span></td>
                        </tr>"""
        total_monto += float(doc.monto_documento.replace(".", ""))
        total_sin_com += float(doc.monto_venta.replace(".", ""))
        total_com += float(doc.monto_comision_bruto.replace(".", ""))
    html_body = f"""
            <html lang="es">
            <head>
                <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
                <style>
                        body {{
                            position: relative;
                        }}
                        body::before {{
                            content: "";
                            position: absolute;
                            top: 0;
                            left: 0;
                            right: 0;
                            bottom: 0;
                            background-image: url("data:image/jpeg;base64,{image_data}");
                            background-size: 98% 70%;
                            background-position: center center;
                            background-repeat: no-repeat;
                            opacity: 0.05;
                            z-index: -1;
                        }}
                        .container {{
                            text-align: center;
                        }}
                        .header-container {{
                            text-align: center;
                        }}
                        h2 {{
                            letter-spacing: 3px;
                        }}
                        table {{
                            width: 100%;
                            border-collapse: collapse;
                            border: 1px solid;
                        }}
                        td, th {{
                            border: 1px solid;
                            padding: 10px;
                            font-size: 14px;
                        }}
                        footer {{
                            padding: 10px;
                            text-align: left;
                        }}
                    </style>
            </head>
            <body>
                <div class="header-container">
                    <table>
                        <tbody>
                            <tr>
                                <td style="width: 5%; border: none;">
                                </td>
                                <td style="width: 90%; border: none;">
                                    <h1 style="text-align: center;">
                                        <span>CARTOLA {documentos[0].fecha_documento + ' a ' + documentos[-1].fecha_documento}</span>
                                    </h1>
                                </td>
                                <td style="width: 5%; border: none;">
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
                <div class="container">
                    <h2>Datos Vendedor</h2>
                    <table style="border-collapse: collapse; width: 100%; margin-left: auto; margin-right: auto;" border="1" cellpadding="5px">
                    <tbody>
                        <tr>
                            <td style="width: 24.9785%; text-align: center;"><span>Nombre Vendedor</span></td>
                            <td style="text-align: center; width: 31.0586%;"><span>Rut</span></td>
                            <td style="width: 27.2278%; text-align: center;"><span>Email</span></td>
                            <td style="text-align: center; width: 16.7039%;">
                                <div><span>Comuna</span></div>
                            </td>
                        </tr>
                        <tr>
                            <td style="width: 24.9785%; text-align: center;"><span>{documentos[0].vendedor.nombre_usuario}</span></td>
                            <td style="text-align: center; width: 31.0586%;"><span>{documentos[0].vendedor.rut_usuario}</span></td>
                            <td style="width: 27.2278%; text-align: center;"><span>{documentos[0].vendedor.mail_usuario}</span></td>
                            <td style="text-align: center; width: 16.7039%;"><span>{documentos[0].vendedor.desc_comuna}</span></td>
                        </tr>
                    </tbody>
                </table>
                </div>
                <div class="container">
                    <h2>Documentos</h2>
                    <table style="border-collapse: collapse; width: 99.9831%; border-color: #000000; border-style: none; height: 57.6px;">
                    <tbody>
                        <tr style="height: 21px;">
                            <td style="text-align: center; width: 8%;"><span>Cod</span></td>
                            <td style="text-align: center; width: 18.4%;"><span>Fecha</span></td>
                            <td style="text-align: center; width: 18.4%;"><span>Estado</span></td>
                            <td style="text-align: center; width: 18.4%;"><span>Monto c/Comisión</span></td>
                            <td style="text-align: center; width: 18.4%;"><span>Monto s/Comisión</span></td>
                            <td style="text-align: center; width: 18.4%;"><span>Monto Comisión</span></td>
                        </tr>
                        {detalle}
                    </tbody>
                    <tfoot>
                        <tr>
                            <td colspan="3" style="text-align: center;"><span><strong>Total</strong></span></td>
                            <td>
                                <div style="text-align: center;"><span>{CLP_format(total_monto)}</span></div>
                            </td>
                            <td>
                                <div style="text-align: center;"><span>{CLP_format(total_sin_com)}</span></div>
                            </td>
                            <td>
                                <div style="text-align: center;"><span>{CLP_format(total_com)}</span></div>
                            </td>
                        </tr>
                    </tfoot>
                </table>
                </div>
            </body>
            <footer>
                <p>&copy; 2023 Mas Cincuenta&trade;. Todos los derechos reservados.</p>
            </footer>
            </html>
            """
    temp_html_file = tempfile.NamedTemporaryFile(suffix=".html").name
    with open(temp_html_file, 'w') as archivo:
        archivo.write(html_body)
        archivo.close()

    with open(temp_html_file, 'r') as html_file:
        html_content = html_file.read()
        html_file.close()

    temp_pdf_file = tempfile.NamedTemporaryFile(suffix=".pdf").name
    weasyprint.HTML(string=html_content).write_pdf(temp_pdf_file)

    os.remove(temp_html_file)

    return temp_pdf_file


def pdf_liquidacion(liquidacion: LiquidacionPDF) -> str:
    # Carga el contenido de la imagen en base64
    with open('./temporales_desarrollo/imagenes/default.jpeg', 'rb') as image_file:
        image_data = base64.b64encode(image_file.read()).decode('utf-8')
    detail = ""
    for detalle in liquidacion.detalles:
        detail += f"""<tr style="height: 19px;">
                            <td style="text-align: center; vertical-align: middle;"><span>{detalle.cod_documento}</span></td>
                            <td style="text-align: center; vertical-align: middle;"><span>{CLP_format(detalle.monto_documento)}</span></td>
                        </tr>"""
    html_body = f"""
            <html lang="es">
            <head>
                <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
                <style>
                        body {{
                            position: relative;
                        }}
                        body::before {{
                            content: "";
                            position: absolute;
                            top: 0;
                            left: 0;
                            right: 0;
                            bottom: 0;
                            background-image: url("data:image/jpeg;base64,{image_data}");
                            background-size: 98% 70%;
                            background-position: center center;
                            background-repeat: no-repeat;
                            opacity: 0.05;
                            z-index: -1;
                        }}
                        .container {{
                            text-align: center;
                        }}
                        .header-container {{
                            text-align: center;
                        }}
                        h2 {{
                            letter-spacing: 3px;
                        }}
                        table {{
                            width: 100%;
                            border-collapse: collapse;
                            border: 1px solid;
                        }}
                        td, th {{
                            border: 1px solid;
                            padding: 10px;
                            font-size: 14px;
                        }}
                        footer {{
                            padding: 10px;
                            text-align: left;
                        }}
                    </style>
            </head>
            <body>
                <div class="header-container">
                    <table>
                        <tbody>
                            <tr>
                                <td style="width: 5%; border: none;">
                                </td>
                                <td style="width: 90%; border: none;">
                                    <h1 style="text-align: center;">
                                        <span>LIQUIDACIÓN N&deg; {liquidacion.cod_liquidacion}</span>
                                    </h1>
                                </td>
                                <td style="width: 5%; border: none;">
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
                <div class="container">
                    <h2>Datos Vendedor</h2>
                    <table style="border-collapse: collapse; width: 100%; margin-left: auto; margin-right: auto;" border="1" cellpadding="5px">
                    <tbody>
                        <tr>
                            <td style="width: 24.9785%; text-align: center;"><span>Nombre Vendedor</span></td>
                            <td style="text-align: center; width: 31.0586%;"><span>Rut</span></td>
                            <td style="width: 27.2278%; text-align: center;"><span>Email</span></td>
                            <td style="text-align: center; width: 16.7039%;">
                                <div><span>Comuna</span></div>
                            </td>
                        </tr>
                        <tr>
                            <td style="width: 24.9785%; text-align: center;"><span>{liquidacion.nombre_usuario}</span></td>
                            <td style="text-align: center; width: 31.0586%;"><span>{liquidacion.rut_usuario}</span></td>
                            <td style="width: 27.2278%; text-align: center;"><span>{liquidacion.mail_usuario}</span></td>
                            <td style="text-align: center; width: 16.7039%;"><span>{liquidacion.desc_comuna}</span></td>
                        </tr>
                    </tbody>
                </table>
                </div>
                <div class="container">
                    <h2>Datos Generales</h2>
                    <table style="border-collapse: collapse; width: 100%; margin: 0 auto; padding: 5px;">
                    <tbody>
                        <tr>
                            <td style="width: 24.7506%; padding: 5px; text-align: center;">
                                <div style="text-align: center;"><span>Fecha</span></div>
                            </td>
                            <td style="width: 24.7506%; padding: 5px; text-align: center;"><span>Monto Venta</span></td>
                            <td style="width: 24.7506%; padding: 5px; text-align: center;"><span>Monto Liquidación</span></td>
                            <td style="width: 24.7506%; padding: 5px; text-align: center;">
                                <div style="text-align: center;"><span>&nbsp;<span>Observación</span></span></div>
                            </td>
                        </tr>
                        <tr>
                            <td style="width: 24.7506%; padding: 5px; text-align: center;"><span>{liquidacion.fecha_liquidacion}</span></td>
                            <td style="width: 24.7506%; padding: 5px; text-align: center;"><span>{CLP_format(liquidacion.monto_venta)}</span></td>
                            <td style="width: 24.7506%; padding: 5px; text-align: center;">
                                <span>{CLP_format(liquidacion.monto_liquidacion)}</span>
                            </td>
                            <td style="width: 24.7506%; padding: 5px; text-align: center;"><span>{liquidacion.desc_liquidacion}</span></td>
                        </tr>
                    </tbody>
                </table>
                </div>
                <div class="container">
                    <h2>Detalles</h2>
                    <table style="border-collapse: collapse; width: 99.9831%; border-color: #000000; border-style: none; height: 57.6px;">
                    <tbody>
                        <tr style="height: 21px;">
                            <td style="text-align: center; width: 50%;"><span>Cod Documento</span></td>
                            <td style="text-align: center; width: 50%;"><span>Monto Documento</span></td>
                        </tr>
                        {detail}
                    </tbody>
                </table>
                </div>
            </body>
            <footer>
                <p>&copy; 2023 Mas Cincuenta&trade;. Todos los derechos reservados.</p>
            </footer>
            </html>
            """
    temp_html_file = tempfile.NamedTemporaryFile(suffix=".html").name
    with open(temp_html_file, 'w') as archivo:
        archivo.write(html_body)
        archivo.close()

    with open(temp_html_file, 'r') as html_file:
        html_content = html_file.read()
        html_file.close()

    temp_pdf_file = tempfile.NamedTemporaryFile(suffix=".pdf").name
    weasyprint.HTML(string=html_content).write_pdf(temp_pdf_file)

    os.remove(temp_html_file)

    return temp_pdf_file
