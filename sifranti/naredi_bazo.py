from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User, Group

from izpiti.models import *
from student.models import *
from .forms import *
from .models import *
import datetime

from openpyxl import *

def narediIzvedbo(predmetnik, prof):

    prof.predmeti.add(predmetnik.predmet)
    izvedba = IzvedbaPredmeta(predmet = predmetnik.predmet, studijsko_leto= predmetnik.studijsko_leto, ucitelj_1= prof)
    izvedba.save()
    prof.save()
    return

def brezSumnikov(beseda):
    a = beseda

    i = 0
    for c in beseda:
        if c == "č":
            a = a[:i] + "c" + a[i+1:]
        elif c == "š":
            a = a[:i] + "s" + a[i+1:]
        elif c == "ž":
            a = a[:i] + "z" + a[i+1:]
        elif c == "ć":
            a = a[:i] + "c" + a[i+1:]
        i = i+1
    return a

def narediProfesorja(imes,priimeks):
    ime = brezSumnikov(imes.lower())
    priimek = brezSumnikov(priimeks.lower())
    if Ucitelj.objects.filter(ime=imes,priimek=priimeks).exists():
        return Ucitelj.objects.filter(ime=imes,priimek=priimeks)[0]

    user, created = User.objects.get_or_create(username=ime +priimek, email=ime+"."+priimek+  "@fri.uni-lj.si")
    user.first_name = imes
    user.last_name = priimeks
        
    if created:
        user.set_password("adminadmin")
        user.is_staff=False
        user.is_superuser=False
        prof_group, status = Group.objects.get_or_create(name='professors') 
        prof_group.user_set.add(user)

    user.save()

    profesor = Ucitelj(ime = imes, priimek = priimeks, email = ime+"."+priimek+  "@fri.uni-lj.si")
    #print(profesor.email)
    profesor.save()
    return profesor


def uvozi_drzave():
    print('\x1b[6;30;42m' + 'Začetek uvažanja držav ' + '\x1b[0m')
    wb = load_workbook('sifranti/ŠifrantDržav.xlsx')
    sheet = wb.active
    cellsa = sheet['A3':'F251']
    for dvomestna, tromestna, numericna_oz, iso, slovenski, opombaa in cellsa:
        if opombaa.value == None:
            opombaa.value = ""

        a = Drzava(id=numericna_oz.value, 
        dvomestna_koda=dvomestna.value, 
        tromestna_oznaka=tromestna.value,
         iso_naziv=iso.value, 
         slovenski_naziv=slovenski.value,
         opomba=opombaa.value, 
         veljaven=True)

        a.save()
    print('\x1b[6;30;42m' + 'Konec uvažanja držav ' + '\x1b[0m')
        
    return

def uvozi_obcine():
    print('\x1b[6;30;42m' + 'Začetek uvažanja občin ' + '\x1b[0m')
    wb = load_workbook('sifranti/ŠifrantObčin.xlsx')
    sheet = wb.active
    cellsa = sheet['A2':'B213']
    for sifra, imee in cellsa:
        
        a = Obcina(id = sifra.value, ime = imee.value)

        a.save()
    print('\x1b[6;30;42m' + 'Konec uvažanja občin ' + '\x1b[0m')
        
    return

def uvozi_poste():
    print('\x1b[6;30;42m' + 'Začetek uvažanja pošt ' + '\x1b[0m')
    wb = load_workbook('sifranti/ŠifrantPošt.xlsx')
    sheet = wb.active
    cellsa = sheet['B5':'C482']
    for sifra, imee in cellsa:
        
        a = Posta(id = sifra.value, kraj = imee.value)

        a.save()
    print('\x1b[6;30;42m' + 'Konec uvažanja pošt ' + '\x1b[0m')
        
    return


def naredi_bazo(request):
    
    print('\x1b[6;30;42m' + 'Začetek delanja baze ' + '\x1b[0m')

    uvozi_drzave()
    uvozi_obcine()
    uvozi_poste()

    

    a_slo = Drzava.objects.get(id=703)
    a_sklObcina = Obcina.objects.get(id = 122)
    a_ljObcina = Obcina.objects.get(id = 61)
    a_ljPosta = Posta.objects.get(id=1000)
    a_sklPosta = Posta.objects.get(id=4220)
    a_sklPosta.save()

    a_studijskiProgram = StudijskiProgram(id=1000475,sifra="L2",stopnja="C - (predbolonjski) univerzitetni", semestri=9, naziv= "RAČUNAL. IN INFORMATIKA UN")
    a_studijskiProgram.save()
    a_vrstaStudija = VrstaStudija(id=12001,opis="Osnovnošolska izobrazba", nacin_zakljucka="zakljucena osnovna šola", raven_klasius=1)
    a_vrstaStudija.save()
    a_vrstaVpisa = VrstaVpisa(id=1, opis="Prvi vpis v letnik/dodatno leto", mozni_letniki="Vsi letniki in dodatno leto")
    a_vrstaVpisa.save()
    a_nacinStudija = NacinStudija(id=1, opis="redni",ang_opis="full-time")
    a_nacinStudija.save()
    a = OblikaStudija(id=1, opis="na lokaciji", ang_opis="on-site" )
    a.save()
    #naredi studenta
    primozt = Student(vpisna_stevilka = 63150000, emso=1511996500207, ime="Primož", drzava_rojstva=a_slo,obcina_rojstva= a_ljObcina,  priimek="Trubar",naslov_stalno_bivalisce="Kranjska ulica 12", drzava= Drzava.objects.filter(pk=4)[0], posta= Posta.objects.filter(pk=1293)[0],obcina= Obcina.objects.filter(pk=1)[0],telefon="040123456",email="pt0000@fri.uni-lj.si")
    primozt.save()

    

    user, created = User.objects.get_or_create(username="student", email="pt0000@fri.uni-lj.si")
    user.first_name = "Primož"
    user.last_name = "Trubar"

    if created:
        user.set_password("adminadmin")
        user.is_staff=False
        user.is_superuser=False
        ref_group, status = Group.objects.get_or_create(name='students') 
        ref_group.user_set.add(user)
    
    user.save()
    
    # student 1 letnik
    ivan = Student(vpisna_stevilka = 63180000, emso=1511996500207, ime="Ivan", drzava_rojstva=a_slo,obcina_rojstva= a_ljObcina,  priimek="Cankar",naslov_stalno_bivalisce="Na klancu 29", drzava= Drzava.objects.filter(pk=4)[0], posta= Posta.objects.filter(pk=1293)[0],obcina= Obcina.objects.filter(pk=1)[0],telefon="040123456",email="ic1111@fri.uni-lj.si")
    ivan.save()

    user, created = User.objects.get_or_create(username="ivan", email="ic1111@fri.uni-lj.si")
    user.first_name = "Ivan"
    user.last_name = "Cankar"

    if created:
        user.set_password("adminadmin")
        user.is_staff=False
        user.is_superuser=False
        ref_group, status = Group.objects.get_or_create(name='students') 
        ref_group.user_set.add(user)
    
    user.save()

    # student 2 letnik
    drago = Student(vpisna_stevilka = 63170000, emso=1511996500207, ime="Drago", drzava_rojstva=a_slo,obcina_rojstva= a_ljObcina,  priimek="Furja",naslov_stalno_bivalisce="Ropotoče 28", drzava= Drzava.objects.filter(pk=4)[0], posta= Posta.objects.filter(pk=1293)[0],obcina= Obcina.objects.filter(pk=1)[0],telefon="040123456",email="df2222@fri.uni-lj.si")
    drago.save()

    user, created = User.objects.get_or_create(username="drago", email="df2222@fri.uni-lj.si")
    user.first_name = "Drago"
    user.last_name = "Furja"

    if created:
        user.set_password("adminadmin")
        user.is_staff=False
        user.is_superuser=False
        ref_group, status = Group.objects.get_or_create(name='students') 
        ref_group.user_set.add(user)
    
    user.save()


    # student 3 letnik brez izbire
    martin = Student(vpisna_stevilka = 63160000, emso=1511996500207, ime="Martin", drzava_rojstva=a_slo,obcina_rojstva= a_ljObcina,  priimek="Luter",naslov_stalno_bivalisce="Dunajska 124", drzava= Drzava.objects.filter(pk=4)[0], posta= Posta.objects.filter(pk=1293)[0],obcina= Obcina.objects.filter(pk=1)[0],telefon="040123456",email="ml3333@fri.uni-lj.si")
    martin.save()

    user, created = User.objects.get_or_create(username="martin", email="ml3333@fri.uni-lj.si")
    user.first_name = "Martin"
    user.last_name = "Luter"

    if created:
        user.set_password("adminadmin")
        user.is_staff=False
        user.is_superuser=False
        ref_group, status = Group.objects.get_or_create(name='students') 
        ref_group.user_set.add(user)
    
    user.save()

    # student 3 letnik brez izbire
    tine = Student(vpisna_stevilka = 63160001, emso=1511996500207, ime="Tine", drzava_rojstva=a_slo,obcina_rojstva= a_ljObcina,  priimek="Prejovc",naslov_stalno_bivalisce="Tavčarjeva 4", drzava= Drzava.objects.filter(pk=4)[0], posta= Posta.objects.filter(pk=1293)[0],obcina= Obcina.objects.filter(pk=1)[0],telefon="040123456",email="tp4444@fri.uni-lj.si")
    tine.save()

    user, created = User.objects.get_or_create(username="tine", email="tp4444@fri.uni-lj.si")
    user.first_name = "Tine"
    user.last_name = "Prejovc"

    if created:
        user.set_password("adminadmin")
        user.is_staff=False
        user.is_superuser=False
        ref_group, status = Group.objects.get_or_create(name='students') 
        ref_group.user_set.add(user)
    
    user.save()

    #naredi referenta
    user, created = User.objects.get_or_create(username="referentka", email="referentka@fri.uni-lj.si")
    user.first_name = "Tatjana"
    user.last_name = "Novak"
        
    if created:
        user.set_password("adminadmin")
        user.is_staff=False
        user.is_superuser=False
        ref_group, status = Group.objects.get_or_create(name='referent') 
        ref_group.user_set.add(user)

    a_1Letnik = Letnik(ime="1.")
    a_1Letnik.save()
    a_2Letnik = Letnik(ime="2.")
    a_2Letnik.save()
    a_3Letnik= Letnik(ime="3.")
    a_3Letnik.save()

    a_stud = StudijskiProgram(id=1000475,sifra="L2",stopnja="C - (predbolonjski) univerzitetni", semestri=9, naziv= "RAČUNAL. IN INFORMATIKA UN")
    a_stud.save()
    a_stud2 = StudijskiProgram(id=1000471,sifra="L1",stopnja="L - druga stopnja: magistrski", semestri=4, naziv= "RAČUNALN. IN INFORM. MAG II.ST")
    a_stud2.save()
    a = StudijskiProgram(id=1000468 ,sifra="VT",stopnja="K - prva stopnja: univerzitetni", semestri=6, naziv= "RAČUNALN. IN INFORM. UN-I.ST")
    a.save()
    a = StudijskiProgram(id=1000470 ,sifra="VU",stopnja="J - prva stopnja: visokošolski strokovni", semestri=6, naziv= "RAČUNALN. IN INFORM. VS-I.ST")
    a.save()


    a = StudijskoLeto(ime = "2016/2017")
    a.save()
    a_17_18 = StudijskoLeto(ime = "2017/2018")
    a_17_18.save()
    a = StudijskoLeto(ime = "2018/2019")
    a.save()

    vsi_predmeti()

    #
    a_teh = Predmet.objects.get(ime = "Tehnologija programske opreme")

    a_obl = Predmet.objects.get(ime = "Osnove oblikovanja")
    
    a_ep = Predmet.objects.get(ime = "Ekonomika in podjetništvo")

    a_oim = Predmet.objects.get(ime = "Organizacija in management")

    a_P1 = Predmet.objects.filter(ime = "Programiranje 1")[0]

    a = Predmet.objects.filter(ime = "Programiranje 2")[0]

    a_aps1 = Predmet.objects.get(ime = "Algoritmi in podatkovne strukture 1")

    a_vilijan = Ucitelj(ime = "Viljan", priimek = "Mahnič", email = "viljan.mahnic@fri.uni-lj.si")
    a_vilijan.save()
    a_vilijan.predmeti.add(a_teh,a_P1)
    a_narvika = Ucitelj(ime = "Narvika", priimek = "Bovcon", email = "narvika.bavcon@fri.uni-lj.si")
    a_narvika.save()
    a_narvika.predmeti.add(a_obl)
    a_darja = Ucitelj(ime = "Darja", priimek = "Peljhan", email = "darja.peljhan@fri.uni-lj.si")#ep
    a_darja.save()
    a_jaka = Ucitelj(ime = "Jaka", priimek = "Lindič", email = "jaka.lindic@fri.uni-lj.si")#ep
    a_jaka.save()
    a_mateja = Ucitelj(ime = "Mateja", priimek = "Drnovšek", email = "mateja.drnovsek@fri.uni-lj.si") #ep
    a_mateja.save()
    a = Ucitelj(ime = "Tomaž", priimek = "Hovelja", email = "tomaz.hovelja@fri.uni-lj.si")
    a.save()
    a = Ucitelj(ime = "Boštjan", priimek = "Slivnik", email = "bostjan.slivnik@fri.uni-lj.si")
    a.save()
    a = Ucitelj(ime = "Igor", priimek = "Kononenko", email = "igor.kononenko@fri.uni-lj.si")
    a.save()

    a_izv_teh = IzvedbaPredmeta(predmet = a_teh, studijsko_leto = a_17_18, ucitelj_1 = a_vilijan)
    a_izv_teh.save()

    a_obl_izv = IzvedbaPredmeta(predmet = a_obl, studijsko_leto = a_17_18, ucitelj_1 = a_narvika)
    a_obl_izv.save()
    a = IzvedbaPredmeta(predmet = a_ep, studijsko_leto = a_17_18, ucitelj_1 = a_darja, ucitelj_2 = a_jaka, ucitelj_3 = a_mateja)
    a.save()
    
    a = Posta(id=1231, kraj="Ljubljana-Črnuče")
    a.save()
    a = Posta(id=1215, kraj="Medvode")
    a.save()

    a_stud = StudijskiProgram(id=1000475,sifra="L2",stopnja="C - (predbolonjski) univerzitetni", semestri=9, naziv= "RAČUNAL. IN INFORMATIKA UN")
    a_stud.save()
    a_stud2 = StudijskiProgram(id=1000471,sifra="L1",stopnja="L - druga stopnja: magistrski", semestri=4, naziv= "RAČUNALN. IN INFORM. MAG II.ST")
    a_stud2.save()
    a = StudijskiProgram(id=1000468 ,sifra="VT",stopnja="K - prva stopnja: univerzitetni", semestri=6, naziv= "RAČUNALN. IN INFORM. UN-I.ST")
    a.save()
    a = StudijskiProgram(id=1000470 ,sifra="VU",stopnja="J - prva stopnja: visokošolski strokovni", semestri=6, naziv= "RAČUNALN. IN INFORM. VS-I.ST")
    a.save()

    a_vs1 = VrstaStudija(id=12001,opis="Osnovnošolska izobrazba", nacin_zakljucka="zaključena osnovna šola", raven_klasius=1)
    a_vs1.save()
    a_vs2 = VrstaStudija(id=14001,opis="Srednja poklicna izobrazba", nacin_zakljucka="zaključni izpit", raven_klasius=4)
    a_vs2.save()
    a = VrstaStudija(id=15001,opis="Srednja strokovna izobrazba", nacin_zakljucka="zaključni izpit", raven_klasius=5)
    a.save()
    a = VrstaStudija(id=15002,opis="Srednja splošna izobrazba", nacin_zakljucka="splošna matura", raven_klasius=5)
    a.save()

    a_vv1 = VrstaVpisa(id=1, opis="Prvi vpis v letnik/dodatno leto", mozni_letniki="Vsi letniki in dodatno leto")
    a_vv1.save()
    a_vv2 = VrstaVpisa(id=2, opis="Ponavljanje letnika", mozni_letniki="V zadnjem letniku in v dodatnem letu ponavljanje ni več možno.")
    a_vv2.save()
    a = VrstaVpisa(id=3, opis="Nadaljevanje letnika", mozni_letniki="Vpis ni več dovoljen.")
    a.save()
    a = VrstaVpisa(id=4, opis="Podalšanje statuda študenta", mozni_letniki="Vsi letniki, dodatno leto")
    a.save()
    a = VrstaVpisa(id=5, opis="Vpis v semester skupnega št. programa", mozni_letniki="Vsi letniki razen prvega, dodatno leto ni dovoljeno")
    a.save()
    a = VrstaVpisa(id=6, opis="Nadaljevanje letnika", mozni_letniki="Vsi letniki, samo za skupne študijske programe")
    a.save()
    a = VrstaVpisa(id=7, opis="Nadaljevanje letnika", mozni_letniki="Vsi letniki, dodatno letno ni dovoljeno")
    a.save()
    a = VrstaVpisa(id=98, opis="Nadaljevanje letnika", mozni_letniki="Zadnji letnik. Namenjeno samo strokovmim delavcem v študentskem referatu")
    a.save()

    a_ns1 = NacinStudija(id=1, opis="redni",ang_opis="full-time")
    a_ns1.save()
    a_ns2 = NacinStudija(id=2, opis="izredni",ang_opis="part-time")
    a_ns2.save()
    #naredi 2 zetona za studenta

    zeton = Zeton(student=primozt,studijski_program=StudijskiProgram.objects.filter(pk=1000468)[0],letnik=a_2Letnik,vrsta_vpisa=a_vv1,nacin_studija=a_ns1,vrsta_studija=a_vs1)
    zeton.save()
    zeton2 = Zeton(student=primozt,studijski_program=a_stud2,letnik=a_1Letnik,vrsta_vpisa=a_vv2,nacin_studija=a_ns2,vrsta_studija=a_vs2)
    zeton2.save()

    #izvedba
    a_p1_izv = IzvedbaPredmeta(predmet = a_P1, studijsko_leto = a_17_18, ucitelj_1 = a_vilijan)
    a_p1_izv.save()

    a_aljaz = Student(vpisna_stevilka = "63150255", emso = "5869362456789", priimek="Rupar", ime="Aljaž", naslov_stalno_bivalisce="Godešič 163, 4220 Škofja Loka", drzava=a_slo, drzava_rojstva = a_slo, posta= a_sklPosta, obcina=a_sklObcina,obcina_rojstva= a_ljObcina, telefon="031866686", email="ar1961@student.uni-lj.si")
    a_aljaz.save()


    a_verlic = Student(vpisna_stevilka = "63150256", emso = "5869362456755", priimek="Verlič", ime="Aljaž", naslov_stalno_bivalisce="Voje 55, 1290 Grosuplje", drzava=a_slo,drzava_rojstva=a_slo,obcina_rojstva= a_ljObcina, posta= a_ljPosta, obcina=a_ljObcina, telefon="041786345", email="av1974@student.uni-lj.si")
    a_verlic.save()

    a_sega = Student(vpisna_stevilka = "63150245", emso = "5869362469812", priimek="Šega", ime="Nejc", naslov_stalno_bivalisce="Reteče 33, 4220 Škofja Loka", drzava=a_slo,drzava_rojstva=a_slo,obcina_rojstva= a_ljObcina, posta= a_ljPosta, obcina=a_ljObcina, telefon="041568324", email="sn1944@student.uni-lj.si")
    a_sega.save()

    a_maja = Student(vpisna_stevilka = "63150211", emso = "5869362464876", priimek="Šega", ime="Maja", naslov_stalno_bivalisce="Sveti duh, 4220 Škofja Loka", drzava=a_slo,drzava_rojstva=a_slo,obcina_rojstva= a_ljObcina, posta= a_ljPosta, obcina=a_ljObcina, telefon="041356765", email="sm1944@student.uni-lj.si")
    a_maja.save()

    a = OblikaStudija(id=1, opis="na lokaciji", ang_opis="on-site" )
    a.save()
    a = OblikaStudija(id=2, opis="na daljavo", ang_opis="distance learning" )
    a.save()
    a = OblikaStudija(id=3, opis="e-studij", ang_opis="e-learning" )
    a.save()


    a_vpisAljaz = Vpis(student=a_aljaz, studijsko_leto=a_17_18, studijski_program=a_studijskiProgram, letnik=a_3Letnik, vrsta_vpisa=a_vrstaVpisa,nacin_studija=a_nacinStudija, vrsta_studija=a_vrstaStudija)
    a_vpisAljaz.save()

    a_vpisVerlic = Vpis(student=a_verlic, studijsko_leto=a_17_18, studijski_program=a_studijskiProgram, letnik=a_3Letnik, vrsta_vpisa=a_vrstaVpisa,nacin_studija=a_nacinStudija, vrsta_studija=a_vrstaStudija)
    a_vpisVerlic.save()

    a_vpisSega = Vpis(student=a_sega, studijsko_leto=a_17_18, studijski_program=a_studijskiProgram, letnik=a_3Letnik, vrsta_vpisa=a_vrstaVpisa,nacin_studija=a_nacinStudija, vrsta_studija=a_vrstaStudija)
    a_vpisSega.save()
    
    a_vpisMaja = Vpis(student=a_maja, studijsko_leto=a_17_18, studijski_program=a_studijskiProgram, letnik=a_3Letnik, vrsta_vpisa=a_vrstaVpisa,nacin_studija=a_nacinStudija, vrsta_studija=a_vrstaStudija)
    a_vpisMaja.save()


    #a_aljaz.vpisi.add(a_vpisAljaz)
  
    a_predmetiStudentaAljaz = PredmetiStudenta()
    a_predmetiStudentaAljaz.save()
    a_predmetiStudentaAljaz.vpis = a_vpisAljaz
    a_predmetiStudentaAljaz.predmeti.add(a_teh,a_oim,a_ep,a_obl,a_P1)
    a_predmetiStudentaAljaz.save()

    a_predmetiStudentaVerlic = PredmetiStudenta()
    a_predmetiStudentaVerlic.save()
    a_predmetiStudentaVerlic.vpis = a_vpisVerlic
    a_predmetiStudentaVerlic.predmeti.add(a_teh,a_oim,a_ep,a_obl,a_aps1)
    a_predmetiStudentaVerlic.save()

    a_predmetiStudentaSega = PredmetiStudenta()
    a_predmetiStudentaSega.save()
    a_predmetiStudentaSega.vpis = a_vpisSega
    a_predmetiStudentaSega.predmeti.add(a_teh,a_oim,a_ep,a_obl,a_aps1)
    a_predmetiStudentaSega.save()

    a_predmetiStudentaMaja = PredmetiStudenta()
    a_predmetiStudentaMaja.save()
    a_predmetiStudentaMaja.vpis = a_vpisMaja
    a_predmetiStudentaMaja.predmeti.add(a_teh,a_oim,a_ep,a_obl,a_aps1)
    a_predmetiStudentaMaja.save()



    new_date = datetime.datetime(2013, 6, 9, 11, 13)
    a = Rok(izvedba_predmeta = a_izv_teh, datum = new_date)
    a.save()

    #podatki za vpis ocen izpita
    #podatki za vpis ocen izpita
    new_date = datetime.datetime(2018, 3, 3, 14, 15)
    a_rok = Rok(izvedba_predmeta = a_izv_teh, datum = new_date, prostor_izvajanja = "A1")
    a_rok.save()

    #roki za demonstracijo
    rok_date = datetime.datetime(2018, 5, 11, 12, 10)
    rok1 = Rok(izvedba_predmeta = a_izv_teh, datum = rok_date)
    rok1.save()

    rok_date = datetime.datetime(2018, 5, 14, 15, 55)
    rok1 = Rok(izvedba_predmeta = a_izv_teh, datum = rok_date)
    rok1.save()

    rok_date = datetime.datetime(2018, 5, 15, 6, 5)
    rok1 = Rok(izvedba_predmeta = a_izv_teh, datum = rok_date)
    rok1.save()

    rok_date = datetime.datetime(2018, 5, 25, 13, 2)
    rok1 = Rok(izvedba_predmeta = a_izv_teh, datum = rok_date)
    rok1.save()

    rok_date = datetime.datetime(2018, 5, 6, 18, 7)
    rok1 = Rok(izvedba_predmeta = a_izv_teh, datum = rok_date)
    rok1.save()

    rok_date = datetime.datetime(2018, 6, 5, 16, 35)
    rok1 = Rok(izvedba_predmeta = a_izv_teh, datum = rok_date)
    rok1.save()

    rok_date = datetime.datetime(2018, 6, 6, 12, 15)
    rok1 = Rok(izvedba_predmeta = a_izv_teh, datum = rok_date)
    rok1.save()



    new_date = datetime.datetime(2018, 2, 15, 14, 30)
    a_prijava1 = Prijava(created_at = new_date, predmeti_studenta = a_predmetiStudentaAljaz, rok = a_rok, zaporedna_stevilka_polaganja = 1)
    a_prijava1.save()

    new_date = datetime.datetime(2018, 2, 16, 14, 20)
    a_prijava2 = Prijava(created_at = new_date, predmeti_studenta = a_predmetiStudentaVerlic, rok = a_rok, zaporedna_stevilka_polaganja = 2)
    a_prijava2.save()

    new_date = datetime.datetime(2018, 2, 12, 14, 20)
    a_prijava3 = Prijava(created_at = new_date, predmeti_studenta = a_predmetiStudentaSega, rok = a_rok, zaporedna_stevilka_polaganja = 3)
    a_prijava3.save()

    new_date = datetime.datetime(2018, 2, 12, 19, 20)
    a_prijava4 = Prijava(created_at = new_date, predmeti_studenta = a_predmetiStudentaMaja, rok = a_rok, zaporedna_stevilka_polaganja = 1)
    a_prijava4.save()


    #zagovor odjave

    #rok na katerega se lahko prijavis in odjavis.
    rok_date = datetime.datetime(2018, 6, 29, 10, 10)
    rok1 = Rok(izvedba_predmeta = a_p1_izv, datum = rok_date)
    rok1.save()

    #rok na katerega si prijavljen vendar odjava ni več mogoča
    rok_date = datetime.datetime(2018, 5, 21, 19, 00)
    rok1 = Rok(izvedba_predmeta = a_p1_izv, datum = rok_date)
    rok1.save()

    new_date = datetime.datetime(2018, 5, 18, 15, 15)
    a_prijava5 = Prijava(created_at = new_date, predmeti_studenta = a_predmetiStudentaAljaz, rok = rok1, zaporedna_stevilka_polaganja = 1)
    a_prijava5.save()



    #naredi referenta
    user, created = User.objects.get_or_create(username="referentka", email="referentka@fri.uni-lj.si")
    user.first_name = "Tatjana"
    user.last_name = "Novak"
    user.set_password("adminadmin")
    if created:
        user.set_password("adminadmin")
        user.is_staff=False
        user.is_superuser=False
        ref_group, status = Group.objects.get_or_create(name='referent') 
        ref_group.user_set.add(user)

    user.save()

    #naredi profesorja
    user, created = User.objects.get_or_create(username="profesor", email="profesor@fri.uni-lj.si")
    user.first_name = "Lado"
    user.last_name = "Gubara"
        
    if created:
        user.set_password("adminadmin")
        user.is_staff=False
        user.is_superuser=False
        prof_group, status = Group.objects.get_or_create(name='professors') 
        prof_group.user_set.add(user)

    user.save()

    user, created = User.objects.get_or_create(username="viljanmahnic", email="viljan.mahnic@fri.uni-lj.si")
    user.first_name = "Viljan"
    user.last_name = "Mahnič"
        
    if created:
        user.set_password("adminadmin")
        user.is_staff=False
        user.is_superuser=False
        prof_group, status = Group.objects.get_or_create(name='professors') 
        prof_group.user_set.add(user)

    user.save()

    user, created = User.objects.get_or_create(username="aljazrupar", email="ar1961@student.uni-lj.si")
    user.first_name = "Aljaž"
    user.last_name = "Rupar"
        
    if created:
        user.set_password("adminadmin")
        user.is_staff=False
        user.is_superuser=False
        prof_group, status = Group.objects.get_or_create(name='students') 
        prof_group.user_set.add(user)

    user.save()


    print('\x1b[6;30;42m' + 'Uspešno dodana baza! ' + '\x1b[0m')
    return HttpResponse("Narejena baza!")


def vsi_predmeti():

    UNI = StudijskiProgram.objects.get(id=1000468)
    LETO = StudijskoLeto.objects.get(ime="2018/2019")
    LETNIK = Letnik.objects.get(ime="1.")

    #1 letnik
    a = Predmet(ime = "Programiranje 1", id="63277")
    a.save()
    pr = Predmetnik(studijski_program = UNI, studijsko_leto=LETO, letnik = LETNIK, predmet = a)
    pr.save()
    a = Predmet(ime = "Programiranje 2", id="63278")
    a.save()
    pr = Predmetnik(studijski_program = UNI, studijsko_leto=LETO, letnik = LETNIK, predmet = a)
    pr.save()
    a = Predmet(ime = "Diskretne strukture", id="63203")
    a.save()
    pr = Predmetnik(studijski_program = UNI, studijsko_leto=LETO, letnik = LETNIK, predmet = a)
    pr.save()
    a = Predmet(ime = "Fizika", id="63205")
    a.save()
    pr = Predmetnik(studijski_program = UNI, studijsko_leto=LETO, letnik = LETNIK, predmet = a)
    pr.save()
    a = Predmet(ime = "Osnove digitalnih vezij", id="63204")
    a.save()
    pr = Predmetnik(studijski_program = UNI, studijsko_leto=LETO, letnik = LETNIK, predmet = a)
    pr.save()
    a = Predmet(ime = "Osnove matematične analize", id="63202")
    a.save()
    pr = Predmetnik(studijski_program = UNI, studijsko_leto=LETO, letnik = LETNIK, predmet = a)
    pr.save()
    a = Predmet(ime = "Linearna algebra", id="63207")
    a.save()
    pr = Predmetnik(studijski_program = UNI, studijsko_leto=LETO, letnik = LETNIK, predmet = a)
    pr.save()
    a = Predmet(ime = "Osnove informacijskih sistemov", id="63215")
    a.save()
    pr = Predmetnik(studijski_program = UNI, studijsko_leto=LETO, letnik = LETNIK, predmet = a)
    pr.save()
    a = Predmet(ime = "Računalniške komunikacije", id="63209")
    a.save()
    pr = Predmetnik(studijski_program = UNI, studijsko_leto=LETO, letnik = LETNIK, predmet = a)
    pr.save()
    a = Predmet(ime = "Arhitektura računalniških sistemov", id="63212")
    a.save()
    pr = Predmetnik(studijski_program = UNI, studijsko_leto=LETO, letnik = LETNIK, predmet = a)
    pr.save()

    LETNIK = Letnik.objects.get(ime="2.")

    #2 letnik obvezni
    a = Predmet(ime = "Verjetnost in statistika", id="63213")
    a.save()
    pr = Predmetnik(studijski_program = UNI, studijsko_leto=LETO, letnik = LETNIK, predmet = a)
    pr.save()
    a = Predmet(ime = "Algoritmi in podatkovne strukture 1", id="63279")
    a.save()
    pr = Predmetnik(studijski_program = UNI, studijsko_leto=LETO, letnik = LETNIK, predmet = a)
    pr.save()
    a = Predmet(ime = "Osnove podatkovnih baz", id="63208")
    a.save()
    pr = Predmetnik(studijski_program = UNI, studijsko_leto=LETO, letnik = LETNIK, predmet = a)
    pr.save()
    a = Predmet(ime = "Organizacija računalniških sistemov", id="63218")
    a.save()
    pr = Predmetnik(studijski_program = UNI, studijsko_leto=LETO, letnik = LETNIK, predmet = a)
    pr.save()
    a = Predmet(ime = "Izračunljivost in računska zahtevnost", id="63283")
    a.save()
    pr = Predmetnik(studijski_program = UNI, studijsko_leto=LETO, letnik = LETNIK, predmet = a)
    pr.save()
    a = Predmet(ime = "Teorija informacij in sistemov", id="63216")
    a.save()
    pr = Predmetnik(studijski_program = UNI, studijsko_leto=LETO, letnik = LETNIK, predmet = a)
    pr.save()
    a = Predmet(ime = "Algoritmi in podatkovne strukture 2", id="63280")
    a.save()
    pr = Predmetnik(studijski_program = UNI, studijsko_leto=LETO, letnik = LETNIK, predmet = a)
    pr.save()
    a = Predmet(ime = "Operacijski sistemi", id="63217")
    a.save()
    pr = Predmetnik(studijski_program = UNI, studijsko_leto=LETO, letnik = LETNIK, predmet = a)
    pr.save()

    #2 letnik strokovni
    a = Predmet(ime = "Principi programskih jezikov", id="63220", )
    a.save()
    pr = Predmetnik(studijski_program = UNI, studijsko_leto=LETO, letnik = LETNIK, predmet = a, obvezen=False, strokoven=True)
    pr.save()
    a = Predmet(ime = "Računalniške tehnologije", id="63221")
    a.save()
    pr = Predmetnik(studijski_program = UNI, studijsko_leto=LETO, letnik = LETNIK, predmet = a, obvezen=False, strokoven=True)
    pr.save()
    a = Predmet(ime = "Matematično modeliranje", id="63219")
    a.save()
    pr = Predmetnik(studijski_program = UNI, studijsko_leto=LETO, letnik = LETNIK, predmet = a, obvezen=False, strokoven=True)
    pr.save()

    LETNIK = Letnik.objects.get(ime="3.")

    #3 letnik obvezni
    a = Predmet(ime = "Osnove umetne inteligence", id="63214")
    a.save()
    pr = Predmetnik(studijski_program = UNI, studijsko_leto=LETO, letnik = LETNIK, predmet = a)
    pr.save()
    a = Predmet(ime = "Ekonomika in podjetništvo", id="63248")
    a.save()
    pr = Predmetnik(studijski_program = UNI, studijsko_leto=LETO, letnik = LETNIK, predmet = a)
    pr.save()
    a = Predmet(ime = "Diplomski seminar", id="63281")
    a.save()
    pr = Predmetnik(studijski_program = UNI, studijsko_leto=LETO, letnik = LETNIK, predmet = a)
    pr.save()


    #moduli
    modul1 = Modul(ime="Informacijski sistemi")
    modul1.save()
    modul2 = Modul(ime="Obvladovanje informatike")
    modul2.save()
    modul3 = Modul(ime="Računalniška omrežja")
    modul3.save()
    modul4 = Modul(ime="Umetna inteligenca")
    modul4.save()
    modul5 = Modul(ime="Razvoj programske opreme")
    modul5.save()
    modul6 = Modul(ime="Medijske tehnologije")
    modul6.save()


    #informacijski sistemi
    a = Predmet(ime = "Elektronsko poslovanje", id="63249")
    a.save()
    pr = Predmetnik(studijski_program = UNI, studijsko_leto=LETO, letnik = LETNIK, predmet = a, obvezen=False, modul=modul1)
    pr.save()
    a = Predmet(ime = "Poslovna inteligenca", id="63251")
    a.save()
    pr = Predmetnik(studijski_program = UNI, studijsko_leto=LETO, letnik = LETNIK, predmet = a, obvezen=False, modul=modul1)
    pr.save()
    a = Predmet(ime = "Organizacija in management", id="63250")
    a.save()
    pr = Predmetnik(studijski_program = UNI, studijsko_leto=LETO, letnik = LETNIK, predmet = a, obvezen=False, modul=modul1)
    pr.save()

    #obladovanje informatike
    a = Predmet(ime = "Razvoj informacijskih sistemov", id="63252")
    a.save()
    pr = Predmetnik(studijski_program = UNI, studijsko_leto=LETO, letnik = LETNIK, predmet = a, obvezen=False, modul=modul2)
    pr.save()
    a = Predmet(ime = "Tehnologija upravljanja podatkov", id="63226")
    a.save()
    pr = Predmetnik(studijski_program = UNI, studijsko_leto=LETO, letnik = LETNIK, predmet = a, obvezen=False, modul=modul2)
    pr.save()
    a = Predmet(ime = "Planiranje in upravljanje informatike", id="63253")
    a.save()
    pr = Predmetnik(studijski_program = UNI, studijsko_leto=LETO, letnik = LETNIK, predmet = a, obvezen=False, modul=modul2)
    pr.save()

    #racunalniska omrezja
    a = Predmet(ime = "Modeliranje računalniških omrežij", id="63257")
    a.save()
    pr = Predmetnik(studijski_program = UNI, studijsko_leto=LETO, letnik = LETNIK, predmet = a, obvezen=False, modul=modul3)
    pr.save()
    a = Predmet(ime = "Komunikacijski protokoli", id="63258")
    a.save()
    pr = Predmetnik(studijski_program = UNI, studijsko_leto=LETO, letnik = LETNIK, predmet = a, obvezen=False, modul=modul3)
    pr.save()
    a = Predmet(ime = "Brezžična in mobilna omrežja", id="63259")
    a.save()
    pr = Predmetnik(studijski_program = UNI, studijsko_leto=LETO, letnik = LETNIK, predmet = a, obvezen=False, modul=modul3)
    pr.save()

    #umetna inteligenca
    a = Predmet(ime = "Inteligentni sistemi", id="63266")
    a.save()
    pr = Predmetnik(studijski_program = UNI, studijsko_leto=LETO, letnik = LETNIK, predmet = a, obvezen=False, modul=modul4)
    pr.save()
    a = Predmet(ime = "Umetno zaznavanje", id="63267")
    a.save()
    pr = Predmetnik(studijski_program = UNI, studijsko_leto=LETO, letnik = LETNIK, predmet = a, obvezen=False, modul=modul4)
    pr.save()
    a = Predmet(ime = "Razvoj inteligentnih sistemov", id="63262")
    a.save()
    pr = Predmetnik(studijski_program = UNI, studijsko_leto=LETO, letnik = LETNIK, predmet = a, obvezen=False, modul=modul4)
    pr.save()

    #razvoj programske opreme
    a = Predmet(ime = "Postopki razvoja programske opreme", id="63254")
    a.save()
    pr = Predmetnik(studijski_program = UNI, studijsko_leto=LETO, letnik = LETNIK, predmet = a, obvezen=False, modul=modul5)
    pr.save()
    a = Predmet(ime = "Spletno programiranje", id="63255")
    a.save()
    pr = Predmetnik(studijski_program = UNI, studijsko_leto=LETO, letnik = LETNIK, predmet = a, obvezen=False, modul=modul5)
    pr.save()
    a = Predmet(ime = "Tehnologija programske opreme", id="63256")
    a.save()
    pr = Predmetnik(studijski_program = UNI, studijsko_leto=LETO, letnik = LETNIK, predmet = a, obvezen=False, modul=modul5)
    pr.save()

    #medijske tehnologije
    a = Predmet(ime = "Računalniška grafika in tehnologija iger", id="63269")
    a.save()
    pr = Predmetnik(studijski_program = UNI, studijsko_leto=LETO, letnik = LETNIK, predmet = a, obvezen=False, modul=modul6)
    pr.save()
    a = Predmet(ime = "Multimedijski sistemi", id="63270")
    a.save()
    pr = Predmetnik(studijski_program = UNI, studijsko_leto=LETO, letnik = LETNIK, predmet = a, obvezen=False, modul=modul6)
    pr.save()
    a = Predmet(ime = "Osnove oblikovanja", id="63271")
    a.save()
    pr = Predmetnik(studijski_program = UNI, studijsko_leto=LETO, letnik = LETNIK, predmet = a, obvezen=False, modul=modul6)
    pr.save()

    LETNIK = Letnik.objects.get(ime="2.")

    #splosno izbirni predmeti
    a = Predmet(ime = "Tehnične veščine", id="63284", kreditne_tocke=3)
    a.save()
    LETNIK = Letnik.objects.get(ime="2.")
    pr = Predmetnik(studijski_program = UNI, studijsko_leto=LETO, letnik = LETNIK, predmet = a, obvezen=False)
    pr.save()
    LETNIK = Letnik.objects.get(ime="3.")
    pr = Predmetnik(studijski_program = UNI, studijsko_leto=LETO, letnik = LETNIK, predmet = a, obvezen=False)
    pr.save()

    a = Predmet(ime = "Angleški jezik nivo A", id="63222", kreditne_tocke=3)
    a.save()
    LETNIK = Letnik.objects.get(ime="2.")
    pr = Predmetnik(studijski_program = UNI, studijsko_leto=LETO, letnik = LETNIK, predmet = a, obvezen=False)
    pr.save()
    LETNIK = Letnik.objects.get(ime="3.")
    pr = Predmetnik(studijski_program = UNI, studijsko_leto=LETO, letnik = LETNIK, predmet = a, obvezen=False)
    pr.save()

    a = Predmet(ime = "Angleški jezik nivo B", id="63746", kreditne_tocke=3)
    a.save()
    LETNIK = Letnik.objects.get(ime="2.")
    pr = Predmetnik(studijski_program = UNI, studijsko_leto=LETO, letnik = LETNIK, predmet = a, obvezen=False)
    pr.save()
    LETNIK = Letnik.objects.get(ime="3.")
    pr = Predmetnik(studijski_program = UNI, studijsko_leto=LETO, letnik = LETNIK, predmet = a, obvezen=False)
    pr.save()

    a = Predmet(ime = "Angleški jezik nivo C", id="63747", kreditne_tocke=3)
    a.save()
    LETNIK = Letnik.objects.get(ime="2.")
    pr = Predmetnik(studijski_program = UNI, studijsko_leto=LETO, letnik = LETNIK, predmet = a, obvezen=False)
    pr.save()
    LETNIK = Letnik.objects.get(ime="3.")
    pr = Predmetnik(studijski_program = UNI, studijsko_leto=LETO, letnik = LETNIK, predmet = a, obvezen=False)
    pr.save()

    a = Predmet(ime = "Računalništvo v praksi I", id="63752", kreditne_tocke=3)
    a.save()
    LETNIK = Letnik.objects.get(ime="2.")
    pr = Predmetnik(studijski_program = UNI, studijsko_leto=LETO, letnik = LETNIK, predmet = a, obvezen=False)
    pr.save()
    LETNIK = Letnik.objects.get(ime="3.")
    pr = Predmetnik(studijski_program = UNI, studijsko_leto=LETO, letnik = LETNIK, predmet = a, obvezen=False)
    pr.save()

    a = Predmet(ime = "Računalništvo v praksi II", id="63242", kreditne_tocke=3)
    a.save()
    LETNIK = Letnik.objects.get(ime="2.")
    pr = Predmetnik(studijski_program = UNI, studijsko_leto=LETO, letnik = LETNIK, predmet = a, obvezen=False)
    pr.save()
    LETNIK = Letnik.objects.get(ime="3.")
    pr = Predmetnik(studijski_program = UNI, studijsko_leto=LETO, letnik = LETNIK, predmet = a, obvezen=False)
    pr.save()

    VSS = StudijskiProgram.objects.get(id=1000470)
    LETO = StudijskoLeto.objects.get(ime="2018/2019")
    LETNIK = Letnik.objects.get(ime="1.")

    a = Predmet(ime = "Računalniške komunikacije", id="63708")
    a.save()
    pr = Predmetnik(studijski_program = VSS, studijsko_leto=LETO, letnik = LETNIK, predmet = a)
    pr.save()
    narediIzvedbo(pr, narediProfesorja("Mojca","Ciglarič"))

    a = Predmet(ime = "Programiranje 1", id="63702")
    a.save()
    pr = Predmetnik(studijski_program = VSS, studijsko_leto=LETO, letnik = LETNIK, predmet = a)
    pr.save()
    narediIzvedbo(pr, narediProfesorja("Janez","Demšar"))

    a = Predmet(ime = "Podatkovne baze", id="63707")
    a.save()
    pr = Predmetnik(studijski_program = VSS, studijsko_leto=LETO, letnik = LETNIK, predmet = a)
    pr.save()
    narediIzvedbo(pr, narediProfesorja("Matjaž","Kukar"))

    a = Predmet(ime = "Programiranje 2", id="63706")
    a.save()
    pr = Predmetnik(studijski_program = VSS, studijsko_leto=LETO, letnik = LETNIK, predmet = a)
    pr.save()
    narediIzvedbo(pr, narediProfesorja("Tomaž","Dobravec"))

    a = Predmet(ime = "Diskretne strukture", id="63705")
    a.save()
    pr = Predmetnik(studijski_program = VSS, studijsko_leto=LETO, letnik = LETNIK, predmet = a)
    pr.save()
    narediIzvedbo(pr, narediProfesorja("Sandi","Klavžar"))

    a = Predmet(ime = "Matematika", id="63704")
    a.save()
    pr = Predmetnik(studijski_program = VSS, studijsko_leto=LETO, letnik = LETNIK, predmet = a)
    pr.save()
    narediIzvedbo(pr, narediProfesorja("Roman","Drnovšek"))

    a = Predmet(ime = "Uvod v računalništvo", id="63701")
    a.save()
    pr = Predmetnik(studijski_program = VSS, studijsko_leto=LETO, letnik = LETNIK, predmet = a)
    pr.save()
    narediIzvedbo(pr, narediProfesorja("Danijel","Skočaj"))

    a = Predmet(ime = "Računalniška arhitektura", id="63703")
    a.save()
    pr = Predmetnik(studijski_program = VSS, studijsko_leto=LETO, letnik = LETNIK, predmet = a)
    pr.save()
    narediIzvedbo(pr, narediProfesorja("Igor","Škraba"))

def narediStudenta(vpisna_stevilka_, ime_, priimek_, emso_, drzava_rojstva_, obcina_rojstva_, stalni_naslov_, drzava_, posta_, mail_number, telefon_):
    student = Student(
     vpisna_stevilka = vpisna_stevilka_, #number
     emso=emso_, #str
     ime=ime_, #str
     drzava_rojstva=drzava_rojstva_,
     obcina_rojstva= obcina_rojstva_,  
     priimek=priimek_, #str
     naslov_stalno_bivalisce=stalni_naslov_,
     drzava= Drzava.objects.filter(pk=4)[0], 
     posta= Posta.objects.filter(pk=1293)[0],
     obcina= Obcina.objects.filter(pk=1)[0],
     telefon=telefon_,
     email=str("%c%c%04d@student.uni-lj.si" % (ime_[0].lower(), priimek_[0].lower(), mail_number)))
    student.save()

    

    user, created = User.objects.get_or_create(username=str("%s%s" % (ime_.lower(), priimek_.lower())), email=str("%c%c%04d@student.uni-lj.si" % (ime_[0].lower(), priimek_[0].lower(), mail_number)))
    user.first_name = ime_
    user.last_name = priimek_

    if created:
        user.set_password("adminadmin")
        user.is_staff=False
        user.is_superuser=False
        ref_group, status = Group.objects.get_or_create(name='students') 
        ref_group.user_set.add(user)
    
    user.save()
    return student

def narediReferenta(ime, priimek):
    #naredi referenta
    user, created = User.objects.get_or_create(username=str("%s%s" % (ime.lower(), priimek.lower())), email=str("%s%s@fri.uni-lj.si" % (ime, priimek)))
    user.first_name = ime
    user.last_name = priimek
    user.set_password("adminadmin")
    if created:
        user.set_password("adminadmin")
        user.is_staff=False
        user.is_superuser=False
        ref_group, status = Group.objects.get_or_create(name='referent') 
        ref_group.user_set.add(user)

    user.save()

