import cv2
import numpy as np


# Cargar la imagen del documento y la plantilla de referencia
imagen_documento = cv2.imread(
    'img/2023/10/2/130024382_OELSOOOB1OHMCTRLAG.jpg', cv2.IMREAD_GRAYSCALE)
plantilla_referencia = cv2.imread(
    'templates/edoMex.jpg', cv2.IMREAD_GRAYSCALE)

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

cv2.waitKey(0)
cv2.destroyAllWindows()
