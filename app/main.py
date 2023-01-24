"""API identificaiones.

Se cambio el uso de flask por FastAPI por motivos de eficiencia y docker
"""
from fastapi import FastAPI, File, UploadFile, responses, Form
import aiofiles
import requests
from app.recognition.ine import idk
from pydantic import BaseModel
import qrcode
from PIL import Image
import pathlib
from datetime import datetime
import os
import cv2
from base64 import b64decode
import time
from os.path import isfile, join
from pathlib import Path
from os import listdir, unlink
from csv import writer

app = FastAPI()

class logEnramada(BaseModel):
    """Objeto a recivir en el apartado de QR.

    Se hizo una clase en para que en un futuro, si se quieren aumentar los
    parametros sea mas sencillo.
    """
    building: str
    floor: str
    conjunto: str
    idCArd: str
    face: str

class Item(BaseModel):
    """Objeto a recivir en el apartado de QR.

    Se hizo una clase en para que en un futuro, si se quieren aumentar los
    parametros sea mas sencillo.
    """

    url: str    # String del cual se va a generar el QR


class Refren(BaseModel):
    """Objeto a recivir en el apartado de QR.

    Se hizo una clase en para que en un futuro, si se quieren aumentar los
    parametros sea mas sencillo.
    """
    img: str
    name: str
    tag: str


class Re(BaseModel):
    """Objeto a recivir en el apartado de QR.

    Se hizo una clase en para que en un futuro, si se quieren aumentar los
    parametros sea mas sencillo.
    """
    qr: str
    tag: str
    status: str


@app.get("/refrendo2/{tag}/{photo}")
async def retorna_TagPhoto(tag, photo):
    """Monitorear el procesamiento.

    Metodo exclusivo para regresar las imagenes
    de tal modo de ver los reultados
    """
    try:
        path = str(tag) + "/" + str(photo)
    except Exception as ex:
        return {"error": ex.args}
    try:
        print("app/tag/{path}")
        return responses.FileResponse(f"app/tag/{path}")
    except Exception as ex:
        return {"error": ex.args}


@app.get("/refrendoo/{photo}")
async def retorna_Tag(photo):
    """Monitorear el procesamiento.

    Metodo exclusivo para regresar las imagenes
    de tal modo de ver los reultados
    """
    try:
        tag = int(photo)
    except Exception as ex:
        return {"error": ex.args}
    newPath = "app/tag/"+str(tag)
    if not (os.path.exists(newPath)):
        return {"ERROR": "No hay fotos de ese tag"}
    onlyfiles = [f for f in listdir(newPath) if isfile(join(newPath, f))]
    onlyfiles.sort()
    js = {}

    num = len(onlyfiles)
    for i in range(1, num+1):
        js[str(i)] ="http://localhost:4999/refrendo2/" + str(tag)+"/"+str(onlyfiles[num-i])
    return js

@app.post("/enramadalog")
async def logEnramada(item: logEnramada):

    lista = []

    pathDefault = "app/imgAPI/0.jpg"
    building = item.building
    floor = item.floor
    idCArd = item.idCArd
    face = item.face
    conjunto = item.conjunto

    timestamp = time.strftime("%Y%m%d-%H%M%S")

    with open(pathDefault, "wb") as f:
        f.write(b64decode(idCArd))
    aux, op = idk(pathDefault)
    print(aux)
    if not op:
        aux["clave"] = timestamp
        aux["name"] = "EMPTY"
        name = timestamp + ".jpg"
        cv2.imwrite("app/img/fail/"+timestamp + ".jpg",
                    cv2.imread("app/imgAPI/0.jpg"))
    else:
        name = aux["name"]
    newPath = "app/" + conjunto+"/"+aux["clave"]+"/"
    tmp = conjunto+"_" + building+"_"+floor+"_" + name

    

    idPath =  "idCard" + "_" +tmp + ".png"
    facePath =  "face" + "_" + tmp + ".png"
    if not (os.path.exists(newPath)):
        os.mkdir(newPath)
    with open(newPath +idPath, "wb") as f:
        f.write(b64decode(idCArd))
    with open(newPath +facePath, "wb") as f:
        f.write(b64decode(face))
    lista.extend([conjunto, building, floor, str(timestamp), aux["name"],idPath,facePath],"SIN ASIGNAR","SIN CAMARA AXIS","FALTA DE ANTENA/HANDHELD","FALSE")
    with open("app/Enramada/" + 'log.csv', 'a') as f_object:
        writer_object = writer(f_object)
        writer_object.writerow(lista)
        f_object.close()
    return {"msg":"ok"}

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
        aux, op = idk("app/imgAPI/0.jpg")
        if not op:
            cv2.imwrite("app/img/fail/"+str(datetime.now()) +
                        ".jpg", cv2.imread("app/imgAPI/0.jpg"))
            return op
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


@app.post("/refrendo")
async def postRefrendo(item: Re):
    print(item.tag + "  " + item.status+"  "+item.qr)
    postLomas(tag=item.tag, qr=item.qr, status=item.status)


@app.post("/reporte")
async def postRefrendo(item: Re):
    postLomas(tag=item.tag, qr=item.qr)


@app.post('/base64')
def file_upload(item: Refren):
    newPath = "app/tag/"+item.tag+"/"
    if not (os.path.exists(newPath)):
        os.mkdir(newPath)
    name = item.name
    if (os.path.isfile(newPath + name)):
        name = "refrendo2023__" + time.strftime("%Y%m%d-%H%M%S")+".png"
    with open(newPath + name, "wb") as f:
        f.write(b64decode(item.img))


def postLomas(tag: str, qr: str, status: str):
    aux = r'file://192.168.2.202/Files/tagsRefrendo/'
    # aux = file://192.168.1.202/Files/tagsRefrendo/
    js = {
        "tag": tag,
        "url": aux + tag + "/",
        "estado": status
    }
    js2 = {
        "tag": tag,
        "qr": qr
    }
    url = "http://192.168.1.202:3001/tag/odoo"
    url2 = "http://192.168.1.202:3001/tag/odoo/qr"
    response = requests.post(url, json=js)
    response = requests.post(url2, json=js2)
