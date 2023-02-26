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
from pathlib import Path
from os import path
from csv import writer
import json
import time
import _thread
import json
import os

token = "0f678cb4f8aab5fad68e3a941a004545ea037db0"

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
    autorizo: str
    car: str
    origen: str
    guard: str


class deleteLog(BaseModel):
    """Objeto a recivir en el apartado de QR.

    Se hizo una clase en para que en un futuro, si se quieren aumentar los
    parametros sea mas sencillo.
    """
    building: str
    floor: str
    conjunto: str
    date : str
    time :str

class logCarless(BaseModel):
    """Objeto a recivir en el apartado de QR.

    Se hizo una clase en para que en un futuro, si se quieren aumentar los
    parametros sea mas sencillo.
    """
    building: str
    floor: str
    conjunto: str
    idCArd: str
    face: str
    autorizo: str
    origen: str
    guard: str
    reason: str


class Item(BaseModel):
    """Objeto a recivir en el apartado de QR.

    Se hizo una clase en para que en un futuro, si se quieren aumentar los
    parametros sea mas sencillo.
    """

    url: str    # String del cual se va a generar el QR


@app.post("/enramadalog")
async def logEnramada(item: logEnramada):

    lista = []

    pathDefault = "app/imgAPI/0.jpg"
    pathDefault2 = "app/plate/5.jpg"
    building = item.building
    floor = item.floor
    idCArd = item.idCArd
    face = item.face
    conjunto = item.conjunto
    autorizo = item.autorizo
    car = item.car
    guardia = item.guard

    timestamp = time.strftime("%Y%m%d-%H%M%S")
    newPath = "app/plate"
    if not (os.path.exists(newPath)):
        os.mkdir(newPath)

    with open(pathDefault, "wb") as f:
        f.write(b64decode(idCArd))
    with open(pathDefault2, "wb") as f:
        f.write(b64decode(car))
        f.close()
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
    newPath = "app/" + conjunto
    if not (os.path.exists(newPath)):
        os.mkdir(newPath)
    newPath = newPath+"/"+building
    if not (os.path.exists(newPath)):
        os.mkdir(newPath)
    newPath = newPath + "/"+floor
    if not (os.path.exists(newPath)):
        os.mkdir(newPath)
    plate = "Error"
    make = "Error"
    m = "Error"
    color = "Error"
    idPath = "/" + "idCard" + "_" + name + ".jpg"
    facePath = "/" + "face" + "_" + name + ".jpg"
    carPath = "/" + "car" + "_" + name + ".jpg"
    if not (os.path.exists(newPath)):
        os.mkdir(newPath)
    newPath = newPath+"/"+timestamp
    if not (os.path.exists(newPath)):
        os.mkdir(newPath)
    carPath = newPath + carPath
    with open(carPath, "wb") as f:
        f.write(b64decode(car))
        f.close()
    with open(newPath + idPath, "wb") as f:
        f.write(b64decode(idCArd))
    with open(newPath + facePath, "wb") as f:
        f.write(b64decode(face))

    print(carPath)
    with open(pathDefault2, 'rb') as fp:
        if not (fp):
            plate = "Error de archivo"
            make = "Error de archivo"
            m = "Error de archivo"
            color = "Error de archivo"
        else:
            print("paso el plate")
            try:
                response = requests.post(
                    'https://api.platerecognizer.com/v1/plate-reader/',
                    data=dict(regions=['mx', 'us-ca'], mmc=True),
                    files=dict(upload=fp),
                    headers={'Authorization': 'Token '+token})
                tmp = json.dumps(response.json())
                print(tmp)
                f = open("apiResponse.json", "w")
                f.write(tmp)
                f.close()
                if (json.loads(tmp)["results"]):
                    plate = (json.loads(tmp)["results"][0]["plate"])
                    make = (json.loads(tmp)["results"]
                            [0]["model_make"][0]["make"])
                    m = (json.loads(tmp)["results"][0]
                         ["model_make"][0]["model"])
                    color = (json.loads(tmp)["results"]
                             [0]["color"][0]["color"])
            except requests.exceptions.ConnectionError:
                print("Fallo de coneccion")

    lista.extend([item.origen, conjunto, building, floor, str(timestamp), autorizo, aux["name"], idPath,
                 facePath, plate.upper(), make, m, color, guardia, "FALTA DE ANTENA/HANDHELD", "FALSE"])
    with open("app/Enramada/" + 'log.csv', 'a') as f_object:
        writer_object = writer(f_object)
        writer_object.writerow(lista)
        f_object.close()
    return {"msg": "ok"}


@app.post("/logcarless")
async def logGral(item: logCarless):
    _thread.start_new_thread(logCarLess, (item.building, item.floor, item.idCArd,
                             item.face, item.conjunto, item.autorizo, item.guard, item.origen, item.reason))
    return {"msg": "ok"}

@app.post("/ppOut")
async def ppOut(item: deleteLog):
    filename = 'data.json'
    if not os.path.exists(filename):
        return {"msg":"no funciono"}
    with open(filename, "r") as file:
        data = json.load(file)
    if not item.time in data[item.conjunto][item.building][item.floor][item.date]:
        return {"msg":"no funciono"}
    del data[item.conjunto][item.building][item.floor][item.date][item.time]
    with open(filename, "w") as f:
        json.dump(data, f)
    



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


@app.get("/adentro/")
async def returnJS():
    """Borrar Qr generado.

    Metodo para uso exclusivo de el bot de whatsapp, borra la imagen que este
    generada en caso de que no exista el archivo, retorna un mensaje diciendo
    que no existe.
    """
    filename = 'data.json'
    if not os.path.exists(filename):
        print("mamo")
        return {}
    with open(filename, "r") as file:
        data = json.load(file)

    return data


@app.post("/debug")
async def debug(item: Item):

    lista = []

    pathDefault = "app/imgAPI/0.jpg"
    idCArd = item.url

    with open(pathDefault, "wb") as f:
        f.write(b64decode(idCArd))
        f.close()

    print(pathDefault)
    with open(pathDefault, 'rb') as fp:
        if not (fp):
            plate = "Error de archivo"
            make = "Error de archivo"
            m = "Error de archivo"
            color = "Error de archivo"
        else:
            print("paso el plate")
            try:
                response = requests.post(
                    'https://api.platerecognizer.com/v1/plate-reader/',
                    data=dict(regions=['mx', 'us-ca'], mmc=True),
                    files=dict(upload=fp),
                    headers={'Authorization': 'Token '+token})
                tmp = json.dumps(response.json())
                print(tmp)
                f = open("apiResponse.json", "w")
                f.write(tmp)
                f.close()
                if (json.loads(tmp)["results"]):
                    plate = (json.loads(tmp)["results"][0]["plate"])
                    make = (json.loads(tmp)["results"]
                            [0]["model_make"][0]["make"])
                    m = (json.loads(tmp)["results"][0]
                         ["model_make"][0]["model"])
                    color = (json.loads(tmp)["results"]
                             [0]["color"][0]["color"])
            except requests.exceptions.ConnectionError:
                print("Fallo de coneccion")

    lista.extend([plate, make, m, color, "FALTA DE ANTENA/HANDHELD", "FALSE"])
    with open("app/Enramada/" + 'log.csv', 'a') as f_object:
        writer_object = writer(f_object)
        writer_object.writerow(lista)
        f_object.close()
    return {"msg": "ok"}


def logCarLess(building, floor, idCArd, face, conjunto, autorizo, guardia, origen, reason):
    data = {}
    filename = 'data.json'
    lista = []
    pathDefault = "app/imgAPI/0.jpg"
    year = time.strftime("%Y")
    mont = time.strftime("%m")
    day = time.strftime("%Y%m%d")
    timeMin = time.strftime("%H%M%S") + " "+reason
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    newPath = "app/Bitacora/"+conjunto
    if not (os.path.exists(newPath)):
        os.mkdir(newPath)

    with open(pathDefault, "wb") as f:
        f.write(b64decode(idCArd))
        f.close()
    aux, op = idk(pathDefault)
    if not op:
        aux["clave"] = timestamp
        aux["name"] = "EMPTY"
        name = timestamp + ".jpg"
        cv2.imwrite("app/img/fail/"+timestamp + ".jpg",
                    cv2.imread("app/imgAPI/0.jpg"))
    else:
        name = aux["name"]
    newPath = "app/Bitacora/" + conjunto
    if not (os.path.exists(newPath)):
        os.mkdir(newPath)
    newPath = newPath+"/"+building
    if not (os.path.exists(newPath)):
        os.mkdir(newPath)
    newPath = newPath + "/"+floor
    if not (os.path.exists(newPath)):
        os.mkdir(newPath)
    plate = "No Disponible"
    make = "No Disponible"
    m = "No Disponible"
    color = "No Disponible"
    idPath = "/" + "idCard" + "_" + name + ".jpg"
    facePath = "/" + "face" + "_" + name + ".jpg"
    carPath = "/" + "car" + "_" + name + ".jpg"
    if not (os.path.exists(newPath)):
        os.mkdir(newPath)
    newPath = newPath+"/"+year
    if not (os.path.exists(newPath)):
        os.mkdir(newPath)
    newPath = newPath+"/"+mont
    if not (os.path.exists(newPath)):
        os.mkdir(newPath)
    newPath = newPath+"/"+day
    if not (os.path.exists(newPath)):
        os.mkdir(newPath)
    newPath = newPath+"/"+timeMin
    if not (os.path.exists(newPath)):
        os.mkdir(newPath)
    carPath = newPath + carPath
    with open(newPath + idPath, "wb") as f:
        f.write(b64decode(idCArd))
    with open(newPath + facePath, "wb") as f:
        f.write(b64decode(face))
    lista.extend([origen, conjunto, building, floor, str(timestamp), autorizo, aux["name"], idPath,
                 facePath, plate.upper(), make, m, color, guardia, "FALTA DE ANTENA/HANDHELD", "FALSE"])
    with open("app/Bitacora/" + conjunto+"/" + 'log.csv', 'a') as f_object:
        writer_object = writer(f_object)
        writer_object.writerow(lista)
        f_object.close()
    if os.path.exists(filename):
        with open(filename, "r") as file:
            data = json.load(file)
    if not conjunto in data:
        data[conjunto] = {}
    if not building in data[conjunto]:
        data[conjunto][building] = {}
    if not floor in data[conjunto][building]:
        data[conjunto][building][floor] = {}
    if not day in data[conjunto][building][floor]:
        data[conjunto][building][floor][day] = {}
    if not timeMin in data[conjunto][building][floor][day]:
        data[conjunto][building][floor][day][timeMin] = {"marca": make,
                                                         "origen": origen,
                                                         "time": str(timestamp),
                                                         "autorizo": autorizo,
                                                         "name": aux["nombre"] + aux["paterno"],
                                                         "model": m,
                                                         "guardia": guardia,
                                                         "motivo": reason
                                                         }
    jss = json.dumps(data)
    f = open("data.json", "w")
    f.write(jss)
    f.close()
