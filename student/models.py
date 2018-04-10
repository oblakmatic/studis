from django.db import models

class Student(models.Model):
    emso = models.CharField(max_length = 13)
    priimek = models.CharField(max_length = 30)
    ime = models.CharField(max_length = 30)
    naslov_stalno_bivalisce = models.CharField(max_length = 260)
    naslov_zacasno_bivalisce = models.CharField(max_length = 260)
    # foreign key drzava
    kraj_rojstva = models.CharField(max_length = 260) # kako bomo preverjali konsistentnost drzave in obcine rojstva
    naslov_posta = models.CharField(max_length = 260)
    # posta = models.ForeignKey(Posta)
    # foreign key obcina
    telefon = models.CharField(max_length = 15) # reci je treba se mal preverit
    email = models.CharField(max_length = 60)
    # tu naj bi prisli se vsi vpisi, verjetno bodo vpisi kazali na studenta
    dodatno_leto = models.BooleanField(default = True)

class Kandidat(models.Model):
    vpisna_stevilka = models.IntegerField(primary_key = True)
    ime = models.CharField(max_length = 30)
    priimek = models.CharField(max_length = 30)
    email = models.CharField(max_length = 60)
    # studijski_program FK
    izkoriscen = models.BooleanField(default = False)



class Vpis(models.Model):
    student = models.ForeignKey(Student, primary_key = True, on_delete = models.CASCADE)
    # studijsko_leto = models.ForeignKey(StudijskoLeto, primary_key = True)
    # studijski program   FK
    letnik = models.IntegerField()
    # studijski_program   FK
    # vrsta_vpisa         FK
    # nacin_studija       FK
    # oblika_studija      FK
    # predmeti_studenta   FK
    potrjen = models.BooleanField(default = False)
    prosta_izira = models.BooleanField(default = False)


