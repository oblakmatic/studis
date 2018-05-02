from django.forms import ModelForm
from django import forms
from sifranti.models import *
from student.models import *


class TokenForm(ModelForm):
    class Meta:
        model = Zeton
        fields = '__all__'
