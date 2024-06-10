import os
from datetime import datetime
from fastapi import APIRouter, Response, UploadFile, File, Form, Header
from psycopg2.extras import RealDictCursor
import uuid
from starlette.status import *
from bd_con.conexion import PsqlConnection
from dev_tools.json_web_token import validar_token
from middlewares.verifica_ruta_token import VerificaRutaToken
from PIL import Image
from io import BytesIO

router = APIRouter(
    route_class=VerificaRutaToken,
)


@router.post("/save")
async def save_image(response: Response, img: UploadFile = File(), cod_servicio: int = Form(None), cod_documento: int = Form(None), Authorization: str = Header(None)):
    token = Authorization.split(" ")[1]
    token_info = validar_token(token, output=True)
    conn = PsqlConnection().conn
    conn.autocommit = True
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    img_uuid = uuid.uuid4()

    formato = "png"
    file = await img.read()

    image = Image.open(BytesIO(file))
    image = image.resize((image.width // 2, image.height // 2))

    if os.name == 'nt':
        image.save(os.path.join("temporales_desarrollo", "imagenes", f"{img_uuid}.{formato}"), "PNG")
    else:
        image.save(os.path.join("/app", "temporales_desarrollo", "imagenes", f"{img_uuid}.{formato}"), "PNG")

    if cod_servicio:
        query = """UPDATE servicio SET path_imagen = %s, user_id = %s WHERE cod_servicio = %s"""
        cursor.execute(
            query,
            (
                f"{img_uuid}.{formato}",
                token_info.get("desc_usuario"),
                cod_servicio,
            )
        )
    elif cod_documento:
        query = """UPDATE despacho SET path_imagen_comprobante = %s, user_id = %s WHERE cod_documento = %s"""
        cursor.execute(
            query,
            (
                f"{img_uuid}.{formato}",
                token_info.get("desc_usuario"),
                cod_documento
            )
        )
    else:
        query = """UPDATE usuario set path_imagen = %s, user_id = %s WHERE cod_usuario = %s"""
        cursor.execute(
            query,
            (
                f"{img_uuid}.{formato}",
                token_info.get("desc_usuario"),
                token_info.get("cod_usuario"),
            )
        )
    response.status_code = HTTP_201_CREATED
    return {"mensaje": f"Imagen guardada exitosamente"}


@router.put("/update")
async def update_image(response: Response, img: UploadFile = File(), path: str = Form(...)):
    file = await img.read()
    if os.name == 'nt':
        file_path = os.path.join("temporales_desarrollo", "imagenes")
    else:
        file_path = os.path.join("/app", "temporales_desarrollo", "imagenes")

    # Elimino la imagen existente
    if os.path.exists(os.path.join(file_path, path)):
        os.remove(os.path.join(file_path, path))

    image = Image.open(BytesIO(file))
    image = image.resize((image.width // 2, image.height // 2))
    image.save(os.path.join(file_path, path), "PNG")

    response.status_code = HTTP_200_OK
    return {"mensaje": f"Imagen actualizada exitosamente"}
