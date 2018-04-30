from django.forms import ModelForm
from django import forms
from sifranti.models import *
from student.models import *


class NameStudentForm(ModelForm):
	class Meta:
		model = Student
		exclude = ['vpisna_stevilka','dodatno_leto']

	def __init__(self, *args, **kwargs):
		super(NameStudentForm, self).__init__(*args, **kwargs)
		for visible in self.visible_fields():
			visible.field.widget.attrs['class'] = 'form-control'


class VpisForm(ModelForm):

	class Meta:
		model = Vpis
		exclude = ['student','potrjen','prosta_izbira','izkoriscen']

	def __init__(self, *args, **kwargs):
		super(VpisForm, self).__init__(*args, **kwargs)
		for visible in self.visible_fields():
			visible.field.widget.attrs['class'] = 'form-control'
