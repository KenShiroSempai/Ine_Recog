import easyocr
import cv2
import numpy as np


RED = (0.0, 0.0, 255.0)
reader = easyocr.Reader(['es'], gpu=False)


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
    text = removeLabel(ocr_result)
    return text, aligned


def removeLabel(ocr_result):
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
