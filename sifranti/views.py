from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib.auth.models import User, Group
from django.core.paginator import Paginator

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
		form = eval(diff+'Form2')(request.POST)
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
			elements =  eval(diff).all_objects.order_by('pk').values()
			paginator = Paginator(elements, 25)

			page = request.GET.get('page')
			elemen = paginator.get_page(page)



			keyList = []

			if elements:
				enEL = elements[0]
				
				for key in enEL.keys():
					
					verbose = eval(diff)._meta.get_field(key).verbose_name
					
					keyList.append(verbose)

			form_iskanje = SearchForm()
			form = eval(diff+'Form2')()
			context = {
			'object_name' : diff,
			'elements' : elemen,
			'form': form,
			'form2' : form_iskanje,
			'verbose_names' : keyList,
			
			}
			return render(request,'sifranti/changesif.html',context)

		else:
			return HttpResponseRedirect("Ni take tabele")

def update(request, diff, index):
	if request.method == 'POST' and diff in diff_names:
		# create a form instance and populate it with data from the request:
		existing_object = eval(diff).all_objects.get(pk=index)
		form = eval(diff+'Form')(request.POST, instance=existing_object)

		if form.is_valid():
		# example Posta --> PostaForm
			
			# check whether it's valid:
			# and update into database
			
			form.save()
			return HttpResponseRedirect("/sifranti/"+diff+"/") 
		else:
			context = {
				'object_name' : diff,
				'form': form,
				'element' : eval(diff).all_objects.filter(pk=index).values(),
			}
			return render(request,'sifranti/update.html',context)
		
		
		

	# if a GET (or any other method) we'll create a blank form
	else:
		if diff in diff_names:
			element = eval(diff).all_objects.filter(pk=index).values()

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
		
		element = eval(diff).all_objects.get(id=index)
		if element.veljaven:
			element.veljaven = False
		else:
			element.veljaven = True
		
		element.save()
		return HttpResponseRedirect('/sifranti/'+ diff +'/')

def search2(request, diff, key, iskani_el ):

	if request.method == 'POST' and diff in diff_names:
		# create a form instance and populate it with data from the request:
		
		# example Posta --> PostaForm
		form = eval(diff+'Form2')(request.POST)
		# check whether it's valid:
		# and saves into database
		if form.is_valid():
			
			new_object = form.save()
			return HttpResponseRedirect('/sifranti/'+ diff +'/')
		else:
			elements = eval(diff).all_objects.values()
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
			#elements =  eval(diff).objects.order_by('pk').values()
			elements = vrniFiltriraneElemente(diff, key, iskani_el)
			paginator = Paginator(elements, 25)

			page = request.GET.get('page')
			elemen = paginator.get_page(page)

			keyList = []

			if elements:
				enEL = elements[0]
				
				for key in enEL.keys():
					
					verbose = eval(diff)._meta.get_field(key).verbose_name
					
					keyList.append(verbose)

			form_iskanje = SearchForm()
			form = eval(diff+'Form2')()
			context = {
			'object_name' : diff,
			'elements' : elemen,
			'form': form,
			'form2' : form_iskanje,
			'verbose_names' : keyList,
			
			}
			return render(request,'sifranti/changesif.html',context)

		else:
			return HttpResponse("Ni take tabele")

def vrniFiltriraneElemente(diff, isci_element, element):


	polje = None
	enEL =  eval(diff).all_objects.order_by('pk').values()[0]
	for key in enEL.keys():
			
			verbose = eval(diff)._meta.get_field(key).verbose_name
			
			if verbose == isci_element:
				polje = key
				break     
		
	polje = polje + "__istartswith"
	rezultat = eval(diff).all_objects.filter(**{polje: element}).values()
	return rezultat

def search(request, diff):

	if request.method == 'POST':
		form = SearchForm(request.POST)

		if form.is_valid() and diff in diff_names:
			isci_element = form.cleaned_data['isci_element']
			element = form.cleaned_data['element']
			
			return HttpResponseRedirect('/sifranti/'+ diff +'/'+isci_element+'/'+element+'/')
	else:
		HttpResponseRedirect('/sifranti/')

def naredi_bazo(request):
	return None