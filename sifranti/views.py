from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib.auth.models import User, Group

from .forms import *
from .models import *

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
            return HttpResponse("Uspesno dodan element") 
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
    a = Obcina(id=80, ime="Murska Sobota")
    a.save()
    a = Obcina(id=102, ime="Radovljica")
    a.save()
    a = Obcina(id=186, ime="Trzin")
    a.save()

    a = Posta(id=1293, kraj="Šmarje-Sap")
    a.save()
    a = Posta(id=1000, kraj="Ljubljana")
    a.save()
    a = Posta(id=1290, kraj="Grosuplje")
    a.save()
    a = Posta(id=1231, kraj="Ljubljana-Črnuče")
    a.save()
    a = Posta(id=1215, kraj="Medvode")
    a.save()

    a = StudijskiProgram(id=1000475,sifra="L2",stopnja="C - (predbolonjski) univerzitetni", semestri=9, naziv= "RAČUNAL. IN INFORMATIKA UN")
    a.save()
    a = StudijskiProgram(id=1000471,sifra="L1",stopnja="L - druga stopnja: magistrski", semestri=4, naziv= "RAČUNALN. IN INFORM. MAG II.ST")
    a.save()
    a = StudijskiProgram(id=1000468 ,sifra="VT",stopnja="K - prva stopnja: univerzitetni", semestri=6, naziv= "RAČUNALN. IN INFORM. UN-I.ST")
    a.save()
    a = StudijskiProgram(id=1000470 ,sifra="VU",stopnja="J - prva stopnja: visokošolski strokovni", semestri=6, naziv= "RAČUNALN. IN INFORM. VS-I.ST")
    a.save()

    a = VrstaStudija(id=12001,opis="Osnovnošolska izobrazba", nacin_zakljucka="zaključena osnovna šola", raven_klasius=1)
    a.save()
    a = VrstaStudija(id=14001,opis="Srednja poklicna izobrazba", nacin_zakljucka="zaključni izpit", raven_klasius=4)
    a.save()
    a = VrstaStudija(id=15001,opis="Srednja strokovna izobrazba", nacin_zakljucka="zaključni izpit", raven_klasius=5)
    a.save()
    a = VrstaStudija(id=15002,opis="Srednja splošna izobrazba", nacin_zakljucka="splošna matura", raven_klasius=5)
    a.save()

    a = VrstaVpisa(id=1, opis="Prvi vpis v letnik/dodatno leto", mozni_letniki="Vsi letniki in dodatno leto")
    a.save()
    a = VrstaVpisa(id=2, opis="Ponavljanje letnika", mozni_letniki="V zadnjem letniku in v dodatnem letu ponavljanje ni več možno.")
    a.save()
    a = VrstaVpisa(id=3, opis="Nadaljevanje letnika", mozni_letniki="Vpis ni več dovoljen.")
    a.save()

    a = NacinStudija(id=1, opis="redni",ang_opis="full-time")
    a.save()
    a = NacinStudija(id=2, opis="izredni",ang_opis="part-time")
    a.save()

    a = OblikaStudija(id=1, opis="na lokaciji", ang_opis="on-site" )
    a.save()
    a = OblikaStudija(id=2, opis="na daljavo", ang_opis="distance learning" )
    a.save()
    a = OblikaStudija(id=3, opis="e-studij", ang_opis="e-learning" )
    a.save()

    #naredi referenta
    user, created = User.objects.get_or_create(username="referentka", email="referentka@fri.uni-lj.si")
    user.first_name = "Tatjana"
    user.last_name = "Novak"
        
    if created:
        user.set_password("adminadmin")
        user.is_staff=False
        user.is_superuser=False
        ref_group, status = Group.objects.get_or_create(name='referent') 
        ref_group.user_set.add(user)

    user.save()

    #naredi profesorja
    user, created = User.objects.get_or_create(username="profesor", email="profesor@fri.uni-lj.si")
    user.first_name = "Lado"
    user.last_name = "Gubara"
        
    if created:
        user.set_password("adminadmin")
        user.is_staff=False
        user.is_superuser=False
        prof_group, status = Group.objects.get_or_create(name='professors') 
        prof_group.user_set.add(user)

    user.save()


    return HttpResponse("Narejena baza!")

