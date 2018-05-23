from django.db import models
from sifranti.models import *

#ONLY one key is allowed

class Student(models.Model):
    #vpisna stevilka je primarni kljuc
    
    vpisna_stevilka = models.IntegerField(primary_key = True)
    emso = models.CharField(max_length = 13, verbose_name= "EMŠO")
    priimek = models.CharField(max_length = 30, verbose_name= "Priimek")
    ime = models.CharField(max_length = 30, verbose_name= "Ime")
    datum_rojstva = models.CharField(max_length=100)

    #obcine so blank=True, zaradi konsistentosti
    naslov_stalno_bivalisce = models.CharField(max_length = 260, verbose_name= "Stalno prebivališče") #Formata: Godešič 163, 4220 Škofja Loka --> Za izpis potrdila o vpisu
    drzava = models.ForeignKey(Drzava, null=True, on_delete = models.SET_NULL, verbose_name= "Država stalno",related_name="drzava_stalno")
    obcina = models.ForeignKey(Obcina, on_delete = models.SET_NULL, blank=True, null=True, verbose_name= "Občina stalno",related_name="obcina_stalno")
    posta = models.ForeignKey(Posta,blank=True, on_delete = models.SET_NULL, null=True, verbose_name= "Pošta",related_name="posta")

    #ce sploh potrebuje zacasni naslov
    # if true ima zacasno bivalisce
    ima_zacasno = models.BooleanField(default=False, verbose_name="Začasni naslov")
    # if true posilji posto na zacasni naslov otherwise na stalno bivalisce
    ima_posto_na_zacasni = models.BooleanField(default=False, verbose_name="Pošiljanje pošte na začasni naslov")

    naslov_zacasno_bivalisce = models.CharField(max_length = 260, blank=True, null=True, verbose_name= "Začasno prebivališče")
    drzava_zacasno = models.ForeignKey(Drzava, null=True, blank=True,on_delete = models.SET_NULL, verbose_name= "Država začasno",related_name="drzava_zacasno")
    obcina_zacasno = models.ForeignKey(Obcina, blank=True,on_delete = models.SET_NULL, null=True, verbose_name= "Občina začasno",related_name="obcina_zacasno")
    posta_zacasno = models.ForeignKey(Posta, blank=True, on_delete = models.SET_NULL, null=True, verbose_name= "Pošta začasno",related_name="posta_zacasno")

    #datum_rojstva = models.DateField(auto_now=True, verbose_name="Datum rojstvaa")
    #

    drzava_rojstva = models.ForeignKey(Drzava, null=True, on_delete = models.SET_NULL, verbose_name= "Država rojstva",related_name="drzava_rojstva")
    obcina_rojstva = models.ForeignKey(Obcina, blank=True, on_delete = models.SET_NULL, null=True, verbose_name= "Občina rojstva",related_name="obcina_rojstva")

    telefon = models.CharField(max_length = 15, verbose_name= "Telefon") # reci je treba se mal preverit
    email = models.CharField(max_length = 60, unique = True, verbose_name= "e-pošta")
    # tu naj bi prisli se vsi vpisi, verjetno bodo vpisi kazali na studenta
    # one to many se izrazi z foreign keyom
    # ce je ze izkoristil absolventa
    dodatno_leto = models.BooleanField(default = True)


    def __str__(self):
        return str(self.vpisna_stevilka) + ", " + self.priimek + " " + self.ime
    class Meta:
        ordering = ['priimek', 'ime', 'vpisna_stevilka']

class Kandidat(models.Model):
    vpisna_stevilka = models.IntegerField(primary_key = True)
    ime = models.CharField(max_length = 30)
    priimek = models.CharField(max_length = 30)
    email = models.CharField(max_length = 60)
    # studijski_program FK
    studijski_program = models.ForeignKey(StudijskiProgram, null = True, on_delete= models.SET_NULL)
    izkoriscen = models.BooleanField(default = False)

class Zeton(models.Model):
    student = models.ForeignKey(Student, on_delete= models.CASCADE)
    studijski_program = models.ForeignKey(StudijskiProgram, null = True, on_delete= models.SET_NULL)
    letnik = models.ForeignKey(Letnik, null=True, on_delete= models.SET_NULL)

    vrsta_vpisa = models.ForeignKey(VrstaVpisa, null=True, on_delete= models.SET_NULL)
    nacin_studija = models.ForeignKey(NacinStudija, null=True, on_delete= models.SET_NULL)
    # vrsta studija je kao oblika studija
    vrsta_studija  = models.ForeignKey(VrstaStudija, null=True, on_delete= models.SET_NULL)
    oblika_studija = models.ForeignKey(OblikaStudija, null=True, on_delete= models.SET_NULL)
    # ce ima pravico do proste izbire predmetov v 3.letniku
    pravica_do_izbire = models.BooleanField(default = False)
    #ali je bil zeton izkoriscen, torej ce ga je student ze uporabil za vpis
    izkoriscen = models.BooleanField(default=False)


class Vpis(models.Model):
    student = models.ForeignKey(Student, primary_key = True,  on_delete= models.CASCADE)
    
    studijsko_leto = models.ForeignKey(StudijskoLeto, null= True, on_delete=models.SET_NULL)

    studijski_program = models.ForeignKey(StudijskiProgram, null=True, on_delete= models.SET_NULL)
    letnik = models.ForeignKey(Letnik, null=True, on_delete= models.SET_NULL)

    vrsta_vpisa = models.ForeignKey(VrstaVpisa, null=True, on_delete= models.SET_NULL)
    
    nacin_studija = models.ForeignKey(NacinStudija, null=True, on_delete= models.SET_NULL)
    
    oblika_studija = models.ForeignKey(OblikaStudija, null=True, on_delete= models.SET_NULL)
    # vrsta studija je kao oblika studija
    vrsta_studija  = models.ForeignKey(VrstaStudija, null=True, on_delete= models.SET_NULL)
    # predmeti_studenta s foreign keyom
    # ali je bil vpis ze potrjen, ali ga je referentka potrdila
    potrjen = models.BooleanField(default = False)
    #pravica do proste izbire predmetov v 3. letniku
    prosta_izbira = models.BooleanField(default = False)
    #ce je dokoncal vpis - potrebuje se pri izpisu vpisov na /vpis
    dokoncan_vpis = models.BooleanField(default = False)

    class Meta:
        unique_together = (('student', 'studijsko_leto'),)
    
class Modul(models.Model):
    ime = models.CharField(max_length=100, unique=True,verbose_name="Ime Modula")

class Predmetnik(models.Model):
    studijski_program = models.ForeignKey(StudijskiProgram, on_delete= models.CASCADE)
    studijsko_leto = models.ForeignKey(StudijskoLeto, null=True, on_delete= models.SET_NULL)
    letnik = models.ForeignKey(Letnik, null=True, on_delete= models.SET_NULL)
    predmet = models.ForeignKey(Predmet, null=True, on_delete= models.SET_NULL)
    obvezen = models.BooleanField(default = True)
    ima_modul = models.BooleanField(default = False)
    strokoven = models.BooleanField(default = False)

    modul = models.ForeignKey(Modul, null=True, blank=True, on_delete= models.SET_NULL)

    class Meta:
        unique_together = (('studijski_program', 'studijsko_leto', 'letnik', 'predmet'),)



