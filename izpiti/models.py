from django.db import models
from sifranti.models import *
from student.models import *
from django.conf import settings
from datetime import datetime

class Ucitelj(models.Model):
    ime = models.CharField(max_length = 30)
    priimek = models.CharField(max_length = 30)
    email = models.CharField(max_length = 60, unique = True)
    predmeti = models.ManyToManyField(Predmet, null = True)#dodv da ves kere mu pokazat za vpis roka

    def __str__(self):
        return str("(%07d) %s %s" % (self.id, self.ime, self.priimek))

class IzvedbaPredmeta(models.Model):
    predmet = models.ForeignKey(Predmet, on_delete = models.SET_NULL, null = True)
    studijsko_leto = models.ForeignKey(StudijskoLeto, on_delete = models.SET_NULL, null = True)
    ucitelj_1 = models.ForeignKey(Ucitelj, related_name = "ucitelj_1", on_delete = models.SET_NULL, null = True)
    ucitelj_2 = models.ForeignKey(Ucitelj, related_name = "ucitelj_2", on_delete = models.SET_NULL, default=None, blank=True, null=True)
    ucitelj_3 = models.ForeignKey(Ucitelj, related_name = "ucitelj_3", on_delete = models.SET_NULL, default=None, blank=True, null=True)

class Rok(models.Model):
    izvedba_predmeta = models.ForeignKey(IzvedbaPredmeta, on_delete = models.SET_NULL, null = True)
    datum = models.DateTimeField()
    prostor_izvajanja = models.CharField(max_length = 30)

class PredmetiStudenta(models.Model):
    vpis = models.ForeignKey(Vpis, on_delete = models.SET_NULL, null = True)#
    predmeti = models.ManyToManyField(Predmet, null = True) #Dodob ManyToManyField pa zbrisu on_delete = models.SET_NULL
    

class Prijava(models.Model):
    created_at = models.DateTimeField(default=datetime.now)
    predmeti_studenta = models.ForeignKey(PredmetiStudenta, on_delete = models.SET_NULL, null = True)
    rok = models.ForeignKey(Rok, on_delete = models.SET_NULL, null = True)

    zaporedna_stevilka_polaganja = models.IntegerField() #ubistvu se ne rab ce gremo po novem.
    podatki_o_placilu = models.CharField(max_length = 260, default=None, blank=True, null=True)
    aktivna_prijava = models.BooleanField(default = True)
    ocena = models.IntegerField(default=None,null=True)
    ocena_izpita = models.IntegerField(default=None,null=True)
    #dodav, ko ucitelj odjavi izpit--> se zabelezijo podatki o odjavilteju in cas odjave
    cas_odjave = models.DateTimeField(default=None,null=True)
    odjavitelj = models.CharField(max_length = 100, default=None, blank=True, null=True)