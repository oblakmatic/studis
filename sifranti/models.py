from django.db import models

# Create your models here.
# Add ONLY if the table does not have foreign keys (sifrant)
# IF you add new sifrant here, add name into table diff_names (views.py)
# AND you have to add Form Class in forms.py, go and see it is easy

#razred ki je odgovoren za default query
# ce je query Sifrant.objects.all() se ubistvu izvede Sifrant.objects.filter(veljaven=True)

#ce zelis vse sifrante, tudi neveljavne daj Sifrant.all_objects.all()

class Veljavni(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(veljaven=True)

class Drzava(models.Model):

    # id je numerična oznaka
    id = models.DecimalField(primary_key=True, max_digits=3, decimal_places=0, verbose_name="Numerična oznaka" )
    dvomestna_koda = models.CharField(max_length=2,unique = True, verbose_name="Dvomestna koda")
    tromestna_oznaka = models.CharField(max_length=3, unique = True, verbose_name="Tromestna oznaka")
    iso_naziv = models.CharField(max_length=100, verbose_name="ISO naziv")
    slovenski_naziv = models.CharField(max_length=100, verbose_name="Slovenski naziv")
    opomba = models.CharField(max_length=400, verbose_name="Opomba")
    veljaven = models.BooleanField(default=True, verbose_name="Veljavnost šifranta")

    objects = Veljavni()
    all_objects = models.Manager()

    def __str__(self):
        return str(self.id) + " " + self.slovenski_naziv

class Obcina(models.Model):

    #id je sifra obcine
    id = models.DecimalField(primary_key=True, max_digits=3, decimal_places=0, verbose_name="Šifra občine" )
    ime = models.CharField(max_length=100, verbose_name="Ime")
    veljaven = models.BooleanField(default=True, verbose_name="Veljavnost šifranta")
    def __str__(self):
        return str(self.id) + " " + self.ime

    objects = Veljavni()
    all_objects = models.Manager()


class Posta(models.Model):
    
    #id je sifra obcine
    id = models.IntegerField(primary_key=True, verbose_name="Poštna številka" )
    kraj = models.CharField(max_length=100 , verbose_name="Kraj")
    veljaven = models.BooleanField(default = True, verbose_name="Veljavnost šifranta")

    objects = Veljavni()
    all_objects = models.Manager()

    def __str__(self):
        return str(self.id) + " " + self.kraj

class StudijskiProgram(models.Model):
#dodiplomski, magisterki, doktorski,
    
    #id je sŠifra EVŠ
    id = models.DecimalField(primary_key=True, verbose_name="Šifra EVŠ",decimal_places=0, max_digits= 7)
    sifra = models.CharField(max_length=2, verbose_name="Šifra",unique=True)
    stopnja = models.CharField(max_length=100, verbose_name="Stopnja")
    semestri = models.IntegerField(verbose_name="Število semestrov")
    naziv = models.CharField(max_length=100,verbose_name="Naziv")
    veljaven = models.BooleanField(default=True, verbose_name="Veljavnost šifranta")

    objects = Veljavni()
    all_objects = models.Manager()

    def __str__(self):
        return self.naziv
class VrstaStudija(models.Model):
#univerzitetni, visokosolski

    id = models.IntegerField(primary_key=True,verbose_name="Šifra")
    opis = models.CharField(max_length=150, verbose_name="Opis")
    nacin_zakljucka = models.CharField(max_length=100, verbose_name="Način zaključka šolanja")
    raven_klasius = models.CharField(max_length=10,verbose_name="Raven izobrazbe po KLASIUS-SRV")
    veljaven = models.BooleanField(default=True, verbose_name="Veljavnost šifranta")

    objects = Veljavni()
    all_objects = models.Manager()

    def __str__(self):
        return str(self.id) + " " + self.opis 

class VrstaVpisa(models.Model):

    id = models.IntegerField(primary_key=True,verbose_name="Šifra")
    opis = models.CharField(max_length=100, verbose_name="Opis vrste vpisa")
    mozni_letniki = models.CharField(max_length=200, verbose_name="Možni letniki študija")
    veljaven = models.BooleanField(default=True, verbose_name="Veljavnost šifranta")

    objects = Veljavni()
    all_objects = models.Manager()
    def __str__(self):
        return self.opis

class NacinStudija(models.Model):
#redni, izredni

    id = models.IntegerField(primary_key=True,verbose_name="Šifra")
    opis = models.CharField(max_length=100, verbose_name="Opis")
    ang_opis = models.CharField(max_length=100, verbose_name="Angleški opis")
    veljaven = models.BooleanField(default=True, verbose_name="Veljavnost šifranta")

    objects = Veljavni()
    all_objects = models.Manager()    

    def __str__(self):
        return self.opis   


class OblikaStudija(models.Model):

    id = models.IntegerField(primary_key=True,verbose_name="Šifra")
    opis = models.CharField(max_length=100, verbose_name="Opis")
    ang_opis = models.CharField(max_length=100, verbose_name="Angleški opis")
    veljaven = models.BooleanField(default=True, verbose_name="Veljavnost šifranta")

    objects = Veljavni()
    all_objects = models.Manager()

    def __str__(self):
        return str(self.id) + " " + self.opis


class Predmet(models.Model):

    id = models.IntegerField(primary_key=True,verbose_name="Šifra")
    ime = models.CharField(max_length=100,unique=True,verbose_name="Ime predmeta")
    kreditne_tocke=models.IntegerField(default=6, verbose_name="Kreditne točke")
    veljaven = models.BooleanField(default=True, verbose_name="Veljavnost šifranta")
    
    objects = Veljavni()
    all_objects = models.Manager()

    def __str__(self):
        return self.ime


class StudijskoLeto(models.Model):
# 2017/2018, 2018/2019
    ime = models.CharField(max_length=100, unique=True,verbose_name="Ime")
    veljaven = models.BooleanField(default=True, verbose_name="Veljavnost šifranta")

    objects = Veljavni()
    all_objects = models.Manager()

    def __str__(self):
        return self.ime

class Letnik(models.Model):
    ime = models.CharField(max_length=100, unique=True,verbose_name="Ime")
    veljaven = models.BooleanField(default=True, verbose_name="Veljavnost šifranta")

    objects = Veljavni()
    all_objects = models.Manager()

    def __str__(self):
        return self.ime