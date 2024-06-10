from fastapi import APIRouter
from fastapi.responses import FileResponse
import os

router = APIRouter()

DATA_PATH_WIN = "./temporales_desarrollo/imagenes/"
DATA_PATH_LIN = "/app/temporales_desarrollo/imagenes/"


@router.get("/{img}")
async def get_image(img: str):
    if os.name == 'nt':
        if os.path.exists(f"{DATA_PATH_WIN}{img}"):
            return FileResponse(path=f"{DATA_PATH_WIN}{img}")
        else:
            return FileResponse(path=f"{DATA_PATH_WIN}default.jpeg")
    else:
        if os.path.exists(f"{DATA_PATH_LIN}{img}"):
            return FileResponse(path=f"{DATA_PATH_LIN}{img}")
        else:
            return FileResponse(path=f"{DATA_PATH_LIN}default.jpeg")
