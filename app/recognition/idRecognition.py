import numpy as np
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi import status
from scripts.paths import createDatePath
from extras.globalData import IMGPATH, TEMPLATES, TEMPLATE
from recognition.recognition import imageAlignment, extractT
import cv2


def idRecognition(file):
    if (file.content_type[:5] != 'image'):
        res = {
            'message': 'content_type should be image',
            'content_type': file.content_type,
            'file Name': file.filename
        }
        content = jsonable_encoder(res)
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=content)
    content = file.file.read()
    nparr = np.frombuffer(content, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    filename, response = recognitionMiddle(img)
    filename = file.filename
    response = {}
    open(createDatePath(IMGPATH) + filename, 'wb').write(content)
    return response


def recognitionMiddle(img):
    # js = {}
    # tmp = ""
    # ape = ""
    # flag = False
    for template in TEMPLATES:
        points_list = TEMPLATES[template]
        img_template = cv2.imread(TEMPLATE + template)
        aligned, matchedVis = imageAlignment(image=img, template=img_template)
        cv2.imwrite("imgAPI/1.jpg", aligned)
        cv2.imwrite('imgAPI/3.jpg', matchedVis)
        name, image = extractT(
            aligned,
            points_list[2],
            points_list[3]
        )
        print(name)
        # for point in templatepath:
        #     print(point)

        # for tmp in TEMPLATES[template]:
        # pointEle = TEMPLATES[template][0]
        # pointEle2 = TEMPLATES[template][0]
        # pointNam = TEMPLATES[template][0]
        # pointNam2 = TEMPLATES[template][0]
        # print(pointEle, pointEle2, pointNam, pointNam2)
    # filename = ''
    # js, op = ine1(img)
    # if op:
    #     return js, filename
    return "", ""
