"""API identificaiones.

Se cambio el uso de flask por FastAPI por motivos de eficiencia y docker
"""
from fastapi import FastAPI, File, UploadFile, responses, Request
from fastapi.responses import FileResponse
from extras.tags import listOfTag
from extras.struct import logCarless, deleteLog, tagRange, kibanaLog, carList, persona
from logs.logs import logCarLess, saveCsv
import os
import json
import _thread
from scripts.consult import saveFace
from scripts.paths import createIDPath
from scripts.file_recognition.proces import from_post
from extras.const import MIDDLEWARE
import base64


app = FastAPI()


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
def subir_identification(file: UploadFile = File(...)):
    """Subir identificaciones.

    En esta ruta vamos a recibir las identificaciones y retorna un JSON con
    los datos de la Identificacion.
    """
    return from_post(file)


# @app.post("/recognition")
# def recog_identification(file: UploadFile = File(...)):
#     """Subir identificaciones.

#     En esta ruta vamos a recibir las identificaciones y retorna un JSON con
#     los datos de la Identificacion.
#     """
#     return from_post(file)


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


@app.middleware('http')
async def some_middleware(request: Request, call_next):
    if request.url.path in MIDDLEWARE:
        request.scope['path'] = MIDDLEWARE[request.url.path]
    else:
        request.scope['path'] = request.url.path
    headers = dict(request.scope['headers'])
    # headers[b'custom-header'] = b'my custom header'
    request.scope['headers'] = [(k, v) for k, v in headers.items()]
    return await call_next(request)


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


@app.post("/getphoto/")
def getCredential(persona: persona):
    date, cve = saveFace(persona.persona)
    path = createIDPath(cve, date)
    print(path)
    return responses.FileResponse(path)


@app.post("/getphoto2/")
def getCredentialB64(persona: persona):
    date, cve = saveFace(persona.persona)
    path = createIDPath(cve, date)
    print(path)
    with open(path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    return encoded_string


@app.post("/polarea")
def logCars(data: carList):
    print(data)
