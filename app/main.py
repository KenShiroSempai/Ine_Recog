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
from csv import writer
import threading

app = FastAPI()


class Item(BaseModel):
    """Objeto a recivir en el apartado de QR.

    Se hizo una clase en para que en un futuro, si se quieren aumentar los
    parametros sea mas sencillo.
    """

    url: str    # String del cual se va a generar el QR


class foto(BaseModel):
    """Objeto a recivir en el apartado de QR.

    Se hizo una clase en para que en un futuro, si se quieren aumentar los
    parametros sea mas sencillo.
    """

    url: str    # IP de la camara con la que tomara foto
    path: str   # Nombre con el que se va  a guardar la foto


class rfid(BaseModel):
    """Objeto creado para los parametros de TAG fallido

    Guardara los parametros necesarios para llevar el registro de tags leidos
    con la sunmi ya que esta solo se debe de usar cuando la antena no lo
    detecto
    """

    tag: str        # Tag leido
    timestamp: str  # Tiempo en el que el tag fue tomado
    ip: str         # Ip de la camara que tomara foto
    salida: str     # Nombre de la pluma que se abrio


@app.get("/")
async def root():
    """Ruta defaul.

    se usa esta ruta para ver si la API esta en linea antes de hacer pruebas
    """
    return {"Estado": "Funcionando"}


@app.post("/upload")
async def subir_identification(file: UploadFile = File(...)):
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
async def retorna_Img(photo):
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
async def create_whatsQr(item: Item):
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
async def abrir_pluma(item: Item):
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
async def borrar_whatsQr():
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
        t2 = threading.Thread(
            name=aux.path, target=takePicture, args=(aux.url, aux.path))
        t2.start()

    return {"msg": msg}


@app.post("/rfid/")
async def tag_defectuoso(item: rfid):
    """Recibe los detalles de un tag defectuoso.

    Registramos todos los parametros para llevar un control de los tag
    defectuosos
    """
    lista = []
    # Extraemos los datos del cuerpo del post
    tag = item.tag
    timestamp = item.timestamp
    ip = item.ip
    salida = item.salida
    # Con el cuerpo del post, tomaremos una foto
    url = "rtsp://root:mfmssmcl@"+ip+"/axis-media/media.amp"
    cap = cv2.VideoCapture(url)
    ret, frames = cap.read()
    # verificamos que la camara se abrio con exito
    if not ret:
        # si no se abrio bien, hacemos el registro sin foto
        foto = "Hubo un error al acceder a la camara"
    else:
        # si se abrio bien, tomamos la foto y guardamos el registro
        foto = salida+"_"+timestamp+"_"+tag+".jpg"
        cv2.imwrite("app/Castrosa/img/"+foto, frames)
    lista.extend([foto, tag, timestamp, salida])
    with open('app/Castrosa/tags.csv', 'a') as f_object:
        writer_object = writer(f_object)
        writer_object.writerow(lista)
        f_object.close()
    return {"msg": "toocool"}


def takePicture(ip: str, name: str):
    u = "http://"+ip+"/axis-cgi/jpg/image.cgi"
    r = requests.get(u, auth=HTTPDigestAuth('root', 'mfmssmcl'), timeout=1)
    path = name
    if r.status_code == 200:
        with open(path, 'wb') as f:
            for chunk in r:
                f.write(chunk)
