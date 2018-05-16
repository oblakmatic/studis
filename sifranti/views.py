from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib.auth.models import User, Group

from izpiti.models import *
from student.models import *
from .forms import *
from .models import *
import datetime

# Create your views here.
#diff_ names is array with all possible models
diff_names = [ "Predmet", "Letnik", "NacinStudija", "Drzava" , "Posta" , "Obcina", "StudijskiProgram", "OblikaStudija","VrstaVpisa","VrstaStudija","StudijskoLeto" ]

def index(request):
	context = {
		'diff_names' : sorted(diff_names)

	}
	return render(request,'sifranti/index.html',context)

def changesif(request, diff):
	
	if request.method == 'POST' and diff in diff_names:
		# create a form instance and populate it with data from the request:
		
		# example Posta --> PostaForm
		form = eval(diff+'Form')(request.POST)
		# check whether it's valid:
		# and saves into database
		if form.is_valid():
			
			new_object = form.save()
			return HttpResponseRedirect('/sifranti/'+ diff +'/')
		else:
			elements = eval(diff).objects.values()
			form_iskanje = SearchForm()
			context = {
			'object_name' : diff,
			'elements' : elements,
			'form': form,
			'form2' : form_iskanje
			}
			return render(request,'sifranti/changesif.html',context)

	# if a GET (or any other method) we'll create a blank form
	else:
		if diff in diff_names:
			elements =  eval(diff).objects.order_by('pk').values()
			keyList = []

			if elements:
				enEL = elements[0]
				
				for key in enEL.keys():
					
					verbose = eval(diff)._meta.get_field(key).verbose_name
					
					keyList.append(verbose)

			form_iskanje = SearchForm()
			form = eval(diff+'Form')()
			context = {
			'object_name' : diff,
			'elements' : elements,
			'form': form,
			'form2' : form_iskanje,
			'verbose_names' : keyList,
			
			}
			return render(request,'sifranti/changesif.html',context)

		else:
			return HttpResponse("Ni take tabele")

def update(request, diff, index):
	if request.method == 'POST' and diff in diff_names:
		# create a form instance and populate it with data from the request:
		existing_object = eval(diff).objects.get(pk=index)
		form = eval(diff+'Form')(request.POST, instance=existing_object)

		if form.is_valid():
		# example Posta --> PostaForm
			
			# check whether it's valid:
			# and update into database
			
			form.save()
			return HttpResponse("Uspesno posodobljen element") 
		else:
			context = {
				'object_name' : diff,
				'form': form,
				'element' : eval(diff).objects.filter(pk=index).values(),
			}
			return render(request,'sifranti/update.html',context)
		
		
		

	# if a GET (or any other method) we'll create a blank form
	else:
		if diff in diff_names:
			element = eval(diff).objects.filter(pk=index).values()

			form = eval(diff+'Form')(initial = element[0])
			context = {
			'object_name' : diff,
			'form': form,
			'element' : element,
			
			}
			return render(request,'sifranti/update.html',context)

		else:
			return HttpResponse("Ni takega elementa")    

def delete(request, diff, index):
	
	if diff in diff_names and request.method == 'POST':
		
		element = eval(diff).objects.get(id=index)
		if element.veljaven:
			element.veljaven = False
		else:
			element.veljaven = True
		
		element.save()
		return HttpResponseRedirect('/sifranti/'+ diff +'/')

def search(request, diff):

	if request.method == 'POST':
		form = SearchForm(request.POST)

		if form.is_valid() and diff in diff_names:
			isci_element = form.cleaned_data['isci_element']
			element = form.cleaned_data['element']
			
			polje = None
			enEL =  eval(diff).objects.order_by('pk').values()[0]
			for key in enEL.keys():
					
					verbose = eval(diff)._meta.get_field(key).verbose_name
					
					if verbose == isci_element:
						polje = key
						break


			if polje:       

				rezultat = eval(diff).objects.filter(**{polje: element}).values()
				if rezultat:
					return HttpResponseRedirect('/sifranti/'+ diff +'/'+str(rezultat[0]["id"])+'/')
				else:
					return HttpResponse("Ni bil najden element!")

			else:
				return HttpResponse("Ni tega elementa!")


def naredi_bazo(request):
	a = Drzava(id=4, dvomestna_koda="AF", tromestna_oznaka="AFG", iso_naziv="Afghanistan", slovenski_naziv="Afganistan",opomba="", veljaven=True)
	a.save()

	a_slo = Drzava(id=703, dvomestna_koda="SI", tromestna_oznaka="SVN", iso_naziv="Slovenia", slovenski_naziv="Slovenija",opomba="")
	a_slo.save()

	a = Drzava(id=703, dvomestna_koda="SI", tromestna_oznaka="SVN", iso_naziv="Slovenia", slovenski_naziv="Slovenija",opomba="", veljaven=True)
	a.save()
	a = Drzava(id=40, dvomestna_koda="AT", tromestna_oznaka="AUT", iso_naziv="Austria", slovenski_naziv="Avstrija",opomba="", veljaven=True)
	a.save()
	a = Drzava(id=56, dvomestna_koda="BE", tromestna_oznaka="BEL", iso_naziv="Belgium", slovenski_naziv="Belgija",opomba="", veljaven=True)
	a.save()
	a = Drzava(id=250, dvomestna_koda="FR", tromestna_oznaka="FRA", iso_naziv="France", slovenski_naziv="Francija",opomba="", veljaven=True)
	a.save()
	a = Drzava(id=276, dvomestna_koda="DE", tromestna_oznaka="DEU", iso_naziv="Germany", slovenski_naziv="Nemčija",opomba="")
	a.save()
	a = Drzava(id=826, dvomestna_koda="GB", tromestna_oznaka="GBR", iso_naziv="United Kingdom", slovenski_naziv="Velika Britanija", opomba="")
	a.save()
	a = Drzava(id=807, dvomestna_koda="MK", tromestna_oznaka="MKD", iso_naziv="Macedonia, the former Yugoslav Republic of", slovenski_naziv="Makedonija",opomba="")
	a.save()
	

	a = Obcina(id = 213, ime="Ankaran")
	a.save()
	a = Obcina(id = 1, ime="Ajdovščina")
	a.save()
	a = Obcina(id = 19, ime="Divača")
	a.save()
	a = Obcina(id = 20, ime="Dobropolje")
	a.save()

def search(request, diff):
	polje = polje + "__istartswith"
	rezultat = eval(diff).all_objects.filter(**{polje: element}).values()
	return rezultat