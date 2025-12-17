import tkinter as tk
from tkinter import ttk
import random
import json

#Kujundus (värvid + ttk stiilid)
BG = "#F5F7FB"
SIDEBAR_BG = "#FFFFFF"
CARD_BG = "#FFFFFF"
BORDER = "#E6EAF2"
TEXT = "#0F172A"
MUTED = "#475569"
ACCENT = "#2563EB"
ACCENT_HOVER = "#1D4ED8"

kapp = "kapp.json"
retsept ="retseptid.json"

with open(retsept, "r", encoding="utf-8") as f:
    retseptid = json.load(f) #avame retseptide faili

#FUNKTSIOONID

#Parema akna tühjendamine
def tühjenda_raam():
    for w in parem_raam.winfo_children():
        w.destroy()

def ava_soovituse_vaade():
    global retsepti_nimi, retsepti_sisu

    tühjenda_raam()

    kaart = ttk.Frame(parem_raam, style="Card.TFrame", padding=16)
    kaart.pack(fill="both", expand=True)

    retsepti_nimi = ttk.Label(kaart, text="Sisesta enda külmkapi sisu ja siis jätkame!", style="H2.TLabel")
    retsepti_nimi.pack(fill="x", pady=(0, 10))

    retsepti_sisu = tk.Label(
        kaart,
        text="",
        bg=CARD_BG,
        fg=MUTED,
        justify="left",
        anchor="nw",
        font=("Arial", 11),
        wraplength=900
    )
    retsepti_sisu.pack(fill="both", expand=True)

def soovita_ja_ava():
    ava_soovituse_vaade()
    soovita_retsept()



#külmkapi toiduainete lisamine
def lisa_toiduaine():
    tekst = sisestus.get().strip()  
    if tekst and tekst not in toiduained:  
        toiduained.append(tekst)
        with open(kapp, "w", encoding="UTF-8") as f:
            json.dump(toiduained, f, ensure_ascii=False, indent=2)
        loend.insert(tk.END, tekst)
        print(toiduained) 
        sisestus.delete(0, tk.END)  

def eemalda_toiduaine():  #toiduainete eemaldamine
    valik = loend.curselection()
    if valik:
        index = valik[0]
        toiduained.pop(index)
        loend.delete(index)
        with open(kapp, "w", encoding="Utf-8") as f:
            json.dump(toiduained, f, ensure_ascii=False, indent=2)

def soovita_retsept():
    # loeme filtrite valikud
    aeg = aeg_valik.get()
    tervis = tervis_valik.get()

    # filtreeri retseptid aja ja tervise järgi
    sobivad = []
    for r in retseptid:  #lisab uude listi kõik retseptid, mis sobivad valitud tingimustele(kui tekib vastuolu tingimusega siis tuleb continue ja võtab uue retsepti)
        # aeg filter
        if aeg == "Kiire (≤10 min)" and r["aeg_minutites"] > 10:
            continue
        if aeg == "Keskmine (10–30 min)" and not (10 < r["aeg_minutites"] <= 30):
            continue
        if aeg == "Aeglane (30+ min)" and r["aeg_minutites"] <= 30:
            continue

        # tervislikkus filter
        if tervis == "Tervislik (8–10)" and r["tervislikkus_10_palli"] < 8:
            continue
        if tervis == "Keskmine (4–7)" and not (4 <= r["tervislikkus_10_palli"] <= 7):
            continue
        if tervis == "Ebatervislik (1–3)" and r["tervislikkus_10_palli"] > 3:
            continue

        sobivad.append(r)

    # kui midagi jäi järele, eelistame neid, mille koostisosad kattuvad kapiga
    if sobivad:
        # arvuta kattuvus: mitu retsepti koostisosa leidub kapis
        kapp_set = {x.strip().lower() for x in toiduained}

        def kattuvus(r):
            return sum(1 for i in r["koostisosad"] if i.strip().lower() in kapp_set)
        
        #koostab top5 parima kattuvusega retseptid
        skoorid = [(kattuvus(r), r) for r in sobivad]
        skoorid.sort(key=lambda x: x[0], reverse=True)
        top5 = [r for s, r in skoorid[:5]]
        retsept = random.choice(top5)

        # kuvamine
        retsepti_nimi.config(text=retsept["toidu_nimi"])
        retsepti_sisu.config(
            text=f"Koostisosad: {', '.join(retsept['koostisosad'])}\n\n"
                 f"Aeg: {retsept['aeg_minutites']} min\n"
                 f"Tervislikkus: {retsept['tervislikkus_10_palli']}/10\n"
                 f"Kalorid: {retsept['kalorid_kcal']} kcal\n\n"
                 f"Juhis:\n{retsept['valmistamise_juhis']}"
        )

    else:
        # kui ühtegi sobivat retsepti ei leitud
        retsepti_nimi.config(text="Ühtegi sobivat retsepti ei leitud")
        retsepti_sisu.config(text="")




#lisa retsept aken 
def ava_lisa_retsept():
    global nimi_sisestus, koostisosad_sisestus, aeg_sisestus
    global tervislikkus_sisestus, kalorid_sisestus, juhis_text, teade

    tühjenda_raam()

    retsepti_pealkiri = ttk.Label(parem_raam, text="Lisa oma retsept", style="CardTitle.TLabel")
    retsepti_pealkiri.pack(fill="x", pady=(0, 12))

    retsepti_vorm = ttk.Frame(parem_raam, style="Card.TFrame", padding=16)
    retsepti_vorm.pack(fill="x", anchor="nw")

    retsepti_vorm.columnconfigure(1, weight=1)

    ttk.Label(retsepti_vorm, text="Toidu nimi:", style="H2.TLabel").grid(row=0, column=0, sticky="w", pady=6, padx=(0, 10))
    nimi_sisestus = ttk.Entry(retsepti_vorm)
    nimi_sisestus.grid(row=0, column=1, sticky="ew", pady=6)

    ttk.Label(retsepti_vorm, text="Koostisosad:", style="H2.TLabel").grid(row=1, column=0, sticky="w", pady=6, padx=(0, 10))
    koostisosad_sisestus = ttk.Entry(retsepti_vorm)
    koostisosad_sisestus.grid(row=1, column=1, sticky="ew", pady=6)

    ttk.Label(retsepti_vorm, text="Aeg (min):", style="H2.TLabel").grid(row=2, column=0, sticky="w", pady=6, padx=(0, 10))
    aeg_sisestus = ttk.Entry(retsepti_vorm, width=10)
    aeg_sisestus.grid(row=2, column=1, sticky="w", pady=6)

    ttk.Label(retsepti_vorm, text="Tervislikkus (1–10):", style="H2.TLabel").grid(row=3, column=0, sticky="w", pady=6, padx=(0, 10))
    tervislikkus_sisestus = ttk.Entry(retsepti_vorm, width=10)
    tervislikkus_sisestus.grid(row=3, column=1, sticky="w", pady=6)

    ttk.Label(retsepti_vorm, text="Kalorid (kcal):", style="H2.TLabel").grid(row=4, column=0, sticky="w", pady=6, padx=(0, 10))
    kalorid_sisestus = ttk.Entry(retsepti_vorm, width=10)
    kalorid_sisestus.grid(row=4, column=1, sticky="w", pady=6)

    ttk.Label(retsepti_vorm, text="Valmistamise juhis:", style="H2.TLabel").grid(row=5, column=0, sticky="nw", pady=6, padx=(0, 10))
    juhis_text = tk.Text(
        retsepti_vorm,
        height=7,
        wrap="word",
        bg="#FFFFFF",
        fg=TEXT,
        relief="flat",
        highlightthickness=1,
        highlightbackground=BORDER,
        font=("Arial", 11)
    )
    juhis_text.grid(row=5, column=1, sticky="ew", pady=6)

    ttk.Button(retsepti_vorm, text="Lisa retsept", command=lisa_retsept, style="Primary.TButton")\
        .grid(row=6, column=1, sticky="e", pady=(10, 4))

    teade = ttk.Label(retsepti_vorm, text="", style="Body.TLabel")
    teade.grid(row=7, column=0, columnspan=2, sticky="w", pady=(6, 0))

# Retsepti lisamine


def lisa_retsept():
    nimi = nimi_sisestus.get().strip()
    koost_str = koostisosad_sisestus.get().strip()
    aeg_str = aeg_sisestus.get().strip()
    terv_str = tervislikkus_sisestus.get().strip()
    kcal_str = kalorid_sisestus.get().strip()
    juhis = juhis_text.get("1.0", "end").strip()

    #kontroll kas koik lahtrid on täidetud korrektselt
    if not (nimi and koost_str and aeg_str and terv_str and kcal_str and juhis):
        
        try:
            teade.config(text="Täida kõik väljad.", foreground="red")
        except:
            print("Täida kõik väljad.")
        return

    # koostisosad on tühikutega eraldatud
    koostisosad = [x.strip() for x in koost_str.split() if x.strip()]
    if not koostisosad:
        try:
            teade.config(text="Koostisosad peavad olema tühikutega eraldatud ja mitte tühjad.", foreground="red")
        except:
            print("Koostisosad ei tohi olla tühjad.")
        return

    try:
        aeg = int(aeg_str)
        terv = int(terv_str)
        kcal = int(kcal_str)
    except:
        try:
            teade.config(text="Aeg, tervislikkus ja kalorid peavad olema täisarvud.", foreground="red")
        except:
            print("Aeg/tervislikkus/kalorid peavad olema täisarvud.")
        return

    if aeg <= 0 or kcal <= 0:
        try:
            teade.config(text="Aeg ja kalorid peavad olema positiivsed.", foreground="red")
        except:
            print("Aeg ja kalorid peavad olema positiivsed.")
        return

    if not (1 <= terv <= 10):
        try:
            teade.config(text="Tervislikkus peab olema vahemikus 1–10.", foreground="red")
        except:
            print("Tervislikkus peab olema 1–10.")
        return

    uus = {
        "toidu_nimi": nimi,
        "koostisosad": koostisosad,
        "aeg_minutites": aeg,
        "tervislikkus_10_palli": terv,
        "kalorid_kcal": kcal,
        "valmistamise_juhis": juhis
    }

    # lisa faili
    retseptid.append(uus)
    with open(retsept, "w", encoding="utf-8") as f:
        json.dump(retseptid, f, ensure_ascii=False, indent=2)

    try:
        teade.config(text="Retsept lisatud!", foreground="green")
    except:
        print("Retsept lisatud!")
    nimi_sisestus.delete(0, tk.END)
    koostisosad_sisestus.delete(0, tk.END)
    aeg_sisestus.delete(0, tk.END)
    tervislikkus_sisestus.delete(0, tk.END)
    kalorid_sisestus.delete(0, tk.END)
    juhis_text.delete("1.0", tk.END)

    
#ANDMED

try:
    with open(kapp, "r", encoding="utf-8") as f:
        toiduained = json.load(f)
except:
    toiduained = []  # siia salvestame kõik sisestatud toiduained


#AKEN


aken = tk.Tk()

aken.title("Otsustusvõimetu-kokk")
aken.geometry("1600x1000")


aken.configure(bg=BG)

stiil = ttk.Style()
stiil.theme_use("clam")

stiil.configure("App.TFrame", background=BG)
stiil.configure("Sidebar.TFrame", background=SIDEBAR_BG)
stiil.configure("Card.TFrame", background=CARD_BG)

stiil.configure("Title.TLabel", background=BG, foreground=TEXT, font=("Arial", 16, "bold"))
stiil.configure("H2.TLabel", background=CARD_BG, foreground=TEXT, font=("Arial", 12, "bold"))
stiil.configure("Body.TLabel", background=CARD_BG, foreground=MUTED, font=("Arial", 10))

stiil.configure("TLabel", background=SIDEBAR_BG, foreground=TEXT, font=("Arial", 10))
stiil.configure("TButton", font=("Arial", 10), padding=(10, 7))
stiil.map("TButton", background=[("active", "#EEF2FF")])

stiil.configure("Primary.TButton", background=ACCENT, foreground="white")
stiil.map("Primary.TButton",
          background=[("active", ACCENT_HOVER), ("pressed", ACCENT_HOVER)],
          foreground=[("disabled", "#CBD5E1")])

stiil.configure("TEntry", padding=(8, 6))
stiil.configure("TCombobox", padding=(8, 6))

stiil.configure("CardTitle.TLabel", background=CARD_BG, foreground=TEXT, font=("Arial", 16, "bold"))




#Sisestusaken

vasak_raam = ttk.Frame(aken, style="Sidebar.TFrame", padding=14)
vasak_raam.pack(side="left", fill="y", padx=(16, 10), pady=16)

silt = ttk.Label(vasak_raam, text="Külmkapp", style="Title.TLabel")
silt.pack(anchor="w", pady=(2, 12))

sisestus = ttk.Entry(vasak_raam, width=28)
sisestus.pack(fill="x", pady=(0, 8))
sisestus.bind("<Return>", lambda event: lisa_toiduaine())

nuppude_rida = ttk.Frame(vasak_raam, style="Sidebar.TFrame")
nuppude_rida.pack(fill="x", pady=(0, 10))



lisa_nupp = ttk.Button(nuppude_rida, text="Lisa", command=lisa_toiduaine, style="Primary.TButton")
lisa_nupp.pack(side="left", fill="x", expand=True)

eemalda_nupp = ttk.Button(nuppude_rida, text="Eemalda", command=eemalda_toiduaine)
eemalda_nupp.pack(side="left", fill="x", expand=True, padx=(8, 0))

loend = tk.Listbox(
    vasak_raam,
    width=28,
    height=12,
    bg="#FFFFFF",
    fg=TEXT,
    highlightthickness=1,
    highlightbackground=BORDER,
    selectbackground="#DBEAFE",
    selectforeground=TEXT,
    relief="flat"
)
loend.pack(fill="x", pady=(0, 12))

#kapi toiduainete kuvamine
for aine in toiduained:
    loend.insert(tk.END, aine)

ttk.Separator(vasak_raam).pack(fill="x", pady=10)

soovita_nupp = ttk.Button(vasak_raam, text="Soovita retsepti", command=soovita_ja_ava, style="Primary.TButton")
soovita_nupp.pack(fill="x", pady=(0, 10))


#Aja ja tervislikkuse filtrid

aeg_label = ttk.Label(vasak_raam, text="Vali tegemise aeg:")
aeg_label.pack(anchor="w", pady=(0, 4))

aeg_valik = ttk.Combobox(
    vasak_raam,
    values=["Kõik", "Kiire (≤10 min)", "Keskmine (10–30 min)", "Aeglane (30+ min)"],
    state="readonly"
)
aeg_valik.current(0)
aeg_valik.pack(fill="x", pady=(0, 10))

tervis_label = ttk.Label(vasak_raam, text="Vali tervislikkus:")
tervis_label.pack(anchor="w", pady=(0, 4))

tervis_valik = ttk.Combobox(
    vasak_raam,
    values=["Kõik", "Tervislik (8–10)", "Keskmine (4–7)", "Ebatervislik (1–3)"],
    state="readonly"
)
tervis_valik.current(0)
tervis_valik.pack(fill="x", pady=(0, 12))

#Lisa oma retsept nupp
btn_lisa_retsept = ttk.Button(vasak_raam, text="Lisa oma retsept", command=ava_lisa_retsept)
btn_lisa_retsept.pack(fill="x")


#parem pool UI-st
parem_raam = ttk.Frame(aken, style="App.TFrame", padding=16)
parem_raam.pack(side="right", fill="both", expand=True, padx=(0, 16), pady=16)

kaart = ttk.Frame(parem_raam, style="Card.TFrame", padding=16)
kaart.pack(fill="both", expand=True)

retsepti_nimi = ttk.Label(kaart, text="Sisesta enda külmkapi sisu ja siis jätkame!", style="CardTitle.TLabel")
retsepti_nimi.configure(background=CARD_BG)
retsepti_nimi.pack(fill="x", pady=(0, 10))

retsepti_sisu = tk.Label(
    kaart,
    text="",
    bg=CARD_BG,
    fg=MUTED,
    justify="left",
    anchor="nw",
    font=("Arial", 11),
    wraplength=900
)
retsepti_sisu.pack(fill="both", expand=True)

aken.mainloop()