from django.forms import ModelForm
from django import forms
from student.models import *

class VpisForm(ModelForm):
    class Meta:
        model = Vpis
        exclude = ['student']