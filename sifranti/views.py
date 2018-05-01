from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib.auth.models import User, Group

from izpiti.models import *
from student.models import *
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
			return HttpResponse("Uspesno posodobljen element") 
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

	a_sklObcina = Obcina(id = 122, ime="Škofja Loka")
	a_sklObcina.save()
	a_ljObcina = Obcina(id = 61, ime="Ljubljana")
	a_ljObcina.save()

	a = Obcina(id=80, ime="Murska Sobota")
	a.save()
	a = Obcina(id=102, ime="Radovljica")
	a.save()
	a = Obcina(id=186, ime="Trzin")
	a.save()

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
	#naredi studenta
	a = Student(vpisna_stevilka = 63150000, emso=1511996500207, ime="Primož", drzava_rojstva=a_slo,obcina_rojstva= a_ljObcina,  priimek="Trubar",naslov_stalno_bivalisce="Kranjska ulica 12", drzava= Drzava.objects.filter(pk=4)[0], posta= Posta.objects.filter(pk=1293)[0],obcina= Obcina.objects.filter(pk=1)[0],telefon="040123456",email="pt0000@fri.uni-lj.si")
	a.save()
	user, created = User.objects.get_or_create(username="student", email="pt0000@fri.uni-lj.si")
	user.first_name = "Primož"
	user.last_name = "Trubar"

	if created:
		user.set_password("adminadmin")
		user.is_staff=False
		user.is_superuser=False
		ref_group, status = Group.objects.get_or_create(name='students') 
		ref_group.user_set.add(user)
	
	user.save()

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

	a_vilijan = Ucitelj(ime = "Viljan", priimek = "Mahnič", email = "vilijan.mahnic@fri.uni-lj.si")
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

	a = IzvedbaPredmeta(predmet = a_teh, studijsko_leto = a_17_18, ucitelj_1 = a_vilijan)
	a.save()
	a = IzvedbaPredmeta(predmet = a_obl, studijsko_leto = a_17_18, ucitelj_1 = a_narvika)
	a.save()
	a = IzvedbaPredmeta(predmet = a_ep, studijsko_leto = a_17_18, ucitelj_1 = a_darja, ucitelj_2 = a_jaka, ucitelj_3 = a_mateja)

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
	a = IzvedbaPredmeta(predmet = a_P1, studijsko_leto = a_17_18, ucitelj_1 = a_vilijan)
	a.save()

	a_aljaz = Student(vpisna_stevilka = "63150255", emso = "5869362456789", priimek="Rupar", ime="Aljaž", naslov_stalno_bivalisce="Škofja Loka", drzava=a_slo, drzava_rojstva = a_slo, posta= a_sklPosta, obcina=a_sklObcina,obcina_rojstva= a_ljObcina, telefon="031866686", email="ar1961@student.uni-lj.si")
	a_aljaz.save()


	a_verlic = Student(vpisna_stevilka = "63150256", emso = "5869362456755", priimek="Verlič", ime="Aljaž", naslov_stalno_bivalisce="Ljubljana Trnovo", drzava=a_slo,drzava_rojstva=a_slo,obcina_rojstva= a_ljObcina, posta= a_ljPosta, obcina=a_ljObcina, telefon="041786345", email="av1974@student.uni-lj.si")
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

	user, created = User.objects.get_or_create(username="vilijanmahnic", email="vilijan.mahnic@fri.uni-lj.si")
	user.first_name = "Vilijan"
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

	#naredi za 2 letnik strokovni
	for i in range(19, 22):
		predmet_1 = Predmet.objects.get(id=i)
		predmetnik = Predmetnik(studijski_program = UNI, studijsko_leto=LETO, letnik = LETNIK, predmet = predmet_1, obvezen=False)
		
		predmetnik.save()

	LETNIK = Letnik.objects.get(ime="3.")
	#naredi za 3 letnik obvezni
	for i in range(22, 25):
		predmet_1 = Predmet.objects.get(id=i)
		predmetnik = Predmetnik(studijski_program = UNI, studijsko_leto=LETO, letnik = LETNIK, predmet = predmet_1)
		
		predmetnik.save()

	#za module
	for i in range(25, 43):	
		predmet_1 = Predmet.objects.get(id=i)
		predmetnik = Predmetnik(studijski_program = UNI, studijsko_leto=LETO, letnik = LETNIK, predmet = predmet_1, obvezen=False, ima_modul=True)
		predmetnik.save()

	modul = Modul(ime="Informacijski sistemi")
	modul.save()
	modul = Modul(ime="Obladovanje informatike")
	modul.save()
	modul = Modul(ime="Računalniška omrežja")
	modul.save()
	modul = Modul(ime="Umetna inteligenca")
	modul.save()
	modul = Modul(ime="Razvoj programske opreme")
	modul.save()
	modul = Modul(ime="Medijske tehnologije")
	modul.save()

	count = 1
	for i in range (25, 43, 3):
	
		modul = Modul.objects.get(id=count)
		modul.predmetniki.add(Predmetnik.objects.get(id=i))
		modul.predmetniki.add(Predmetnik.objects.get(id=i+1))
		modul.predmetniki.add(Predmetnik.objects.get(id=i+2))
		modul.save()
		
		count=count+1

	#izbirni 2. letnik??
	LETNIK = Letnik.objects.get(ime="2.")
	for i in range(43, 46):	
		predmet_1 = Predmet.objects.get(id=i)
		predmetnik = Predmetnik(studijski_program = UNI, studijsko_leto=LETO, letnik = LETNIK, predmet = predmet_1, obvezen=False)
		predmetnik.save()

	#izbirni 3. letnik??
	LETNIK = Letnik.objects.get(ime="3.")
	for i in range(43, 46):	
		predmet_1 = Predmet.objects.get(id=i)
		predmetnik = Predmetnik(studijski_program = UNI, studijsko_leto=LETO, letnik = LETNIK, predmet = predmet_1, obvezen=False)
		predmetnik.save()
