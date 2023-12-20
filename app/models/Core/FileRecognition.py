from utils.Constants import ESSENSIALS_PATHS, IMGPATH
from scripts.Paths import createPath, createDatePath
from utils.FileName import IMG_POSTED
from .ImgRecognizer import ImgRecognizer
import numpy as np
import imutils
import cv2


class FileRecognition(ImgRecognizer):
    def __init__(self):
        for each in ESSENSIALS_PATHS:
            createPath(each)
        super().__init__()

    def __compare_templates__(self, templates, image) -> dict:
        """
        This method compares the given image with a set of templates.

        Parameters:
        templates (list): A list of templates to compare with the image.
        image (ndarray): The image to be compared.

        Returns:
        response (dict): The result of the comparison.
        """
        response = None
        for template, matches, kps in templates:
            print(template[1])
            aligned = self.imageAlignment(image, template, matches, kps)
            response = self.procesAligned(aligned, template[1])
            if response is not None:
                break
        return response

    def proces_image(self, image) -> dict:
        """
        This method processes the given image.

        Parameters:
        image (ndarray): The image to be processed.

        Returns:
        response (dict): The result of the processing.
        """
        response = None
        image = imutils.resize(image, width=2000)
        imgGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        obs_matches_list = self.match_templates(imgGray)
        response = self.__compare_templates__(obs_matches_list, image)

        if response is None:
            filename = 'error.jpg'
        else:
            filename = response['filename']
        cv2.imwrite(createDatePath(IMGPATH) + filename, image)
        return response

    def from_post(self, file) -> dict:
        response = None
        content = file.file.read()
        # if (file.content_type[:5] != 'image'):
        #     res = {
        #         'message': 'content_type should be image',
        #         'content_type': file.content_type,
        #         'file Name': file.filename
        #     }
        open(IMGPATH + IMG_POSTED, 'wb').write(content)
        #     content = jsonable_encoder(res)
        #     return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=content)
        nparr = np.frombuffer(content, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        # cv2.imwrite('init.jpg', img)
        response = self.proces_image(img)
        if response is None:
            response = False
            # response = {'message': '¿Estas seguro de que subiste una identificaion?'}
        return response
