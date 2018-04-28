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
	
def dodaj_izpit(request):

    if request.method == 'POST' and 'dodaj_izpit' in request.POST:

        datum_ = request.POST['datum']

        id_IzvedbaPredmeta = request.POST['id_IzvedbaPredmeta']
        vnos_izvedbaPredmeta = IzvedbaPredmeta.objects.all()
        for curr_izvedbaPredmeta in vnos_izvedbaPredmeta:
            if str(curr_izvedbaPredmeta.id) == id_IzvedbaPredmeta:
                vnesi = curr_izvedbaPredmeta


        a = Rok(izvedba_predmeta = vnesi, datum = datum_)
        a.save()
    
        return render(request,'izpiti-message.html')

    elif request.method == 'POST' and 'prijava_izpit' in request.POST:

        return render(request,'izpiti-message.html')


def prijava(request):

    if(request.user.groups.all()[0].name == "students"):
        all_roki = Rok.objects.select_related()
        email_stud = request.user.email

       
        for student in Student.objects.all():
            if student.email == email_stud:
                curr_student = student

        if curr_student is None:
            return HttpResponse("Student ne obstaja!")
        else:
            all_predmetiStudenta = PredmetiStudenta.objects.all()

            #gres cez predmetiStudenta da pomachas vpis
            for predmetiStudenta in all_predmetiStudenta:
                if predmetiStudenta.vpis.student.email == curr_student.email:
                    curr_predmetiStudenta = predmetiStudenta
        
        #print(curr_predmetiStudenta.vpis.student.ime)
        #pazi ker ce gres gledat tko kt js pol je lahko izvedbaPredmeta za en predmet z istmu imeno za 2 leti!



    else:
        return HttpResponse("Nimaš dovoljenja.")

    context={
    'arr': all_roki
    }

    return render(request,'prijava.html',context)


   
