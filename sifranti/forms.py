from django.forms import ModelForm
from django import forms
from .models import *



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