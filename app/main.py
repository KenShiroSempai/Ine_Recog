"""API identificaiones.

Se cambio el uso de flask por FastAPI por motivos de eficiencia y docker
"""
from fastapi import FastAPI, File, UploadFile, responses
import aiofiles
import app.recognition.idRecognition as id
import requests
from requests.auth import HTTPDigestAuth

app = FastAPI()


@app.get("/")
async def root():
    """Ruta defaul.

    se usa esta ruta para ver si la API esta en linea antes de hcaer pruebas
    """
    requests.get("http://192.168.1.180/axis-cgi/io/port.cgi?action=2%3A%2F500%5C", auth=HTTPDigestAuth('root', 'mfmssmcl'))
    return {"Estado": "Funcionando"}


@app.get("/pluma/")
async def open():
    """Monitorear el procesamiento.

    Metodo exclusivo para regresar las imagenes
    de tal modo de ver los reultados
    """
    try:
        requests.get("http://192.168.1.180/axis-cgi/io/port.cgi?action=2%3A%2F500%5C", auth=HTTPDigestAuth('root', 'mfmssmcl'))
        return {"msg": "OK"}
    except Exception as ex:
        return {"error": ex.args}


@app.post("/upload")
async def identification(file: UploadFile = File(...)):
    """Subir identificaciones.

    En esta ruta vamos a recibir las identificaciones
    """
    async with aiofiles.open("app/imgAPI/0.jpg", 'wb') as out_file:
        content = await file.read()  # async read
        await out_file.write(content)  # async write
        aux = id.ineToJson("app/imgAPI/0.jpg")
        print(aux)
        return aux


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
    if ((num < 4) and (num > -1)):
        return responses.FileResponse(f"app/imgAPI/{photo}.jpg")
    return {"error": "malasolicitud"}
