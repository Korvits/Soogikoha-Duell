def soogikohad_failist(failinimi): 

    soogikohad = []
    with open(failinimi, 'r') as f:
        for rida in f:
            soogikohad.append(rida.strip())
    return soogikohad

def küsimine(soogikoht):
    
    vastus = input(f"Kas sulle meeldib söögikoht '{soogikoht}'? (jah/ei): ").strip().lower()
    if vastus == "jah":
        return 1
    elif vastus == "ei":
        return 0
    else:
        print("Vigane sisend, palun sisesta 'jah' või 'ei'.")
        return küsimine(soogikoht)

def kasutajate_vastused(soogikohad, kasutaja_nr):
    
    print(f"Kasutaja {kasutaja_nr}, sisesta oma eelistused.")
    vastused = []

    
    for soogikoht in soogikohad:
        print(f"\nSöögikoht: {soogikoht}")
        vastus = küsimine(soogikoht)  
        vastused.append(vastus)

    
    return vastused

def ühine_söögikoht(soogikohad, kasutaja_1, kasutaja_2):
    
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


main()

