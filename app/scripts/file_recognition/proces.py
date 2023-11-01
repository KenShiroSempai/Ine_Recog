from extras.const import TEMPLATES, IMGPATH
import numpy as np
from scripts.file_recognition.ocr import extractT
from scripts.file_recognition.strings import filterCve, filterName, makeResponse
from scripts.file_recognition.templates import findTemplate
from scripts.paths import createDatePath

import cv2
import imutils


def procesAligned(aligned, template):
    response = None
    points_list = TEMPLATES[template]
    name, image = extractT(
        aligned,
        points_list[2],
        points_list[3]
    )
    name = filterName(name, template)
    if (len(name) < 3):
        return response
    cve, finalImage = extractT(
        image,
        points_list[0],
        points_list[1]
    )
    cv2.imwrite('imgAPI/1.jpg', finalImage)
    # if (len(cve) == 0):
    #     continue
    cve = filterCve(cve, name[0])
    if (len(name) > 1 and len(cve) > 8):
        response = makeResponse(
            name, cve, template)
    return response


def proces_image(image):
    response = None
    image = imutils.resize(image, width=2000)
    imgGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    response = findTemplate(imgGray)
    if response is None:
        filename = 'error.jpg'
    else:
        filename = response['filename']
    cv2.imwrite(createDatePath(IMGPATH) + filename, image)
    return response


def from_post(file):
    response = None
    content = file.file.read()
    # if (file.content_type[:5] != 'image'):
    #     res = {
    #         'message': 'content_type should be image',
    #         'content_type': file.content_type,
    #         'file Name': file.filename
    #     }
    open('imgAPI/0.jpg', 'wb').write(content)
    #     content = jsonable_encoder(res)
    #     return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=content)
    nparr = np.frombuffer(content, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    # cv2.imwrite('init.jpg', img)
    response = proces_image(img)
    if response is None:
        response = False
        # response = {'message': '¿Estas seguro de que subiste una identificaion?'}
    return response
