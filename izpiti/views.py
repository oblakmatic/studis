from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from izpiti.models import *
from sifranti.models import *
from sifranti.models import *
from .models import *
from time import gmtime, strftime
from datetime import datetime
from django.core.exceptions import ValidationError
import pytz
from datetime import timedelta


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
    if request.method == 'POST' and 'prikaz_rokov' in request.POST:

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

    elif request.method == 'POST' and 'dodaj_izpit' in request.POST:

        datum_ = request.POST['datum']

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



            for curr_predmetiStudenta in PredmetiStudenta.objects.all():
                if str(curr_predmetiStudenta.id) == predmeti_studenta_id:
                    vnesi_predmeti_studenta = curr_predmetiStudenta
        
            for rok in Rok.objects.all():
                if str(rok.id) == rok_id:
                    vnesi_rok = rok

            print(vnesi_rok.datum)
            a = Prijava(predmeti_studenta = vnesi_predmeti_studenta, rok = vnesi_rok, zaporedna_stevilka_polaganja = 1)
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

                    print("prijava oznacena kot neaktivna!")
                    prijava.aktivna_prijava = False
                    prijava.save()

#PRIJAVA NA IZPIT
        
        all_roki = Rok.objects.select_related()
        email_stud = request.user.email

       
        for student in Student.objects.all():
            if student.email == email_stud:
                curr_student = student

        if curr_student is None:
            return HttpResponse("Student ne obstaja!")
        else:
            
            all_predmetiStudenta = PredmetiStudenta.objects.all()
            for predmetiStudenta in all_predmetiStudenta:
                if predmetiStudenta.vpis.student.email == curr_student.email:
                    curr_predmetiStudenta = predmetiStudenta
        
        #pazi ker ce gres gledat tko kt js pol je lahko izvedbaPredmeta za en predmet z istmu imeno za 2 leti!
            all_izvedba = IzvedbaPredmeta.objects.all()
            all_izvedba_studenta = []
            for predmet in curr_predmetiStudenta.predmeti.all():
                for curr_izvedba in all_izvedba:
                    #print(predmet.ime + "----" + curr_izvedba.predmet.ime)
                    if predmet == curr_izvedba.predmet:
                        all_izvedba_studenta.append(curr_izvedba)

            all_rok = Rok.objects.all()
            roki = []
            utc=pytz.UTC
            time_now = datetime.now()
            
            for rok in all_rok:
                #time_now = strftime("%Y-%m-%d %H:%M:00+00:00", gmtime())
                if rok.datum > utc.localize(time_now):
                    for izvedba in all_izvedba_studenta:
                        if rok.izvedba_predmeta == izvedba:
                            roki.append(rok)
            

            #gres se cez vse prijave da ves na kerga si se ze prjavu-->
            all_prijava = Prijava.objects.all()
            prijavljeni_roki = []
            neprijavljeni_roki = []
            time_tomorrow = time_now + timedelta(days=1)
            #print(time_now.time() < datetime.time(12, 00))
            
            
            if all_prijava:
                for rok in roki:
                    #print(rok.datum)
                    #print(time_now)
                    #print(datetime(rok.datum.year, rok.datum.month, rok.datum.day - 1, 12))
                    if time_now >= datetime(rok.datum.year, rok.datum.month, rok.datum.day - 1, 12):
                        #rok['enabled'] = True
                        for prijava in all_prijava:
                            if rok == prijava.rok and prijava.aktivna_prijava == True:
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


   
