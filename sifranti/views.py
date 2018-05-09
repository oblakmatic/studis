from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib.auth.models import User, Group
from django.core.paginator import Paginator

from izpiti.models import *
from student.models import *
from .forms import *
from .models import *
import datetime

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
		form = eval(diff+'Form2')(request.POST)
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
			elements =  eval(diff).all_objects.order_by('pk').values()
			paginator = Paginator(elements, 25)

			page = request.GET.get('page')
			elemen = paginator.get_page(page)



			keyList = []

			if elements:
				enEL = elements[0]
				
				for key in enEL.keys():
					
					verbose = eval(diff)._meta.get_field(key).verbose_name
					
					keyList.append(verbose)

			form_iskanje = SearchForm()
			form = eval(diff+'Form2')()
			context = {
			'object_name' : diff,
			'elements' : elemen,
			'form': form,
			'form2' : form_iskanje,
			'verbose_names' : keyList,
			
			}
			return render(request,'sifranti/changesif.html',context)

		else:
			return HttpResponseRedirect("Ni take tabele")

def update(request, diff, index):
	if request.method == 'POST' and diff in diff_names:
		# create a form instance and populate it with data from the request:
		existing_object = eval(diff).all_objects.get(pk=index)
		form = eval(diff+'Form')(request.POST, instance=existing_object)

		if form.is_valid():
		# example Posta --> PostaForm
			
			# check whether it's valid:
			# and update into database
			
			form.save()
			return HttpResponseRedirect("/sifranti/"+diff+"/") 
		else:
			context = {
				'object_name' : diff,
				'form': form,
				'element' : eval(diff).all_objects.filter(pk=index).values(),
			}
			return render(request,'sifranti/update.html',context)
		
		
		

	# if a GET (or any other method) we'll create a blank form
	else:
		if diff in diff_names:
			element = eval(diff).all_objects.filter(pk=index).values()

			form = eval(diff+'Form')(initial = element[0])
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
		
		element = eval(diff).all_objects.get(id=index)
		if element.veljaven:
			element.veljaven = False
		else:
			element.veljaven = True
		
		element.save()
		return HttpResponseRedirect('/sifranti/'+ diff +'/')

def search2(request, diff, key, iskani_el ):

	if request.method == 'POST' and diff in diff_names:
		# create a form instance and populate it with data from the request:
		
		# example Posta --> PostaForm
		form = eval(diff+'Form2')(request.POST)
		# check whether it's valid:
		# and saves into database
		if form.is_valid():
			
			new_object = form.save()
			return HttpResponseRedirect('/sifranti/'+ diff +'/')
		else:
			elements = eval(diff).all_objects.values()
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
			#elements =  eval(diff).objects.order_by('pk').values()
			elements = vrniFiltriraneElemente(diff, key, iskani_el)
			paginator = Paginator(elements, 25)

			page = request.GET.get('page')
			elemen = paginator.get_page(page)

			keyList = []

			if elements:
				enEL = elements[0]
				
				for key in enEL.keys():
					
					verbose = eval(diff)._meta.get_field(key).verbose_name
					
					keyList.append(verbose)

			form_iskanje = SearchForm()
			form = eval(diff+'Form2')()
			context = {
			'object_name' : diff,
			'elements' : elemen,
			'form': form,
			'form2' : form_iskanje,
			'verbose_names' : keyList,
			
			}
			return render(request,'sifranti/changesif.html',context)

		else:
			return HttpResponse("Ni take tabele")

def vrniFiltriraneElemente(diff, isci_element, element):


	polje = None
	enEL =  eval(diff).all_objects.order_by('pk').values()[0]
	for key in enEL.keys():
			
			verbose = eval(diff)._meta.get_field(key).verbose_name
			
			if verbose == isci_element:
				polje = key
				break     
		
	polje = polje + "__istartswith"
	rezultat = eval(diff).all_objects.filter(**{polje: element}).values()
	return rezultat

def search(request, diff):
	if created:
		user.set_password("adminadmin")
		user.is_staff=False
		user.is_superuser=False
		ref_group, status = Group.objects.get_or_create(name='referent') 
		ref_group.user_set.add(user)

	a_1Letnik = Letnik(ime="1.")
	a_1Letnik.save()
	a_2Letnik = Letnik(ime="2.")
	a_2Letnik.save()
	a_3Letnik= Letnik(ime="3.")
	a_3Letnik.save()

	vsi_predmeti()

	#Aljaz dodal ampak je matic spremenil
	a_teh = Predmet.objects.get(ime = "Tehnologija programske opreme")

	a_obl = Predmet.objects.get(ime = "Osnove oblikovanja")
	
	a_ep = Predmet.objects.get(ime = "Ekonomika in podjetništvo")

	a_oim = Predmet.objects.get(ime = "Organizacija in management")

	a_P1 = Predmet.objects.get(ime = "Programiranje 1")

	a = Predmet.objects.get(ime = "Programiranje 2")

	a_aps1 = Predmet.objects.get(ime = "Algoritmi in podatkovne strukture 1")


	a = StudijskoLeto(ime = "2016/2017")
	a.save()
	a_17_18 = StudijskoLeto(ime = "2017/2018")
	a_17_18.save()
	a = StudijskoLeto(ime = "2018/2019")
	a.save()

	a_vilijan = Ucitelj(ime = "Viljan", priimek = "Mahnič", email = "viljan.mahnic@fri.uni-lj.si")
	a_vilijan.save()
	a_vilijan.predmeti.add(a_teh,a_P1)
	a_narvika = Ucitelj(ime = "Narvika", priimek = "Bovcon", email = "narvika.bavcon@fri.uni-lj.si")
	a_narvika.save()
	a_narvika.predmeti.add(a_obl)
	a_darja = Ucitelj(ime = "Darja", priimek = "Peljhan", email = "darja.peljhan@fri.uni-lj.si")#ep
	a_darja.save()
	a_jaka = Ucitelj(ime = "Jaka", priimek = "Lindič", email = "jaka.lindic@fri.uni-lj.si")#ep
	a_jaka.save()
	a_mateja = Ucitelj(ime = "Mateja", priimek = "Drnovšek", email = "mateja.drnovsek@fri.uni-lj.si") #ep
	a_mateja.save()
	a = Ucitelj(ime = "Tomaž", priimek = "Hovelja", email = "tomaz.hovelja@fri.uni-lj.si")
	a.save()
	a = Ucitelj(ime = "Boštjan", priimek = "Slivnik", email = "bostjan.slivnik@fri.uni-lj.si")
	a.save()
	a = Ucitelj(ime = "Igor", priimek = "Kononenko", email = "igor.kononenko@fri.uni-lj.si")
	a.save()

	a_izv_teh = IzvedbaPredmeta(predmet = a_teh, studijsko_leto = a_17_18, ucitelj_1 = a_vilijan)
	a_izv_teh.save()

	a_izv_obl = IzvedbaPredmeta(predmet = a_obl, studijsko_leto = a_17_18, ucitelj_1 = a_narvika)
	a_izv_obl.save()

	a = IzvedbaPredmeta(predmet = a_ep, studijsko_leto = a_17_18, ucitelj_1 = a_darja, ucitelj_2 = a_jaka, ucitelj_3 = a_mateja)
	a.save()

	a = Posta(id=1231, kraj="Ljubljana-Črnuče")
	a.save()
	a = Posta(id=1215, kraj="Medvode")
	a.save()

	a_stud = StudijskiProgram(id=1000475,sifra="L2",stopnja="C - (predbolonjski) univerzitetni", semestri=9, naziv= "RAČUNAL. IN INFORMATIKA UN")
	a_stud.save()
	a_stud2 = StudijskiProgram(id=1000471,sifra="L1",stopnja="L - druga stopnja: magistrski", semestri=4, naziv= "RAČUNALN. IN INFORM. MAG II.ST")
	a_stud2.save()
	a = StudijskiProgram(id=1000468 ,sifra="VT",stopnja="K - prva stopnja: univerzitetni", semestri=6, naziv= "RAČUNALN. IN INFORM. UN-I.ST")
	a.save()
	a = StudijskiProgram(id=1000470 ,sifra="VU",stopnja="J - prva stopnja: visokošolski strokovni", semestri=6, naziv= "RAČUNALN. IN INFORM. VS-I.ST")
	a.save()

	a_vs1 = VrstaStudija(id=12001,opis="Osnovnošolska izobrazba", nacin_zakljucka="zaključena osnovna šola", raven_klasius=1)
	a_vs1.save()
	a_vs2 = VrstaStudija(id=14001,opis="Srednja poklicna izobrazba", nacin_zakljucka="zaključni izpit", raven_klasius=4)
	a_vs2.save()
	a = VrstaStudija(id=15001,opis="Srednja strokovna izobrazba", nacin_zakljucka="zaključni izpit", raven_klasius=5)
	a.save()
	a = VrstaStudija(id=15002,opis="Srednja splošna izobrazba", nacin_zakljucka="splošna matura", raven_klasius=5)
	a.save()

	a_vv1 = VrstaVpisa(id=1, opis="Prvi vpis v letnik/dodatno leto", mozni_letniki="Vsi letniki in dodatno leto")
	a_vv1.save()
	a_vv2 = VrstaVpisa(id=2, opis="Ponavljanje letnika", mozni_letniki="V zadnjem letniku in v dodatnem letu ponavljanje ni več možno.")
	a_vv2.save()
	a = VrstaVpisa(id=3, opis="Nadaljevanje letnika", mozni_letniki="Vpis ni več dovoljen.")
	a.save()
	a = VrstaVpisa(id=4, opis="Podalšanje statuda študenta", mozni_letniki="Vsi letniki, dodatno leto")
	a.save()
	a = VrstaVpisa(id=5, opis="Vpis v semester skupnega št. programa", mozni_letniki="Vsi letniki razen prvega, dodatno leto ni dovoljeno")
	a.save()
	a = VrstaVpisa(id=6, opis="Nadaljevanje letnika", mozni_letniki="Vsi letniki, samo za skupne študijske programe")
	a.save()
	a = VrstaVpisa(id=7, opis="Nadaljevanje letnika", mozni_letniki="Vsi letniki, dodatno letno ni dovoljeno")
	a.save()
	a = VrstaVpisa(id=98, opis="Nadaljevanje letnika", mozni_letniki="Zadnji letnik. Namenjeno samo strokovmim delavcem v študentskem referatu")
	a.save()

	a_ns1 = NacinStudija(id=1, opis="redni",ang_opis="full-time")
	a_ns1.save()
	a_ns2 = NacinStudija(id=2, opis="izredni",ang_opis="part-time")
	a_ns2.save()
	#naredi 2 zetona za studenta

	zeton = Zeton(student=primozt,studijski_program=StudijskiProgram.objects.filter(pk=1000468)[0],letnik=a_2Letnik,vrsta_vpisa=a_vv1,nacin_studija=a_ns1,vrsta_studija=a_vs1)
	zeton.save()
	zeton2 = Zeton(student=primozt,studijski_program=a_stud2,letnik=a_1Letnik,vrsta_vpisa=a_vv2,nacin_studija=a_ns2,vrsta_studija=a_vs2)
	zeton2.save()

	#izvedba
	a_ns2.save()
	a = IzvedbaPredmeta(predmet = a_P1, studijsko_leto = a_17_18, ucitelj_1 = a_vilijan)
	a.save()

	a_aljaz = Student(vpisna_stevilka = "63150255", emso = "5869362456789", priimek="Rupar", ime="Aljaž", naslov_stalno_bivalisce="Godešič 163, 4220 Škofja Loka", drzava=a_slo, drzava_rojstva = a_slo, posta= a_sklPosta, obcina=a_sklObcina,obcina_rojstva= a_ljObcina, telefon="031866686", email="ar1961@student.uni-lj.si")
	a_aljaz.save()


	a_verlic = Student(vpisna_stevilka = "63150256", emso = "5869362456755", priimek="Verlič", ime="Aljaž", naslov_stalno_bivalisce="Voje 55, 1290 Grosuplje", drzava=a_slo,drzava_rojstva=a_slo,obcina_rojstva= a_ljObcina, posta= a_ljPosta, obcina=a_ljObcina, telefon="041786345", email="av1974@student.uni-lj.si")
	a_verlic.save()

	a = OblikaStudija(id=1, opis="na lokaciji", ang_opis="on-site" )
	a.save()
	a = OblikaStudija(id=2, opis="na daljavo", ang_opis="distance learning" )
	a.save()
	a = OblikaStudija(id=3, opis="e-studij", ang_opis="e-learning" )
	a.save()


	a_vpisAljaz = Vpis(student=a_aljaz, studijsko_leto=a_17_18, studijski_program=a_studijskiProgram, letnik=a_3Letnik, vrsta_vpisa=a_vrstaVpisa,nacin_studija=a_nacinStudija, vrsta_studija=a_vrstaStudija)
	a_vpisAljaz.save()

	a_vpisVerlic = Vpis(student=a_verlic, studijsko_leto=a_17_18, studijski_program=a_studijskiProgram, letnik=a_3Letnik, vrsta_vpisa=a_vrstaVpisa,nacin_studija=a_nacinStudija, vrsta_studija=a_vrstaStudija)
	a_vpisVerlic.save()
	
	

	#a_aljaz.vpisi.add(a_vpisAljaz)
  
	a_predmetiStudentaAljaz = PredmetiStudenta()
	a_predmetiStudentaAljaz.save()
	a_predmetiStudentaAljaz.vpis = a_vpisAljaz
	a_predmetiStudentaAljaz.predmeti.add(a_teh,a_oim,a_ep,a_obl,a_P1)
	a_predmetiStudentaAljaz.save()

	a_predmetiStudentaVerlic = PredmetiStudenta()
	a_predmetiStudentaVerlic.save()
	a_predmetiStudentaVerlic.vpis = a_vpisVerlic
	a_predmetiStudentaVerlic.predmeti.add(a_teh,a_oim,a_ep,a_obl,a_aps1)
	a_predmetiStudentaVerlic.save()


	new_date = datetime.datetime(2013, 6, 9, 11, 13)
	a = Rok(izvedba_predmeta = a_izv_teh, datum = new_date,prostor_izvajanja = "A1")
	a.save()

	#podatki za vpis ocen izpita
	new_date = datetime.datetime(2018, 3, 3, 14, 15)
	a_rok = Rok(izvedba_predmeta = a_izv_teh, datum = new_date,prostor_izvajanja = "P22")
	a_rok.save()

	#se rok za referentko
	new_date = datetime.datetime(2018, 4, 4, 15, 15)
	a_rok_obl = Rok(izvedba_predmeta = a_izv_obl, datum = new_date,prostor_izvajanja = "P14")
	a_rok_obl.save()

	new_date = datetime.datetime(2018, 2, 15, 14, 30)
	a_prijava1 = Prijava(created_at = new_date, predmeti_studenta = a_predmetiStudentaAljaz, rok = a_rok, zaporedna_stevilka_polaganja = 1)
	a_prijava1.save()

	new_date = datetime.datetime(2018, 2, 16, 14, 20)
	a_prijava2 = Prijava(created_at = new_date, predmeti_studenta = a_predmetiStudentaVerlic, rok = a_rok, zaporedna_stevilka_polaganja = 1)
	a_prijava2.save()

	new_date = datetime.datetime(2018, 2, 18, 14, 35)
	a_prijava2 = Prijava(created_at = new_date, predmeti_studenta = a_predmetiStudentaAljaz, rok = a_rok_obl, zaporedna_stevilka_polaganja = 1)
	a_prijava2.save()


	#naredi referenta
	user, created = User.objects.get_or_create(username="referentka", email="referentka@fri.uni-lj.si")
	user.first_name = "Tatjana"
	user.last_name = "Novak"
	user.set_password("adminadmin")
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

	user, created = User.objects.get_or_create(username="viljanmahnic", email="viljan.mahnic@fri.uni-lj.si")
	user.first_name = "Viljan"
	user.last_name = "Mahnic"
		
	if created:
		user.set_password("adminadmin")
		user.is_staff=False
		user.is_superuser=False
		prof_group, status = Group.objects.get_or_create(name='professors') 
		prof_group.user_set.add(user)

	user.save()

	user, created = User.objects.get_or_create(username="aljazrupar", email="ar1961@student.uni-lj.si")
	user.first_name = "Aljaž"
	user.last_name = "Rupar"
		
	if created:
		user.set_password("adminadmin")
		user.is_staff=False
		user.is_superuser=False
		prof_group, status = Group.objects.get_or_create(name='students') 
		prof_group.user_set.add(user)

	user.save()

	#PREDMETNIK
	naredi_predmetnik()

	return HttpResponse("Narejena baza!")


def vsi_predmeti():

	#1 letnik
	a = Predmet(ime = "Programiranje 1")
	a.save()
	a = Predmet(ime = "Programiranje 2")
	a.save()
	a = Predmet(ime = "Diskretne strukture")
	a.save()
	a = Predmet(ime = "Fizika")
	a.save()
	a = Predmet(ime = "Osnove digitalnih vezij")
	a.save()
	a = Predmet(ime = "Osnove matematične analize")
	a.save()
	a = Predmet(ime = "Linearna algebra")
	a.save()
	a = Predmet(ime = "Osnove informacijskih sistemov")
	a.save()
	a = Predmet(ime = "Računalniške komunikacije")
	a.save()
	a = Predmet(ime = "Arhitektura računalniških sistemov")
	a.save()

	#2 letnik obvezni
	a = Predmet(ime = "Verjetnost in statistika")
	a.save()
	a = Predmet(ime = "Algoritmi in podatkovne strukture 1")
	a.save()
	a = Predmet(ime = "Osnove podatkovnih baz")
	a.save()
	a = Predmet(ime = "Organizacija računalniških sistemov")
	a.save()
	a = Predmet(ime = "Izračunljivost in računska zahtevnost")
	a.save()
	a = Predmet(ime = "Teorija informacij in sistemov")
	a.save()
	a = Predmet(ime = "Algoritmi in podatkovne strukture 2")
	a.save()
	a = Predmet(ime = "Operacijski sistemi")
	a.save()

	#2 letnik strokovni
	a = Predmet(ime = "Principi programskih jezikov")
	a.save()
	a = Predmet(ime = "Računalniške tehnologije")
	a.save()
	a = Predmet(ime = "Matematično modeliranje")
	a.save()

	#3 letnik obvezni
	a = Predmet(ime = "Osnove umetne inteligence")
	a.save()
	a = Predmet(ime = "Ekonomika in podjetništvo")
	a.save()
	a = Predmet(ime = "Diplomski seminar")
	a.save()

	#informacijski sistemi
	a = Predmet(ime = "Elektronsko poslovanje")
	a.save()
	a = Predmet(ime = "Poslovna inteligenca")
	a.save()
	a = Predmet(ime = "Organizacija in management")
	a.save()

	#obladovanje informatike
	a = Predmet(ime = "Razvoj informacijskih sistemov")
	a.save()
	a = Predmet(ime = "Tehnologija upravljanja podatkov")
	a.save()
	a = Predmet(ime = "Planiranje in upravljanje informatike")
	a.save()

	#racunalniska omrezja
	a = Predmet(ime = "Modeliranje računalniških omrežij")
	a.save()
	a = Predmet(ime = "Komunikacijski protokoli")
	a.save()
	a = Predmet(ime = "Brezžična in mobilna omrežja")
	a.save()

	#umetna inteligenca
	a = Predmet(ime = "Inteligentni sistemi")
	a.save()
	a = Predmet(ime = "Umetno zaznavanje")
	a.save()
	a = Predmet(ime = "Razvoj inteligentnih sistemov")
	a.save()

	#razvoj programske opreme
	a = Predmet(ime = "Postopki razvoja programske opreme")
	a.save()
	a = Predmet(ime = "Spletno programiranje")
	a.save()
	a = Predmet(ime = "Tehnologija programske opreme")
	a.save()

	#medijske tehnologije
	a = Predmet(ime = "Računalniška grafika in tehnologija iger")
	a.save()
	a = Predmet(ime = "Multimedijski sistemi")
	a.save()
	a = Predmet(ime = "Osnove oblikovanja")
	a.save()

	#splosno izbirni predmeti
	a = Predmet(ime = "Tehnične veščine")
	a.save()
	a = Predmet(ime = "Angleški jezik")
	a.save()
	a = Predmet(ime = "Računalništvo v praksi")
	a.save()

def naredi_predmetnik():

	UNI = StudijskiProgram.objects.get(id=1000468)
	LETO = StudijskoLeto.objects.get(ime="2018/2019")
	LETNIK = Letnik.objects.get(ime="1.")

	#naredi za 1 letnik
	for i in range(1, 11):
		predmet_1 = Predmet.objects.get(id=i)
		predmetnik = Predmetnik(studijski_program = UNI, studijsko_leto=LETO, letnik = LETNIK, predmet = predmet_1)
		predmetnik.save()

	LETNIK = Letnik.objects.get(ime="2.")

	#naredi za 2 letnik obvezni
	for i in range(11, 19):
		predmet_1 = Predmet.objects.get(id=i)
		predmetnik = Predmetnik(studijski_program = UNI, studijsko_leto=LETO, letnik = LETNIK, predmet = predmet_1)
		
		predmetnik.save()

	if request.method == 'POST':
		form = SearchForm(request.POST)

		if form.is_valid() and diff in diff_names:
			isci_element = form.cleaned_data['isci_element']
			element = form.cleaned_data['element']
			
			return HttpResponseRedirect('/sifranti/'+ diff +'/'+isci_element+'/'+element+'/')
	else:
		HttpResponseRedirect('/sifranti/')

def naredi_bazo(request):
	return None