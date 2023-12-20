import os
from extras.const import LOGPATH, IMGPATH, DEFAULID
from csv import writer
from datetime import datetime
import fnmatch


def createPath(newPath):
    try:
        os.makedirs(newPath, exist_ok=True)
    except Exception as e:
        logExeption(e, "app/paths/log.createPath")


def logExeption(e, fun):
    lista = []
    time = datetime.now()
    lista.extend([time, e, fun])
    writeLog(lista, 'logException.csv')


def logRecognition(doc, pat, mat, nom, cve, filename):
    lista = []
    time = datetime.now()
    lista.extend([time, doc, pat, mat, nom, cve, filename])
    writeLog(lista, 'logRecognition.csv')


def writeLog(list, filename):
    with open(LOGPATH + filename, 'a') as f_object:
        writer_object = writer(f_object)
        writer_object.writerow(list)
        f_object.close()


def createDatePath(basePath):
    today = datetime.now()
    year = str(today.year)
    month = str(today.month)
    day = str(today.day)
    time = str(today.strftime("%H%M%S%f"))
    newPath = basePath + year + '/' + month + '/' + day + '/'
    createPath(newPath)
    return newPath + time[:9] + '_'


def createIDPath(cve, date):
    if date is not None:
        year = str(date.year)
        month = str(date.month)
        day = str(date.day)
        newPath = IMGPATH + year + '/' + month + '/' + day + '/'
        patern = '*' + cve + '.jpg'
        idpaht = find(patern, newPath)
        if len(idpaht) > 0:
            return idpaht[0]
        idpaht = find(patern, IMGPATH)
        if len(idpaht) > 0:
            return idpaht[0]
    return DEFAULID


def find(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result
