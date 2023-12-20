from scripts.recognition.proces import proces_image
import cv2

paths = []
path = 'img/2023/10/1/143327971_VaMA72io15HDFZRLO9.jpg'
paths.append(path)
path = 'img/2023/10/2/130024382_OELSOOOB1OHMCTRLAG.jpg'
paths.append(path)
path = 'img/2023/10/5/091055764_error.jpg'
paths.append(path)
# path = 'img/2023/10/5/123419512_error.jpg'

img = cv2.imread(path)
print('init')
for each in paths:
    img = cv2.imread(each)
    print(proces_image(img))
