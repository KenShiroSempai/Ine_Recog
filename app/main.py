"""API identificaiones.

Se cambio el uso de flask por FastAPI por motivos de eficiencia y docker
"""
from fastapi import FastAPI, File, UploadFile, responses
import aiofiles
import app.recognition.idRecognition as id
import requests
from requests.auth import HTTPDigestAuth
from pydantic import BaseModel
import qrcode
from PIL import Image
import pathlib
import os
import cv2
from typing import List

app = FastAPI()


class Item(BaseModel):
    """Objeto a recivir en el apartado de QR.

    Se hizo una clase en para que en un futuro, si se quieren aumentar los
    parametros sea mas sencillo.
    """

    url: str


class foto(BaseModel):
    """Objeto a recivir en el apartado de QR.

    Se hizo una clase en para que en un futuro, si se quieren aumentar los
    parametros sea mas sencillo.
    """

    url: str
    path: str


@app.get("/")
async def root():
    """Ruta defaul.

    se usa esta ruta para ver si la API esta en linea antes de hacer pruebas
    """
    return {"Estado": "Funcionando"}


@app.post("/upload")
async def identification(file: UploadFile = File(...)):
    """Subir identificaciones.

    En esta ruta vamos a recibir las identificaciones y retorna un JSON con
    los datos de la Identificacion.
    """
    async with aiofiles.open("app/imgAPI/0.jpg", 'wb') as out_file:
        content = await file.read()  # async read
        await out_file.write(content)  # async write
        aux = id.ineToJson("app/imgAPI/0.jpg")
        return aux


@app.get("/img/{photo}")
async def get_Img(photo):
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


@app.post("/qr/")
async def create_qrImg(item: Item):
    """Generador de QR.

    Metodo para uso exclusivo del bot de whatsapp, recibe un string y genera
    un codigo qr con dicho string lo guarda en la carpeta espejeada en disk2
    para que pueda ser tomado por otro docker
    """
    if item.url:
        R = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
        R.add_data(item.url)
        R.make
        Q = R.make_image(fill_color='Black', back_color='White').convert('RGB')
        Q = Q.resize((1000, 1000), Image.ANTIALIAS)
        Q.save(r'app/qr/QrWhats.png')
    return {"msg": "too cool "}


@app.post("/plumas/")
async def abrir_plumas(item: Item):
    """Abrir plumas de emergencia.

    Metodo creado para abrir plumas, recibe una ip y manda el pulso
    a la camara para
    """
    url = "http://"+item.url+"/axis-cgi/io/port.cgi?action=2%3A%2F500%5C"
    try:
        requests.get(url, auth=HTTPDigestAuth('root', 'mfmssmcl'), timeout=1)
    except Exception as ex:
        return {"error": ex.args}
    return {"msg": "OK"}


@app.get("/delete/")
async def create_item():
    """Borrar Qr generado.

    Metodo para uso exclusivo de el bot de whatsapp, borra la imagen que este
    generada en caso de que no exista el archivo, retorna un mensaje diciendo
    que no existe.
    """
    file_to_rem = pathlib.Path("app/qr/QrWhats.png")
    if (os.path.isfile(file_to_rem)):
        file_to_rem.unlink()
        return {"msg": "Archivo eliminado"}
    return {"msg": "No hay archivo para eliminar"}


@app.post("/photo/")
async def tomar_foto(item: List[foto]):
    """Toma una foto de la camara enviada.

    Para facilitar la captura de fotos, esta funcion toma
    la foto por ti.
    """
    msg = "No hay elementos en la lista "
    for aux in item:
        path = aux.path
        url = "rtsp://root:mfmssmcl@"+aux.url+"/axis-media/media.amp"
        cap = cv2.VideoCapture(url)
        ret, frames = cap.read()
        if not ret:
            msg = "Error con la camara " + aux.url
        else:
            cv2.imwrite("app/pai/"+path, frames)
            msg = "toocol"
    return {"msg": msg}
