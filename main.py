"""API identificaiones.

Se cambio el uso de flask por FastAPI por motivos de eficiencia y docker
"""
from fastapi import FastAPI, File, UploadFile, responses
import aiofiles

app = FastAPI()


@app.get("/")
async def root():
    """Ruta defaul.

    se usa esta ruta para ver si la API esta en linea antes de hcaer pruebas
    """
    return {"Estado": "Funcionando"}


@app.post("/upload")
async def identification(file: UploadFile = File(...)):
    """Subir identificaciones.

    En esta ruta vamos a recibir las identificaciones
    """
    print(type(file.file))
    async with aiofiles.open("tmp.jpg", 'wb') as out_file:
        content = await file.read()  # async read
        await out_file.write(content)  # async write

    return {"": file.filename}


@app.get("/results/{photo}")
async def returnImg(photo):
    """Monitorear el procesamiento.

    Metodo exclusivo para regresar las imagenes
    de tal modo de ver los reultados
    """
    try:
        num = int(photo)
    except Exception as ex:
        return {"error": ex.args}
    if ((num < 5) and (num > -1)):
        return responses.FileResponse(f"imgAPI/{photo}.jpg")
    return {"error": "malasolicitud"}
