import cv2
from app.recognition.recognition import imageAlignment, extractT
from datetime import datetime

# templates
ine0Template = "app/templates/ine0.jpeg"
ine1Template = "app/templates/ine1.jpeg"
ifeTemplate = "app/templates/ife.jpeg"


def ife(img):
    js = {}
    op = 0
    tmp = ""
    ape = ""
    flag = False
    template = cv2.imread(ifeTemplate)
    pointEle = (10, 433)
    pointEle2 = (511, 476)
    pointNam = (0, 181)
    pointNam2 = (365, 289)
    aligned, matchedVis = imageAlignment(image=img, template=template)
    cv2.imwrite("app/imgAPI/1.jpg", aligned)

    name, image = extractT(
        aligned,
        pointNam,
        pointNam2
    )
    if (len(name) < 3):
        return js, op
    elector, finalImage = extractT(
        image,
        pointEle,
        pointEle2
    )
    cv2.imwrite("app/imgAPI/2.jpg", finalImage)
    cv2.imwrite('app/imgAPI/3.jpg', matchedVis)
    if "NOMBRE" in name:
        name.remove("NOMBRE")
    if (len(name[0]) < 3):
        name.pop(0)
    pat = name[0]
    mat = name[1]
    name.pop(0)
    name.pop(0)
    for aux in name:
        tmp += aux + " "
    for aux in elector:
        if aux[0] == pat[0] or flag:
            if aux != " ":
                ape += aux
            flag = True
    js["paterno"] = pat
    js["materno"] = mat
    js["nombre"] = tmp
    js["clave"] = ape
    return js, 1


def ine0(img):
    js = {}
    op = 0
    tmp = ""
    ape = ""
    flag = False
    template = cv2.imread(ine0Template)
    pointEle = (488, 403)
    pointEle2 = (784, 456)
    pointNam = (300, 160)
    pointNam2 = (665, 289)
    aligned, matchedVis = imageAlignment(image=img, template=template)
    cv2.imwrite("app/imgAPI/1.jpg", aligned)

    name, image = extractT(
        aligned,
        pointNam,
        pointNam2
    )
    if (len(name) < 3):
        return js, op
    elector, finalImage = extractT(
        image,
        pointEle,
        pointEle2
    )
    cv2.imwrite("app/imgAPI/2.jpg", finalImage)
    cv2.imwrite('app/imgAPI/3.jpg', matchedVis)
    if "NOMBRE" in name:
        name.remove("NOMBRE")
    if (len(name[0]) < 3):
        name.pop(0)
    pat = name[0]
    mat = name[1]
    name.pop(0)
    name.pop(0)
    for aux in name:
        tmp += aux + " "
    for aux in elector:
        if aux[0] == pat[0] or flag:
            if aux != " ":
                ape += aux
            flag = True
    js["paterno"] = pat
    js["materno"] = mat
    js["nombre"] = tmp
    js["clave"] = ape
    return js, 1


def ine1(img):
    js = {}
    op = 0
    tmp = ""
    ape = ""
    flag = False
    template = cv2.imread(ine1Template)
    pointEle = (500, 438)
    pointEle2 = (784, 476)
    pointNam = (315, 175)
    pointNam2 = (655, 303)
    aligned, matchedVis = imageAlignment(image=img, template=template)
    cv2.imwrite("app/imgAPI/1.jpg", aligned)

    name, image = extractT(
        aligned,
        pointNam,
        pointNam2
    )
    if (len(name) < 3):
        return js, op
    elector, finalImage = extractT(
        image,
        pointEle,
        pointEle2
    )
    cv2.imwrite("app/imgAPI/2.jpg", finalImage)
    cv2.imwrite('app/imgAPI/3.jpg', matchedVis)
    if "NOMBRE" in name:
        name.remove("NOMBRE")
    if (len(name[0]) < 3):
        name.pop(0)
    pat = name[0]
    mat = name[1]
    name.pop(0)
    name.pop(0)
    for aux in name:
        tmp += aux + " "
    for aux in elector:
        if aux[0] == pat[0] or flag:
            if aux != " ":
                ape += aux
            flag = True
    js["paterno"] = pat
    js["materno"] = mat
    js["nombre"] = tmp
    js["clave"] = ape
    return js, 1


def idk(im):
    """Template1.

    Esta funcion no esta optimizada, por eso sigue en mejoras
    y se repite en este archivo
    """
    img = cv2.imread(im)
    js, op = ine1(img)
    if op != 0:
        cv2.imwrite("app/img/ine1"+str(datetime.now())+js["clave"]+".jpg", img)
        return js, op
    print("no 0")
    js, op = ine0(img)
    if op != 0:
        cv2.imwrite("app/img/ine0"+str(datetime.now())+js["clave"]+".jpg", img)
        return js, op
    print("no 1")
    js, op = ife(img)
    if op != 0:
        cv2.imwrite("app/img/ife"+str(datetime.now())+js["clave"]+".jpg", img)
        return js, op
    print("no 2")
    return js, op
