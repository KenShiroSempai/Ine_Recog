import cv2
import imutils

# Cargar las plantillas
plantilla_ine = cv2.imread('templates/edoMex.jpg', 0)  # Carga la plantilla de la INE en escala de grises
plantilla_pasaporte = cv2.imread('templates/ine0.jpeg', 0)  # Carga la plantilla del pasaporte en escala de grises

plantilla_ine = imutils.resize(plantilla_ine, width=2000)
plantilla_pasaporte = imutils.resize(plantilla_pasaporte, width=2000)


# Cargar la imagen de entrada
imagen = cv2.imread('img/2023/10/1/143327971_VaMA72io15HDFZRLO9.jpg', 0)  # Carga la imagen de entrada en escala de grises
imagen = imutils.resize(imagen, width=2000)

# Realizar coincidencia de plantillas
resultado_ine = cv2.matchTemplate(imagen, plantilla_ine, cv2.TM_CCOEFF_NORMED)
resultado_pasaporte = cv2.matchTemplate(imagen, plantilla_pasaporte, cv2.TM_CCOEFF_NORMED)

# Obtener los valores máximos y sus posiciones
_, max_val_ine, _, max_loc_ine = cv2.minMaxLoc(resultado_ine)
_, max_val_pasaporte, _, max_loc_pasaporte = cv2.minMaxLoc(resultado_pasaporte)


# Definir un umbral para la coincidencia
umbral = 0.1  # Ajusta este valor según tus necesidades

# Comprobar si la imagen coincide con la plantilla de la INE o el pasaporte
if max_val_ine > umbral:
    print("Es una INE")
elif max_val_pasaporte > umbral:
    print("Es un pasaporte")
else:
    print("No se pudo identificar")
