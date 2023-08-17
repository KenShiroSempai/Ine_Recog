'''
GLOBAL PATHS
'''
IMGPATH = 'img/'
LOGPATH = IMGPATH + 'log/'
SUCCESSPATH = IMGPATH + 'success/'
FAILPATH = IMGPATH + 'fail/'
FILEPATH = IMGPATH + 'file/'
'''
DIC OF TEMPLATES AND HIS IMPORTANT POINTS
'''
TEMPLATE = 'templates/'
TEMPLATES = {'template_0.jpeg': [(499, 413), (784, 462), (300, 160), (665, 294)],
             'ine0.jpeg': [(499, 413), (784, 462), (300, 160), (665, 294)],
             'ine1.1.jpeg': [(505, 433), (784, 476), (315, 175), (655, 303)],
             'ine1.jpeg': [(505, 433), (784, 476), (315, 175), (655, 303)],
             'ife.jpeg': [(10, 433), (511, 472), (0, 182), (365, 289)],
             'lic.jpeg': [(128, 1254), (655, 1525), (146, 757), (854, 945)]
             }
NAMEBLACKLIST = ['NOMBRE', 'NONBRE', 'NCMPRE']
CVEBLACKLIST = ['ELECTOR', 'RFC', 'CURP']
KEEPPERCENTS = [2000, 2250, 2500]
