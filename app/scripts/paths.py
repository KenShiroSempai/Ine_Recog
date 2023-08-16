import os
from extras.globalData import LOGPATH
from csv import writer
from datetime import datetime


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
