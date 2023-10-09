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
'''
DIC OF TEMPLATES AND HIS IMPORTANT POINTS
'''
POINTS = {
    'INE ': ''
}
TEMPLATE = 'templates/'
TEMPLATES = {'template_0.jpeg': [(998, 826), (1568, 924), (600, 320), (1330, 588)],
             'ine0.jpeg': [(998, 826), (1568, 924), (600, 320), (1330, 588)],
             'ine1.1.jpeg': [(1010, 866), (1568, 952), (630, 350), (1310, 606)],
             'ine1.jpeg': [(1010, 866), (1568, 952), (630, 350), (1310, 606)],
             'edoMex.jpg': [(626, 310), (1540, 450), (626, 450), (1540, 822)],
             'ife.jpeg': [(20, 866), (1022, 934), (0, 364), (730, 579)],
             'lic.jpeg': [(256, 2508), (1310, 3050), (292, 1514), (1707, 1850)],
             'edoMex1.jpg': [(686, 310), (1540, 450), (686, 450), (1540, 802)]
             }
TEMPLATE_NAME = {'INE': ['template_0.jpeg', 'ine0.jpeg'], 'INE_2021': [
    'ine1.1.jpeg', 'ine1.jpeg'], 'IFE': ['ife.jpeg'], 'LIC': ['lic.jpeg'], 'LIC EdoMex': ['edoMex0.jpg', 'edoMex.jpg', 'edoMex1.jpg']}
NAMEBLACKLIST = ['NOMBRE', 'NONBRE', 'NCMPRE', 'NOMBREIS', 'ACELUOO', 'PATEANO', 'APELUDO', 'MATEANO:', 'NOMBREIS):', 'INSTITUTO', 'NACIONAL', 'CREDENCIAL', 'VOTAR',
                 'APELLIDO', 'PATERNO', 'MATERNO', 'PATEHNO', 'MATEANO', 'MAIEANO', 'NOVARE(S}', 'PATEHNO:', 'ESTADO', 'DEL', 'MEXICO']
CVEBLACKLIST = ['ELECTOR', 'RFC', 'CURP', 'CLAVE', 'CLAVE DE ELECTOR', 'CUAP']
KEEPPERCENTS = [2000, 2250, 2500]
'''
DATABASE CREDENTIALS
'''
NAME = 'avispa'
HOST = '192.168.2.202'
# HOST = '192.168.100.216'
USER = 'postgres'
PSSW = 'mfmssmcl'
PORT = '5432'
'''
VALUES DEFAUL
'''
NOTD = 'No Disponible'
RECOGFAIL = "EMPTY"
DATAFILE = 'Bitacora/data.json'


MAXFEATURES = 2000
KEEPPERCENT = .2

INSIDE = ['/insideReal/', '/insideReal']
SALIDA = ['/salidaReal', '/salidaReal/']
CARLESS = ['/careal', '/careal/']
