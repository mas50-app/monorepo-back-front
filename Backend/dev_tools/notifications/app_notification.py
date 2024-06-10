from psycopg2.extras import RealDictCursor
from bd_con.conexion import PsqlConnection
from dev_tools.firebase.firebase_manage import sendPush


def create_notification(titulo: str, cuerpo: str, user_id: str, cod_usuario: int):
    """
    Crea una notificacion en la base de datos y a la vez envia un push mediante firebase a la app
    :param titulo: titulo de la notificacion
    :param cuerpo: mensaje de la notificacion
    :param user_id: usuario que está creando esta notificacion
    :param cod_usuario: cod usuario que recibe la notificacion
    :return: null
    """
    conn = PsqlConnection().conn
    conn.autocommit = True
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    # Se guarda la notificacion en la base de datos
    query = """INSERT INTO notificacion (desc_notificacion, user_id, cod_notificada, 
                                    cod_leida, cod_usuario, titulo, cuerpo) 
            VALUES (%s,%s,%s,%s,%s,%s,%s) returning cod_notificacion"""
    cursor.execute(
        query,
        (
            f"{user_id} notifica {titulo}",
            user_id,
            "S",
            "N",
            cod_usuario,
            titulo,
            cuerpo
        )
    )
    notificacion = cursor.fetchone()
    cod_notificacion = notificacion.get("cod_notificacion")

    # Se envia el Push con la integración de Firebase
    query = """SELECT cod_usuario, json_agg(token) as tokens 
                FROM firebase_token_usuario WHERE cod_usuario = %s 
                group by cod_usuario"""
    cursor.execute(
        query,
        (
            cod_usuario,
        )
    )
    tokens = cursor.fetchone()

    sendPush(
        title=titulo,
        msg=cuerpo,
        registration_tokens=tokens.get("tokens", [])
    )
    conn.close()
    print(f"Notificacion con cod {cod_notificacion} enviada con exito a usuario con cod {cod_usuario}")
