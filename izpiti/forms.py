from django.forms import ModelForm
from django import forms
from .models import *
from django.forms import Field

class ocenaForm(forms.Form):
    ocena = forms.IntegerField(max_value=100, min_value = 0)
    odjava = forms.BooleanField(required=False)