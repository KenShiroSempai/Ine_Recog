import cv2
from app.recognition.recognition import imageAlignment, extractT
from datetime import datetime

# templates
ine0T = "app/templates/ine0.jpeg"
ine1T = "app/templates/ine1.jpeg"
ifeT = "app/templates/ife.jpeg"
licT = "app/templates/lic.jpeg"


def ife(img):
    js = {}
    tmp = ""
    ape = ""
    flag = False
    template = cv2.imread(ifeT)
    pointEle = (10, 433)
    pointEle2 = (511, 472)
    pointNam = (0, 182)
    pointNam2 = (365, 289)
    aligned, matchedVis = imageAlignment(image=img, template=template)
    cv2.imwrite("app/imgAPI/1.jpg", aligned)

    name, image = extractT(
        aligned,
        pointNam,
        pointNam2
    )
    if (len(name) < 3):
        return js, False
    elector, finalImage = extractT(
        image,
        pointEle,
        pointEle2
    )
    cv2.imwrite("app/imgAPI/2.jpg", finalImage)
    cv2.imwrite('app/imgAPI/3.jpg', matchedVis)
    if "NOMBRE" in name:
        name.remove("NOMBRE")
    if "NoMBRE" in name:
        name.remove("NoMBRE")
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
    js["name"] = ape + "_" + pat + "_" + mat
    return js, True


def ine0(img):
    js = {}
    tmp = ""
    ape = ""
    flag = False
    template = cv2.imread(ine0T)
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
        return js, False
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
    js["name"] = ape + "_" + pat + "_" + mat
    return js, True


def ine1(img):
    js = {}
    tmp = ""
    ape = ""
    flag = False
    template = cv2.imread(ine1T)
    pointEle = (505, 433)
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
        return js, False
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
    js["name"] = ape + "_" + pat + "_" + mat
    return js, True


def lic(img):
    js = {}
    tmp = ""
    ape = ""
    flag = False
    template = cv2.imread(licT)
    pointEle = (500, 438)
    pointEle2 = (784, 476)
    pointNam = (315, 175)
    pointNam2 = (655, 303)
    aligned, matchedVis = imageAlignment(image=img, template=template)
    cv2.imwrite("app/imgAPI/1.jpg", aligned)
    cv2.imwrite('app/imgAPI/3.jpg', matchedVis)
    name, image = extractT(
        aligned,
        pointNam,
        pointNam2
    )
    if (len(name) < 3):
        return js, False
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
    js["name"] = ape + "_" + pat + "_" + mat
    return js, True


def idk(im):
    """Template1.

    Esta funcion no esta optimizada, por eso sigue en mejoras
    y se repite en este archivo
    """
    img = cv2.imread(im)
    js, op = ine1(img)
    if op:
        cv2.imwrite("app/img/"+str(datetime.now()) + "_ine1" +
                    "_"+js["name"]+".jpg", cv2.imread("app/imgAPI/1.jpg"))
        return js, op
    print("no ine1")
    js, op = ine0(img)
    if op:
        cv2.imwrite("app/img/"+str(datetime.now()) + "_ine0" +
                    "_"+js["name"]+".jpg", cv2.imread("app/imgAPI/1.jpg"))
        return js, op
    print("no ine0")
    js, op = ife(img)
    if op:
        cv2.imwrite("app/img/"+str(datetime.now()) + "_ife" +
                    "_"+js["name"]+".jpg", cv2.imread("app/imgAPI/1.jpg"))
        return js, op
    print("no ife")
    js, op = lic(img)
    if op:
        cv2.imwrite("app/img/"+str(datetime.now()) + "_lic" +
                    "_"+js["name"]+".jpg", cv2.imread("app/imgAPI/1.jpg"))
        return js, op
    print("no lic")
    return js, False
