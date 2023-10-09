from extras.const import TEMPLATES, TEMPLATE, MAXFEATURES, KEEPPERCENT, NAMEBLACKLIST, CVEBLACKLIST, TEMPLATE_NAME
import cv2
import numpy as np
import imutils
import re
import easyocr


RED = (0.0, 0.0, 255.0)
reader = easyocr.Reader(['es'], gpu=False)
templateList = []
orb = cv2.ORB_create(MAXFEATURES)
matcher = cv2.DescriptorMatcher_create(
    cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING
)


def makeList():
    for template in TEMPLATES:
        image = cv2.imread(TEMPLATE + template)
        image = imutils.resize(image, width=2000)
        imgGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        (kpsB, descsB) = orb.detectAndCompute(imgGray, None)
        templateList.append([imgGray, template, (kpsB, descsB)])


def findTemplate(imgGray):
    (kpsA, descsA) = orb.detectAndCompute(imgGray, None)
    for each in templateList:
        (kpsB, descsB) = each[2]
        matches = matcher.match(descsA, descsB, None)
        matches = sorted(matches, key=lambda x: x.distance)
        matchN = 0
        for aux in matches[:5]:
            matchN += aux.distance
        print(matchN)
        if matchN < 105:
            return each, matches, (kpsA, descsA)
    return None, None, None


def imageAlignment(image, template, matches, kps):
    # Nos quedamos solo con cierto porcentaje
    keep = int(len(matches) * KEEPPERCENT)
    matches = matches[:keep]
    # Reservamos memoria para los puntos claves
    ptsA = np.zeros((len(matches), 2), dtype='float')
    ptsB = np.zeros((len(matches), 2), dtype='float')
    # Obtenemos los puntos en ambas imagenes
    for (i, m) in enumerate(matches):
        ptsA[i] = kps[0][m.queryIdx].pt
        ptsB[i] = template[2][0][m.trainIdx].pt
    # Obtenemos la homografia
    (H, mask) = cv2.findHomography(ptsA, ptsB, method=cv2.RANSAC)
    # Y la usamos para alinear la imagen
    (h, w) = template[0].shape[:2]
    aligned = cv2.warpPerspective(image, H, (w, h))
    aligned = imutils.resize(aligned, width=2000)
    cv2.imwrite('aligned.png', aligned)
    return aligned


def preprocess_ocr_output(text: str) -> str:
    output = text
    output = re.sub(r"1(?![\s%])(?=\w+)", "I", output)
    output = re.sub(r"(?<=\w)(?<![\s+\-])1", "I", output)
    output = re.sub(r"I(?!\s)(?=[\d%])", "1", output)
    output = re.sub(r"(?<=[+\-\d])(?<!\s)I", "1", output)
    return output


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
            if len(tmp2) > 2:
                newName.append(preprocess_ocr_output(tmp2).upper())
    tmpName = [x for x in newName if x not in NAMEBLACKLIST]
    regex = re.compile(r'^NO+[A-Z]+RE$')
    filtered = [i for i in tmpName if ((not regex.match(i)))]
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
    cv2.rectangle(aligned, point1, point2, RED)
    # cv2.imwrite('Roi.jpg', rgb)
    ocr_result = reader.readtext(rgb)
    text = removeLabel(ocr_result, roi)
    return text, aligned


def removeLabel(ocr_result, roi):
    bigger = 0
    scale = (11/13)
    text = []
    for result in ocr_result:
        height = np.sum(np.subtract(result[0][2], result[0][1]))
        if height > bigger:
            if height*scale > bigger:
                text.clear()
            bigger = height
        if height > bigger*scale:
            text.append(result[1])
    return text


def makeResponse(name, cve, doc):
    filename = cve + '.jpg'
    names = ""
    for aux in name[2:len(name)]:
        names += (aux + " ")
    for each in TEMPLATE_NAME:
        if doc in TEMPLATE_NAME[each]:
            doc = each
            break
    res = {
        'paterno': name[0],
        'materno': name[1],
        'nombre': names,
        'filename': filename,
        'clave': cve,
        'documento': doc
    }
    # logRecognition(doc, name[0], name[1], names, cve, filename)
    return res


def procesAligned(aligned, template):
    response = None
    points_list = TEMPLATES[template]
    name, image = extractT(
        aligned,
        points_list[2],
        points_list[3]
    )
    name = filterName(name, template)
    # if (len(name) < 3):
    #     continue
    cve, finalImage = extractT(
        image,
        points_list[0],
        points_list[1]
    )
    cv2.imwrite('final.jpg', finalImage)
    # if (len(cve) == 0):
    #     continue
    cve = filterCve(cve, name[0])
    if (len(name) > 0 and len(cve) > 8):
        response = makeResponse(
            name, cve, template)
    return response


def bit2(image):
    image = imutils.resize(image, width=2000)
    imgGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    template, matches, kps = findTemplate(imgGray)
    if template is not None:
        print(template[1])
        aligned = imageAlignment(image, template, matches, kps)
        print(procesAligned(aligned, template[1]))


makeList()
