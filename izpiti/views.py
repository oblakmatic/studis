from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from izpiti.models import *
from sifranti.models import *
from sifranti.models import *
from .models import *

# Create your views here.
def index_izpiti(request):
    # pr profesorju se pojavjo sam te k jih ma on nacez. 
    # izpis kera vloga je

    all_subjects_id = IzvedbaPredmeta.objects.select_related().values('predmet'); #tle cudn pokaze tale predmet
    predmet_objekti = Predmet.objects.select_related().values();
    print(predmet_objekti)

    for ObjektIzvedba in all_subjects_id:
        trenutni_id = ObjektIzvedba['predmet']
        print(trenutni_id)
        for predmet in predmet_objekti:
           if trenutni_id == predmet['id']:
                print(str(predmet['id']) + " " + predmet['ime'])
           


    
    #print(all_subjects)

    #print(all_subjects)
    all_subjects = Predmet.objects.select_related().values();
    context = {
        'arr': all_subjects

        }

    return render(request,'index_izpiti.html',context)

def dodaj_izpit(request):
    predmet_ = request.POST.get('ime_predmeta')
    datum_ = request.POST.get('datum')

    izvedbaPredmeta_izBaze = IzvedbaPredmeta.objects.get(predmet=predmet_) #mogoce se more nanasat tut na studijsko leto? 
   
    dodaj_rok = Rok.objects.create(izvedba_predmeta=izvedbaPredmeta_izBaze, datum=datum_)

    return render(request,'izpiti-message.html')

def fill_database(request):

    #add_predmet=Predmet.objects.get(ime="TPO")
    add_predmet=Predmet(ime="TPO1")
    add_predmet.save()
    #add_studijskoLeto=StudijskoLeto.objects.get(ime="2017/2018")
    add_studijskoLeto=StudijskoLeto(ime="2017/2018")
    add_studijskoLeto.save()

    add_ucitelj=Ucitelj(ime="Vilijan",priimek="Mahnič",email="vilijan.mahnic@gmail.com")
    add_ucitelj.save()

    add_IzvedbaPredmeta=IzvedbaPredmeta(predmet=add_predmet,studijsko_leto=add_studijskoLeto,ucitelj_1=add_ucitelj)
    add_IzvedbaPredmeta.save()

    return render(request,'napolni-bazo.html')
    

    #add_predmet=Predmet(ime="Organizacija in management")
    #add_predmet.save()
   
    #add_predmet=Predmet(ime="Programiranje 1")
    #add_predmet.save()

    #add_predmet=Predmet(ime="Algoritmi in podatkovne strukture")
    #add_predmet.save()
   
