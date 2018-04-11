from django.db import models

# Create your models here.
# Add ONLY if the table does not have foreign keys (sifrant)
# IF you add new sifrant here, add name into table diff_names (views.py)
# AND you have to add Form Class in forms.py, go and see it is easy
class Drzava(models.Model):
    ime = models.CharField(max_length=100)

    def __str__(self):
        return self.ime

class Obcina(models.Model):
    ime = models.CharField(max_length=100)

class Posta(models.Model):
    ime = models.CharField(max_length=100)
    postna_stevilka = models.IntegerField()

    def __str__(self):
        return self.ime

class StudijskiProgram(models.Model):
#dodiplomski, magisterki, doktorski,
    
    PROGRAMS = (
        ('DIPL','Dodiplomski'),
        ('MAG','Magistrski'),
        ('DR','Doktorski')
    )
    ime = models.CharField(max_length=4, choices=PROGRAMS)
    def __str__(self):
        return self.get_ime_display()

class Predmet(models.Model):

    ime = models.CharField(max_length=100)

    def __str__(self):
        return self.get_ime_display()

class Modul(models.Model):
# sestavljen iz treh predmetov
# OK modul ni sifrant sam naj mu bo
    ime= models.CharField(max_length=100)

    predmet_ena = models.ForeignKey(Predmet, on_delete= models.SET_NULL, null=True, related_name = 'predmet_ena')
    predmet_dva = models.ForeignKey(Predmet, on_delete= models.SET_NULL, null=True, related_name = 'predmet_dva')
    predmet_tri = models.ForeignKey(Predmet, on_delete= models.SET_NULL, null=True, related_name = 'predmet_tri')

class VrstaVpisa(models.Model):
#prvi vpis, ponovni vpis, absolvent
    VPISI = (
        (('PRVI', 'Prvi vpis'),
        ('PONO', 'Ponovni'),
        ('ABSO','Absolvent'))
    )


    ime = models.CharField(max_length=100, choices = VPISI)

    def __str__(self):
        return self.get_ime_display()

class VrstaStudija(models.Model):
#univerzitetni, visokosolski
    VRSTE = (
        ('VSŠ','Visokošolski'),
        ('UNI','Univerzitetni')

    )

    ime = models.CharField(max_length=100, choices=VRSTE)

class Letnik(models.Model):
#1., 2. ,3. letnik
    LETNIKI = (
        ('1.','1. letnik'),
        ('2.','2. letnik'),
        ('3.','3. letnik')
    )

    ime = models.CharField(max_length=100,choices =LETNIKI)
    def __str__(self):
        return self.get_ime_display()

class StudijskoLeto(models.Model):
# 2017/2018, 2018/2019
    ime = models.CharField(max_length=100)

    def __str__(self):
        return self.ime


class NacinStudija(models.Model):
#redni, izredni
    NACINI = (
        ('RED','Redni'),
        ('IZR','Izredni')
    )

    ime = models.CharField(max_length=100,choices= NACINI)
    def __str__(self):
        return self.get_ime_display()   