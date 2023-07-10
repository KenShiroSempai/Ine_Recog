"""API identificaiones.

Se cambio el uso de flask por FastAPI por motivos de eficiencia y docker
"""
from fastapi import FastAPI, File, UploadFile, responses
from fastapi.responses import FileResponse, JSONResponse
import aiofiles
from recognition.ine import idk
from extras.tags import listOfTag
from extras.struct import logCarless, deleteLog, Item, tagRange, kibanaLog
from logs.logs import logCarLess, saveCsv
import qrcode
from PIL import Image
import pathlib
from datetime import datetime
import os
import cv2
import json
import _thread
from fastapi.middleware.cors import CORSMiddleware


token = "0f678cb4f8aab5fad68e3a941a004545ea037db0"

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
async def logGral(item: logCarless):
    _thread.start_new_thread(logCarLess, (item.building, item.floor, item.idCArd,
                             item.face, item.conjunto, item.autorizo, item.guard, item.origen, item.reason))
    return {"msg": "ok"}


@app.post("/ppOut")
async def ppOut(item: deleteLog):
    filename = 'app/Bitacora/data.json'

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
async def root():
    """Ruta defaul.

    se usa esta ruta para ver si la API esta en linea antes de hacer pruebas
    """
    return {"Estado": "Funcionando"}


# @app.middleware("http")
# @app.post("/middle")
# async def middle(file: UploadFile = File(...)):
#     response = subir_identification(file)
#     response.headers["X-Process-Time"] = str(1234)
#     print(response)
#     return response


# @app.middleware("http")
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
        # print(aux)
        headers = {"Access-Control-Allow-Origin": "*"}
        response = JSONResponse(content=aux, headers=headers)
        # response.headers["X-Process-Time"] = str(1234)
        print(response)
        return response


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


@app.get("/tags", response_class=FileResponse)
async def returnTags(item: tagRange):
    """Loop Tags

    Ingresas inicio y fin de el rango que quieres obtener y te
    retorna el archivo
    """
    headers = {'Content-Disposition': 'attachment; filename="Book.xlsx"'}
    listOfTag(item.ini, item.fin)
    return FileResponse("app/Bitacora/tag.txt", headers=headers)


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
    filename = 'app/Bitacora/data.json'
    if not os.path.exists(filename):
        print("mamo")
        return {}
    with open(filename, "r") as file:
        data = json.load(file)

    return data
