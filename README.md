# Autorid

- Tõnis Ustav
- Markus Rannaste

# Hetke progress

Koostöö on sujunud hästi, oleme selget ära jaganud, kes mida teeb, üks vastutab retseptide andmebaasi ning tkinteri kasutamise eest ning teine kirjutab programmi backendi ehk erinevaid funktsioone. Aega on hetkel kulunud projektile mõlema peale kokku ca 15 tundi. Hetkel pole me programmi kujundusele eriti rõhku pannud, vaid keskendunud, et programmi keskne idee ehk retseptide soovitamine töötaks hästi. Hetkel suudab programm sinu sisestuste järgi sulle soovitada retsepte. Lisaks on võimalik kasutada ka ajakulu ja tervislikkuse filtrit oma valikut tehes. Kuna hetkel saad kirjutada oma retsepte ainult otse jsoni faili kirjutades. Siis järgmine edasiarendus on oma retseptide lisamine läbi UI, lisaks tuleb veel filtreid, mida kasutada, näiteks mitu toiduainet sinu külmkapist peavad kattuma retseptis olevate toorainetega. Viimasena hakkame tegelema põhjalikumalt UI kujundusega ning teeme selle kasutajasõbralikuks.

# programmi kirjeldus

Programm otsustusvõimetu_kokk aitab kasutajal valida, mida olemasolevatest toiduainestest oma külmkapis süüa teha.

# Kasutamine

- Hetkel jookseb programm TKinteris
- Failiga tuli kaasa ka fail retseptid.json, kus on juba hulk retsepte olemas, kuna hetkel UI-s puudub võimalus oma retsepte lisada, siis hetkel saab oma retseptid kirjutada otse faili
- Runi kood--->Sisesta külmkapi sisu, kirjutades lahtrisse toiduaine nimetus--->Kui tahad midagi eemaldada, siis clicki sellel ja vajuta "eemalda"--->
  Saad valida kahe filtri vahel: ajakulu ja tervislikkus--->Vajuta "Soovita retsepti" ja sinule paremini sobiv retsept peaks ilmuma ekraanile
