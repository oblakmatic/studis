from django.db import models
from sifranti.models import *
from student.models import *


class Ucitelj(models.Model):
    ime = models.CharField(max_length = 30)
    priimek = models.CharField(max_length = 30)
    email = models.CharField(max_length = 60, unique = True)
    predmeti = models.ManyToManyField(Predmet, null = True)#dodv da ves kere mu pokazat za vpis roka

class IzvedbaPredmeta(models.Model):
    predmet = models.ForeignKey(Predmet, on_delete = models.SET_NULL, null = True)
    studijsko_leto = models.ForeignKey(StudijskoLeto, on_delete = models.SET_NULL, null = True)
    ucitelj_1 = models.ForeignKey(Ucitelj, related_name = "ucitelj_1", on_delete = models.SET_NULL, null = True)
    ucitelj_2 = models.ForeignKey(Ucitelj, related_name = "ucitelj_2", on_delete = models.SET_NULL, default=None, blank=True, null=True)
    ucitelj_3 = models.ForeignKey(Ucitelj, related_name = "ucitelj_3", on_delete = models.SET_NULL, default=None, blank=True, null=True)

class Rok(models.Model):
    izvedba_predmeta = models.ForeignKey(IzvedbaPredmeta, on_delete = models.SET_NULL, null = True)
    datum = models.DateTimeField()

class PredmetiStudenta(models.Model):
    vpis = models.ForeignKey(Vpis, on_delete = models.SET_NULL, null = True)#
    predmeti = models.ManyToManyField(Predmet, null = True) #Dodob ManyToManyField pa zbrisu on_delete = models.SET_NULL
    

class Prijava(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    predmeti_studenta = models.ForeignKey(PredmetiStudenta, on_delete = models.SET_NULL, null = True)
    rok = models.ForeignKey(Rok, on_delete = models.SET_NULL, null = True)

    zaporedna_stevilka_polaganja = models.IntegerField() #ubistvu se ne rab ce gremo po novem.
    podatki_o_placilu = models.CharField(max_length = 260, default=None, blank=True, null=True)

class PrijaveStudenta(models.Model):
    student = models.ForeignKey(Student, primary_key = True, on_delete= models.CASCADE)
    prijave = models.ManyToManyField(Prijava, null = True)
    

    