def söögid_failist(failinimi):
    söögid = {}
    with open(failinimi, 'r', encoding="UTF-8") as fail2:
        for rida in fail2:
            osad = rida.strip().split(";")
            söögikoht = osad[0]
            ühe_koha_söögid = osad[1:]
            söögid[söögikoht] = ühe_koha_söögid
    return söögid

söögid = "soogid.txt"
toidud = söögid_failist(söögid)


for i in range(len(toidud["Vapiano"])):
    print(f"-{toidud['Vapiano'][i]}")
