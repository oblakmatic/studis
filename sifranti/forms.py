from django.forms import ModelForm
from django import forms
from .models import *

my_default_errors = {
    
}

from django.forms import Field
from django.utils.translation import ugettext_lazy
Field.default_error_messages = {
    'required': ugettext_lazy("To polje je obvezno"),
    'invalid': ugettext_lazy("Vnesite pravilno vrednost"),
    'unique': ugettext_lazy("Ta zapis že obstaja"),
    'max_decimal_places' : ugettext_lazy("Ta zapis že obstaja"),
    'max_digit' : ugettext_lazy("Ta zapis že obstaja"),
    'invalid_choice' : ugettext_lazy("Vnesite pravilno vrednost"),
}
class SearchForm(forms.Form):
    isci_element = forms.CharField(label='Isci element po atributu:',max_length=100)
    element = forms.CharField(max_length=100)


class PostaForm(ModelForm):
    class Meta:
        model = Posta
        exclude = ['id'] #['ime', 'postna_stevilka']
        

class DrzavaForm(ModelForm):
    class Meta:
        model = Drzava
        exclude = ['id']

class ObcinaForm(ModelForm):
    class Meta:
        model = Obcina
        exclude = ['id']

class StudijskiProgramForm(ModelForm):
    class Meta:
        model = StudijskiProgram
        exclude = ['id']

class VrstaVpisaForm(ModelForm):
    class Meta:
        model = VrstaVpisa
        exclude = ['id']

class VrstaStudijaForm(ModelForm):
    class Meta:
        model = VrstaStudija
        exclude = ['id']

class LetnikForm(ModelForm):
    class Meta:
        model = Letnik
        exclude = ['id']

class StudijskoLetoForm(ModelForm):
    class Meta:
        model = StudijskoLeto
        exclude = ['id']

class NacinStudijaForm(ModelForm):
    class Meta:
        model = NacinStudija
        exclude = ['id']

class PredmetForm(ModelForm):
    class Meta:
        model = Predmet
        exclude = ['id']

class OblikaStudijaForm(ModelForm):
    class Meta:
        model = OblikaStudija
        exclude = ['id']



class PostaForm2(ModelForm):
    class Meta:
        model = Posta
        exclude = ['id'] #['ime', 'postna_stevilka']
        

class DrzavaForm2(ModelForm):
    class Meta:
        model = Drzava
        fields = '__all__'

class ObcinaForm2(ModelForm):
    class Meta:
        model = Obcina
        fields = '__all__'

class StudijskiProgramForm2(ModelForm):
    class Meta:
        model = StudijskiProgram
        fields = '__all__'

class VrstaVpisaForm2(ModelForm):
    class Meta:
        model = VrstaVpisa
        fields = '__all__'

class VrstaStudijaForm2(ModelForm):
    class Meta:
        model = VrstaStudija
        fields = '__all__'

class LetnikForm2(ModelForm):
    class Meta:
        model = Letnik
        fields = '__all__'

class StudijskoLetoForm2(ModelForm):
    class Meta:
        model = StudijskoLeto
        fields = '__all__'

class NacinStudijaForm2(ModelForm):
    class Meta:
        model = NacinStudija
        fields = '__all__'

class PredmetForm2(ModelForm):
    class Meta:
        model = Predmet
        fields = '__all__'

class OblikaStudijaForm2(ModelForm):
    class Meta:
        model = OblikaStudija
        fields = '__all__'