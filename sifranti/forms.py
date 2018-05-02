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
        fields = '__all__' #['ime', 'postna_stevilka']

class DrzavaForm(ModelForm):
    class Meta:
        model = Drzava
        fields = '__all__'

class ObcinaForm(ModelForm):
    class Meta:
        model = Obcina
        fields = '__all__'

class StudijskiProgramForm(ModelForm):
    class Meta:
        model = StudijskiProgram
        fields = '__all__'

class VrstaVpisaForm(ModelForm):
    class Meta:
        model = VrstaVpisa
        fields = '__all__'

class VrstaStudijaForm(ModelForm):
    class Meta:
        model = VrstaStudija
        fields = '__all__'

class LetnikForm(ModelForm):
    class Meta:
        model = Letnik
        fields = '__all__'

class StudijskoLetoForm(ModelForm):
    class Meta:
        model = StudijskoLeto
        fields = '__all__'

class NacinStudijaForm(ModelForm):
    class Meta:
        model = NacinStudija
        fields = '__all__'

class PredmetForm(ModelForm):
    class Meta:
        model = Predmet
        fields = '__all__'

class OblikaStudijaForm(ModelForm):
    class Meta:
        model = OblikaStudija
        fields = '__all__'