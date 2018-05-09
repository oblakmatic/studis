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
from django.db.models import Q
from .forms import *

from django.forms import formset_factory

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
            return HttpResponse("Prijavi se z učiteljem, ki je v bazi")
        
        all_izvedbaPredmeta = IzvedbaPredmeta.objects.select_related()
        list = []
        for izvedba_predmeta in all_izvedbaPredmeta:
            print(izvedba_predmeta.studijsko_leto)
            print(izvedba_predmeta.predmet)
            if izvedba_predmeta.ucitelj_1 == ucitelj_:
                print(izvedba_predmeta)
                list.append(izvedba_predmeta)
            elif izvedba_predmeta.ucitelj_2 == ucitelj_:
                print(izvedba_predmeta)
                list.append(izvedba_predmeta)
            elif izvedba_predmeta.ucitelj_3 == ucitelj_:
                print(izvedba_predmeta)
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
        showRoki = []
        if(request.user.groups.all()[0].name == "professors"):
            email_ = request.user.email
            
            for rok in Rok.objects.all().order_by("datum"):
                if rok.izvedba_predmeta.ucitelj_1 != None and rok.izvedba_predmeta.ucitelj_1.email == email_:
                    showRoki.append(rok)
                elif rok.izvedba_predmeta.ucitelj_2 != None and rok.izvedba_predmeta.ucitelj_2.email == email_:
                    showRoki.append(rok)
                elif rok.izvedba_predmeta.ucitelj_3 != None and rok.izvedba_predmeta.ucitelj_3.email == email_:
                    showRoki.append(rok)

        elif(request.user.groups.all()[0].name == "referent"):
            showRoki = Rok.objects.all()
    
        context = {
            'arr': showRoki
            }

        return render(request,'izpiti-message.html',context)

    elif request.method == 'POST' and 'dodaj_izpit' in request.POST:

        prostor = request.POST['prostor']

        datum_ = request.POST['datum']
        cas_ = request.POST['cas']
        datum_split = datum_.split(".")
        cas_split = cas_.split(":")
        
        datum_ = datetime(int(datum_split[2]), int(datum_split[1]), int(datum_split[0]), int(cas_split[0]), int(cas_split[1]))


        id_IzvedbaPredmeta = request.POST['id_IzvedbaPredmeta']
        vnos_izvedbaPredmeta = IzvedbaPredmeta.objects.all()
        for curr_izvedbaPredmeta in vnos_izvedbaPredmeta:
            print(curr_izvedbaPredmeta.id)
            if str(curr_izvedbaPredmeta.id) == id_IzvedbaPredmeta:
                vnesi = curr_izvedbaPredmeta

        

        a = Rok(izvedba_predmeta = vnesi, datum = datum_, prostor_izvajanja = prostor)
        a.save()

        #da mu pokaze se vse roke k jih je razpisov
        email_ = request.user.email
        showRoki = []
        for rok in Rok.objects.all():
            if rok.izvedba_predmeta.ucitelj_1 != None and rok.izvedba_predmeta.ucitelj_1.email == email_:
                showRoki.append(rok)
            elif rok.izvedba_predmeta.ucitelj_2 != None and rok.izvedba_predmeta.ucitelj_2.email == email_:
                showRoki.append(rok)
            elif rok.izvedba_predmeta.ucitelj_3 != None and rok.izvedba_predmeta.ucitelj_3.email == email_:
                showRoki.append(rok)
    
        context = {
            'arr': showRoki
            }

        return render(request,'izpiti-message.html',context)

   

def prijava(request):
#VNOS PRIJAVE
    # TODO: Implementacija omejitev, frontend indikatorji neustreznosti
    if(request.user.groups.all()[0].name == "students"):
        if request.method == 'POST' and 'prijava_izpit' in request.POST:

            predmeti_studenta_id = request.POST['predmeti_studenta']
            rok_id = request.POST['rok_']
            
            predmet = IzvedbaPredmeta.objects.filter(rok__id = rok_id)[0]
            
            trenutno_studijsko_leto = ptsl()
            polaganja_trenutno_leto = Prijava.objects.filter(predmeti_studenta__vpis__student__email = request.user.email, rok__izvedba_predmeta = predmet, rok__izvedba_predmeta__studijsko_leto = trenutno_studijsko_leto).count()
            if(polaganja_trenutno_leto >= 3):

                print('WARNING (GOING IN)! Stevilo dovoljenih prijav v enem letu prekoraceno!', polaganja_trenutno_leto)
            print("polaganja letos", polaganja_trenutno_leto)
            
            # stevilo_dosedanjih_polaganj = Prijava.objects.filter(predmeti_studenta__vpis__student__email = request.user.email, rok__izvedba_predmeta = predmet, aktivna_prijava = True).count()
            stevilo_dosedanjih_polaganj = Prijava.objects.filter(predmeti_studenta__vpis__student__email = request.user.email, rok__izvedba_predmeta = predmet, aktivna_prijava = True).count()
            print("polaganja skupaj", stevilo_dosedanjih_polaganj)
            if(stevilo_dosedanjih_polaganj >= 4):
                print('WARNING (GOING IN)! Placljivo polaganje!', stevilo_dosedanjih_polaganj)

            if(stevilo_dosedanjih_polaganj >= 6):
                print('WARNING (GOING IN)! Stevilo najvec moznih polaganj predmeta prekoraceno!', stevilo_dosedanjih_polaganj)

            # print(trenutno_leto)
            

            # zadnje_prijave = Prijava.objects.filter(predmeti_studenta__vpis__student__email = request.user.email, rok__izvedba_predmeta = predmet, rok__izvedba_predmeta__studijsko_leto = trenutno_studijsko_leto, aktivna_prijava = True).order_by("-id")[0].created_at
            

            for curr_predmetiStudenta in PredmetiStudenta.objects.all():
                print(curr_predmetiStudenta.id)
                if str(curr_predmetiStudenta.id) == predmeti_studenta_id:
                    vnesi_predmeti_studenta = curr_predmetiStudenta

            vnesi_rok = Rok.objects.filter(id = rok_id)[0]

            zadnje_prijave = Prijava.objects.filter(predmeti_studenta__vpis__student__email = request.user.email, rok__izvedba_predmeta = predmet, rok__izvedba_predmeta__studijsko_leto = trenutno_studijsko_leto, aktivna_prijava = True).order_by("-id")
            if(zadnje_prijave.count() != 0):
                print(vars(zadnje_prijave[0]))
                datum_zadnje_prijave = zadnje_prijave[0].created_at
                print(datum_zadnje_prijave)
                if((datum_zadnje_prijave - vnesi_rok.datum).days <= 10): # TODO: Omejitev po dnevih naj bi bila nastavljiva
                    print("WARNING (GOING IN)! Med prejsnjim polaganjem in tem rokom je preteklo manj kot 10 dni!")
            
            a = Prijava(predmeti_studenta = vnesi_predmeti_studenta, rok = vnesi_rok, zaporedna_stevilka_polaganja = stevilo_dosedanjih_polaganj)
            a.save()

#IZBRIS PRIJAVE

        elif request.method == 'POST' and 'odjava_izpit' in request.POST:
            predmeti_studenta_id = request.POST['predmeti_studenta']
            rok_id = request.POST['rok_']

            for curr_predmetiStudenta in PredmetiStudenta.objects.all():
                print(curr_predmetiStudenta.id)
                if str(curr_predmetiStudenta.id) == predmeti_studenta_id:
                    vnesi_predmeti_studenta = curr_predmetiStudenta
        
            for rok in Rok.objects.all():
                print(rok.id)
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

            all_rok = Rok.objects.all().order_by("datum")
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
            disabled_roki = []
            payable_roki = []
            disable_odjava_roki = []
            time_tomorrow = time_now + timedelta(days=1)
            #print(time_now.time() < datetime.time(12, 00))
            
            
            if all_prijava:
                for rok in roki:
                    print("###############################################")
                    ###########################################################################
                    predmet = rok.izvedba_predmeta
            
                    trenutno_studijsko_leto = ptsl()
                    polaganja_trenutno_leto = Prijava.objects.filter(predmeti_studenta__vpis__student__email = request.user.email, rok__izvedba_predmeta = predmet, rok__izvedba_predmeta__studijsko_leto = trenutno_studijsko_leto, aktivna_prijava = True).count()
                    if(polaganja_trenutno_leto >= 3):

                        print('WARNING! Stevilo dovoljenih prijav v enem letu prekoraceno!', polaganja_trenutno_leto)
                    
                    # stevilo_dosedanjih_polaganj = Prijava.objects.filter(predmeti_studenta__vpis__student__email = request.user.email, rok__izvedba_predmeta = predmet, aktivna_prijava = True).count()
                    stevilo_dosedanjih_polaganj = Prijava.objects.filter(predmeti_studenta__vpis__student__email = request.user.email, rok__izvedba_predmeta = predmet, aktivna_prijava = True).count()
                    print("polaganja skupaj", stevilo_dosedanjih_polaganj)
                    if(stevilo_dosedanjih_polaganj >= 4):
                        print('WARNING! Placljivo polaganje!', stevilo_dosedanjih_polaganj)

                    if(stevilo_dosedanjih_polaganj >= 6):
                        print('WARNING! Stevilo najvec moznih polaganj predmeta prekoraceno!', stevilo_dosedanjih_polaganj)

                    # print(trenutno_leto)
                    

                    # zadnje_prijave = Prijava.objects.filter(predmeti_studenta__vpis__student__email = request.user.email, rok__izvedba_predmeta = predmet, rok__izvedba_predmeta__studijsko_leto = trenutno_studijsko_leto, aktivna_prijava = True).order_by("-id")[0].created_at
                    

                    vnesi_rok = rok

                    zadnje_prijave = Prijava.objects.filter(predmeti_studenta__vpis__student__email = request.user.email, rok__izvedba_predmeta = predmet, rok__izvedba_predmeta__studijsko_leto = trenutno_studijsko_leto, aktivna_prijava = True).order_by("-id")
                    if(zadnje_prijave.count() != 0):
                        #print(vars(zadnje_prijave[0]))
                        datum_zadnje_prijave = zadnje_prijave[0].created_at
                        print("datum zadnje prijave", datum_zadnje_prijave)
                        print("vnesi rok datum", vnesi_rok.datum)
                        #print("razlika", (datum_zadnje_prijave - vnesi_rok.datum).days)
                        if((vnesi_rok.datum - datum_zadnje_prijave).days <= 10): # TODO: Omejitev po dnevih naj bi bila nastavljiva
                            print("WARNING! Med prejsnjim polaganjem in tem rokom je preteklo manj kot 10 dni!")   
                    ################################################################################################################################                 
                    #print(rok.datum)
                    #print(time_now)
                    #print(datetime(rok.datum.year, rok.datum.month, rok.datum.day - 1, 12))
                    
                    #rok['enabled'] = True
                    for prijava in all_prijava:
                        
                        if rok == prijava.rok and prijava.aktivna_prijava == True:
                            if time_now >= datetime(rok.datum.year, rok.datum.month, rok.datum.day - 1, 12):
                                print("disabled odjava add ~~~~~~~~~~~~~~~~~~~~~~~~~~~", rok.datum)
                                disable_odjava_roki.append(rok)
                            else:
                                print("odjava add~~~~~~~~~~~~~~~~~~~~~~~", rok.datum)
                                prijavljeni_roki.append(rok)
                        else:
                            if (polaganja_trenutno_leto >= 3 or stevilo_dosedanjih_polaganj >= 6 or (vnesi_rok.datum - datum_zadnje_prijave).days <= 10 or time_now >= datetime(rok.datum.year, rok.datum.month, rok.datum.day - 1, 0) ):
                                print("disabled prijava add~~~~~~~~~~~~~~~~~~~~~~~", rok.datum)
                                disabled_roki.append(rok)
                                continue
                            elif stevilo_dosedanjih_polaganj >= 4:
                                print("payable prijava add~~~~~~~~~~~~~~~~~~~~~~~~~", rok.datum)
                                payable_roki.append(rok)
                            else:
                                print("prijava add~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~", rok.datum)
                                neprijavljeni_roki.append(rok)

    else:
        return HttpResponse("Nimaš dovoljenja.")

    context={
    'arr': roki,
    'arr1': prijavljeni_roki,
    'disabled_odjava': disable_odjava_roki,
    'disabled': disabled_roki,
    'payable': payable_roki,
    'predmetiStudenta': curr_predmetiStudenta
    }

    return render(request,'prijava.html',context)

def pridobi_trenutno_studijsko_leto():
    utc = pytz.UTC
    trenutni_datum = utc.localize(datetime.now()).date()
            
    # print(trenutni_datum.year-1, trenutni_datum.year, trenutni_datum.year+1)
    if (trenutni_datum.month >= 10 and trenutni_datum.day >= 1):
        trenutno_leto = str(trenutni_datum.year) + "/" + str(trenutni_datum.year+1)
    else:
        trenutno_leto = str(trenutni_datum.year-1) + "/" + str(trenutni_datum.year)
            
    # polaganja_trenutno_leto = Prijava.objects.filter(predmeti_studenta__vpis__student__email = request.user.email, rok__izvedba_predmeta = predmet, rok__izvedba_predmeta__studijsko_leto = trenutno_studijsko_leto, aktivna_prijava = True).count()
    trenutno_studijsko_leto = StudijskoLeto.objects.filter(ime = trenutno_leto)[0]
    return trenutno_studijsko_leto

   
def izberi_rok(request):
    if(request.user.groups.all()[0].name == "professors"):
        curr_roki = []
        email_ = request.user.email
        roki = Rok.objects.filter( Q(izvedba_predmeta__ucitelj_1__email = email_) | Q(izvedba_predmeta__ucitelj_2__email = email_) | Q(izvedba_predmeta__ucitelj_3__email = email_) , Q(datum__lte=datetime.now().date()))

        context = {
            'arr': roki
            }

        return render(request,'vnesi_ocene.html', context)
    elif(request.user.groups.all()[0].name == "referent"):
        curr_roki = []
        roki = Rok.objects.filter(datum__lte=datetime.now().date())

        context = {
            'arr': roki
            }

        return render(request,'vnesi_ocene.html', context)
    else:
        return HttpResponse("Nimaš dovoljenja.")

def vnesi_ocene_predmeta(request):
#UCITELJ
    if(request.user.groups.all()[0].name == "professors"):
        if request.method == 'POST' and 'vnesi_ocene' in request.POST:
            rok_id = request.POST['id_rok']

            prijave = Prijava.objects.filter(~Q(ocena = -1), rok__id = rok_id).order_by('id')
            print(prijave)
            formset = formset_factory(ocenaForm, extra = prijave.count())
            
            context = {
                'arr': prijave,
                'formset': formset,
                'rok_id': rok_id
                }

            return render(request,'vnesi_ocene_predmeta.html',context)

        if request.method == 'POST' and 'vnesi_vec_ocen' in request.POST:
            rok_id = request.POST['id_rok']
            formsetOcena = formset_factory(ocenaForm)
            formset = formsetOcena(request.POST)
            prijave = Prijava.objects.filter(~Q(ocena = -1), rok__id = rok_id).order_by('id')
            ime_ = request.user.first_name
            priimek_ = request.user.last_name
            ime_priimek = ime_ + " " + priimek_

            i = 0
            for form in formset:
                curr = prijave[i]
                ocena_ = form['ocena'].value()
                odjava = form['odjava'].value()
                if odjava == True:
                    curr.ocena = -1
                    curr.odjavitelj = ime_priimek
                    curr.cas_odjave = datetime.now()
                    curr.save()
                elif ocena_:
                    curr.ocena = ocena_
                    curr.save()
                if odjava == False:
                    i +=1
                

            
            prijave = Prijava.objects.filter(~Q(ocena = -1), rok__id = rok_id).order_by('id')
            formset = formset_factory(ocenaForm, extra = prijave.count())
            context = {
                'arr': prijave,
                'formset': formset,
                'rok_id': rok_id
                }

            return render(request,'vnesi_ocene_predmeta.html',context)
#REFERENTKA
    if(request.user.groups.all()[0].name == "referent"):
        if request.method == 'POST' and 'vnesi_ocene' in request.POST:
            rok_id = request.POST['id_rok']

            prijave = Prijava.objects.filter(~Q(ocena = -1), rok__id = rok_id).order_by('id')
            print(prijave)
            formset = formset_factory(ocenaForm, extra = prijave.count())
            
            context = {
                'arr': prijave,
                'formset': formset,
                'rok_id': rok_id
                }

            return render(request,'vnesi_ocene_predmeta.html',context)

        if request.method == 'POST' and 'vnesi_vec_ocen' in request.POST:
            rok_id = request.POST['id_rok']
            formsetOcena = formset_factory(ocenaForm)
            formset = formsetOcena(request.POST)
            prijave = Prijava.objects.filter(rok__id = rok_id, aktivna_prijava = True).order_by('id')
            ime_ = request.user.first_name
            priimek_ = request.user.last_name
            ime_priimek = ime_ + " " + priimek_

            i = 0
            for form in formset:
                curr = prijave[i]
                ocena_ = form['ocena'].value()
                odjava = form['odjava'].value()
                if odjava == True:
                    curr.ocena = -1
                    curr.odjavitelj = ime_priimek
                    curr.cas_odjave = datetime.now()
                    curr.save()
                elif ocena_:
                    curr.ocena = ocena_
                    curr.save()
                if odjava == False:
                    i +=1
                

            
            prijave = Prijava.objects.filter(~Q(ocena = -1), rok__id = rok_id).order_by('id')
            formset = formset_factory(ocenaForm, extra = prijave.count())
            context = {
                'arr': prijave,
                'formset': formset,
                'rok_id': rok_id
                }

            return render(request,'vnesi_ocene_predmeta.html',context)
    else:
        return HttpResponse("Nimaš dovoljenja.")
        
def ptsl():
    return pridobi_trenutno_studijsko_leto()

def seznam_ocen(request):
    rok_id = request.POST['id_rok']
    print(rok_id)
    prijave = Prijava.objects.filter(rok__id = rok_id)

    context = {
        'arr': prijave
        }
    return render(request,'seznam_ocen.html',context)