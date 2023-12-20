'''
GLOBAL PATHS
'''
IMGPATH = 'img/'
LOGPATH = IMGPATH + 'log/'
SUCCESSPATH = IMGPATH + 'success/'
BITPATH = 'Bitacora/'
FAILPATH = IMGPATH + 'fail/'
FILEPATH = IMGPATH + 'file/'
DEFAULID = 'templates/empty.jpg'
TEMPLATES_PATH = 'data/templates/'
KEEPPERCENTS = [2000, 2300]
ESSENSIALS_PATHS = [IMGPATH, LOGPATH, SUCCESSPATH, FAILPATH, FILEPATH, BITPATH]

'''
VALUES DEFAUL
'''
NOTD = 'No Disponible'
RECOGFAIL = "EMPTY"
DATAFILE = 'Bitacora/data.json'


MAXFEATURES = 2000
KEEPPERCENT = .2

MIDDLEWARE = {
    '/insideReal/': '/adentro/',
    '/insideReal': '/adentro/',
    '/salidaReal': '/ppOut',
    '/salidaReal/': '/ppOut',
    '/careal': '/logcarless',
    '/careal/': '/logcarless'
}
