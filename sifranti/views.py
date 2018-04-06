from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from .models import *

# Create your views here.

diff_names = [ "Drzava" , "Posta" , "Obcina" ]

def index(request):
    context = {
        'diff_names' : diff_names

    }
    return render(request,'sifranti/index.html',context)

def changesif(request, diff):
    if diff in diff_names:
        elements = eval(diff).objects.values_list()
        
        context = {
        'elements' : elements

        }
        return render(request,'sifranti/changesif.html',context)

    else:
        return HttpResponse("Ni take tabele")