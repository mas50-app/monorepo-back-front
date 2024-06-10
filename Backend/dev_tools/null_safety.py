"""Control de nulos en los modelos de datos"""

def null_str(value):
    """
    Convierte el None en ''
    :param value: Se pasa el valor del validador
    """
    if value:
        return value
    value = ''
    return value


def null_int(value):
    """
    Convierte el None en 0
    :param value: Se pasa el valor del validador
    """
    if value:
        return value
    value = 0
    return value

def null_date(value):
    """
    Convierte el None en '1900-01-01'
    :param value: Se pasa el valor del validador
    """
    if value:
        return value
    value = '1900-01-01'
    return value

def null_time(value):
    """
    Convierte el None en '00:00'
    :param value: Se pasa el valor del validador
    """
    if value:
        return value
    value = '00:00'
    return value

def null_bool(value):
    """
    Convierte el None en '00:00'
    :param value: Se pasa el valor del validador
    """
    if value:
        return value
    value = False
    return value
