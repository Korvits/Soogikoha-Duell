def failist_listi(andmefail):
    fail = open(andmefail, encoding="UTF-8")

    soogikohad = []

    for rida in fail:
        soogikohad.append(rida.strip())
    fail.close()
    return soogikohad
