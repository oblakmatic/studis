# Generated by Django 2.0.4 on 2018-04-06 09:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Kandidat',
            fields=[
                ('vpisna_stevilka', models.IntegerField(primary_key=True, serialize=False)),
                ('ime', models.CharField(max_length=30)),
                ('priimek', models.CharField(max_length=30)),
                ('email', models.CharField(max_length=60)),
                ('izkoriscen', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('emso', models.CharField(max_length=13)),
                ('priimek', models.CharField(max_length=30)),
                ('ime', models.CharField(max_length=30)),
                ('vpisna_stevilka', models.IntegerField(primary_key=True, serialize=False)),
                ('naslov_stalno_bivalisce', models.CharField(max_length=260)),
                ('naslov_zacasno_bivalisce', models.CharField(max_length=260)),
                ('kraj_rojstva', models.CharField(max_length=260)),
                ('naslov_posta', models.CharField(max_length=260)),
                ('telefon', models.CharField(max_length=15)),
                ('email', models.CharField(max_length=60)),
                ('dodatno_leto', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Vpis',
            fields=[
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='student.Student')),
                ('letnik', models.IntegerField()),
                ('potrjen', models.BooleanField(default=False)),
                ('prosta_izira', models.BooleanField(default=False)),
            ],
        ),
    ]
