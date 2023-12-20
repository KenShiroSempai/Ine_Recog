from utils.BlackList import NAME, CVE
from utils.KeyPoints import ID_NAME
from typing import List, Tuple, Dict
import numpy as np
import easyocr
import re


class Text:
    def __init__(self):
        self.reader = easyocr.Reader(['es'], gpu=False)

    def extractT(self, roi: np.ndarray) -> Tuple[List[str], np.ndarray]:
        """
        Extract text from specific boxes.
        We pass as an argument the already cropped image and the points
        where you want to extract text, it is not similar to the one above
        because they are different methods.

        Parameters:
        aligned (np.ndarray): The already cropped image.

        Returns:
        text (list): The extracted text from the image.
        """
        # rgb = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)
        # cv2.imwrite('Roi.jpg', rgb)
        ocr_result = self.reader.readtext(roi)
        text = self.removeLabel(ocr_result)
        return text

    def removeLabel(self, ocr_result: List[List]) -> List[str]:
        """
        Removes labels from the OCR result.

        Parameters:
        ocr_result (List[List]): The result from OCR.

        Returns:
        text (List[str]): The text without labels.
        """
        bigger = 0
        scale = (11/13)
        text = []
        for result in ocr_result:
            height = np.sum(np.subtract(result[0][2], result[0][1]))
            if height > bigger:
                if height*scale > bigger:
                    text.clear()
                bigger = height
            if height > bigger*scale:
                text.append(result[1])
        return text

    def makeResponse(self, name: List[str], cve: str, doc: str) -> Dict[str, str]:
        """
        Creates a response dictionary.

        Parameters:
        name (List[str]): The name.
        cve (str): The cve.
        doc (str): The document.

        Returns:
        res (Dict[str, str]): The response dictionary.
        """
        filename = cve + '.jpg'
        names = ""
        for aux in name[2:len(name)]:
            names += (aux + " ")
        for each in ID_NAME:
            if doc in ID_NAME[each]:
                doc = each
                break
        res = {
            'paterno': name[0],
            'materno': name[1],
            'nombre': names,
            'filename': filename,
            'clave': cve,
            'documento': doc
        }
        # logRecognition(doc, name[0], name[1], names, cve, filename)
        return res

    def filterName(self, name: List[str], doc: str) -> List[str]:
        """
        Filters the name.

        Parameters:
        name (List[str]): The name.
        doc (str): The document.

        Returns:
        filtered (List[str]): The filtered name.
        """
        if doc == 'lic.jpeg':
            nameTmp = []
            lenName = len(name) - 1
            for i in range(lenName):
                nameTmp.append(name[lenName-i])
            name = nameTmp
        newName = []
        for tmp in name:
            for tmp2 in tmp.split():
                if len(tmp2) > 2:
                    newName.append(self.preprocess_ocr_output(tmp2).upper())
        tmpName = [x for x in newName if x not in NAME]
        regex = re.compile(r'^NO+[A-Z]+RE$')
        filtered = [i for i in tmpName if ((not regex.match(i)))]
        return filtered

    def filterCve(self, cve, pat) -> str:
        list1 = [x for x in cve if len(x) > 7]
        # list1 = [ele for ele in cve if len(ele) > 4]
        list1 = [ele for ele in list1 if ele not in CVE]
        newCve = ""
        for aux in list1:
            if aux != " ":
                newCve += aux
        if (len(newCve) < 15):
            return ""
        return newCve

    def preprocess_ocr_output(self, text: str) -> str:
        output = text
        output = re.sub(r"1(?![\s%])(?=\w+)", "I", output)
        output = re.sub(r"(?<=\w)(?<![\s+\-])1", "I", output)
        output = re.sub(r"I(?!\s)(?=[\d%])", "1", output)
        output = re.sub(r"(?<=[+\-\d])(?<!\s)I", "1", output)
        return output
