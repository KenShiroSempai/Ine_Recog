import time
import os
from extras.struct import kibanaLog
from csv import writer
import json
from datetime import datetime
from extras.const import LOGPATH, NOTD, RECOGFAIL, DATAFILE, BITPATH
from scripts.Paths import createPath, createDatePath
from scripts.proces_data import merge_dict2
from scripts.base64 import base64toOpenCV, writeB64


def logCarLess(building, floor, idCArd, face, conjunto, autorizo, guardia, origen, reason, recognizer):
    data = {}
    day = time.strftime("%d")
    timeMin = time.strftime("%H%M%S")
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    newPath = BITPATH+conjunto
    createPath(newPath)
    # declaraciones
    id_img = base64toOpenCV(idCArd)
    js = recognizer.proces_image(id_img)
    print(js)
    if js is None:
        js = jsonFail(timestamp)
    cve = js["clave"]
    newPath = BITPATH + conjunto+"/"+building + "/"+floor + '/'
    createPath(newPath)
    plate = make = m = color = NOTD
    idPath = "_" + "idCard" + "_" + cve + ".jpg"
    facePath = "_" + "face" + "_" + cve + ".jpg"
    newPath = createDatePath(newPath)
    writeB64(path=newPath + idPath, data=idCArd)
    writeB64(path=newPath + facePath, data=face)
    lista2 = [origen, conjunto, building, floor, str(timestamp), autorizo, js["nombre"], idPath,
              facePath, plate.upper(), make, m, color, guardia, "FALTA DE ANTENA/HANDHELD", "FALSE"]
    writeCsv(filename=BITPATH + conjunto+"/" + 'log.csv', data=lista2)
    if os.path.exists(DATAFILE):
        try:
            with open(DATAFILE, "r") as file:
                data = json.load(file)
        except Exception:
            data = {}
    res = {"marca": make,
           "origen": origen,
           "time": str(timestamp),
           "autorizo": autorizo,
           "name": js["nombre"] + js["paterno"],
           "model": m,
           "guardia": guardia,
           "motivo": reason
           }
    res2 = {conjunto: {building: {floor: {day: {timeMin: res}}}}}
    z = merge_dict2(res2, data)
    jss = json.dumps(z)
    f = open(DATAFILE, "w")
    f.write(str(jss))
    f.close()


def saveCsv(item: kibanaLog):
    lista = [item.origen, item.conjunto, item.building, item.floor, item.timestamp, item.autorizo, item.name, item.idPath,
             item.facePath, item.plate, item.make, item.model, item.color, item.guardia, item.tag, item.preauth]
    writeCsv(filename="Bitacora/" + item.conjunto+"/" + 'log.csv', data=lista)


def writeCsv(filename, data):
    with open(filename, 'a') as f_object:
        writer_object = writer(f_object)
        writer_object.writerow(data)
        f_object.close()


def jsonFail(timestamp) -> dict:
    js = {}
    js["clave"] = timestamp
    js["nombre"] = js["paterno"] = js['materno'] = js['documento'] = RECOGFAIL
    js['filename'] = timestamp + ".jpg"
    return js


def logExeption(e, fun):
    print("oda")
    lista = []
    time = datetime.now()
    lista.extend([time, e, fun])
    with open(LOGPATH + 'a.csv', 'a') as f_object:
        writer_object = writer(f_object)
        writer_object.writerow(lista)
        f_object.close()
