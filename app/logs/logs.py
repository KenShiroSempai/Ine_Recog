import time
import os
from app.recognition.ine import idk
from app.extras.struct import *
from base64 import b64decode
import cv2
from csv import writer
import json


def logCarLess(building, floor, idCArd, face, conjunto, autorizo, guardia, origen, reason):
    data = {}
    filename = 'app/Bitacora/data.json'
    lista = []
    pathDefault = "app/imgAPI/0.jpg"
    year = time.strftime("%Y")
    mont = time.strftime("%m")
    day = time.strftime("%d")
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
        aux["nombre"] = "EMPTY"
        aux["paterno"] = "EMPTY"
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
    lista.extend([origen, conjunto, building, floor, str(timestamp), autorizo, aux["nombre"], idPath,
                 facePath, plate.upper(), make, m, color, guardia, "FALTA DE ANTENA/HANDHELD", "FALSE"])
    with open("app/Bitacora/" + conjunto+"/" + 'log.csv', 'a') as f_object:
        writer_object = writer(f_object)
        writer_object.writerow(lista)
        f_object.close()
    if os.path.exists(filename):
        with open(filename, "r") as file:
            data = json.load(file)
    if conjunto not in data:
        data[conjunto] = {}
    if building not in data[conjunto]:
        data[conjunto][building] = {}
    if floor not in data[conjunto][building]:
        data[conjunto][building][floor] = {}
    if day not in data[conjunto][building][floor]:
        data[conjunto][building][floor][day] = {}
    if timeMin not in data[conjunto][building][floor][day]:
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
    f = open(filename, "w")
    f.write(jss)
    f.close()

def saveCsv(item:kibanaLog):
    lista = []
    lista.extend([item.origen, item.conjunto, item.building, item.floor, item.timestamp, item.autorizo, item.name, item.idPath,
                 item.facePath, item.plate, item.make, item.model, item.color, item.guardia, item.tag, item.preauth])
    with open("app/Bitacora/" + item.conjunto+"/" + 'log.csv', 'a') as f_object:
        writer_object = writer(f_object)
        writer_object.writerow(lista)
        f_object.close()
    print("webos")