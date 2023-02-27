
def listOfTag(ini,fin):
    print(str(ini) + "" +str(fin))
    filePath = "app/Bitacora/tag.txt"
    f = open(filePath, "a")
    for aux in range(ini,fin): 
        f.write(str(aux-ini)+" - "+"11223344"+str(hex(aux+65536)).replace("x","") +"8899001122"+" - "+ str(aux)+" - "+ str(aux+65536)+ " -  "+ "naranja"+ " - "+ "enramada\n")
        # print(str(aux-ini)+" - "+"11223344"+str(hex(aux+65536)).replace("x","") +"8899001122"+" - "+ str(aux)+" - "+ str(aux+65536)+ " -  "+ "naranja"+ " - "+ "enramada")
    f.close()
