from django.db import models
from sifranti.models import *

#ONLY one key is allowed

class Student(models.Model):
    #vpisna stevilka je primarni kljuc
    vpisna_stevilka = models.IntegerField(primary_key = True)
    emso = models.CharField(max_length = 13, verbose_name= "EMŠO")
    priimek = models.CharField(max_length = 30, verbose_name= "Priimek")
    ime = models.CharField(max_length = 30, verbose_name= "Ime")
    naslov_stalno_bivalisce = models.CharField(max_length = 260, verbose_name= "Stalno prebivališče") #Formata: Godešič 163, 4220 Škofja Loka --> Za izpis potrdila o vpisu
    naslov_zacasno_bivalisce = models.CharField(max_length = 260, blank=True, null=True, verbose_name= "Začasno prebivališče")
    
    drzava_rojstva = models.ForeignKey(Drzava, null=True, on_delete = models.SET_NULL, verbose_name= "Država rojstva",related_name="drzava_rojstva")
    obcina_rojstva = models.ForeignKey(Obcina, on_delete = models.SET_NULL, null=True, verbose_name= "Občina rojstva",related_name="obcina_rojstva")

    drzava = models.ForeignKey(Drzava, null=True, on_delete = models.SET_NULL, verbose_name= "Država")
    posta = models.ForeignKey(Posta, on_delete = models.SET_NULL, null=True, verbose_name= "Pošta")
    obcina = models.ForeignKey(Obcina, on_delete = models.SET_NULL, null=True, verbose_name= "Občina")
    telefon = models.CharField(max_length = 15, verbose_name= "Telefon") # reci je treba se mal preverit
    email = models.CharField(max_length = 60, unique = True, verbose_name= "e-pošta")
    # tu naj bi prisli se vsi vpisi, verjetno bodo vpisi kazali na studenta
    # one to many se izrazi z foreign keyom
    # ce je ze izkoristil absolventa
    dodatno_leto = models.BooleanField(default = True)

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
    # vrsta studija je kao oblika studija
    vrsta_studija  = models.ForeignKey(VrstaStudija, null=True, on_delete= models.SET_NULL)
    # predmeti_studenta s foreign keyom
    # ali je bil vpis ze potrjen, ali ga je referentka potrdila
    potrjen = models.BooleanField(default = False)
    #pravica do proste izbire predmetov v 3. letniku
    prosta_izbira = models.BooleanField(default = False)
    

class Predmetnik(models.Model):
    studijski_program = models.ForeignKey(StudijskiProgram,  primary_key = True, on_delete= models.CASCADE)
    studijsko_leto = models.ForeignKey(StudijskoLeto, null=True, on_delete= models.SET_NULL)
    letnik = models.ForeignKey(Letnik, null=True, on_delete= models.SET_NULL)
    predmet = models.ForeignKey(Predmet, null=True, on_delete= models.SET_NULL)
    obvezen = models.BooleanField(default = True)
