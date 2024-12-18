import tkinter as tk
import ttkbootstrap as tb
from PIL import Image, ImageTk

def söögikohad_failist(failinimi): # Loeb soogikohtade nimetused failist
    söögikohad = []
    with open(failinimi, 'r', encoding="UTF-8") as fail:
        for rida in fail:
            söögikohad.append(rida.strip())
    return söögikohad

def söögid_failist(failinimi): # Loeb söögikohtade söökide valikud failist 
    söögid = {}
    with open(failinimi, 'r', encoding="UTF-8") as fail2:
        for rida in fail2:
            osad = rida.strip().split(";")
            söögikoht = osad[0]
            ühe_koha_söögid = osad[1:]
            söögid[söögikoht] = ühe_koha_söögid
    return söögid

def kuidas_kasutada(): # Loob õpetuse hüpikakna programmile
    lisa_aken = tk.Toplevel(window)
    lisa_aken.title("Kuidas kasutada?")
    lisa_aken.geometry("") #sobitab ise akna suuruse, et kogu ekraanil olev mahuks peale
    lisa_aken.minsize(400,400)
    
    juhend = ""
    try:
        with open("juhend.txt", "r", encoding="utf-8") as fail:
            read = fail.readlines()
            juhend = "\n\n".join(rida.strip() for rida in read if rida.strip())
    except FileNotFoundError:
        pass
        
    if juhend:
        juhend_label = tb.Label(lisa_aken, text=juhend, bootstyle="white", wraplength=380)
        juhend_label.pack(pady=20, padx=20)
        
    juhend_kinni = tb.Button(lisa_aken, text="Sulge juhend", command=lisa_aken.destroy, bootstyle="primary")
    juhend_kinni.pack(pady=10)

def alusta(): # Alustab programmi tööd
    global tervitus_label, nupp 
    tervitus_label.grid_forget() 
    nupp.grid_forget() 
    esita_küsimus()

def esita_küsimus(): # Funktsioon, mis paneb küsimused koos piltidega ja vastuse valikutega ekraanile
    global söögikoht_indeks, kasutaja_indeks
    if söögikoht_indeks < len(söögikohad):
        küsimus_label.config(text=f"'{söögikohad[söögikoht_indeks]}'")
        küsimus_label.grid(row=1, column=1, columnspan=1)
        
        söögid_label.config(text="\n".join(söögid[söögikohad[söögikoht_indeks]]))
        söögid_label.grid(row=2,column=1, columnspan=1, sticky="n")
        
        jah_nupp.grid(row=3, column=2, columnspan=1)
        ei_nupp.grid(row=3, column=0, columnspan=1)
        
        window.bind("<Right>", lambda x:[salvesta_vastus("jah"), pilt_edasi(3)]) # Saab nooltega jah või ei panna
        window.bind("<Left>", lambda x:[salvesta_vastus("ei"), pilt_edasi(3)])
    else:
        if kasutaja_indeks == 0:
            kasutaja_indeks = 1
            söögikoht_indeks = 0
            img_label.config(image=img_list[0])
            alusta2_start()
        else:
            ühised_söögikohad()

def salvesta_vastus(vastus): # Salvestab vastused, et jah on 1 ja ei 0
    global söögikoht_indeks
    if vastus == "jah":
        kasutaja_vastused[kasutaja_indeks].append(1)
    elif vastus == "ei":
        kasutaja_vastused[kasutaja_indeks].append(0)
    söögikoht_indeks += 1
    esita_küsimus()

def alusta2_start():  # Teisele kasutajale lisame eraldi nupu ja teksti
    global nupp2, kasutaja2_label
    
    küsimus_label.grid_forget() #eemaldab koik varasemad nupud ja teksti 
    jah_nupp.grid_forget() 
    ei_nupp.grid_forget()
    nupp.grid_forget()
    söögid_label.grid_forget()
    
    # Kuvab juhatava teksti
    kasutaja2_label = tb.Label(content_frame, text="Kasutaja 2, nüüd on sinu kord vastata!", font=("Arial", 14), bootstyle="white")
    kasutaja2_label.grid(row=1, column=1, columnspan=1)
    
    # Paigutab nupu ekraanile millega saab programmi alustada
    nupp2 = tb.Button(content_frame, text="Alustame", command =lambda: [kasutaja2_alustab(), pilt_edasi(2)], bootstyle="primary, outline")
    nupp2.grid(row=2, column=1, columnspan=1)
    
    # Eemaldab noolte kasutamise võimaluse
    window.unbind("<Right>")
    window.unbind("<Left>")

def kasutaja2_alustab(): # Alustab programmi uuesti 2 kasutaja jaoks
    # Eemaldame "Alustame" nupu ja teise kasutaja teksti
    kasutaja2_label.grid_forget()
    nupp2.grid_forget()
    esita_küsimus()  # Alustab küsimustega teise kasutaja jaoks

def ühised_söögikohad(): # Vaatab millised söögikohad olid ühised ja kuvab need ekraanile
    window.unbind("<Right>")
    window.unbind("<Left>")
    
    ühised = [söögikohad[i] for i in range(len(söögikohad)) if kasutaja_vastused[0][i] == 1 and kasutaja_vastused[1][i] == 1]
    content_frame.destroy()  # Kustutab kõik eelneva ekraanilt
    
    # Loob uue raami, kuhu asjad sisse panna
    new_frame = tb.Frame(window)
    new_frame.pack(expand=True, fill="both")
    
    # Loob canvase, kus saab kasutada scrollwheeli ja muid asju veel
    canvas = tk.Canvas(new_frame)
    # Ilmutab molemad ekraanile
    canvas.pack(side="left", fill="both", expand=True)
    
    #Loob scrollbari
    scrollbar = tb.Scrollbar(new_frame, orient="vertical", command=canvas.yview)
    #Määrab scrollbari canvasele ja määrab scorllimise suuna vertikaalseks
    
    canvas.configure(yscrollcommand=scrollbar.set)
    # Teeb nii, et terve programmi raames saaks scrollida
    canvas.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    
    scrollable_frame = tb.Frame(canvas)
    
    #Loob akna kuhu saame oma pildid ja teksti panna
    canvas.create_window((600, 0), window=scrollable_frame, anchor="n")
    
    #Laseb scrollida hiire mousewheeliga
    canvas.bind("<MouseWheel>", lambda event: canvas.yview_scroll(-int(event.delta / 60), "units"))
    
    # Lisame ühised söögikohad ekraanile
    if ühised:
        tb.Label(scrollable_frame, text="Söögikohad, mis meeldisid mõlemale", font=("Arial", 20, "bold")).pack(pady=20)
        for koht in ühised:
            tb.Label(scrollable_frame, text=koht, font=("Arial", 14)).pack(pady=75)
            tb.Label(scrollable_frame, image=img_list[söögikohad.index(koht)+1]).pack(pady=25)
        scrollbar.pack(side="right", fill="y")
        tb.Button(scrollable_frame, text="EXIT", bootstyle="danger", command=window.destroy).pack(pady=35)
    else:
        tb.Label(scrollable_frame, text="Ei leidunud söögikohti, mis meeldiksid mõlemale!", font=("Arial", 20), bootstyle="red").pack(pady=20)
        tb.Button(scrollable_frame, text="EXIT", bootstyle="danger", command=window.destroy).pack(pady=35)
        canvas.unbind("<MouseWheel>")
        
def pilt_edasi(pildi_nr): # Muudab pilti, mida näidatakse ja confib nuppe, et nad annaksid uusi väärtuseid funktsiooni
    
    if pildi_nr > len(img_list): # Kontrollib kas listis on veel pilte
        return
    img_label.config(image=img_list[pildi_nr - 1]) # Muudab pildi ära
    
    jah_nupp.config(command=lambda: [salvesta_vastus("jah"), pilt_edasi(pildi_nr + 1)]) #Muudab nuppude funktsioone peale igat vajutust, et saaks järgmist pilti listist
    ei_nupp.config(command=lambda: [salvesta_vastus("ei"), pilt_edasi(pildi_nr + 1)])
    
    window.bind("<Right>", lambda x:[salvesta_vastus("jah"), pilt_edasi(pildi_nr + 1)]) #Sama asi, aga noole nuppudele
    window.bind("<Left>", lambda x:[salvesta_vastus("ei"), pilt_edasi(pildi_nr + 1)])
    
def main():
    global söögikohad, kasutaja_vastused, kasutaja_indeks, söögikoht_indeks, content_frame
    global window, küsimus_label, tulemus_label, tervitus_label, nupp, jah_nupp, ei_nupp
    global img_label, img_list
    global söögid, söögid_label
    
    failinimi = "soogikohad.txt"
    söögikohad = söögikohad_failist(failinimi)
    söögid_fail = "soogid.txt"
    söögid = söögid_failist(söögid_fail)

    kasutaja_vastused = [[], []]
    kasutaja_indeks = 0
    söögikoht_indeks = 0
    
    # Loob terve programmi akna, annab sellele tiitli ja määrab ikooni
    window = tb.Window(themename='superhero')
    window.title("Söögikoha duell")
    window.iconbitmap("images\logo.ico")
    
    # Võtab hetkel kasutusel oleva ekraani laiuse ja kõrguse
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Arvutab x ja y koordinaadid, et paigutada programm ekraani keskele
    x = (screen_width / 2) - (1200 / 2)
    y = (screen_height / 2) - (1000 / 2)
    
    # Määrab programmi akna suuruse ja paigutuse ekraanil
    window.geometry(f"1200x1000+{int(x)}+{int(y)-45}")
    
    # Loob raami 
    content_frame = tb.Frame(window)
    content_frame.pack(expand=True, fill="both")
    
    # Määrab kui palju read ja veerud peaksid ruumi endale võtma
    content_frame.grid_rowconfigure(0, weight=1)
    content_frame.grid_rowconfigure(1, weight=1)
    content_frame.grid_rowconfigure(2, weight=1)
    content_frame.grid_rowconfigure(4, weight=1)
    content_frame.grid_columnconfigure(0, weight=1)
    content_frame.grid_columnconfigure(1, weight=1)
    content_frame.grid_columnconfigure(2, weight=1)
    
    # Võtab kõik pildid programmi ja muudab nende suurust
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
    
    # Loob ja kuvab pildi
    img_label = tb.Label(content_frame, image=my_img1)
    img_label.grid(row=0, column=0, columnspan=3) 

    # Loob ja kuvab uvab algse küsimuse
    tervitus_label = tb.Label(content_frame,
                              text="Kas tunnete tihti, et ei suuda jõuda kokkuleppele, kuhu Tartus sööma minna? Las ma aitan Teid!",
                              font=("Franklin", 14),
                              bootstyle="white",
                              wraplength=800)
    
    tervitus_label.grid(row=1, column=1, columnspan=1, pady=15) 
    
    # Loob ja kuvab nupu, millega programmi alustada
    nupp = tb.Button(content_frame, text="Kas alustame?", command=lambda: [alusta(), pilt_edasi(2)], bootstyle="primary, outline")
    nupp.grid(row=2, column=1, columnspan=1, pady=15)
    
    # Loob küsimuste- ja söögikoha info labelid
    küsimus_label = tb.Label(content_frame, text="", bootstyle="white",  font=("Franklin", 14))
    söögid_label = tb.Label(content_frame, text="", bootstyle="white", font=("Franklin", 14))
    
    # Loob jah ja ei nupud
    jah_nupp = tb.Button(content_frame, text="Jah", bootstyle="success", width=15, command=lambda:[salvesta_vastus("jah"), pilt_edasi(3)])
    ei_nupp = tb.Button(content_frame, text="Ei", bootstyle="danger", width=15, command=lambda:[salvesta_vastus("ei"), pilt_edasi(3)])
    
    # Loob juhendi nupu
    juhend_nupp = tb.Button(content_frame, text="Kuidas kasutada?", command=kuidas_kasutada, bootstyle="info, outline")
    juhend_nupp.grid(row=3, column=1, columnspan=1, pady=15)
    
    window.mainloop()

if __name__ == "__main__":
    main()


