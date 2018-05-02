# Generated by Django 2.0.4 on 2018-05-02 20:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sifranti', '0001_initial'),
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
            name='Predmetnik',
            fields=[
                ('studijski_program', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='sifranti.StudijskiProgram')),
                ('obvezen', models.BooleanField(default=True)),
                ('letnik', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='sifranti.Letnik')),
                ('predmet', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='sifranti.Predmet')),
                ('studijsko_leto', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='sifranti.StudijskoLeto')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('vpisna_stevilka', models.IntegerField(primary_key=True, serialize=False)),
                ('emso', models.CharField(max_length=13, verbose_name='EMŠO')),
                ('priimek', models.CharField(max_length=30, verbose_name='Priimek')),
                ('ime', models.CharField(max_length=30, verbose_name='Ime')),
                ('naslov_stalno_bivalisce', models.CharField(max_length=260, verbose_name='Stalno prebivališče')),
                ('naslov_zacasno_bivalisce', models.CharField(blank=True, max_length=260, null=True, verbose_name='Začasno prebivališče')),
                ('telefon', models.CharField(max_length=15, verbose_name='Telefon')),
                ('email', models.CharField(max_length=60, unique=True, verbose_name='e-pošta')),
                ('dodatno_leto', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['priimek', 'ime', 'vpisna_stevilka'],
            },
        ),
        migrations.CreateModel(
            name='Zeton',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pravica_do_izbire', models.BooleanField(default=False)),
                ('izkoriscen', models.BooleanField(default=False)),
                ('letnik', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='sifranti.Letnik')),
                ('nacin_studija', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='sifranti.NacinStudija')),
            ],
        ),
        migrations.CreateModel(
            name='Vpis',
            fields=[
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='student.Student')),
                ('potrjen', models.BooleanField(default=False)),
                ('prosta_izbira', models.BooleanField(default=False)),
                ('letnik', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='sifranti.Letnik')),
                ('nacin_studija', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='sifranti.NacinStudija')),
                ('studijski_program', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='sifranti.StudijskiProgram')),
                ('studijsko_leto', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='sifranti.StudijskoLeto')),
                ('vrsta_studija', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='sifranti.VrstaStudija')),
                ('vrsta_vpisa', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='sifranti.VrstaVpisa')),
            ],
        ),
        migrations.AddField(
            model_name='zeton',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.Student'),
        ),
        migrations.AddField(
            model_name='zeton',
            name='studijski_program',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='sifranti.StudijskiProgram'),
        ),
        migrations.AddField(
            model_name='zeton',
            name='vrsta_studija',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='sifranti.VrstaStudija'),
        ),
        migrations.AddField(
            model_name='zeton',
            name='vrsta_vpisa',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='sifranti.VrstaVpisa'),
        ),
        migrations.AddField(
            model_name='student',
            name='drzava',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='sifranti.Drzava', verbose_name='Država'),
        ),
        migrations.AddField(
            model_name='student',
            name='drzava_rojstva',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='drzava_rojstva', to='sifranti.Drzava', verbose_name='Država rojstva'),
        ),
        migrations.AddField(
            model_name='student',
            name='obcina',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='sifranti.Obcina', verbose_name='Občina'),
        ),
        migrations.AddField(
            model_name='student',
            name='obcina_rojstva',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='obcina_rojstva', to='sifranti.Obcina', verbose_name='Občina rojstva'),
        ),
        migrations.AddField(
            model_name='student',
            name='posta',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='sifranti.Posta', verbose_name='Pošta'),
        ),
        migrations.AddField(
            model_name='kandidat',
            name='studijski_program',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='sifranti.StudijskiProgram'),
        ),
    ]
