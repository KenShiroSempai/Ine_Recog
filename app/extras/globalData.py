'''
GLOBAL PATHS
'''
IMGPATH = 'img/'
LOGPATH = IMGPATH + 'log/'
SUCCESSPATH = IMGPATH + 'success/'
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
TEMPLATES = {'template_0.jpeg': [(499, 413), (784, 462), (300, 160), (665, 294)],
             'ine0.jpeg': [(499, 413), (784, 462), (300, 160), (665, 294)],
             'ine1.1.jpeg': [(505, 433), (784, 476), (315, 175), (655, 303)],
             'ine1.jpeg': [(505, 433), (784, 476), (315, 175), (655, 303)],
             'edoMex.jpg': [(290, 155), (690, 225), (290, 205), (690, 411)],
             'ife.jpeg': [(10, 433), (511, 472), (0, 182), (365, 289)],
             'lic.jpeg': [(128, 1254), (655, 1525), (146, 757), (854, 945)],
             'edoMex0.jpg': [(348, 155), (690, 225), (340, 205), (690, 411)],
             'edoMex1.jpg': [(348, 155), (690, 225), (340, 205), (690, 411)]
             }
TEMPLATE_NAME = {'INE': ['template_0.jpeg', 'ine0.jpeg'], 'INE_2021': [
    'ine1.1.jpeg', 'ine1.jpeg'], 'IFE': ['ife.jpeg'], 'LIC': ['lic.jpeg'], 'LIC EdoMex': ['edoMex0.jpg', 'edoMex.jpg', 'edoMex1.jpg']}
NAMEBLACKLIST = ['NOMBRE', 'NONBRE', 'NCMPRE', 'NOMBREIS', 'ACELUOO', 'PATEANO', 'APELUDO', 'MATEANO:',
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
