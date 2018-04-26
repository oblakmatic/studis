from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from izpiti.models import *
from sifranti.models import *
from sifranti.models import *
from .models import *
from time import gmtime, strftime
from django.core.exceptions import ValidationError

# Create your views here.
def index_izpiti(request):
    all_izvedbaPredmeta = IzvedbaPredmeta.objects.select_related()
    context = {
        'arr': all_izvedbaPredmeta,
        'curr_date': strftime("%Y-%m-%dT%H:%M", gmtime())

        }

    return render(request,'index_izpiti.html',context)

def dodaj_izpit(request):

    if request.method == 'POST':

        datum_ = request.POST['datum']
        #print(datum_)

        id_IzvedbaPredmeta = request.POST['id_IzvedbaPredmeta']
        vnos_izvedbaPredmeta = IzvedbaPredmeta.objects.all()
        for curr_izvedbaPredmeta in vnos_izvedbaPredmeta:
            if str(curr_izvedbaPredmeta.id) == id_IzvedbaPredmeta:
                vnesi = curr_izvedbaPredmeta

        
        a = Rok(izvedba_predmeta = vnesi, datum = datum_)
        print(a.datum + " " + "hehe")
        a.save()
    
    return render(request,'izpiti-message.html')


    #add_predmet=Predmet(ime="Organizacija in management")
    #add_predmet.save()
   
    #add_predmet=Predmet(ime="Programiranje 1")
    #add_predmet.save()

    #add_predmet=Predmet(ime="Algoritmi in podatkovne strukture")
    #add_predmet.save()
   
