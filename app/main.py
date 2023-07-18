"""API identificaiones.

Se cambio el uso de flask por FastAPI por motivos de eficiencia y docker
"""
from fastapi import FastAPI, File, UploadFile, responses
from fastapi.responses import FileResponse, JSONResponse
import aiofiles
from recognition.ine import idk
from extras.tags import listOfTag
from extras.struct import logCarless, deleteLog, tagRange, kibanaLog
from logs.logs import logCarLess, saveCsv
from datetime import datetime
import os
import cv2
import json
import _thread
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)


@app.post("/logcarless")
def logGral(item: logCarless):
    _thread.start_new_thread(logCarLess, (item.building, item.floor, item.idCArd,
                             item.face, item.conjunto, item.autorizo, item.guard, item.origen, item.reason))
    return {"msg": "ok"}


@app.post("/ppOut")
def ppOut(item: deleteLog):
    filename = 'Bitacora/data.json'

    if not os.path.exists(filename):
        return {"msg": "no funciono"}
    with open(filename, "r") as file:
        data = json.load(file)
    if item.time not in data[item.conjunto][item.building][item.floor][item.date]:
        return {"msg": "no funciono"}
    del data[item.conjunto][item.building][item.floor][item.date][item.time]
    if (len(data[item.conjunto][item.building][item.floor][item.date]) < 1):
        del data[item.conjunto][item.building][item.floor][item.date]
    if (len(data[item.conjunto][item.building][item.floor]) < 1):
        del data[item.conjunto][item.building][item.floor]
    with open(filename, "w") as f:
        json.dump(data, f)
    aux = kibanaLog(item.origen, item.conjunto, item.building, item.floor, item.time, item.name, item.autorizo,
                    "SALIDA", "SALIDA", "SALIDA", "SALIDA", "SALIDA", "SALIDA", item.guardia, "SALIDA", "SALIDA")

    saveCsv(aux)


@app.get("/")
def root():
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
    async with aiofiles.open("imgAPI/0.jpg", 'wb') as out_file:
        content = await file.read()  # async read
        await out_file.write(content)  # async write
        aux, op = idk("imgAPI/0.jpg")
        if not op:
            cv2.imwrite("img/fail/"+str(datetime.now()) +
                        ".jpg", cv2.imread("imgAPI/0.jpg"))
            return op
        # print(aux)
        headers = {"Access-Control-Allow-Origin": "*"}
        response = JSONResponse(content=aux, headers=headers)
        # response.headers["X-Process-Time"] = str(1234)
        # print(response._headers)
        return response


@app.get("/img/{photo}")
def retorna_Img(photo):
    """Monitorear el procesamiento.

    Metodo exclusivo para regresar las imagenes
    de tal modo de ver los reultados
    """
    try:
        num = int(photo)
    except Exception as ex:
        return {"error": ex.args}
    if ((num < 4) and (num > -1)):
        return responses.FileResponse(f"imgAPI/{photo}.jpg")
    return {"error": "malasolicitud"}


@app.get("/tags", response_class=FileResponse)
def returnTags(item: tagRange):
    """Loop Tags

    Ingresas inicio y fin de el rango que quieres obtener y te
    retorna el archivo
    """
    headers = {'Content-Disposition': 'attachment; filename="Book.xlsx"'}
    listOfTag(item.ini, item.fin)
    return FileResponse("Bitacora/tag.txt", headers=headers)


@app.get("/adentro/")
def returnJS():
    """Borrar Qr generado.

    Metodo para uso exclusivo de el bot de whatsapp, borra la imagen que este
    generada en caso de que no exista el archivo, retorna un mensaje diciendo
    que no existe.
    """
    filename = 'Bitacora/data.json'
    if not os.path.exists(filename):
        print("mamo")
        return {}
    with open(filename, "r") as file:
        data = json.load(file)

    return data

@app.post("/polarea")
def logCars():
    pass
