import numpy as np
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi import status
from scripts.paths import createDatePath, logRecognition
from extras.globalData import IMGPATH, TEMPLATES, TEMPLATE, NAMEBLACKLIST, CVEBLACKLIST
from recognition.recognition import imageAlignment, extractT
import cv2
import re


def idRecognition(file):
    if (file.content_type[:5] != 'image'):
        res = {
            'message': 'content_type should be image',
            'content_type': file.content_type,
            'file Name': file.filename
        }
        content = jsonable_encoder(res)
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=content)
    content = file.file.read()
    nparr = np.frombuffer(content, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    filename, response = recognitionMiddle(img)
    if not filename:
        filename = "error.jpg"
    filename = 'a.jpg'
    open(createDatePath(IMGPATH) + filename, 'wb').write(content)
    return response


def recognitionMiddle(img):
    response = None
    filename = None
    for template in TEMPLATES:
        if response is not None:
            continue
        points_list = TEMPLATES[template]
        img_template = cv2.imread(TEMPLATE + template)
        aligned, matchedVis = imageAlignment(image=img, template=img_template)
        cv2.imwrite("imgAPI/1.jpg", aligned)
        cv2.imwrite('imgAPI/3.jpg', matchedVis)
        name, image = extractT(
            aligned,
            points_list[2],
            points_list[3]
        )
        if (len(name) == 0):
            continue
        name = filterName(name)
        cve, finalImage = extractT(
            image,
            points_list[0],
            points_list[1]
        )
        cv2.imwrite(createDatePath('imgAPI/')+'.jpg', finalImage)
        if (len(cve) == 0):
            continue
        cve = filterCve(cve)
        if (len(name) > 0 and len(cve) > 0):
            filename, response = makeResponse(name, cve)
    if not response:
        response = False
    return filename, response


def filterName(name):
    newName = []
    for tmp in name:
        newName.append(preprocess_ocr_output(tmp))
    newName = [ele for ele in newName if ele not in NAMEBLACKLIST]
    # regex = re.compile(r'N+[o,O,0]+[A-Z]+[a-z]+E+')
    # filtered = [i for i in newName if not regex.match(i)]
    return newName


def filterCve(cve):
    list1 = [ele for ele in cve if len(ele) > 1]
    list1 = [ele for ele in list1 if ele not in CVEBLACKLIST]
    newCve = ""
    for aux in cve:
        if aux != " ":
            newCve += aux
    return newCve


def makeResponse(name, cve):
    filename = 'a.jpg',
    res = {
        'paterno': name[0],
        'materno': name[1],
        'nombre': name[2],
        'filename': filename,
        'clave': cve
    }
    content = jsonable_encoder(res)
    response = JSONResponse(
        status_code=status.HTTP_200_OK, content=content)
    logRecognition("document", name[0], name[1], name[2], cve, filename)
    return filename, response


def preprocess_ocr_output(text: str) -> str:
    output = text
    output = re.sub(r"1(?![\s%])(?=\w+)", "I", output)
    output = re.sub(r"(?<=\w)(?<![\s+\-])1", "I", output)
    output = re.sub(r"I(?!\s)(?=[\d%])", "1", output)
    output = re.sub(r"(?<=[+\-\d])(?<!\s)I", "1", output)
    return output
