from django.forms import ModelForm
from django import forms
from sifranti.models import *
from student.models import *

class VpisForm(ModelForm):

    class Meta:
        model = Vpis
        exclude = ['student']
