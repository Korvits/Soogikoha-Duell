import tkinter as tk
import ttkbootstrap as tb
from PIL import Image, ImageTk

def söögikohad_failist(failinimi): #alg koodist lihtsalt
    söögikohad = []
    with open(failinimi, 'r', encoding="UTF-8") as fail:
        for rida in fail:
            söögikohad.append(rida.strip())
    return söögikohad

def alusta():
    global tervitus_label, nupp #see global phm selleks et ma saaks muuta siin funktsioonis mingit eelnevat funktsiooni v muutujat vms
    tervitus_label.grid_forget()  # Eemaldame tervituslabeli
    nupp.grid_forget()  # Eemaldame alustamise nupu
    esita_küsimus()

def esita_küsimus(): 
    global söögikoht_indeks, kasutaja_indeks, jah_nupp, ei_nupp, img_label, img_list
    if söögikoht_indeks < len(söögikohad):
        küsimus_label.config(text=f"Kasutaja {kasutaja_indeks + 1}, kas sulle meeldib söögikoht '{söögikohad[söögikoht_indeks]}'?")
        küsimus_label.grid(row=1, column=1, columnspan=1, padx=15, pady=15)
        jah_nupp.grid(row=2, column=2, columnspan=1, padx=15, pady=15)
        ei_nupp.grid(row=2, column=0, columnspan=1, padx=15, pady=15)
        
        window.bind("<Right>", lambda x:[salvesta_vastus("jah"), pilt_edasi(3)]) # Saab noolteks jah või ei panna
        window.bind("<Left>", lambda x:[salvesta_vastus("ei"), pilt_edasi(3)])
    else:
        if kasutaja_indeks == 0:
            kasutaja_indeks = 1
            söögikoht_indeks = 0
            img_label.config(image=img_list[0])
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

def alusta2_start():  # Teisele kasutajale lisame eraldi nupu ja teksti
    global nupp2, kasutaja2_label
    
    küsimus_label.grid_forget() #eemaldab jah ja ei nupud mis enne ekraanil olid
    jah_nupp.grid_forget() 
    ei_nupp.grid_forget()
    nupp.grid_forget()

    kasutaja2_label = tb.Label(window, text="Kasutaja 2, nüüd on sinu kord vastata!", bootstyle="white")
    kasutaja2_label.grid(row=1, column=1, columnspan=1, padx=15, pady=15)
    
    nupp2 = tb.Button(window, text="Alustame", command =lambda: [kasutaja2_alustab(), pilt_edasi(2)], bootstyle="primary, outline")
    nupp2.grid(row=2, column=1, columnspan=1, padx=15, pady=15)
    
    window.unbind("<Right>")
    window.unbind("<Left>")

def kasutaja2_alustab(): #phm selleks, et kui ta vajutanud nupuleja küsimused ss remome nupu jne
    global nupp2, kasutaja2_label
    # Eemaldame "Alustame" nupu ja teise kasutaja teksti
    kasutaja2_label.grid_forget()
    nupp2.grid_forget()
    esita_küsimus()  # Alustab küsimustega teise kasutaja jaoks

def ühised_söögikohad(): 
    ühised = [söögikohad[i] for i in range(len(söögikohad)) if kasutaja_vastused[0][i] == 1 and kasutaja_vastused[1][i] == 1]
    if ühised:
        tulemus_label.config(text="Söögikohad, mis meeldivad mõlemale:\n" + "\n".join(ühised))
    else:
        tulemus_label.config(text="Pole ühtegi ühist söögikohta, mis mõlemale meeldiks :(")
    küsimus_label.grid_forget()
    jah_nupp.grid_forget() #remob nupud ja küsimused ära, et lõpp oleks clean
    ei_nupp.grid_forget()
    img_label.grid_forget()
    tulemus_label.grid(row=2, column=1, columnspan=1, padx=15, pady=15) 

def pilt_edasi(pildi_nr):
    global img_label, jah_nupp, ei_nupp, img_list
    if pildi_nr > len(img_list): # Kontrollib kas listis on veel pilte
        return
    img_label.config(image=img_list[pildi_nr - 1])
    
    jah_nupp.config(command=lambda: [salvesta_vastus("jah"), pilt_edasi(pildi_nr + 1)]) #Muudab nuppude funktsioone peale igat vajutust
    ei_nupp.config(command=lambda: [salvesta_vastus("ei"), pilt_edasi(pildi_nr + 1)])
    window.bind("<Right>", lambda x:[salvesta_vastus("jah"), pilt_edasi(pildi_nr + 1)]) #Sama asi, aga noole nuppudele
    window.bind("<Left>", lambda x:[salvesta_vastus("ei"), pilt_edasi(pildi_nr + 1)])
    
def main():
    global söögikohad, kasutaja_vastused, kasutaja_indeks, söögikoht_indeks
    global window, küsimus_label, tulemus_label, tervitus_label, nupp, jah_nupp, ei_nupp
    global img_label, img_list
    
    failinimi = "soogikohad.txt"
    söögikohad = söögikohad_failist(failinimi)
    
    

    kasutaja_vastused = [[], []]
    kasutaja_indeks = 0
    söögikoht_indeks = 0

    window = tb.Window(themename='superhero')
    window.title("Söögikoha duell")
    window.iconbitmap("images\logo.ico")
    
    my_img1 = Image.open("images/Logo.jpg").resize((640, 640))
    my_img1 = ImageTk.PhotoImage(my_img1)

    my_img2 = Image.open("images/Vapiano.png").resize((640, 640))
    my_img2 = ImageTk.PhotoImage(my_img2)

    my_img3 = Image.open("images/el_chapo.png").resize((640, 640))
    my_img3 = ImageTk.PhotoImage(my_img3)

    my_img4 = Image.open("images/kebaba.png").resize((289, 512))
    my_img4 = ImageTk.PhotoImage(my_img4)

    my_img5 = Image.open("images/kampus.png").resize((600, 400))
    my_img5 = ImageTk.PhotoImage(my_img5)

    my_img6 = Image.open("images/la_dolce_vita.png").resize((594, 281))
    my_img6 = ImageTk.PhotoImage(my_img6)

    my_img7 = Image.open("images/krempel.png").resize((640, 640))
    my_img7 = ImageTk.PhotoImage(my_img7)

    my_img8 = Image.open("images/mcdonalds.png").resize((640, 640))
    my_img8 = ImageTk.PhotoImage(my_img8)

    my_img9 = Image.open("images/burger_king.png").resize((600, 330))
    my_img9 = ImageTk.PhotoImage(my_img9)

    my_img10 = Image.open("images/kolm_tilli.png").resize((550, 366))
    my_img10 = ImageTk.PhotoImage(my_img10)

    my_img11 = Image.open("images/Pazzo.png").resize((554, 308))
    my_img11 = ImageTk.PhotoImage(my_img11)
    
    img_list = [my_img1, my_img2, my_img3, my_img4, my_img5, my_img6, my_img7, my_img8, my_img9, my_img10, my_img11]
        
    
    img_label = tb.Label(image=my_img1)
    img_label.grid(row=0, column=0, columnspan=3) #Kuvab pildi

    
    tervitus_label = tb.Label(window, text="Kas tunnete tihti, et ei suuda jõuda kokkuleppele, kuhu Tartus sööma minna?\nLas ma aitan Teid!", bootstyle="white")
    tervitus_label.grid(row=1, column=1, columnspan=1, padx=15, pady=15) # Kuvab algse küsimuse

    nupp = tb.Button(window, text="Kas alustame?", command=lambda: [alusta(), pilt_edasi(2)], bootstyle="primary, outline")
    nupp.grid(row=2, column=1, columnspan=1, padx=15, pady=15)

    küsimus_label = tb.Label(window, text="", bootstyle="white", wraplength=400)
    tulemus_label = tb.Label(window, text="", bootstyle="white", wraplength=400)
    jah_nupp = tb.Button(window, text="Jah", bootstyle="success", command=lambda:[salvesta_vastus("jah"), pilt_edasi(3)])
    ei_nupp = tb.Button(window, text="Ei", bootstyle="danger", command=lambda:[salvesta_vastus("ei"), pilt_edasi(3)])
    

    window.mainloop()

if __name__ == "__main__":
    main()

