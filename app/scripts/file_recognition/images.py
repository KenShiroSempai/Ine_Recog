from extras.const import KEEPPERCENT
import numpy as np
import cv2
import imutils


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
    cv2.imwrite('imgAPI/3.jpg', aligned)
    return aligned
