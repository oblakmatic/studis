# Generated by Django 2.0.3 on 2018-04-09 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sifranti', '0002_letnik_modul_studijskiprogram_studijskoleto_vrstastudija_vrstavpisa'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studijskiprogram',
            name='ime',
            field=models.CharField(choices=[('DIPL', 'Dodiplomski'), ('MAG', 'Magistrski'), ('DR', 'Doktorski')], max_length=4),
        ),
    ]
