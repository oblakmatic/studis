from django.db import models
from sifranti.models import *

#ONLY one key is allowed

class Student(models.Model):
    #vpisna stevilka je primarni kljuc
    vpisna_stevilka = models.IntegerField(primary_key = True)
    emso = models.CharField(max_length = 13)
    priimek = models.CharField(max_length = 30)
    ime = models.CharField(max_length = 30)
    naslov_stalno_bivalisce = models.CharField(max_length = 260)
    naslov_zacasno_bivalisce = models.CharField(max_length = 260, blank=True, null=True)
    drzava = models.ForeignKey(Drzava, null=True, on_delete = models.SET_NULL)
    kraj_rojstva = models.CharField(max_length = 260) # kako bomo preverjali konsistentnost drzave in obcine rojstva
    
    posta = models.ForeignKey(Posta, on_delete = models.SET_NULL, null=True)
    obcina = models.ForeignKey(Obcina, on_delete = models.SET_NULL, null=True)
    telefon = models.CharField(max_length = 15) # reci je treba se mal preverit
    email = models.CharField(max_length = 60, unique = True)
    # tu naj bi prisli se vsi vpisi, verjetno bodo vpisi kazali na studenta
    # one to many se izrazi z foreign keyom
    dodatno_leto = models.BooleanField(default = True)

class Kandidat(models.Model):
    vpisna_stevilka = models.IntegerField(primary_key = True)
    ime = models.CharField(max_length = 30)
    priimek = models.CharField(max_length = 30)
    email = models.CharField(max_length = 60)
    # studijski_program FK
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
    # ?? potrjen = models.BooleanField(default = False)
    # ?? prosta_izbira = models.BooleanField(default = False)

