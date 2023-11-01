from extras.const import TEMPLATES, TEMPLATE, KEEPPERCENTS
import cv2
import imutils
from scripts.file_recognition.images import imageAlignment
from scripts.file_recognition.ocr import extractT
from scripts.file_recognition.strings import filterCve, filterName, makeResponse


templateList = []
orbs = []
matcher = cv2.DescriptorMatcher_create(
    cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING
)


def make_orbs():
    for maxFeatures in KEEPPERCENTS:
        aux = cv2.ORB_create(maxFeatures)
        orbs.append(aux)


def makeList():
    for orb in orbs:
        orb_list = []
        for template in TEMPLATES:
            image = cv2.imread(TEMPLATE + template)
            image = imutils.resize(image, width=2000)
            imgGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            (kpsB, descsB) = orb.detectAndCompute(imgGray, None)
            orb_list.append([imgGray, template, (kpsB, descsB)])
        templateList.append(orb_list)


def findTemplate(imgGray):
    templates = []
    for ob, template in zip(orbs, templateList):
        (kpsA, descsA) = ob.detectAndCompute(imgGray, None)
        for each in template:
            (kpsB, descsB) = each[2]
            matches = matcher.match(descsA, descsB, None)
            matches = sorted(matches, key=lambda x: x.distance)
            templates.append([each, matches, (kpsA, descsA)])
            # return each, matches, (kpsA, descsA)
        response = proces_obs_list(templates, imgGray)
        if response is not None:
            return response
    return None


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
    # cv2.imwrite('final.jpg', finalImage)
    # if (len(cve) == 0):
    #     continue
    cve = filterCve(cve, name[0])
    if (len(name) > 1 and len(cve) > 8):
        response = makeResponse(
            name, cve, template)
    return response


def proces_obs_list(templates, image):
    response = None
    for template, matches, kps in templates:
        print(template[1])
        aligned = imageAlignment(image, template, matches, kps)
        if response is not None:
            cv2.imwrite('imgAPI/1.jpg', aligned)
            break
        response = procesAligned(aligned, template[1])
    return response


def init():
    make_orbs()
    makeList()


init()
