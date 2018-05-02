from django.forms import ModelForm
from django import forms
from .models import *
from django.forms import Field

class ocenaForm(forms.Form):
    ocena = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'btn btn-outline-primary mt-2'}), max_value=100, min_value = 0)