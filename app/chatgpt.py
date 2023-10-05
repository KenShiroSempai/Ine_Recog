import imutils
import cv2
import numpy as np


def imageAlignment(image, template, maxFeatures=2000, keepPercent=0.2):
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


# Cargar la imagen del documento y la plantilla de referencia
imagen_documento = cv2.imread(
    'img/2023/10/2/130024382_OELSOOOB1OHMCTRLAG.jpg', cv2.IMREAD_GRAYSCALE)
plantilla_referencia = cv2.imread(
    'templates/edoMex.jpg', cv2.IMREAD_GRAYSCALE)

imagen_doc = cv2.imread(
    'img/2023/10/2/130024382_OELSOOOB1OHMCTRLAG.jpg')
plantilla_ref = cv2.imread(
    'templates/edoMex.jpg')

aligned, match = imageAlignment(imagen_doc, plantilla_ref, maxFeatures=2000)

cv2.imwrite('Imagen Recortada2.jpg', aligned)

# Inicializar el detector de características (SIFT en este caso)
sift = cv2.SIFT_create()

# Encontrar las características clave y los descriptores en ambas imágenes
keypoints_doc, descriptores_doc = sift.detectAndCompute(imagen_documento, None)
keypoints_ref, descriptores_ref = sift.detectAndCompute(
    plantilla_referencia, None)

# Crear el objeto de coincidencia de características (BFMatcher)
bf = cv2.BFMatcher()
matches = bf.knnMatch(descriptores_doc, descriptores_ref, k=2)

# Aplicar el filtro de razón de distancia
good_matches = []
for m, n in matches:
    if m.distance < 0.75 * n.distance:
        good_matches.append(m)

# Obtener las coordenadas de las características en ambas imágenes
doc_pts = np.float32(
    [keypoints_doc[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
ref_pts = np.float32(
    [keypoints_ref[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)

# Calcular la homografía (transformación de perspectiva)
H, _ = cv2.findHomography(doc_pts, ref_pts, cv2.RANSAC, 5.0)

# Obtener las dimensiones de la plantilla de referencia
altura, ancho = plantilla_referencia.shape[:2]

# Aplicar la transformación de perspectiva a la imagen del documento
imagen_recortada = cv2.warpPerspective(imagen_documento, H, (ancho, altura))

# Mostrar la imagen recortada
cv2.imwrite('Imagen Recortada.jpg', imagen_recortada)
cv2.waitKey(0)
cv2.destroyAllWindows()
