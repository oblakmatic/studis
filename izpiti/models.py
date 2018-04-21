from django.db import models
from sifranti.models import *
from student.models import *

class Ucitelj(models.Model):
    ime = models.CharField(max_length = 30)
    priimek = models.CharField(max_length = 30)
    email = models.CharField(max_length = 60, unique = True)

class IzvedbaPredmeta(models.Model):
    predmet = models.ForeignKey(Predmet, on_delete = models.SET_NULL, null = True)
    studijsko_leto = models.ForeignKey(StudijskoLeto, on_delete = models.SET_NULL, null = True)
    ucitelj_1 = models.ForeignKey(Ucitelj, related_name = "ucitelj_1", on_delete = models.SET_NULL, null = True)
    ucitelj_2 = models.ForeignKey(Ucitelj, related_name = "ucitelj_2", on_delete = models.SET_NULL, default=None, blank=True, null=True)
    ucitelj_3 = models.ForeignKey(Ucitelj, related_name = "ucitelj_3", on_delete = models.SET_NULL, default=None, blank=True, null=True)

class Rok(models.Model):
    izvedba_predmeta = models.ForeignKey(IzvedbaPredmeta, on_delete = models.SET_NULL, null = True)
    datum = models.DateField()

class PredmetiStudenta(models.Model):
    vpis = models.ForeignKey(Vpis, on_delete = models.SET_NULL, null = True)
    predmet = models.ForeignKey(Predmet, on_delete = models.SET_NULL, null = True)
    

class Prijava(models.Model):
    predmeti_studenta = models.ForeignKey(PredmetiStudenta, on_delete = models.SET_NULL, null = True)
    rok = models.ForeignKey(Rok, on_delete = models.SET_NULL, null = True)

    zaporedna_stevilka_polaganja = models.IntegerField()
    podatki_o_placilu = models.CharField(max_length = 260, default=None, blank=True, null=True)
