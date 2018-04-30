from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from izpiti.models import *
from sifranti.models import *
from sifranti.models import *
from .models import *
from time import gmtime, strftime
from django.core.exceptions import ValidationError
from datetime import datetime
import pytz


# Create your views here.
def index_izpiti(request):

    #pofixat treba se ce user ne obstaja! --> dam pol vrjetn neb smel sploh nc kazat!
    
    if(request.user.groups.all()[0].name == "referent"):
        all_izvedbaPredmeta = IzvedbaPredmeta.objects.select_related()
    
        context = {
            'arr': all_izvedbaPredmeta,
            'curr_date': strftime("%Y-%m-%dT%H:%M", gmtime())
            }

    elif(request.user.groups.all()[0].name == "professors"):
        email_ = request.user.email

        all_ucitelj = Ucitelj.objects.all()
        
        flag = False
        for ucitelj in all_ucitelj:
            if ucitelj.email == email_:
                ucitelj_ = ucitelj
                flag = True

        if flag == False:
            return HttpResponse("Prijavi se z uciteljom, ki je v bazi")
        
        all_izvedbaPredmeta = IzvedbaPredmeta.objects.select_related()
        list = []
        for izvedba_predmeta in all_izvedbaPredmeta:
            if izvedba_predmeta.ucitelj_1 == ucitelj_:
                list.append(izvedba_predmeta)
            elif izvedba_predmeta.ucitelj_2 == ucitelj_:
                list.append(izvedba_predmeta)
            elif izvedba_predmeta.ucitelj_3 == ucitelj_:
                list.append(izvedba_predmeta)
         
        
        context = {
            'arr': list,
            'curr_date': strftime("%Y-%m-%dT%H:%M", gmtime())

            }
    else:
        return HttpResponse("Nimaš dovoljenja.")

    return render(request,'index_izpiti.html',context)

#DODAJANJE IZPITA PROFESOR/REFERENTKA
def dodaj_izpit(request):

    if request.method == 'POST' and 'dodaj_izpit' in request.POST:

        datum_ = request.POST['datum']
        print("datum v dodaj izpit --> " + datum_)

        id_IzvedbaPredmeta = request.POST['id_IzvedbaPredmeta']
        vnos_izvedbaPredmeta = IzvedbaPredmeta.objects.all()
        for curr_izvedbaPredmeta in vnos_izvedbaPredmeta:
            if str(curr_izvedbaPredmeta.id) == id_IzvedbaPredmeta:
                vnesi = curr_izvedbaPredmeta


        a = Rok(izvedba_predmeta = vnesi, datum = datum_)
        a.save()

        #da mu pokaze se vse roke k jih je razpisov
        email_ = request.user.email
        showRoki = []
        for rok in Rok.objects.all():
            if rok.izvedba_predmeta.ucitelj_1.email == email_:
                showRoki.append(rok)
            elif rok.izvedba_predmeta.ucitelj_2.email == email_:
                showRoki.append(rok)
            elif rok.izvedba_predmeta.ucitelj_3.email == email_:
                showRoki.append(rok)
    
        context = {
            'arr': showRoki
            }

        return render(request,'izpiti-message.html',context)

   

def prijava(request):
#VNOS PRIJAVE

    if(request.user.groups.all()[0].name == "students"):
        if request.method == 'POST' and 'prijava_izpit' in request.POST:

            predmeti_studenta_id = request.POST['predmeti_studenta']
            rok_id = request.POST['rok_']
            
            predmet = IzvedbaPredmeta.objects.filter(rok__id = rok_id)[0]
            stevilo_dosedanjih_polaganj = Prijava.objects.filter(predmeti_studenta__vpis__student__email = request.user.email, rok__izvedba_predmeta = predmet, aktivna_prijava = True).count()
            print("polaganja skupaj", stevilo_dosedanjih_polaganj)
            if(stevilo_dosedanjih_polaganj >= 4):
                print('WARNING! Placljivo polaganje!')

            if(stevilo_dosedanjih_polaganj >= 6):
                print('WARNING! Stevilo najvec moznih polaganj predmeta prekoraceno!')

            utc = pytz.UTC
            trenutni_datum = utc.localize(datetime.now()).date()
            
            # print(trenutni_datum.year-1, trenutni_datum.year, trenutni_datum.year+1)
            if (trenutni_datum.month >= 10 and trenutni_datum.day >= 1):
                trenutno_leto = str(trenutni_datum.year) + "/" + str(trenutni_datum.year+1)
            else:
                trenutno_leto = str(trenutni_datum.year-1) + "/" + str(trenutni_datum.year)
            
            polaganja_trenutno_leto = Prijava.objects.filter(predmeti_studenta__vpis__student__email = request.user.email, rok__izvedba_predmeta = predmet, rok__izvedba_predmeta__studijsko_leto = trenutno_leto, aktivna_prijava = True).count()
            if(polaganja_trenutno_leto >= 3):
                print('WARNING! Stevilo dovoljenih prijav v enem letu prekoraceno!')
            print("polaganja letos", polaganja_trenutno_leto)
            # print(trenutno_leto)
            trenutno_studijsko_leto = StudijskoLeto.objects.filter(ime = trenutno_leto)

            for curr_predmetiStudenta in PredmetiStudenta.objects.all():
                if str(curr_predmetiStudenta.id) == predmeti_studenta_id:
                    vnesi_predmeti_studenta = curr_predmetiStudenta
        
            for rok in Rok.objects.all():
                if str(rok.id) == rok_id:
                    vnesi_rok = rok

            
            a = Prijava(predmeti_studenta = vnesi_predmeti_studenta, rok = vnesi_rok, zaporedna_stevilka_polaganja = stevilo_dosedanjih_polaganj)
            a.save()

#IZBRIS PRIJAVE

        elif request.method == 'POST' and 'odjava_izpit' in request.POST:
            predmeti_studenta_id = request.POST['predmeti_studenta']
            rok_id = request.POST['rok_']

            for curr_predmetiStudenta in PredmetiStudenta.objects.all():
                if str(curr_predmetiStudenta.id) == predmeti_studenta_id:
                    vnesi_predmeti_studenta = curr_predmetiStudenta
        
            for rok in Rok.objects.all():
                if str(rok.id) == rok_id:
                    vnesi_rok = rok
        
            all_prijava = Prijava.objects.all()
            for prijava in all_prijava:
                if prijava.predmeti_studenta == vnesi_predmeti_studenta and prijava.rok == vnesi_rok:
                    print("prijava odstranjena!")
                    prijava.delete()

#PRIJAVA NA IZPIT
        
        all_roki = Rok.objects.select_related()

        curr_student = Student.objects.filter(email = request.user.email)[0]
        
        if curr_student is None:
            return HttpResponse("Student ne obstaja!")
        else:
            
            # all_predmetiStudenta = PredmetiStudenta.objects.all()
            # for predmetiStudenta in all_predmetiStudenta:
            #     if predmetiStudenta.vpis.student.email == curr_student.email:
            #         curr_predmetiStudenta = predmetiStudenta
            curr_predmetiStudenta = PredmetiStudenta.objects.filter(vpis__student__email = curr_student.email)[0]
        #pazi ker ce gres gledat tko kt js pol je lahko izvedbaPredmeta za en predmet z istmu imeno za 2 leti!
            # all_izvedba = IzvedbaPredmeta.objects.all()
            all_izvedba_studenta = []
            for predmet in curr_predmetiStudenta.predmeti.all():
                izvedbe = IzvedbaPredmeta.objects.filter(predmet = predmet)
                for izvedba in izvedbe:
                    all_izvedba_studenta.append(izvedba)
                # for curr_izvedba in all_izvedba:
                #     #print(predmet.ime + "----" + curr_izvedba.predmet.ime)
                #     if predmet == curr_izvedba.predmet:
                #         all_izvedba_studenta.append(curr_izvedba)

            all_rok = Rok.objects.all()
            roki = []

            for rok in all_rok:
                print(rok.datum)
                #if rok.datum > datetime.now(): #preverjanje datuma
                for izvedba in all_izvedba_studenta:
                    if rok.izvedba_predmeta == izvedba:
                        roki.append(rok)
            

            #gres se cez vse prijave da ves na kerga si se ze prjavu-->
            all_prijava = Prijava.objects.all()
            prijavljeni_roki = []
            neprijavljeni_roki = []
            if all_prijava:
                for rok in roki:
                    for prijava in all_prijava:
                        if rok == prijava.rok:
                            prijavljeni_roki.append(rok)
                        else:
                            neprijavljeni_roki.append(rok)

    else:
        return HttpResponse("Nimaš dovoljenja.")

    context={
    'arr': roki,
    'arr1': prijavljeni_roki,
    'predmetiStudenta': curr_predmetiStudenta
    }

    return render(request,'prijava.html',context)


   
