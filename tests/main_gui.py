import tkinter as tk 

def söögikohad_failist(failinimi): #alg koodist lihtsalt
    söögikohad = []
    with open(failinimi, 'r', encoding="utf-8") as fail:
        for rida in fail:
            söögikohad.append(rida.strip())
    return söögikohad

söögikohad = söögikohad_failist("soogikohad.txt")

def esita_küsimus(): 
    global söögikoht_indeks, kasutaja_indeks
    if söögikoht_indeks < len(söögikohad):
        küsimus_label.config(text=f"Kasutaja {kasutaja_indeks + 1}, kas sulle meeldib söögikoht '{söögikohad[söögikoht_indeks]}'?")
        küsimus_label.pack(pady=20)
        jah_nupp.pack(side="left", padx=10) #kus nupud paiknevad
        ei_nupp.pack(side="right", padx=10)
    else:
        if kasutaja_indeks == 0:
            kasutaja_indeks = 1
            söögikoht_indeks = 0
            alusta2_start()
        else:
            ühised_söögikohad()

def salvesta_vastus(vastus): #salvestab vastused, et jah on 1 ja ei 0 yk
    global söögikoht_indeks, kasutaja_indeks
    if vastus == "jah":
        kasutaja_vastused[kasutaja_indeks].append(1)
    elif vastus == "ei":
        kasutaja_vastused[kasutaja_indeks].append(0)
    söögikoht_indeks += 1
    esita_küsimus()

def ühised_söögikohad(): 
    ühised = [söögikohad[i] for i in range(len(söögikohad)) if kasutaja_vastused[0][i] == 1 and kasutaja_vastused[1][i] == 1]
    if ühised:
        tulemus_label.config(text="Söögikohad, mis meeldivad mõlemale:\n" + "\n".join(ühised))
    else:
        tulemus_label.config(text="Pole ühtegi ühist söögikohta, mis mõlemale meeldiks :(")
    küsimus_label.pack_forget()
    jah_nupp.pack_forget() #remob nupud ja küsimused ära, et lõpp oleks clean
    ei_nupp.pack_forget()
    tulemus_label.pack(pady=20) #phm lisab tühikud labeli ümber, et oleks clean, ruumilisus(?)

def alusta():
    global tervitus_label, nupp #see global phm selleks et ma saaks muuta siin funktsioonis mingit eelnevat funktsiooni v muutujat vms
    tervitus_label.pack_forget()  # Eemaldame tervituslabeli
    nupp.pack_forget()  # Eemaldame alustamise nupu
    esita_küsimus()

def alusta2_start():  # Teisele kasutajale lisame eraldi nupu ja teksti
    global nupp2, kasutaja2_label
    
    küsimus_label.pack_forget() #eemaldab jah ja ei nupud mis enne ekraanil olid
    jah_nupp.pack_forget() #pack ongi see, et ta phm paigutab end täpselt sellesse hüpikaknasse ja ei muutu, kui vahetan akna suurust, see bad tho, vaja muuta
    ei_nupp.pack_forget()
    nupp.pack_forget()

    kasutaja2_label = tk.Label(window, text="Kasutaja 2, nüüd on sinu kord vastata!", background="#ADD8E6")
    kasutaja2_label.pack(pady=20)
    nupp2 = tk.Button(window, text="Alustame", command=kasutaja2_alustab, background="white", foreground="black")
    nupp2.pack(pady=20)

def kasutaja2_alustab(): #phm selleks, et kui ta vajutanud nupuleja küsimused ss remome nupu jne
    global nupp2, kasutaja2_label
    # Eemaldame "Alustame" nupu ja teise kasutaja teksti
    kasutaja2_label.pack_forget()
    nupp2.pack_forget()
    esita_küsimus()  # Alustab küsimustega teise kasutaja jaoks

def main():
    global söögikohad, kasutaja_vastused, kasutaja_indeks, söögikoht_indeks
    global window, küsimus_label, tulemus_label, tervitus_label, nupp, jah_nupp, ei_nupp
    failinimi = "soogikohad.txt"
    söögikohad = söögikohad_failist(failinimi)

    kasutaja_vastused = [[], []]
    kasutaja_indeks = 0
    söögikoht_indeks = 0

    window = tk.Tk()
    window.title("Söögikoha duell")
    window.config(background="#ADD8E6") #helesinine värv, saab muuta

    tervitus_label = tk.Label(window, text="Kas tunnete tihti, et ei suuda jõuda kokkuleppele, kuhu Tartus sööma minna?\nLas ma aitan Teid!", background="#ADD8E6", wraplength=400)
    #see wraplength eelmisel real määrab phm, et kui pikalt tekst jookseb enne teisele reale minemist, praegu peaks olema täpselt akna ulatuses
    tervitus_label.pack(pady=20)

    nupp = tk.Button(window, text="Kas alustame?", command=alusta, background="white", foreground="black")
    nupp.pack(pady=20)

    küsimus_label = tk.Label(window, text="", background="#ADD8E6", wraplength=400)
    jah_nupp = tk.Button(window, text="Jah", command=lambda: salvesta_vastus("jah"), background="white", foreground="black")
    ei_nupp = tk.Button(window, text="Ei", command=lambda: salvesta_vastus("ei"), background="white", foreground="black")
#see lambda paneb phm nupu tööle, kui annad talle mingi ülesande
    tulemus_label = tk.Label(window, text="", wraplength=400, background="#ADD8E6")

    window.mainloop()

if __name__ == "__main__":
    main()

