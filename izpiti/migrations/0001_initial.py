# Generated by Django 2.0.4 on 2018-04-30 16:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sifranti', '0001_initial'),
        ('student', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='IzvedbaPredmeta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('predmet', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='sifranti.Predmet')),
                ('studijsko_leto', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='sifranti.StudijskoLeto')),
            ],
        ),
        migrations.CreateModel(
            name='PredmetiStudenta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('predmeti', models.ManyToManyField(null=True, to='sifranti.Predmet')),
                ('vpis', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='student.Vpis')),
            ],
        ),
        migrations.CreateModel(
            name='Prijava',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('zaporedna_stevilka_polaganja', models.IntegerField()),
                ('podatki_o_placilu', models.CharField(blank=True, default=None, max_length=260, null=True)),
                ('predmeti_studenta', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='izpiti.PredmetiStudenta')),
            ],
        ),
        migrations.CreateModel(
            name='PrijaveStudenta',
            fields=[
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='student.Student')),
                ('prijave', models.ManyToManyField(null=True, to='izpiti.Prijava')),
            ],
        ),
        migrations.CreateModel(
            name='Rok',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datum', models.DateTimeField()),
                ('izvedba_predmeta', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='izpiti.IzvedbaPredmeta')),
            ],
        ),
        migrations.CreateModel(
            name='Ucitelj',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ime', models.CharField(max_length=30)),
                ('priimek', models.CharField(max_length=30)),
                ('email', models.CharField(max_length=60, unique=True)),
                ('predmeti', models.ManyToManyField(null=True, to='sifranti.Predmet')),
            ],
        ),
        migrations.AddField(
            model_name='prijava',
            name='rok',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='izpiti.Rok'),
        ),
        migrations.AddField(
            model_name='izvedbapredmeta',
            name='ucitelj_1',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ucitelj_1', to='izpiti.Ucitelj'),
        ),
        migrations.AddField(
            model_name='izvedbapredmeta',
            name='ucitelj_2',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ucitelj_2', to='izpiti.Ucitelj'),
        ),
        migrations.AddField(
            model_name='izvedbapredmeta',
            name='ucitelj_3',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ucitelj_3', to='izpiti.Ucitelj'),
        ),
    ]
