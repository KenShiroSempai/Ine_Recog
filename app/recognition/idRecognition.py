"""Reconocimiento de credencial de identificacion.

En resumen, tomamos la imagen que nos mandan y la comparamos con templates
"""
import numpy as np
import imutils
import cv2
import pytesseract
import easyocr

RED = (0.0, 0.0, 255.0)
reader = easyocr.Reader(['es'], gpu=False)


def imageAlignment(image, template, maxFeatures=1000, keepPercent=0.2):
    """Alineacion de imagenes.

    Recibimos la imagen y template a comparar, no se tiene un template default
    para reutlizar con diferentes ID
    """
    image = imutils.resize(image, width=2000)
    template = imutils.resize(template, width=2000)
    # Convertimos las imagenes a blanco y negro
    imgGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    templateGray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    # Usamos ORB para detectar puntos clave
    orb = cv2.ORB_create(maxFeatures)
    (kpsA, descsA) = orb.detectAndCompute(imgGray, None)
    (kpsB, descsB) = orb.detectAndCompute(templateGray, None)
    # Relacionamos las caracteristicas
    matcher = cv2.DescriptorMatcher_create(
        cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING
    )
    matches = matcher.match(descsA, descsB, None)
    matches = sorted(matches, key=lambda x: x.distance)
    # Nos quedamos solo con cierto porcentaje
    keep = int(len(matches) * keepPercent)
    matches = matches[:keep]
    # Visualizamos los puntos
    matchedVis = cv2.drawMatches(
        image,
        kpsA,
        template,
        kpsB,
        matches,
        None
    )
    matchedVis = imutils.resize(matchedVis, width=1000)
    # Reservamos memoria para los puntos claves
    ptsA = np.zeros((len(matches), 2), dtype='float')
    ptsB = np.zeros((len(matches), 2), dtype='float')
    # Obtenemos los puntos en ambas imagenes
    for (i, m) in enumerate(matches):
        ptsA[i] = kpsA[m.queryIdx].pt
        ptsB[i] = kpsB[m.trainIdx].pt
    # Obtenemos la homografia
    (H, mask) = cv2.findHomography(ptsA, ptsB, method=cv2.RANSAC)
    # Y la usamos para alinear la imagen
    (h, w) = template.shape[:2]
    aligned = cv2.warpPerspective(image, H, (w, h))
    aligned = imutils.resize(aligned, width=1000)
    # cv2.imwrite('aligned.png', aligned)

    return aligned, matchedVis


def extractText(aligned, point1, point2):
    """Extraer texto de cuadros especificos.

    Pasamos como argumento la imagen ya recortada y los puntos
    donde se quiere extraer texto
    """
    height = point2[1] - point1[1]
    width = point2[0] - point1[0]
    roi = aligned[
        point1[1]: point1[1] + height,
        point1[0]: point1[0] + width
    ]
    # rgb = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)
    # cv2.imshow('Roi', rgb)
    text = pytesseract.image_to_string(
        roi,
        lang="spa",
        config="--psm 11"
    )
    cv2.rectangle(aligned, point1, point2, RED)
    return text, aligned


def template(img):
    """Template.

    Esta funcion no esta optimizada, por eso sigue en mejoras
    y se repite en este archivo
    """
    js = {}
    tmp = ""
    ape = ""
    flag = False

    template = cv2.imread('app/templates/-2.jpeg')
    pointEle = (488, 403)
    pointEle2 = (784, 446)
    pointNam = (300, 160)
    pointNam2 = (665, 273)

    aligned, matchedVis = imageAlignment(image=img, template=template)
    elector, image = extractText(
        aligned,
        pointEle,
        pointEle2
    )
    name, finalImage = extractText(
        image,
        pointNam,
        pointNam2
    )
    cv2.imwrite("app/imgAPI/2.jpg", finalImage)
    cv2.imwrite("app/imgAPI/1.jpg", aligned)
    cv2.imwrite('app/imgAPI/3.jpg', matchedVis)
    name = name.split()
    if "NOMBRE" in name:
        name.remove("NOMBRE")
    pat = name[0]
    mat = name[1]

    name.pop(0)
    name.pop(0)
    for aux in name:
        tmp += aux + " "
    elector.split()
    for aux in elector:
        if aux == pat[0] or flag:
            if aux != " ":
                ape += aux
            flag = True
    js["paterno"] = pat
    js["materno"] = mat
    js["nombre"] = tmp
    js["clave"] = ape[0:18]
    return js


def extractT(aligned, point1, point2):
    """Extraer texto de cuadros especificos.

    Pasamos como argumento la imagen ya recortada y los puntos
    donde se quiere extraer texto, no es similar a la de arriba
    porque son metodos dirferentes
    """
    height = point2[1] - point1[1]
    width = point2[0] - point1[0]
    roi = aligned[
        point1[1]: point1[1] + height,
        point1[0]: point1[0] + width
    ]
    rgb = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)
    # cv2.imwrite('Roi.jpg', rgb)
    text = reader.readtext(rgb, detail=0)

    cv2.rectangle(aligned, point1, point2, RED)
    return text, aligned


def template1(img):
    """Template1.

    Esta funcion no esta optimizada, por eso sigue en mejoras
    y se repite en este archivo
    """
    js = {}
    tmp = ""
    ape = ""
    flag = False

    template = cv2.imread('app/templates/-1.jpeg')
    pointEle = (500, 438)
    pointEle2 = (784, 476)
    pointNam = (315, 175)
    pointNam2 = (655, 303)

    aligned, matchedVis = imageAlignment(image=img, template=template)
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
    cv2.imwrite("app/imgAPI/2.jpg", finalImage)
    cv2.imwrite("app/imgAPI/1.jpg", aligned)
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
    return js


def ineToJson(path):
    """Recibimos una INe y la convertimos a JSOM.

    Es la funcion principal en donde mandamos a llamar a las demas funciones
    """
    img = cv2.imread(path)
    js = {}
    try:
        print("1")
        js = template1(img)
    except Exception as ex:
        try:
            print("2")
            js = template(img)
            print(ex)
        except Exception as ex:
            js["msg"] = str(ex)
    return js
