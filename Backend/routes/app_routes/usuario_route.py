import os
import uuid
from PIL import Image
from io import BytesIO

from PIL.Image import Transpose
from fastapi import APIRouter, Response, Header, UploadFile, File, Form
from starlette.responses import JSONResponse
from starlette.status import *
from typing import List
from bd_con.conexion import PsqlConnection
from psycopg2.extras import RealDictCursor

from dev_tools.firebase.firebase_manage import delete_firebase_user
from dev_tools.json_web_token import validar_token
from middlewares.verifica_ruta_token import VerificaRutaToken
from models.app_models.byCod_model import IndentifierCod
from models.app_models.servicio_model import ServicioVerificador
from models.app_models.usuario_model import UsuarioGet, UsuarioUpdate, HorarioGet, Horario, HorarioUsuario

router = APIRouter(
    route_class=VerificaRutaToken
)


DATA_PATH_WIN = ".\\temporales_desarrollo\\imagenes\\"
DATA_PATH_LIN = "./temporales_desarrollo/imagenes/"


@router.get('/all', response_model=List[UsuarioGet])
async def get_allusuario(response: Response):
    conn = PsqlConnection().conn
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = """SELECT * FROM usuario"""
    cursor.execute(query, ())
    data = cursor.fetchall()
    response.status_code = HTTP_200_OK
    conn.close()
    return data


@router.post('/por_cod', response_model=UsuarioGet)
async def get_by_cod_usuario(response: Response, cod: IndentifierCod):
    conn = PsqlConnection().conn
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("""SELECT * FROM usuario where cod_usuario = %s""", (cod.cod,))
    usuario = cursor.fetchone()
    response.status_code = HTTP_200_OK
    return usuario


@router.put('/actualizar')
async def update_usuario(
        response: Response,
        usuario: UsuarioUpdate,
        Authorization: str = Header(None)
):
    token = Authorization.split(" ")[1]
    token_info = validar_token(token, output=True)
    usuario = usuario.dict(exclude_none=True)
    usuario['cod_usuario'] = token_info.get('cod_usuario')
    usuario['user_id'] = token_info.get('desc_usuario')
    conn = PsqlConnection().conn
    conn.autocommit = True
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute(
        """SELECT * FROM usuario WHERE cod_usuario = %s""",
        (usuario.get('cod_usuario'),)
    )
    usuario_existe = cursor.fetchone()
    if not usuario_existe:
        response.status_code = HTTP_206_PARTIAL_CONTENT
        # estado = "Prestador" if usuario.get('cod_es_prestador') == "S" else "Cliente"
        conn.close()
        return {"mensaje": f"usuario no registrado"}

    query = f"""UPDATE usuario set
            {','.join([f'{u}={"%s"}' for u in usuario.keys() if u != 'cod_usuario'])}"""
    query += " WHERE cod_usuario = %s"
    valores = []
    for i in usuario.keys():
        if i == "cod_es_prestador":
            valores.append(usuario.get(i).value)
        elif i != "cod_usuario":
            valores.append(usuario.get(i))
    valores.append(usuario.get('cod_usuario'))
    cursor.execute(
        query,
        valores
    )
    conn.close()
    response.status_code = HTTP_200_OK
    return {"mensaje": f"usuario cod: {usuario.get('cod_usuario')} actualizado exitosamente"}


@router.post('/subir-docs')
async def subir_docuemto(
        img: UploadFile = File(),
        cod_tipo_antecedente: int = Form(...),
        rut_usuario: str = Form(None),
        Authorization: str = Header(None)):
    # x = await req.form()
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
    image = image.transpose(Transpose.ROTATE_270)

    if os.name == 'nt':
        image.save(f"{DATA_PATH_WIN}{img_uuid}.{formato}", "PNG")
    else:
        image.save(f"{DATA_PATH_LIN}{img_uuid}.{formato}", "PNG")

    query = """INSERT INTO antecedente (desc_antecedente, cod_tipo_antecedente, cod_usuario, path_imagen, user_id) 
                VALUES (%s,%s,%s,%s,%s) returning cod_antecedente"""
    cursor.execute(
        query,
        (
            f'{cod_tipo_antecedente}_{token_info.get("apellido1_usuario")}_{token_info.get("nombre_usuario")}',
            cod_tipo_antecedente,
            token_info.get('cod_usuario'),
            f"{img_uuid}.{formato}",
            token_info.get("desc_usuario")
        )
    )
    cod_antecedente = cursor.fetchone().get('cod_antecedente')
    if rut_usuario:
        query = """UPDATE usuario SET rut_usuario = %s, user_id = %s WHERE cod_usuario = %s"""
        cursor.execute(
            query,
            (
                rut_usuario,
                token_info.get('desc_usuario'),
                token_info.get('cod_usuario')
            )
        )
    conn.close()
    return JSONResponse(
        content={"mensaje": f"antecendente creado con cod: {cod_antecedente} y guardado como {f'{img_uuid}.{formato}'} exitosamente"},
        status_code=HTTP_201_CREATED
    )


@router.post('/verificar_registro')
async def verificar_resgitro(response: Response, serv: ServicioVerificador):
    conn = PsqlConnection().conn
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = """select
                    cod_usuario,
                    desc_usuario,
                    u.cod_revisado,
                    case when COALESCE(json_agg(a) FILTER (WHERE a.cod_antecedente IS NOT NULL), '[]')::text = '[]' then false else true end antecedentes,
                    case when COALESCE(json_agg(s) FILTER (WHERE s.cod_servicio IS NOT NULL), '[]')::text = '[]' then false else true end servicios,
                    case when COALESCE(json_agg(cb) FILTER (WHERE cb.cod_cuenta_bancaria IS NOT NULL), '[]')::text = '[]' then false else true end cuentas_bancarias,
                    case when COALESCE(json_agg(hu) FILTER (WHERE hu.cod_horario_usuario IS NOT NULL), '[]')::text = '[]' then false else true end horarios_usuario
                from usuario u
                left join antecedente a using(cod_usuario)
                left join servicio s  using(cod_usuario)
                left join cuenta_bancaria cb using(cod_usuario)
                left join horario_usuario hu using(cod_usuario)
                where cod_usuario = %s
                group by 1, 2, 3"""
    cursor.execute(
        query,
        (serv.cod_usuario,)
    )
    resp = cursor.fetchone()
    response.status_code = HTTP_200_OK
    conn.close()
    return resp


@router.post("/registrar_horarios")
async def set_horario_usuario(
        response:  Response,
        horarios: List[Horario],
        Authorization: str = Header(None)

):
    conn = PsqlConnection().conn
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    conn.autocommit = True
    token = Authorization.split(" ")[1]
    token_info = validar_token(token, output=True)
    # Guardar los horarios del servicio
    for horario in horarios:
        query = """INSERT INTO horario_usuario (desc_horario_usuario, cod_usuario, desde, hasta, user_id) 
                        VALUES (%s,%s,%s,%s,%s) returning cod_horario_usuario"""
        cursor.execute(
            query,
            (
                "",
                token_info.get('cod_usuario'),
                horario.desde,
                horario.hasta,
                token_info.get('desc_usuario')
            )
        )
        cod_horario_usuario = cursor.fetchone().get('cod_horario_usuario')

        # Guardar los distintos horarios que podria tener un mismo dia
        for dia in horario.dias:
            query = """INSERT INTO dia_horario_usuario (desc_dia_horario_usuario, cod_dia, cod_horario_usuario, user_id) 
                            VALUES (%s,%s,%s,%s)"""
            cursor.execute(
                query,
                (
                    "",
                    dia.cod_dia,
                    cod_horario_usuario,
                    token_info.get('desc_usuario')
                )
            )
        response.status_code = HTTP_201_CREATED
        return {"mensaje": "horarios creados exitosamente"}


@router.get("/get_horarios", response_model=List[HorarioGet])
async def get_horarios(response: Response, Authorization: str = Header(None)):
    token = Authorization.split(" ")[1]
    token_info = validar_token(token, output=True)
    conn = PsqlConnection().conn
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = """SELECT hu.*,
                       Json_agg((SELECT d FROM   (SELECT dhu.*, d.desc_dia)d)) AS dias
                    FROM   horario_usuario hu
                       LEFT JOIN dia_horario_usuario dhu
                              ON hu.cod_horario_usuario = dhu.cod_horario_usuario
                       LEFT JOIN dia d
                              ON dhu.cod_dia = d.cod_dia
                    WHERE  cod_usuario = %s
                    GROUP  BY hu.cod_horario_usuario """
    cursor.execute(
        query,
        (
            token_info.get('cod_usuario'),
        )
    )

    horarios = cursor.fetchall()
    conn.close()
    response.status_code = HTTP_200_OK
    return horarios


@router.put("/update_horarios")
async def get_horarios(
        response: Response,
        horarios: List[HorarioGet],
        Authorization: str = Header(None)
):
    token = Authorization.split(" ")[1]
    token_info = validar_token(token, output=True)
    conn = PsqlConnection().conn
    conn.autocommit = True
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    for horario in horarios:
        query = """UPDATE horario_usuario SET desde = %s, hasta = %s, user_id = %s WHERE cod_horario_usuario = %s"""
        cursor.execute(
            query,
            (
                horario.desde,
                horario.hasta,
                token_info.get('desc_usuario'),
                horario.cod_horario_usuario
            )
        )
        print(f"Horario Actualizado con cod {horario.cod_horario_usuario}")
        cods_dias = [d.cod_dia_horario_usuario for d in horario.dias]
        query = """DELETE FROM dia_horario_usuario WHERE cod_dia_horario_usuario not in %s AND cod_horario_usuario = %s"""
        cursor.execute(
            query,
            (
                tuple(cods_dias),
                horario.cod_horario_usuario
            )
        )
        for dia in horario.dias:
            print("Dia", dia)
            if dia.cod_dia_horario_usuario:
                query = """UPDATE dia_horario_usuario SET cod_dia = %s, user_id = %s WHERE cod_dia_horario_usuario = %s"""
                cursor.execute(
                    query,
                    (
                        dia.cod_dia,
                        token_info.get('desc_usuario'),
                        dia.cod_dia_horario_usuario
                    )
                )
                print(f"Día Horario Actualizado con cod {dia.cod_dia_horario_usuario}")
            else:
                # for dia in horario.dias:
                query = """INSERT INTO dia_horario_usuario (desc_dia_horario_usuario, cod_dia, cod_horario_usuario, user_id) 
                                VALUES (%s,%s,%s,%s)"""
                cursor.execute(
                    query,
                    (
                        "",
                        dia.cod_dia,
                        horario.cod_horario_usuario,
                        token_info.get('desc_usuario')
                    )
                )

    conn.close()
    response.status_code = HTTP_200_OK
    return {"mensaje": "Horario actualizado exitosamente"}


@router.post("/delete_horario")
async def delete_horario_usuario(response: Response, horario: HorarioUsuario):
    conn = PsqlConnection().conn
    conn.autocommit = True
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = """DELETE FROM dia_horario_usuario WHERE cod_horario_usuario = %s"""
    cursor.execute(
        query,
        [horario.cod_horario_usuario]
    )
    query = """DELETE FROM horario_usuario WHERE cod_horario_usuario = %s"""
    cursor.execute(
        query,
        [horario.cod_horario_usuario]
    )
    conn.close()
    response.status_code = HTTP_200_OK
    return {"mensaje": f"Horario Usuario con cod: {horario.cod_horario_usuario} eliminado exitosamente"}


@router.get("/cambiar_estado_pausado")
async def cambio_estado_usuario(response: Response, Authorization: str = Header(None)):
    token = Authorization.split(" ")[1]
    token_info = validar_token(token, output=True)
    conn = PsqlConnection().conn
    conn.autocommit = True
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    if token_info.get('cod_pausado') == 'S':
        query = """UPDATE usuario SET cod_pausado = 'N' WHERE cod_usuario = %s"""
        mensaje = f"Usuario con cod: {token_info.get('cod_usuario')} despausado exitosamente"
    else:
        query = """UPDATE usuario SET cod_pausado = 'S' WHERE cod_usuario = %s"""
        mensaje = f"Usuario con cod: {token_info.get('cod_usuario')} pausado exitosamente"

    cursor.execute(query, (token_info.get('cod_usuario'),))
    conn.close()
    response.status_code = HTTP_200_OK
    return {"mensaje": mensaje}


@router.get("/eliminar_perfil")
async def eliminar_perfil(response: Response, Authorization: str = Header(None)):
    token = Authorization.split(" ")[1]
    token_info = validar_token(token, output=True)
    conn = PsqlConnection().conn
    conn.autocommit = True
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = """UPDATE usuario SET cod_eliminado = 'S' WHERE cod_usuario = %s"""
    cursor.execute(
        query,
        (
            token_info.get("cod_usuario"),
        )
    )
    query = """SELECT uuid FROM usuario WHERE cod_usuario = %s"""
    cursor.execute(
        query,
        (
            token_info.get("cod_usuario"),
        )
    )
    usuario = cursor.fetchone()
    delete_firebase_user(usuario.get('uuid'))
    conn.close()
    response.status_code = HTTP_200_OK
    return {"mensaje": "Usuario marcado como eliminado exitosamente"}
