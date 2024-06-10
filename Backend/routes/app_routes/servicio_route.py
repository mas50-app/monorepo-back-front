from fastapi import APIRouter, Response, Header
from starlette.status import *
from typing import List
from unidecode import unidecode
from bd_con.conexion import PsqlConnection
from psycopg2.extras import RealDictCursor
from dev_tools.json_web_token import validar_token
from middlewares.verifica_ruta_token import VerificaRutaToken
from models.app_models.servicio_model import Dia, ServicioBuscador, RespPorCod, ServicioCod, Servicio

router = APIRouter(
    route_class=VerificaRutaToken
)


@router.get('/all', response_model=List[Servicio])
async def get_all_servicios(response: Response, Authorization: str = Header(None)):
    token = Authorization.split(" ")[1]
    token_info = validar_token(token, output=True)
    conn = PsqlConnection().conn
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = """SELECT s.*,
                    to_json(array_agg(DISTINCT c.cod_comuna)) AS comunas,
                    to_json(array_agg(DISTINCT c2.cod_categoria)) AS categorias
                FROM   servicio s
                LEFT JOIN servicio_comuna sc using(cod_servicio)
                LEFT JOIN comuna c ON c.cod_comuna = sc.cod_comuna
                JOIN categoria_servicio cs using(cod_servicio)
                JOIN categoria c2 using(cod_categoria)
                WHERE  s.cod_usuario = %s and s.cod_activo = 'S'
                GROUP  BY s.cod_servicio, s.cod_usuario"""

    cursor.execute(
        query,
        (token_info.get('cod_usuario'),)
    )
    servicios = cursor.fetchall()
    conn.close()
    response.status_code = HTTP_200_OK
    return servicios


@router.post('/por_cod', response_model=RespPorCod, response_model_exclude_none=True)
async def get_by_cod_usuario_prestador(
        response: Response,
        servicio: ServicioCod,
        Authorization: str = Header(None)
):
    token = Authorization.split(" ")[1]
    token_info = validar_token(token, output=True)
    conn = PsqlConnection().conn
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = """SELECT 
                s.*,
                case when fsu.cod_favorito_servicio_usuario is null then false else true end favorito,
                to_json(array_agg(DISTINCT c.cod_comuna)) AS comunas,
                to_json(array_agg(DISTINCT c2.cod_categoria)) AS categorias
            FROM   usuario us
            JOIN servicio s on us.cod_usuario = s.cod_usuario
            LEFT JOIN servicio_comuna sc using(cod_servicio)
            LEFT JOIN comuna c ON c.cod_comuna = sc.cod_comuna
            JOIN categoria_servicio cs using(cod_servicio)
            JOIN categoria c2 using(cod_categoria)
            LEFT JOIN favorito_servicio_usuario fsu on s.cod_servicio = fsu.cod_servicio 
                    and fsu.cod_usuario = %s
            WHERE  s.cod_servicio = %s and s.cod_activo = 'S' and s.cod_pausado = 'N'
            GROUP  BY s.cod_servicio, s.cod_usuario, s.direccion, s.cod_retiro, us.nombre_usuario, us.cod_usuario,
                    s.cod_domicilio, s.cod_es_articulo, s.nom_servicio, s.desc_domicilio, s.cod_activo,
                    fsu.cod_favorito_servicio_usuario"""

    cursor.execute(
        query,
        (
            token_info.get("cod_usuario"),
            servicio.cod_servicio
        )
    )
    serv_resp = cursor.fetchone()

    query = """SELECT itm.*, u.desc_unidad
                FROM item_servicio itm 
                JOIN unidad u on itm.cod_unidad = u.cod_unidad
                WHERE itm.cod_servicio = %s"""

    cursor.execute(
        query,
        (
            servicio.cod_servicio,
        )
    )
    serv_resp['items'] = cursor.fetchall()
    # print(serv_resp)
    query = """SELECT cod_horario_usuario,desde,hasta,
                       To_json(Array_agg(DISTINCT dia.*)) AS dias
                FROM   horario_usuario hu
                       join dia_horario_usuario dhu USING(cod_horario_usuario)
                       join dia USING(cod_dia)
                WHERE cod_usuario =  %s
                GROUP  BY 1,2,3 """

    cursor.execute(
        query,
        (
            servicio.cod_usuario,
        )
    )
    horarios = cursor.fetchall()
    resp = {"servicio": serv_resp, "horarios": horarios}
    conn.close()
    response.status_code = HTTP_200_OK
    return resp


@router.post('/crear')
async def create_servicio(
        response: Response,
        servicio: Servicio,
        Authorization: str = Header(None)
):
    token = Authorization.split(" ")[1]
    token_info = validar_token(token, output=True)
    conn = PsqlConnection().conn
    conn.autocommit = True
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    # Crear el servicio para obtener el cod para relacionar
    query = """
        INSERT INTO servicio 
        (desc_servicio, nom_servicio, cod_usuario, direccion, cod_retiro, cod_es_nacional,
         cod_domicilio, desc_domicilio, cod_es_articulo, dias_antelacion, user_id)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) returning cod_servicio"""

    cursor.execute(
        query,
        (
            servicio.desc_servicio,
            servicio.nom_servicio,
            token_info.get('cod_usuario'),
            servicio.direccion,
            servicio.cod_retiro,
            servicio.cod_es_nacional,
            servicio.cod_domicilio,
            servicio.desc_domicilio,
            servicio.cod_es_articulo,
            servicio.dias_antelacion,
            token_info.get('desc_usuario')
        )
    )
    cod_servicio = cursor.fetchone().get('cod_servicio')

    # Insertar La categoria_servicio
    for cat in servicio.categorias:
        query = """INSERT INTO categoria_servicio (desc_categoria_servicio, cod_servicio, cod_categoria, user_id) 
                        VALUES (%s,%s,%s,%s)"""
        cursor.execute(
            query,
            (
                "",
                cod_servicio,
                cat,
                token_info.get('desc_usuario')
            )
        )

    # Guardar las comunas del servicios
    if servicio.cod_es_nacional == 'N' or servicio.cod_es_nacional is None:
        for comuna in servicio.comunas:
            query = """INSERT INTO servicio_comuna (desc_servicio_comuna, user_id, cod_servicio, cod_comuna) 
                    VALUES (%s,%s,%s,%s)"""
            cursor.execute(
                query,
                (
                    "",
                    token_info.get('desc_usuario'),
                    cod_servicio,
                    comuna
                )
            )

    if servicio.items:
        # Registrar los items
        query = """INSERT INTO item_servicio (desc_item_servicio, cod_servicio, cod_unidad, valor_unidad, user_id)
                        VALUES (%s,%s,%s,%s,%s) returning cod_item_servicio"""
        for item in servicio.items:
            cursor.execute(
                query,
                (
                    item.desc_item_servicio,
                    cod_servicio,
                    item.cod_unidad,
                    item.valor_unidad,
                    token_info.get("desc_usuario")
                )
            )
        print(f"Item Creado con cod: {cursor.fetchone().get('cod_item_servicio')}")

    conn.close()
    response.status_code = HTTP_201_CREATED
    return cod_servicio


@router.post('/buscar', response_model=None)
async def update_servicio(response: Response, filtro: ServicioBuscador, Authorization: str = Header(None)):
    token = Authorization.split(" ")[1]
    token_info = validar_token(token, output=True)
    conn = PsqlConnection().conn
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    print("comuna -----", filtro, token_info.get("cod_usuario"))
    if filtro.filtro == "":
        query = """SELECT u.cod_usuario,
                           u.desc_usuario,
                           u.nombre_usuario,
                           coalesce(u.desc_talento_usuario, '') as desc_talento_usuario,
                           s.cod_servicio,
                           s.cod_revisado,
                           s.desc_servicio,
                           s.nom_servicio,
                           s.dias_antelacion,
                           s.path_imagen,
                           CASE
                             WHEN fsu.cod_favorito_servicio_usuario IS NULL THEN false
                             ELSE true
                           end favorito,
                           Coalesce(Avg(e.valor), 5.0)    AS valoracion,
                           json_agg(its.*) items,
                           coalesce(c2.cod_comuna, '') as cod_comuna
                    FROM   servicio s
                           JOIN usuario u on s.cod_usuario = u.cod_usuario and u.cod_eliminado = 'N' and u.cod_pausado = 'N' and u.cod_activo = 'S'
                           join item_servicio its using(cod_servicio)
                           LEFT JOIN servicio_comuna sc ON s.cod_servicio = sc.cod_servicio
                           LEFT JOIN comuna c2 ON sc.cod_comuna = c2.cod_comuna
                           LEFT JOIN evaluacion e ON e.cod_usuario_evaluado = s.cod_usuario
                           JOIN categoria_servicio cs ON cs.cod_servicio = s.cod_servicio
                           JOIN categoria c USING(cod_categoria)
                           LEFT JOIN favorito_servicio_usuario fsu ON s.cod_servicio = fsu.cod_servicio and fsu.cod_usuario = %s
                    WHERE  s.cod_pausado = 'N' AND s.cod_activo = 'S' AND s.cod_usuario != %s AND (c2.cod_comuna = %s OR s.cod_es_nacional = 'S')
                    GROUP  BY 1,2,3,4,5,6,7,s.dias_antelacion, fsu.cod_favorito_servicio_usuario,desc_usuario, c2.cod_comuna
                    ORDER  BY valoracion, desc_usuario
                    LIMIT  20"""

        cursor.execute(
            query,
            (
                token_info.get('cod_usuario'),
                token_info.get('cod_usuario'),
                filtro.cod_comuna
            )
        )
        servicios = cursor.fetchall()
        conn.close()
        response.status_code = HTTP_200_OK
        print("SERVICIOS BUSCADOS", servicios.__len__())
        return servicios

    query = """SELECT 
                        u.cod_usuario,
                       u.desc_usuario,
                       u.nombre_usuario,
                       coalesce(u.desc_talento_usuario, '') as desc_talento_usuario,
                       s.cod_servicio,
                        s.cod_revisado,
                       s.desc_servicio,
                       s.nom_servicio,
                       s.dias_antelacion,
                       s.path_imagen,
                       case when fsu.cod_favorito_servicio_usuario is null then false else true end favorito,
                       coalesce (Avg(e.valor), 5.0) AS valoracion,
                       json_agg(its.*) items,
                       coalesce(c2.cod_comuna, '') as cod_comuna
                FROM   (WITH words AS (
                                          SELECT word
                                            FROM (
                                              SELECT unnest(string_to_array(%s, ' ')) AS word
                                            ) filtro_palabras
                                        WHERE word != 'y/o'
                                        )
                                        SELECT string_agg(word, ' | ') busqueda
                                        FROM words) filtro, servicio s
                       JOIN usuario u on s.cod_usuario = u.cod_usuario and u.cod_eliminado = 'N' and u.cod_pausado = 'N' and u.cod_activo = 'S'
                       join item_servicio its using(cod_servicio)
                       LEFT JOIN servicio_comuna sc
                             ON s.cod_servicio = sc.cod_servicio
                           LEFT JOIN comuna c2
                             ON sc.cod_comuna = c2.cod_comuna
                       left join evaluacion e
                         ON e.cod_usuario_evaluado = s.cod_usuario
                       join categoria_servicio cs on cs.cod_servicio = s.cod_servicio 
                       join categoria c USING(cod_categoria)
                       LEFT JOIN favorito_servicio_usuario fsu on s.cod_servicio = fsu.cod_servicio and fsu.cod_usuario = %s
                WHERE (
                to_tsvector('spanish', u.desc_usuario) @@ to_tsquery('spanish', busqueda)  or similarity( u.desc_usuario, %s) > 0.2 or
                to_tsvector('spanish', s.nom_servicio) @@ to_tsquery('spanish', busqueda)  or similarity( s.nom_servicio, %s) > 0.2 or 
                to_tsvector('spanish', c.desc_categoria) @@ to_tsquery('spanish', busqueda)  or similarity( c.desc_categoria, %s) > 0.2 or
                to_tsvector('spanish', its.desc_item_servicio) @@ to_tsquery('spanish', busqueda)  or similarity( its.desc_item_servicio, %s) > 0.2
                    )
                       and s.cod_activo = 'S' and s.cod_pausado = 'N' and s.cod_usuario != %s AND (c2.cod_comuna = %s OR s.cod_es_nacional = 'S')
                GROUP  BY 1,2,3,4,5,6,7, s.dias_antelacion, fsu.cod_favorito_servicio_usuario, desc_usuario, c2.cod_comuna
                ORDER  BY valoracion, desc_usuario"""

    cursor.execute(
        query,
        (
            '%' + unidecode(filtro.filtro) + '%',
            token_info.get('cod_usuario'),
            '%' + unidecode(filtro.filtro) + '%',
            '%' + unidecode(filtro.filtro) + '%',
            '%' + unidecode(filtro.filtro) + '%',
            '%' + unidecode(filtro.filtro) + '%',
            token_info.get('cod_usuario'),
            filtro.cod_comuna
        )
    )
    servicios = cursor.fetchall()
    conn.close()
    response.status_code = HTTP_200_OK
    return servicios


@router.put('/actualizar')
async def update_servicio(response: Response, servicio: Servicio, Authorization: str = Header(None)):
    token = Authorization.split(" ")[1]
    token_info = validar_token(token, output=True)
    servicio = servicio.dict(exclude_none=True)
    servicio['user_id'] = token_info.get('desc_usuario')
    conn = PsqlConnection().conn
    conn.autocommit = True
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    query = f"""UPDATE servicio set
                {','.join([f'{u}={"%s"}' for u in servicio.keys() if u not in ['cod_servicio', 'comunas', 'categorias']])}"""
    query += " WHERE cod_servicio = %s"
    valores = []
    # print(servicio)
    for i in servicio.keys():
        if i not in ['cod_servicio', 'comunas', 'categorias']:
            valores.append(servicio.get(i))

    valores.append(servicio.get('cod_servicio'))
    # print(query, valores)
    cursor.execute(
        query,
        valores
    )
    if servicio.get('cod_es_nacional') == 'S':
        cursor.execute(
            """DELETE FROM servicio_comuna WHERE cod_servicio = %s""",
            (
                servicio.get('cod_servicio'),
            )
        )

    if servicio.get('comunas'):
        cursor.execute(
            """DELETE from servicio_comuna WHERE cod_servicio = %s""",
            (
                servicio.get('cod_servicio'),
            )
        )
        # Guardar las comunas del servicios
        for comuna in servicio.get('comunas'):
            query = """INSERT INTO servicio_comuna (desc_servicio_comuna, user_id, cod_servicio, cod_comuna) 
                        VALUES (%s,%s,%s,%s)"""
            cursor.execute(
                query,
                (
                    "",
                    servicio.get('user_id'),
                    servicio.get('cod_servicio'),
                    comuna
                )
            )

    if servicio.get('categorias'):
        cursor.execute(
            """DELETE from categoria_servicio WHERE cod_servicio = %s""",
            (
                servicio.get('cod_servicio'),
            )
        )
        # Guardar La categoria_servicio
        for cat in servicio.get('categorias'):
            query = """INSERT INTO categoria_servicio (desc_categoria_servicio, cod_servicio, cod_categoria, user_id) 
                                VALUES (%s,%s,%s,%s)"""
            cursor.execute(
                query,
                (
                    f"",
                    servicio.get('cod_servicio'),
                    cat,
                    servicio.get('user_id')
                )
            )

    query = """UPDATE servicio SET cod_revisado = 'N' WHERE cod_servicio = %s"""
    cursor.execute(
        query,
        (
            servicio.get('cod_servicio'),
        )
    )
    print(f"{'-' * 10} Servicio con cod: {servicio.get('cod_servicio')} a estado no revisado {'-' * 10}")
    conn.close()
    response.status_code = HTTP_200_OK
    return {"mensaje": f"servicio cod: {servicio.get('cod_servicio')} actualizado exitosamente"}


@router.get('/dias', response_model=List[Dia])
async def get_dias(response: Response):
    conn = PsqlConnection().conn
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = """SELECT * FROM dia ORDER BY cod_dia"""
    cursor.execute(query)
    dias = cursor.fetchall()
    conn.close()
    response.status_code = HTTP_200_OK
    return dias


@router.put("/inactivar")
async def inactivar_servicio(response: Response, servicio: ServicioCod):
    conn = PsqlConnection().conn
    conn.autocommit = True
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    query = """UPDATE servicio SET cod_activo = 'N' WHERE cod_servicio = %s"""

    cursor.execute(
        query,
        (
            servicio.cod_servicio,
        )
    )

    response.status_code = HTTP_200_OK
    conn.close()
    return {"mensaje": "servicio inactivado exitosamente"}


@router.put('/pausar_reanudar')
async def update_servicio(response: Response, servicio: Servicio, Authorization: str = Header(None)):
    token = Authorization.split(" ")[1]
    token_info = validar_token(token, output=True)
    conn = PsqlConnection().conn
    conn.autocommit = True
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = """UPDATE servicio SET cod_pausado = %s, user_id = %s WHERE cod_servicio = %s"""
    print(query, servicio)
    cursor.execute(
        query,
        (
            servicio.cod_pausado,
            token_info.get('desc_usuario'),
            servicio.cod_servicio
        )
    )

    conn.close()
    response.status_code = HTTP_200_OK
    return {"mensaje": f"servicio con cod {servicio.cod_servicio} pausado o reanudado exitosamente"}


@router.post('/favoritos')
async def crear_favorito(response: Response, servicio: ServicioCod, Authorization: str = Header(None)):
    token = Authorization.split(" ")[1]
    token_info = validar_token(token, output=True)
    conn = PsqlConnection().conn
    conn.autocommit = True
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = """INSERT INTO favorito_servicio_usuario (
            desc_favorito_servicio_usuario, user_id, cod_usuario, cod_servicio) 
            VALUES (%s,%s,%s,%s) returning cod_favorito_servicio_usuario"""
    cursor.execute(
        query,
        (
            f"Favorito de {token_info.get('desc_usuario')}",
            token_info.get("desc_usuario"),
            token_info.get("cod_usuario"),
            servicio.cod_servicio
        )
    )
    conn.close()
    response.status_code = HTTP_201_CREATED
    return {"mensaeje": f"Servicio con cod {servicio.cod_servicio} agregado a favoritos exitosamente"}


@router.put('/favoritos')
async def eliminar_favorito(response: Response, servicio: ServicioCod, Authorization: str = Header(None)):
    token = Authorization.split(" ")[1]
    token_info = validar_token(token, output=True)
    conn = PsqlConnection().conn
    conn.autocommit = True
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = """DELETE FROM favorito_servicio_usuario WHERE cod_usuario = %s and cod_servicio = %s"""
    cursor.execute(
        query,
        (
            token_info.get("cod_usuario"),
            servicio.cod_servicio
        )
    )
    conn.close()
    response.status_code = HTTP_200_OK
    return {"mensaeje": f"Servicio con cod {servicio.cod_servicio} eliminado de favoritos exitosamente"}


@router.get('/favoritos')
async def get_favoritos(response: Response, Authorization: str = Header(None)):
    token = Authorization.split(" ")[1]
    token_info = validar_token(token, output=True)
    conn = PsqlConnection().conn
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = """SELECT coalesce(json_agg(f.cod_servicio),'[]') as servicios FROM favorito_servicio_usuario f WHERE cod_usuario = %s"""
    cursor.execute(
        query,
        (
            token_info.get("cod_usuario"),
        )
    )
    favoritos = cursor.fetchone().get('servicios')
    print(favoritos)
    if favoritos:
        query = """SELECT u.cod_usuario,
                           u.desc_usuario,
                           u.nombre_usuario,
                           coalesce(u.desc_talento_usuario, '') as desc_talento_usuario,
                           s.cod_servicio,
                           s.desc_servicio,
                           s.nom_servicio,
                           s.dias_antelacion,
                           s.path_imagen,
                           true as favorito,
                           coalesce(Avg(e.valor), 5.0) AS valoracion
                    FROM   servicio s
                           join usuario u USING(cod_usuario)
                           join item_servicio it using(cod_servicio)
                           left join evaluacion e
                             ON e.cod_usuario_evaluado = s.cod_usuario
                           join categoria_servicio cs on cs.cod_servicio = s.cod_servicio 
                           join categoria c USING(cod_categoria)
                    WHERE s.cod_pausado = 'N' and s.cod_activo = 'S' and s.cod_servicio in %s
                    GROUP  BY 1,2,3,4,5,6,7, s.dias_antelacion, desc_usuario, s.path_imagen
                    ORDER  BY valoracion, desc_usuario"""
        cursor.execute(
            query,
            (
                tuple(favoritos),
            )
        )
        servicios = cursor.fetchall()
        conn.close()
        response.status_code = HTTP_200_OK
        return servicios
    conn.close()
    return []
