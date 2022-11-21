import cv2
from app.recognition.recognition import imageAlignment, extractT

# templates
ine0Template = ""
ine1Template = ""
ifeTemplate = "app/templates/ine0.jpeg"


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
    elector, image = extractT(
        aligned,
        pointEle,
        pointEle2
    )
    name, finalImage = extractT(
        image,
        pointNam,
        pointNam2
    )
    if (len(name) < 3):
        return 0

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
    return js, op


def ine0():
    js = {}
    op = 0
    return js, op


def ine1():
    js = {}
    op = 0
    return js, op


def idk(im):
    """Template1.

    Esta funcion no esta optimizada, por eso sigue en mejoras
    y se repite en este archivo
    """
    img = cv2.imread(im)
    js, op = ife(img)
    return js, op
