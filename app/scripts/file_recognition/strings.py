from extras.const import TEMPLATE_NAME, NAMEBLACKLIST, CVEBLACKLIST
import numpy as np
import re


def makeResponse(name, cve, doc):
    filename = cve + '.jpg'
    names = ""
    for aux in name[2:len(name)]:
        names += (aux + " ")
    for each in TEMPLATE_NAME:
        if doc in TEMPLATE_NAME[each]:
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


def removeLabel(ocr_result):
    bigger = 0
    scale = (10/13)
    text = []
    for result in ocr_result:
        if len(result[1]) < 3:
            continue
        height = np.sum(np.subtract(result[0][2], result[0][1]))
        if height > bigger:
            if height*scale > bigger:
                text.clear()
            bigger = height
        if height > bigger*scale:
            text.append(result[1])
    return text


def filterName(name, doc):
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
                newName.append(preprocess_ocr_output(tmp2).upper())
    tmpName = [x for x in newName if x not in NAMEBLACKLIST]
    regex = re.compile(r'^NO+[A-Z]+RE$')
    filtered = [i for i in tmpName if ((not regex.match(i)))]
    return filtered


def filterCve(cve, pat):
    list1 = [x for x in cve if len(x) > 7]
    # list1 = [ele for ele in cve if len(ele) > 4]
    list1 = [ele for ele in list1 if ele not in CVEBLACKLIST]
    newCve = ""
    for aux in list1:
        if aux != " ":
            newCve += aux
    if (len(newCve) < 15):
        return ""
    return newCve


def preprocess_ocr_output(text: str) -> str:
    output = text
    output = re.sub(r"1(?![\s%])(?=\w+)", "I", output)
    output = re.sub(r"(?<=\w)(?<![\s+\-])1", "I", output)
    output = re.sub(r"I(?!\s)(?=[\d%])", "1", output)
    output = re.sub(r"(?<=[+\-\d])(?<!\s)I", "1", output)
    return output