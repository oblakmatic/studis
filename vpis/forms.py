from django.forms import ModelForm
from django import forms
from student.models import *

class VpisForm(ModelForm):

    studijsko_leto_choices = [(c.id, c.ime) for c in StudijskoLeto.objects.all()]
    studijski_program_choices = [(c.id, c.ime) for c in StudijskiProgram.objects.all()]
    letnik_choices = [(c.id, c.ime) for c in Letnik.objects.all()]
    vrsta_vpisa_choices= [(c.id, c.ime) for c in VrstaVpisa.objects.all()]
    nacin_studija_choices= [(c.id, c.ime) for c in NacinStudija.objects.all()]
    vrsta_studija_choices= [(c.id, c.ime) for c in VrstaStudija.objects.all()]

    studijsko_leto = forms.ChoiceField(required=True, label='Študijsko leto', choices=studijsko_leto_choices)
    studijski_program = forms.ChoiceField(required=True, label='Študijski program', choices=studijski_program_choices)
    letnik = forms.ChoiceField(required=True, label='Letnik', choices=letnik_choices)
    vrsta_vpisa = forms.ChoiceField(required=True, label='Vrsta vpisa', choices=vrsta_vpisa_choices)
    nacin_studija = forms.ChoiceField(required=True, label='Nacin študija', choices=nacin_studija_choices)
    vrsta_studija = forms.ChoiceField(required=True, label='Vrsta študija', choices=vrsta_studija_choices)
    

    class Meta:
        model = Vpis
        exclude = ['student']








    '''#student = models.ForeignKey(Student, primary_key = True,  on_delete= models.CASCADE)
    studijsko_leto = models.ForeignKey(StudijskoLeto, null= True, on_delete=models.SET_NULL)

    studijski_program = models.ForeignKey(StudijskiProgram, null=True, on_delete= models.SET_NULL)
    letnik = models.ForeignKey(Letnik, null=True, on_delete= models.SET_NULL)

    vrsta_vpisa = models.ForeignKey(VrstaVpisa, null=True, on_delete= models.SET_NULL)
    nacin_studija = models.ForeignKey(NacinStudija, null=True, on_delete= models.SET_NULL)
    # vrsta studija je kao oblika studija
    vrsta_studija  = models.ForeignKey(VrstaStudija, null=True, on_delete= models.SET_NULL)
    # predmeti_studenta s foreign keyom
    # ?? potrjen = models.BooleanField(default = False)
    # ?? prosta_izbira = models.BooleanField(default = False)
'''
