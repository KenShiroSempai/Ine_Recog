'''
En este archivo estan los puntos clave para la deteccion de los documentos.
Para añadir un documento nuevo, se debe de agregar un nuevo elemento a KPS_PER_TEMPLATE
y si es un documento nuevo, se debe de agregar un nuevo elemento a ID_NAME
'''
DOCUMENTS = {}
# KPS_PER_TEMPLATE Guarda los puntos clave de cada template con su respectivo nombre
# KPS_PER_TEMPLATE_ = {'template_0.jpeg': [(998, 826), (1568, 924), (600, 320), (1330, 588)],
#                      'ine0.jpeg': [(998, 826), (1568, 924), (600, 320), (1330, 588)],
#                      'ine1.1.jpeg': [(1010, 866), (1568, 952), (630, 350), (1310, 606)],
#                      'ine1.jpeg': [(1010, 866), (1568, 952), (630, 350), (1310, 606)],
#                      'edoMex.jpg': [(626, 310), (1540, 450), (626, 450), (1540, 822)],
#                      'ife.jpeg': [(20, 866), (1022, 934), (0, 364), (730, 579)],
#                      'lic.jpeg': [(256, 2508), (1310, 3050), (292, 1514), (1707, 1850)],
#                      'edoMex1.jpg': [(686, 310), (1540, 450), (686, 450), (1540, 802)]
#                      }
KPS_PER_TEMPLATE = {'template_0.jpeg': {'Name': [(600, 320), (1330, 588)],
                                        'Cve': [(998, 826), (1568, 924)],
                                        'Face': [(150, 400), (700, 1200)]},
                    'ine0.jpeg': {'Name': [(600, 320), (1330, 588)],
                                  'Cve': [(998, 826), (1568, 924)],
                                  'Face': [(150, 400), (700, 1200)]},
                    'ine1.1.jpeg': {'Name': [(630, 350), (1310, 606)],
                                    'Cve': [(1010, 866), (1568, 952)],
                                    'Face': [(200, 350), (630, 950)]},
                    'ine1.jpeg': {'Name': [(630, 350), (1310, 606)],
                                  'Cve': [(1010, 866), (1568, 952)],
                                  'Face': [(200, 350), (630, 950)]},
                    'edoMex.jpg': {'Name': [(626, 450), (1540, 822)],
                                   'Cve': [(626, 310), (1540, 450)],
                                   'Face': [(100, 300), (626, 900)]},
                    'ife.jpeg': {'Name': [(0, 364), (730, 579)],
                                 'Cve': [(20, 866), (1022, 934)],
                                 'Face': [(400, 400), (800, 800)]},
                    'lic.jpeg': {'Name': [(292, 1514), (1707, 1850)],
                                 'Cve': [(256, 2508), (1310, 3050)],
                                 'Face': [(400, 400), (800, 800)]},
                    'edoMex1.jpg': {'Name': [(686, 450), (1540, 802)],
                                    'Cve': [(686, 310), (1540, 450)],
                                    'Face': [(100, 300), (626, 900)]},
                    }
# ID_NAME Guarda el nombre formal del documento y a que template pertenece
ID_NAME = {'INE': ['template_0.jpeg', 'ine0.jpeg', 'ine1.1.jpeg', 'ine1.jpeg'],  'IFE': [
    'ife.jpeg'], 'LIC': ['lic.jpeg'], 'LIC EdoMex': ['edoMex0.jpg', 'edoMex.jpg', 'edoMex1.jpg']}
