import cv2
import imutils
import numpy as np
from utils.Constants import KEEPPERCENTS, KEEPPERCENT, TEMPLATES_PATH
from utils.KeyPoints import KPS_PER_TEMPLATE
from .Text import Text
from utils.FileName import IMG_FINAL, IMG_FACE, IMG_ALIGNED
from utils.Constants import IMGPATH
from typing import List, Tuple
from utils.Colors import RED


class ImgRecognizer(Text):
    def __init__(self):
        super().__init__()
        # Initialize the ID recognition model
        self.orbs = []
        self.templateList = []
        self.matcher = cv2.DescriptorMatcher_create(
            cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING)
        self.__make_orbs__()
        self.__make_template_list__()

    def __make_orbs__(self):
        for maxFeatures in KEEPPERCENTS:
            aux = cv2.ORB_create(maxFeatures)
            self.orbs.append(aux)

    def __make_template_list__(self) -> list:
        for orb in self.orbs:
            orb_list = []
            for template in KPS_PER_TEMPLATE:
                img = cv2.imread(TEMPLATES_PATH + template)
                img = imutils.resize(img, width=2000)
                imgGray = cv2.cvtColor(img.copy(), cv2.COLOR_BGR2GRAY)
                (kpsB, descsB) = orb.detectAndCompute(imgGray, None)
                orb_list.append([imgGray, template, (kpsB, descsB), img])
            self.templateList.append(orb_list)

    def imageAlignment(self, image, template, matches, kps) -> np.ndarray:
        # Nos quedamos solo con cierto porcentaje
        keep = int(len(matches) * KEEPPERCENT)
        matches = matches[:keep]
        # Visualizamos los puntos
        matchedVis = cv2.drawMatches(
            template[3],
            template[2][0],
            image,
            kps[0],
            matches,
            None
        )
        cv2.imwrite(IMGPATH + IMG_ALIGNED, matchedVis)
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
        # cv2.imwrite('imgAPI/3.jpg', aligned)
        return aligned

    def procesAligned(self, aligned, template) -> dict:
        response = None
        points_list = KPS_PER_TEMPLATE[template]
        # Change for new anotation
        img_name = self.cut_img_by_points(aligned, points_list['Name'])
        name = self.extractT(img_name)
        name = self.filterName(name, template)
        if (len(name) < 3):
            return response
        img_cve = self.cut_img_by_points(aligned, points_list['Cve'])
        cve = self.extractT(img_cve)
        # if (len(cve) == 0):
        #     continue
        cve = self.filterCve(cve, name[0])
        if (len(name) > 1 and len(cve) > 8):
            response = self.makeResponse(
                name, cve, template)
        img_face = self.cut_img_by_points(aligned, points_list['Face'])
        cv2.imwrite(IMGPATH + IMG_FACE, img_face)
        cv2.imwrite(IMGPATH + IMG_FINAL, aligned)
        return response

    def match_templates(self, imgGray) -> list:
        templates = []
        for ob, template in zip(self.orbs, self.templateList):
            (kpsA, descsA) = ob.detectAndCompute(imgGray, None)
            for each in template:
                (kpsB, descsB) = each[2]
                matches = self.matcher.match(descsA, descsB, None)
                matches = sorted(matches, key=lambda x: x.distance)
                templates.append([each, matches, (kpsA, descsA)])
        return templates

    def cut_img_by_points(self, img: np.ndarray, points: List[Tuple[int, int]]) -> np.ndarray:
        """
        Cuts an image by given points.

        Parameters:
        img (np.ndarray): The image to be cut.
        points (List[Tuple[int, int]]): A list of tuples where each tuple is a point (x, y).

        Returns:
        roi (np.ndarray): The cut image.
        """
        point1 = points[0]
        point2 = points[1]
        height = point2[1] - point1[1]
        width = point2[0] - point1[0]
        roi = img[
            point1[1]: point1[1] + height,
            point1[0]: point1[0] + width
        ]
        cv2.rectangle(img, point1, point2, RED)
        return roi
