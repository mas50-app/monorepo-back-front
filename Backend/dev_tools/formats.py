from typing import Union


def CLP_format(value: Union[int, float]) -> str:
    return '{:,.0f}'.format(value).replace(',', '.')
