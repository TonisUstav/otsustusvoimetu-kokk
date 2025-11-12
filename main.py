import tkinter as tk
from tkinter import ttk
import random
import json

kapp = "kapp.json"
retsept ="retseptid.json"

with open(retsept, "r", encoding="utf-8") as f:
    retseptid = json.load(f) #avame retseptide faili

#FUNKTSIOONID

def lisa_toiduaine():
    tekst = sisestus.get().strip()  # võtab teksti sisestusväljast
    if tekst and tekst not in toiduained:  # kui pole tühi
        toiduained.append(tekst)
        with open(kapp, "w", encoding="UTF-8") as f:
            json.dump(toiduained, f, ensure_ascii=False, indent=2)
        loend.insert(tk.END, tekst)
        print(toiduained)  # näitame terminalis kapisisu
        sisestus.delete(0, tk.END)  # tühjendab sisestusvälja

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

        # loome listi (skoor, retsept)
        skoorid = [(kattuvus(r), r) for r in sobivad]
        max_skoor = max(s for s, _ in skoorid)  # parim kattuvus
        parimad = [r for s, r in skoorid if s == max_skoor]  # kõik, millel sama parim tulemus

        retsept = random.choice(parimad)  # vali juhuslikult parimate seast

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


#ANDMED

try:
    with open(kapp, "r", encoding="utf-8") as f:
        toiduained = json.load(f)
except:
    toiduained = []  # siia salvestame kõik sisestatud toiduained


#AKEN


aken = tk.Tk()

aken.title("Otsustusvõimetu-kokk")
aken.geometry("800x500")


#Sisestusaken

vasak_raam = tk.Frame(aken, bg="#f0f0f0", padx=10, pady=10, borderwidth=2, relief="solid")
vasak_raam.pack(side="left", fill="y")

silt = tk.Label(vasak_raam, text="Lisa toiduaineid", font="bold", bg="lightblue")
silt.pack(pady=20, padx=10)

sisestus = tk.Entry(vasak_raam, width=25)
sisestus.pack(padx=10, pady=(0,10))
sisestus.bind("<Return>", lambda event: lisa_toiduaine())


lisa_nupp = tk.Button(vasak_raam, text="Lisa", width=10, command=lisa_toiduaine)
lisa_nupp.pack(padx=10, pady=(0,10))

eemalda_nupp = tk.Button(vasak_raam, text="Eemalda toiduaine", width=15, command=eemalda_toiduaine)
eemalda_nupp.pack(padx=10, pady=(0,10))

loend = tk.Listbox(vasak_raam, width=25, height=10)
loend.pack(padx=10, pady=(0,10))

#kapi toiduainete kuvamine
for aine in toiduained:
    loend.insert(tk.END, aine)

#parem pool UI-st
parem_raam = tk.Frame(aken, padx=10, pady=10, borderwidth=2, relief="solid")
parem_raam.pack(side="right", fill="both", expand=True)

retsepti_nimi = tk.Label(parem_raam, text="Sisesta enda külmkapi sisu ja siis jätkame!", font=("Arial", 14, "bold"), anchor="w", justify="left")
retsepti_nimi.pack(fill="x", pady=(0,8))

retsepti_sisu = tk.Label(parem_raam, text="", anchor="nw", justify="left")
retsepti_sisu.pack(fill="both", expand=True)

soovita_nupp = tk.Button(vasak_raam, text="Soovita retsepti", width=18, command=soovita_retsept)
soovita_nupp.pack(padx=10, pady=(0,10))

#Aja ja tervislikkuse filtrid

aeg_label = ttk.Label(vasak_raam, text="Vali tegemise aeg:")
aeg_label.pack(anchor="w", padx=10)
aeg_valik = ttk.Combobox(vasak_raam, values=["Kõik", "Kiire (≤10 min)", "Keskmine (10–30 min)", "Aeglane (30+ min)"])
aeg_valik.current(0)
aeg_valik.pack(fill="x", padx=10, pady=(0,10))

tervis_label = ttk.Label(vasak_raam, text="Vali tervislikkus:")
tervis_label.pack(anchor="w", padx=10)
tervis_valik = ttk.Combobox(vasak_raam, values=["Kõik", "Tervislik (8–10)", "Keskmine (4–7)", "Ebatervislik (1–3)"])
tervis_valik.current(0)
tervis_valik.pack(fill="x", padx=10, pady=(0,10))

aken.mainloop()
