from django.forms import ModelForm
from django import forms
from sifranti.models import *
from student.models import *


class NameStudentForm(ModelForm):

	#datum_rojs = forms.DateField(widget=forms.SelectDateWidget(years=BIRTH_YEAR_CHOICES))
	class Meta:
		BIRTH_YEAR_CHOICES = ('1950','1951','1952','1953','1954','1955','1956','1957','1958','1959',
	'1960','1961','1962','1963','1964','1965','1966','1967','1968'
,'1969','1970','1971','1972','1973','1974','1975','1976','1977','1978','1979','1980','1981','1982','1983'
,'1984','1985','1986','1987','1988','1989','1990','1991','1992','1993','1994','1995','1996'
,'1997','1998','1999','2000','2001','2002','2003','2004','2005','2006','2007','2008','2009','2010','2011','2012','2013','2014','2015','2016','2017','2018')

		model = Student
		exclude = ['vpisna_stevilka','dodatno_leto','email']
		widgets = {
			'datum_rojstva': forms.SelectDateWidget(years=BIRTH_YEAR_CHOICES),
		}

	def __init__(self, *args, **kwargs):
		super(NameStudentForm, self).__init__(*args, **kwargs)
		for visible in self.visible_fields():
			visible.field.widget.attrs['class'] = 'form-control mb-2'

class VpisForm(ModelForm):

	class Meta:
		model = Vpis
		exclude = ['student','potrjen','prosta_izbira','izkoriscen']

	def __init__(self, *args, **kwargs):
		super(VpisForm, self).__init__(*args, **kwargs)
		for visible in self.visible_fields():
			visible.field.widget.attrs['class'] = 'form-control '