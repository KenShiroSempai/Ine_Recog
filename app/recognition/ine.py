import cv2
from recognition.recognition import imageAlignment, extractT
from datetime import datetime

# templates
ine0T = "templates/ine0.jpeg"
ine1T = "templates/ine1.jpeg"
ifeT = "templates/ife.jpeg"
licT = "templates/lic.jpeg"


def has_numbers(inputString):
    return any(char.isdigit() for char in inputString)


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
    cv2.imwrite("imgAPI/1.jpg", aligned)

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
    cv2.imwrite("imgAPI/2.jpg", finalImage)
    cv2.imwrite('imgAPI/3.jpg', matchedVis)
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
    cv2.imwrite("imgAPI/1.jpg", aligned)

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
    cv2.imwrite("imgAPI/2.jpg", finalImage)
    cv2.imwrite('imgAPI/3.jpg', matchedVis)
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
    cv2.imwrite("imgAPI/1.jpg", aligned)

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
    cv2.imwrite("imgAPI/2.jpg", finalImage)
    cv2.imwrite('imgAPI/3.jpg', matchedVis)
    if "NOMBRE" in name:
        name.remove("NOMBRE")
    if "NONBRE" in name:
        name.remove("NOMBRE")
    if "NCMPRE" in name:
        name.remove("NCMPRE")

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
    ape = ""
    namee = ""
    au = []
    template = cv2.imread(licT)
    pointEle = (128, 1354)
    pointEle2 = (589, 1545)
    pointNam = (146, 768)
    pointNam2 = (854, 975)
    aligned, matchedVis = imageAlignment(image=img, template=template)
    cv2.imwrite("imgAPI/1.jpg", aligned)
    cv2.imwrite('imgAPI/3.jpg', matchedVis)
    name, image = extractT(
        aligned,
        pointNam,
        pointNam2
    )

    if (len(name) < 2):
        return js, False
    if (len(name[0]) < 3):
        name.pop(0)
    for tmp in name:
        if not (tmp[0:3] == "Lic"):
            au += tmp.split()
    if (len(au) < 3):
        return js, False
    js["materno"] = au[len(au)-1]
    au.pop(len(au)-1)
    js["paterno"] = au[len(au)-1]
    au.pop(len(au)-1)
    for aaux in au:
        if not has_numbers(aaux):
            namee += aaux + " "
    js["nombre"] = namee

    elector, finalImage = extractT(
        image,
        pointEle,
        pointEle2
    )
    cv2.imwrite("imgAPI/2.jpg", finalImage)
    cv2.imwrite('imgAPI/3.jpg', matchedVis)
    if "RFC" in elector:
        elector.remove("RFC")
    print(elector)
    if len(elector) == 1:
        ape = elector[0]

    js["clave"] = ape
    js["name"] = js["paterno"] + "_" + js["materno"] + \
        "_" + js["nombre"] + "_" + js["clave"]
    return js, True


def idk(im):
    """Template1.

    Esta funcion no esta optimizada, por eso sigue en mejoras
    y se repite en este archivo
    """
    img = cv2.imread(im)
    js, op = ine1(img)
    if op:
        cv2.imwrite("img/"+str(datetime.now()) + "_ine1" +
                    "_"+js["name"]+".jpg", cv2.imread("imgAPI/1.jpg"))
        return js, op
    print("no ine1")
    js, op = ine0(img)
    if op:
        cv2.imwrite("img/"+str(datetime.now()) + "_ine0" +
                    "_"+js["name"]+".jpg", cv2.imread("imgAPI/1.jpg"))
        return js, op
    print("no ine0")
    js, op = ife(img)
    if op:
        cv2.imwrite("img/"+str(datetime.now()) + "_ife" +
                    "_"+js["name"]+".jpg", cv2.imread("imgAPI/1.jpg"))
        return js, op
    print("no ife")
    js, op = lic(img)
    if op:
        cv2.imwrite("img/"+str(datetime.now()) + "_lic" +
                    "_"+js["name"]+".jpg", cv2.imread("imgAPI/1.jpg"))
        return js, op
    print("no lic")
    return js, False
