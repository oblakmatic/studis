from django.db import models

# Create your models here.
# Add ONLY if the table does not have foreign keys (sifrant)
# IF you add new sifrant here, add name into table diff_names
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

