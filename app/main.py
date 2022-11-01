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

app = FastAPI()


class Item(BaseModel):
    url: str



@app.get("/")
async def root():
    """Ruta defaul.

    se usa esta ruta para ver si la API esta en linea antes de hacer pruebas
    """
    return {"Estado": "Funcionando"}


@app.post("/upload")
async def identification(file: UploadFile = File(...)):
    """Subir identificaciones.

    En esta ruta vamos a recibir las identificaciones y retorna un JSON con los datos de la Identificacion
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

    Metodo para uso exclusivo del bot de whatsapp, recibe un string y genera un codigo qr con dicho string
    lo guarda en la carpeta espejeada en disk2 para que pueda ser tomado por otro docker 
    """
    if item.url:
        QRcode = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
        url = item.url
        QRcode.add_data(url)
        QRcode.make
        QRimg = QRcode.make_image(fill_color='Black', back_color='White').convert('RGB')
        QRimg = QRimg.resize((1000,1000),Image.ANTIALIAS)
        QRimg.save(r'app/qr/QrWhats.png')
    return {"msg": "too cool "}

@app.post("/plumas/")
async def abrir_plumas(item: Item):
    """Abrir plumas de emergencia.

    Metodo creado para abrir plumas, recibe una ip y manda el pulso a la camara para
    """
    try:
        requests.get("http://"+item.url+"/axis-cgi/io/port.cgi?action=2%3A%2F500%5C", auth=HTTPDigestAuth('root', 'mfmssmcl'))
        print (item.url)
    except Exception as ex:
        return {"error": ex.args}
    return {"msg": "OK"}

@app.get("/delete/")
async def create_item():
    """Borrar Qr generado.

    Metodo para uso exclusivo de el bot de whatsapp, borra la imagen que este generada
    en caso de que no exista el archivo, retorna un mensaje diciendo que no existe.
    """
    file_to_rem = pathlib.Path("app/qr/QrWhats.png")
    if(os.path.isfile(file_to_rem)):
        file_to_rem.unlink()
        return {"msg":"Archivo eliminado"}
    return {"msg":"No hay archivo para eliminar"}