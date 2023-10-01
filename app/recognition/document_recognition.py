import cv2
from extras.globalData import KEEPPERCENTS, IMGPATH, TEMPLATE, TEMPLATES, NAMEBLACKLIST, CVEBLACKLIST, TEMPLATE_NAME
from scripts.paths import createDatePath
from recognition.recognition import imageAlignment, extractT
import re
from datetime import datetime
import base64


def idRecognition(img, name):
    response = None
    for keep in KEEPPERCENTS:
        if response is not None:
            continue
        print(keep)
        response = recognitionMiddle(img, keep, name)
    if response is None:
        response = makeBlanckREsponse(img, name)
    return response


def recognitionMiddle(img, keep, camName):
    response = None
    for template in TEMPLATES:
        if response is not None:
            continue
        points_list = TEMPLATES[template]
        img_template = cv2.imread(TEMPLATE + template)
        aligned, matchedVis = imageAlignment(
            image=img, template=img_template, maxFeatures=keep)
        # cv2.imwrite("imgAPI/1.jpg", aligned)
        # cv2.imwrite('imgAPI/3.jpg', matchedVis)
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
        if (len(name) > 0 and len(cve) > 8):
            response = makeResponse(
                name, cve, template, img, camName)
    return response


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


def makeResponse(name, cve, doc, img):
    retval, buffer = cv2.imencode('.jpg', img)
    jpg_as_text = base64.b64encode(buffer)
    names = ""
    filename = createDatePath(
        IMGPATH) + (str((datetime.timestamp(datetime.now()))))+'.jpg'
    cv2.imwrite(filename, img)
    for aux in name[2:len(name)]:
        names += (aux + " ")
    for each in TEMPLATE_NAME:
        if doc in TEMPLATE_NAME[each]:
            doc = each
            break
    res = {'paterno': name[0],
           'materno': name[1],
           'nombre': names,
           'filename': filename,
           'clave': cve,
           'photoBase64': str(jpg_as_text),
           'documento': doc}
    return res


def makeBlanckREsponse(img, camName):
    retval, buffer = cv2.imencode('.jpg', img)
    jpg_as_text = base64.b64encode(buffer)
    filename = createDatePath(
        IMGPATH) + (str((datetime.timestamp(datetime.now()))))+'.jpg'
    cv2.imwrite(filename, img)
    res = {'paterno': '',
           'materno': '',
           'nombre': '',
           'filename': filename,
           'clave': '',
           'photoBase64': str(jpg_as_text),
           'documento': 'SIN IDENTIFICAR'}
    return res


def preprocess_ocr_output(text: str) -> str:
    output = text
    output = re.sub(r"1(?![\s%])(?=\w+)", "I", output)
    output = re.sub(r"(?<=\w)(?<![\s+\-])1", "I", output)
    output = re.sub(r"I(?!\s)(?=[\d%])", "1", output)
    output = re.sub(r"(?<=[+\-\d])(?<!\s)I", "1", output)
    return output
