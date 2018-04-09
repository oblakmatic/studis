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

class Predmet(models.Model):

    ime = models.CharField(max_length=100)

class Modul(models.Model):
# sestavljen iz treh predmetov
# OK modul ni sifrant sam naj mu bo
    predmet_ena = models.ForeignKey(Predmet, on_delete= models.SET_NULL, null=True, related_name = 'predmet_ena')
    predmet_dva = models.ForeignKey(Predmet, on_delete= models.SET_NULL, null=True, related_name = 'predmet_dva')
    predmet_tri = models.ForeignKey(Predmet, on_delete= models.SET_NULL, null=True, related_name = 'predmet_tri')

class VrstaVpisa(models.Model):
#prvi vpis, ponovni vpis, absolvent
    ime = models.CharField(max_length=100)


class VrstaStudija(models.Model):
#univerzitetni, visokosolski
    ime = models.CharField(max_length=100)

class Letnik(models.Model):
#1., 2. ,3. letnik
    ime = models.CharField(max_length=100)
class StudijskoLeto(models.Model):
# 2017/2018, 2018/2019
    ime = models.CharField(max_length=100)


class NacinStudija(models.Model):
#redni, izredni
    ime = models.CharField(max_length=100)   