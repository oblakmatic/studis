from django.forms import ModelForm
from django import forms
from sifranti.models import *
from student.models import *


class TokenForm(ModelForm):
	class Meta:
		model = Zeton
		exclude = ['izkoriscen', 'vrsta_studija']

class PredmetnikForm(ModelForm):
	class Meta:
		model = Predmetnik
		exclude = []
	def __init__(self, leto, program, *args, **kwargs):
		super(PredmetnikForm, self).__init__(*args, **kwargs)
		self.fields['modul'].queryset = Modul.objects.filter(studijsko_leto=leto, studijski_program=program)
		for visible in self.visible_fields():
			visible.field.widget.attrs['class'] = 'form-control mb-2'