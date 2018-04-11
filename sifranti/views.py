from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader

from .forms import *
from .models import *

# Create your views here.
#diff_ names is array with all possible models
diff_names = [ "Predmet", "NacinStudija", "Drzava" , "Posta" , "Obcina", "StudijskiProgram", "Modul","VrstaVpisa","VrstaStudija","Letnik","StudijskoLeto" ]

def index(request):
    context = {
        'diff_names' : diff_names

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

    # if a GET (or any other method) we'll create a blank form
    else:
        if diff in diff_names:
            elements = eval(diff).objects.values()
            form_iskanje = SearchForm()
            form = eval(diff+'Form')()
            context = {
            'object_name' : diff,
            'elements' : elements,
            'form': form,
            'form2' : form_iskanje
            }
            return render(request,'sifranti/changesif.html',context)

        else:
            return HttpResponse("Ni take tabele")

def update(request, diff, index):
    if request.method == 'POST' and diff in diff_names:
        # create a form instance and populate it with data from the request:
        
        # example Posta --> PostaForm
        existing_object = eval(diff).objects.get(id=index)
        # check whether it's valid:
        # and update into database
        form = eval(diff+'Form')(request.POST, instance=existing_object)
        form.save()
        
        return HttpResponseRedirect('/sifranti/'+ diff +'/')

    # if a GET (or any other method) we'll create a blank form
    else:
        if diff in diff_names:
            element = eval(diff).objects.values().filter(pk=index)

            form = eval(diff+'Form')()
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
        element.delete()
        return HttpResponseRedirect('/sifranti/'+ diff +'/')

def search(request, diff):

    if request.method == 'POST':
        form = SearchForm(request.POST)

        if form.is_valid() and diff in diff_names:
            isci_element = form.cleaned_data['isci_element']
            element = form.cleaned_data['element']
            print(isci_element)
            print(element)

            rezultat = eval(diff).objects.filter(**{isci_element: element}).values()
            return HttpResponseRedirect('/sifranti/'+ diff +'/'+str(rezultat[0]["id"])+'/')



