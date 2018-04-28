from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib.auth.models import User, Group

from izpiti.models import *
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
    a_slo = Drzava(id=703, dvomestna_koda="SI", tromestna_oznaka="SVN", iso_naziv="Slovenia", slovenski_naziv="Slovenija",opomba="")
    a_slo.save()
    a = Obcina(id = 213, ime="Ankaran")
    a.save()
    a = Obcina(id = 1, ime="Ajdovščina")
    a.save()
    a = Obcina(id = 19, ime="Divača")
    a.save()
    a = Obcina(id = 20, ime="Dobropolje")
    a.save()
    a_sklObcina = Obcina(id = 122, ime="Škofja Loka")
    a_sklObcina.save()
    a_ljObcina = Obcina(id = 61, ime="Ljubljana")
    a_ljObcina.save()
    a = Posta(id=1293, kraj="Šmarje-Sap")
    a.save()
    a_ljPosta = Posta(id=1000, kraj="Ljubljana")
    a_ljPosta.save()
    a = Posta(id=1290, kraj="Grosuplje")
    a.save()
    a_sklPosta = Posta(id=4220, kraj="Škofja Loka")
    a_sklPosta.save()
    a_studijskiProgram = StudijskiProgram(id=1000475,sifra="L2",stopnja="C - (predbolonjski) univerzitetni", semestri=9, naziv= "RAČUNAL. IN INFORMATIKA UN")
    a_studijskiProgram.save()
    a_vrstaStudija = VrstaStudija(id=12001,opis="Osnovnošolska izobrazba", nacin_zakljucka="zakljucena osnovna šola", raven_klasius=1)
    a_vrstaStudija.save()
    a_vrstaVpisa = VrstaVpisa(id=1, opis="Prvi vpis v letnik/dodatno leto", mozni_letniki="Vsi letniki in dodatno leto")
    a_vrstaVpisa.save()
    a_nacinStudija = NacinStudija(id=1, opis="redni",ang_opis="full-time")
    a_nacinStudija.save()
    a = OblikaStudija(id=1, opis="na lokaciji", ang_opis="on-site" )
    a.save()

    a_1Letnik = Letnik(ime="1.")
    a_1Letnik.save()
    a_2Letnik = Letnik(ime="2.")
    a_2Letnik.save()
    a_3Letnik= Letnik(ime="3.")
    a_3Letnik.save()


    #naredi referenta
    user, created = User.objects.get_or_create(username="referentka", email="referentka@fri.uni-lj.si")
    user.first_name = "Tatjana"
    user.last_name = "Novak"

    #Aljaz dodal->
    a_teh = Predmet(ime = "Tehnologija programske opreme")
    a_teh.save()
    a_obl = Predmet(ime = "Osnove oblikovanja")
    a_obl.save()
    a_ep = Predmet(ime = "Ekonomika in podjetništvo")
    a_ep.save()
    a_oim = Predmet(ime = "Organizacija in management")
    a_oim.save()
    a = Predmet(ime = "Programiranje 1")
    a.save()
    a = Predmet(ime = "Programiranje 2")
    a.save()
    a_aps1 = Predmet(ime = "Algoritmi in podatkovne strukture 1")
    a_aps1.save()

    a = StudijskoLeto(ime = "2016/2017")
    a.save()
    a_17_18 = StudijskoLeto(ime = "2017/2018")
    a_17_18.save()
    a = StudijskoLeto(ime = "2018/2019")
    a.save()

    a_vilijan = Ucitelj(ime = "Viljan", priimek = "Mahnič", email = "vilijan.mahnic@gmail.com")
    a_vilijan.save()
    a_narvika = Ucitelj(ime = "Narvika", priimek = "Bovcon", email = "narvika.bavcon@gmail.com")
    a_narvika.save()
    a_darja = Ucitelj(ime = "Darja", priimek = "Peljhan", email = "darja.peljhan@gmail.com")#ep
    a_darja.save()
    a_jaka = Ucitelj(ime = "Jaka", priimek = "Lindič", email = "jaka.lindic@gmail.com")#ep
    a_jaka.save()
    a_mateja = Ucitelj(ime = "Mateja", priimek = "Drnovšek", email = "mateja.drnovsek@gmail.com") #ep
    a_mateja.save()
    a = Ucitelj(ime = "Tomaž", priimek = "Hovelja", email = "tomaz.hovelja@gmail.com")
    a.save()
    a = Ucitelj(ime = "Boštjan", priimek = "Slivnik", email = "bostjan.slivnik@gmail.com")
    a.save()
    a = Ucitelj(ime = "Igor", priimek = "Kononenko", email = "igor.kononenko@gmail.com")
    a.save()

    a = IzvedbaPredmeta(predmet = a_teh, studijsko_leto = a_17_18, ucitelj_1 = a_vilijan)
    a.save()
    a = IzvedbaPredmeta(predmet = a_obl, studijsko_leto = a_17_18, ucitelj_1 = a_narvika)
    a.save()
    a = IzvedbaPredmeta(predmet = a_ep, studijsko_leto = a_17_18, ucitelj_1 = a_darja, ucitelj_2 = a_jaka, ucitelj_3 = a_mateja)
    a.save()

    a_aljaz = Student(vpisna_stevilka = "63150255", emso = "5869362456789", priimek="Rupar", ime="Aljaž", naslov_stalno_bivalisce="Škofja Loka", drzava=a_slo,kraj_rojstva="Kranj", posta= a_sklPosta, obcina=a_sklObcina, telefon="031866686", email="ar1961@student.uni-lj.si")
    a_aljaz.save()

    a_verlic = Student(vpisna_stevilka = "63150256", emso = "5869362456755", priimek="Verlič", ime="Aljaž", naslov_stalno_bivalisce="Ljubljana Trnovo", drzava=a_slo,kraj_rojstva="Ljubljana", posta= a_ljPosta, obcina=a_ljObcina, telefon="041786345", email="av1974@student.uni-lj.si")
    a_verlic.save()

    a_vpisAljaz = Vpis(student=a_aljaz, studijsko_leto=a_17_18, studijski_program=a_studijskiProgram, letnik=a_3Letnik, vrsta_vpisa=a_vrstaVpisa,nacin_studija=a_nacinStudija, vrsta_studija=a_vrstaStudija)
    a_vpisAljaz.save()

    a_vpisVerlic = Vpis(student=a_verlic, studijsko_leto=a_17_18, studijski_program=a_studijskiProgram, letnik=a_3Letnik, vrsta_vpisa=a_vrstaVpisa,nacin_studija=a_nacinStudija, vrsta_studija=a_vrstaStudija)
    a_vpisVerlic.save()
    
  
    a_predmetiStudentaAljaz = PredmetiStudenta()
    a_predmetiStudentaAljaz.save()
    a_predmetiStudentaAljaz.vpis = a_vpisAljaz
    a_predmetiStudentaAljaz.predmeti.add(a_teh,a_oim,a_ep,a_obl)

    a_predmetiStudentaVerlic = PredmetiStudenta()
    a_predmetiStudentaVerlic.save()
    a_predmetiStudentaVerlic.vpis = a_vpisVerlic
    a_predmetiStudentaVerlic.predmeti.add(a_teh,a_oim,a_ep,a_obl,a_aps1)


    
        
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

