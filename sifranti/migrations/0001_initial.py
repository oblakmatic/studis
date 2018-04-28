# Generated by Django 2.0.4 on 2018-04-26 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Drzava',
            fields=[
                ('id', models.DecimalField(decimal_places=0, max_digits=3, primary_key=True, serialize=False, verbose_name='Numerična oznaka')),
                ('dvomestna_koda', models.CharField(max_length=2, unique=True, verbose_name='Dvomestna koda')),
                ('tromestna_oznaka', models.CharField(max_length=3, unique=True, verbose_name='Tromestna oznaka')),
                ('iso_naziv', models.CharField(max_length=100, verbose_name='ISO naziv')),
                ('slovenski_naziv', models.CharField(max_length=100, verbose_name='Slovenski naziv')),
                ('opomba', models.CharField(max_length=100, verbose_name='Opomba')),
                ('veljaven', models.BooleanField(default=True, verbose_name='Veljavnost šifranta')),
            ],
        ),
        migrations.CreateModel(
            name='Letnik',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ime', models.CharField(max_length=100, unique=True, verbose_name='Ime')),
                ('veljaven', models.BooleanField(default=True, verbose_name='Veljavnost šifranta')),
            ],
        ),
        migrations.CreateModel(
            name='NacinStudija',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False, verbose_name='Šifra')),
                ('opis', models.CharField(max_length=100, verbose_name='Opis')),
                ('ang_opis', models.CharField(max_length=100, verbose_name='Angleški opis')),
                ('veljaven', models.BooleanField(default=True, verbose_name='Veljavnost šifranta')),
            ],
        ),
        migrations.CreateModel(
            name='Obcina',
            fields=[
                ('id', models.DecimalField(decimal_places=0, max_digits=3, primary_key=True, serialize=False, verbose_name='Šifra občine')),
                ('ime', models.CharField(max_length=100, verbose_name='Ime')),
                ('veljaven', models.BooleanField(default=True, verbose_name='Veljavnost šifranta')),
            ],
        ),
        migrations.CreateModel(
            name='OblikaStudija',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False, verbose_name='Šifra')),
                ('opis', models.CharField(max_length=100, verbose_name='Opis')),
                ('ang_opis', models.CharField(max_length=100, verbose_name='Angleški opis')),
                ('veljaven', models.BooleanField(default=True, verbose_name='Veljavnost šifranta')),
            ],
        ),
        migrations.CreateModel(
            name='Posta',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False, verbose_name='Poštna številka')),
                ('kraj', models.CharField(max_length=100, unique=True, verbose_name='Kraj')),
                ('veljaven', models.BooleanField(default=True, verbose_name='Veljavnost šifranta')),
            ],
        ),
        migrations.CreateModel(
            name='Predmet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ime', models.CharField(max_length=100, unique=True)),
                ('veljaven', models.BooleanField(default=True, verbose_name='Veljavnost šifranta')),
            ],
        ),
        migrations.CreateModel(
            name='StudijskiProgram',
            fields=[
                ('id', models.DecimalField(decimal_places=0, max_digits=7, primary_key=True, serialize=False, verbose_name='Šifra EVŠ')),
                ('sifra', models.CharField(max_length=2, unique=True, verbose_name='Šifra')),
                ('stopnja', models.CharField(max_length=100, verbose_name='Stopnja')),
                ('semestri', models.IntegerField(verbose_name='Število semestrov')),
                ('naziv', models.CharField(max_length=4, verbose_name='Naziv')),
                ('veljaven', models.BooleanField(default=True, verbose_name='Veljavnost šifranta')),
            ],
        ),
        migrations.CreateModel(
            name='StudijskoLeto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ime', models.CharField(max_length=100, unique=True, verbose_name='Ime')),
                ('veljaven', models.BooleanField(default=True, verbose_name='Veljavnost šifranta')),
            ],
        ),
        migrations.CreateModel(
            name='VrstaStudija',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False, verbose_name='Šifra')),
                ('opis', models.CharField(max_length=100, verbose_name='Opis')),
                ('nacin_zakljucka', models.CharField(max_length=100, verbose_name='Način zaključka šolanja')),
                ('raven_klasius', models.IntegerField(verbose_name='Raven izobrazbe po KLASIUS-SRV')),
                ('veljaven', models.BooleanField(default=True, verbose_name='Veljavnost šifranta')),
            ],
        ),
        migrations.CreateModel(
            name='VrstaVpisa',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False, verbose_name='Šifra')),
                ('opis', models.CharField(max_length=100, verbose_name='Opis vrste vpisa')),
                ('mozni_letniki', models.CharField(max_length=200, verbose_name='Možni letniki študija')),
                ('veljaven', models.BooleanField(default=True, verbose_name='Veljavnost šifranta')),
            ],
        ),
    ]
