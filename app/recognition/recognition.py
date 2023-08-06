import imutils
import cv2
import numpy as np
import easyocr

RED = (0.0, 0.0, 255.0)
reader = easyocr.Reader(['es'], gpu=False)


def imageAlignment(image, template, maxFeatures=2500, keepPercent=0.2):
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
    print(len(matches))
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
