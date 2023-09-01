import numpy as np
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi import status
from scripts.paths import createDatePath, logRecognition
from extras.globalData import IMGPATH, TEMPLATES, TEMPLATE, NAMEBLACKLIST, CVEBLACKLIST, FILEPATH, KEEPPERCENTS
from recognition.recognition import imageAlignment, extractT
import cv2
import re


def idRecognition(file):
    filename = None
    content = file.file.read()
    # if (file.content_type[:5] != 'image'):
    #     res = {
    #         'message': 'content_type should be image',
    #         'content_type': file.content_type,
    #         'file Name': file.filename
    #     }
    #     open(createDatePath(FILEPATH) + file.filename, 'wb').write(content)
    #     content = jsonable_encoder(res)
    #     return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=content)
    nparr = np.frombuffer(content, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    for keep in KEEPPERCENTS:
        if filename:
            continue
        print(keep)
        filename, response = recognitionMiddle(img, keep)

    if not filename:
        filename = "error.jpg"
    open(createDatePath(IMGPATH) + filename, 'wb').write(content)
    open('imgAPI/0.jpg', 'wb').write(content)
    return response


def recognitionMiddle(img, keep):
    response = None
    filename = None
    for template in TEMPLATES:
        if response is not None:
            continue
        points_list = TEMPLATES[template]
        img_template = cv2.imread(TEMPLATE + template)
        aligned, matchedVis = imageAlignment(
            image=img, template=img_template, maxFeatures=keep)
        cv2.imwrite("imgAPI/1.jpg", aligned)
        cv2.imwrite('imgAPI/3.jpg', matchedVis)
        name, image = extractT(
            aligned,
            points_list[2],
            points_list[3]
        )
        name = filterName(name, template)
        if (len(name) < 3):
            continue
        cve, finalImage = extractT(
            image,
            points_list[0],
            points_list[1]
        )
        cv2.imwrite('imgAPI/2.jpg', finalImage)
        if (len(cve) == 0):
            continue
        cve = filterCve(cve, name[0])
        if (len(name) > 0 and len(cve) > 0):
            filename, response = makeResponse(name, cve, template)
    if not response:
        response = False
    return filename, response


def filterName(name, doc):
    if doc == 'lic.jpeg':
        nameTmp = []
        lenName = len(name) - 1
        for i in range(lenName):
            nameTmp.append(name[lenName-i])
        name = nameTmp
    newName = []
    for tmp in name:
        for tmp2 in tmp.split():
            newName.append(preprocess_ocr_output(tmp2).upper())
    newName = [ele for ele in newName if ele not in NAMEBLACKLIST]
    regex = re.compile(r'^NO+[A-Z]+RE$')
    filtered = [i for i in newName if ((not regex.match(i)))]
    return filtered


def filterCve(cve, pat):
    print(cve)
    list1 = [x for x in cve if len(x) > 7]
    # list1 = [ele for ele in cve if len(ele) > 4]
    list1 = [ele for ele in list1 if ele not in CVEBLACKLIST]
    newCve = ""
    for aux in list1:
        if aux != " ":
            newCve += aux
    if (len(newCve) < 15):
        return ""
    return newCve


def makeResponse(name, cve, doc):
    filename = cve + '.jpg'
    names = ""
    for aux in name[2:len(name)]:
        names += (aux + " ")
    res = {
        'paterno': name[0],
        'materno': name[1],
        'nombre': names,
        'filename': filename,
        'clave': cve,
        'documento': doc
    }
    print(res)
    content = jsonable_encoder(res)
    response = JSONResponse(
        status_code=status.HTTP_200_OK, content=content)
    logRecognition(doc, name[0], name[1], names, cve, filename)
    return filename, response


def preprocess_ocr_output(text: str) -> str:
    output = text
    output = re.sub(r"1(?![\s%])(?=\w+)", "I", output)
    output = re.sub(r"(?<=\w)(?<![\s+\-])1", "I", output)
    output = re.sub(r"I(?!\s)(?=[\d%])", "1", output)
    output = re.sub(r"(?<=[+\-\d])(?<!\s)I", "1", output)
    return output
