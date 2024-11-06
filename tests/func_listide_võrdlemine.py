def listide_võrdlemine(inimene1, inimene2):
    tulemus = [] 
    for i in range(len(inimene1)):
        if inimene1[i] == inimene2[i] == 1:
            tulemus.append(1)
        else:
            tulemus.append(0)
    return tulemus        
