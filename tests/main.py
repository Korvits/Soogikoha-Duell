def soogikohad_failist(failinimi):  #Loeb soogikohad failist järjendisse

    soogikohad = []
    fail = open(failinimi, encoding="UTF-8")
    for rida in fail:
        soogikohad.append(rida.strip())
    return soogikohad

def küsimine(soogikoht): #Küsib kasutajalt kas talle meedlib ette antud söögikoht
    
    vastus = input(f"Kas sulle meeldib söögikoht '{soogikoht}'? (jah/ei): ").strip().lower()
    if vastus == "jah":
        return 1
    elif vastus == "ei":
        return 0
    else:
        print("Vigane sisend, palun sisesta 'jah' või 'ei'.")
        return küsimine(soogikoht)

def kasutajate_vastused(soogikohad, kasutaja_nr): #Kasutab eelnevat funktsiooni, et ükshaaval küsida kõik söögikohad läbi ja salvestada vastused järjendisse
    
    print(f"Kasutaja {kasutaja_nr}, sisesta oma eelistused.")
    vastused = []

    for soogikoht in soogikohad:
        print(f"\nSöögikoht: {soogikoht}")
        vastus = küsimine(soogikoht)  
        vastused.append(vastus)
        
    return vastused

def ühine_söögikoht(soogikohad, kasutaja_1, kasutaja_2): #Võrdleb järjendeid, et leida sobivad söögikohad ja esitab need ekraanile
    
    print("\nSöögikohad, mis meeldivad mõlemale on: ")
    for i in range(len(soogikohad)):
        if kasutaja_1[i] == 1 and kasutaja_2[i] == 1:
            print(f"-{soogikohad[i]}")


def main():
    failinimi = 'soogikohad.txt'  
    soogikohad = soogikohad_failist(failinimi)
    
    kasutaja_1 = kasutajate_vastused(soogikohad, 1)
    kasutaja_2 = kasutajate_vastused(soogikohad, 2)
    ühine_söögikoht(soogikohad, kasutaja_1, kasutaja_2) 


if __name__ =="__main__":
    main()

