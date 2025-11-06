import tkinter as tk

#FUNKTSIOONID

def lisa_toiduaine():
    tekst = sisestus.get()  # võtab teksti sisestusväljast
    if tekst:  # kui pole tühi
        toiduained.append(tekst)
        print(toiduained)  # ajutiselt näitame terminalis, et näeksid, kas töötab
        sisestus.delete(0, tk.END)  # tühjendab sisestusvälja

#ANDMED

toiduained = []  # siia salvestame kõik sisestatud toiduained


#AKEN


aken = tk.Tk()

aken.title("Otsustusvõimetu-kokk")
aken.geometry("800x500")

vasak_raam = tk.Frame(aken, bg="#f0f0f0", padx=10, pady=10, borderwidth=2, relief="solid")
vasak_raam.pack(side="left", fill="y")

silt = tk.Label(vasak_raam, text="Siia tulevad toiduained", bg="lightblue")
silt.pack(pady=20, padx=10)

sisestus = tk.Entry(vasak_raam, width=25)
sisestus.pack(padx=10, pady=(0,10))

lisa_nupp = tk.Button(vasak_raam, text="Lisa", width=10, command=lisa_toiduaine)
lisa_nupp.pack(padx=10, pady=(0,10))

aken.mainloop()
