from django.forms import ModelForm
from django import forms
from sifranti.models import *
from student.models import *

class VpisForm(ModelForm):

	class Meta:
		model = Vpis
		exclude = ['student']

	def __init__(self, *args, **kwargs):
		super(VpisForm, self).__init__(*args, **kwargs)
		for visible in self.visible_fields():
			visible.field.widget.attrs['class'] = 'form-control'
