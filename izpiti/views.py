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
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from reportlab.pdfgen import canvas
from reportlab.platypus import *
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter, A4, landscape
from reportlab.lib import colors 
from reportlab.graphics.shapes import Drawing, Line

import csv
import time
from reportlab.lib.enums import TA_JUSTIFY, TA_RIGHT, TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from student.forms import TokenForm
from reportlab.platypus.tables import Table

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
pdfmetrics.registerFont(TTFont('Vera', 'Vera.ttf'))


alphabet = 'abcčdefghijklmnopqrsštuvwxyzž0123456789'


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
		print(datum_.date())
		if (Rok.objects.filter(datum__date=datum_.date()).count() != 0):
			context = {
				'arr': [],
				'message': 'Rok na izbrani datum že obstaja!',
				'msg_type': 'alert-warning'
			}

			return render(request,'izpiti-message.html',context)


		id_IzvedbaPredmeta = request.POST['id_IzvedbaPredmeta']
		vnos_izvedbaPredmeta = IzvedbaPredmeta.objects.all()
		for curr_izvedbaPredmeta in vnos_izvedbaPredmeta:
			print(curr_izvedbaPredmeta.id)
			if str(curr_izvedbaPredmeta.id) == id_IzvedbaPredmeta:
				vnesi = curr_izvedbaPredmeta
				print('izvedba predmet najdena?')

		

		a = Rok(izvedba_predmeta = vnesi, datum = datum_, prostor_izvajanja = prostor)
		a.save()

		#da mu pokaze se vse roke k jih je razpisov
		email_ = request.user.email
		showRoki = []
		for rok in Rok.objects.all().order_by('datum'):
			if rok.izvedba_predmeta.ucitelj_1 != None and rok.izvedba_predmeta.ucitelj_1.email == email_:
				showRoki.append(rok)
			elif rok.izvedba_predmeta.ucitelj_2 != None and rok.izvedba_predmeta.ucitelj_2.email == email_:
				showRoki.append(rok)
			elif rok.izvedba_predmeta.ucitelj_3 != None and rok.izvedba_predmeta.ucitelj_3.email == email_:
				showRoki.append(rok)
	
		context = {
			'arr': showRoki,
			'message': 'Rok uspešno dodan!',
			'msg_type': 'alert-success'
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
				if(abs((vnesi_rok.datum - datum_zadnje_prijave).days) <= 10): # TODO: Omejitev po dnevih naj bi bila nastavljiva
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
			ime_priimek = request.user.first_name + " " + request.user.last_name
			for prijava in all_prijava:
				if prijava.predmeti_studenta == vnesi_predmeti_studenta and prijava.rok == vnesi_rok:
					print("prijava oznacena kot neaktivna!")
					prijava.aktivna_prijava = False
					prijava.odjavitelj = ime_priimek
					prijava.cas_odjave = datetime.now()
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
				if rok.izvedba_predmeta.studijsko_leto == ptsl():
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
					prijava_condition = False
					if(zadnje_prijave.count() != 0):
						#print(vars(zadnje_prijave[0]))
						datum_zadnje_prijave = zadnje_prijave[0].created_at
						print("datum zadnje prijave", datum_zadnje_prijave)
						print("vnesi rok datum", vnesi_rok.datum)
						#print("razlika", (datum_zadnje_prijave - vnesi_rok.datum).days)
						if(abs((vnesi_rok.datum - datum_zadnje_prijave).days) <= 10): # TODO: Omejitev po dnevih naj bi bila 
							prijava_condition = True
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
							if (polaganja_trenutno_leto >= 3 or stevilo_dosedanjih_polaganj >= 6 or prijava_condition or time_now >= datetime(rok.datum.year, rok.datum.month, rok.datum.day - 1, 0) ):
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
		roki = Rok.objects.filter( Q(izvedba_predmeta__ucitelj_1__email = email_) | Q(izvedba_predmeta__ucitelj_2__email = email_) | Q(izvedba_predmeta__ucitelj_3__email = email_) , Q(datum__lte=datetime.now().date())).order_by("datum")

		#prikaz rokov v prihodnosti --> za prikaz seznama prijavljenih, onemogočen vnos ocene!
		roki_forward = Rok.objects.filter( Q(izvedba_predmeta__ucitelj_1__email = email_) | Q(izvedba_predmeta__ucitelj_2__email = email_) | Q(izvedba_predmeta__ucitelj_3__email = email_) , Q(datum__gt=datetime.now().date())).order_by("datum")

		context = {
			'arr': roki,
			'roki_forward': roki_forward
			}

		return render(request,'vnesi_ocene.html', context)
	elif(request.user.groups.all()[0].name == "referent"):
		curr_roki = []
		roki = Rok.objects.filter(datum__lte=datetime.now().date()).order_by("datum")

		#prikaz rokov v prihodnosti --> za prikaz seznama prijavljenih, onemogočen vnos ocene!
		roki_forward = Rok.objects.filter(datum__gt=datetime.now().date()).order_by("datum")

		context = {
			'arr': roki,
			'roki_forward': roki_forward
			}

		return render(request,'vnesi_ocene.html', context)
	else:
		return HttpResponse("Nimaš dovoljenja.")

def vnesi_ocene_predmeta(request):
#UCITELJ
	if(request.user.groups.all()[0].name == "professors"):
		if request.method == 'POST' and 'vnesi_ocene' in request.POST:
			rok_id = request.POST['id_rok']

			prijave = Prijava.objects.filter(~Q(ocena = -1), rok__id = rok_id)
			prijave = sort_prijave(prijave)

			formset = formset_factory(ocenaForm, extra = len(prijave))

			#dodal paginator
			paginator = Paginator(prijave, 20)
			page = request.GET.get('page')
			all_students = paginator.get_page(page)
			
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
			prijave = Prijava.objects.filter(~Q(ocena = -1), rok__id = rok_id)
			prijave = sort_prijave(prijave)
			ime_ = request.user.first_name
			priimek_ = request.user.last_name
			ime_priimek = ime_ + " " + priimek_

			i = 0
			for form in formset:
				curr = prijave[i]
				ocena_ = form['ocena'].value()
				ocena_izpita_ = form['ocena_izpita'].value()
				odjava = form['odjava'].value()
				
				if odjava == True:
					curr.ocena_izpita = -1
					curr.ocena = -1
					curr.odjavitelj = ime_priimek
					curr.cas_odjave = datetime.now()
					curr.save()
				elif ocena_ or ocena_izpita_:
					if (ocena_):
						curr.ocena = ocena_
					if (ocena_izpita_ ):
						curr.ocena_izpita = ocena_izpita_
					curr.save()
				if odjava == False:
					i +=1
				

			
			prijave = Prijava.objects.filter(~Q(ocena = -1), rok__id = rok_id)
			prijave = sort_prijave(prijave)
			formset = formset_factory(ocenaForm, extra = len(prijave))


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

			prijave = Prijava.objects.filter(~Q(ocena = -1), rok__id = rok_id)
			prijave = sort_prijave(prijave)
			
			formset = formset_factory(ocenaForm, extra = len(prijave))
			
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
			prijave = Prijava.objects.filter(rok__id = rok_id, aktivna_prijava = True)
			prijave = sort_prijave(prijave)
			ime_ = request.user.first_name
			priimek_ = request.user.last_name
			ime_priimek = ime_ + " " + priimek_

			i = 0
			for form in formset:
				curr = prijave[i]
				ocena_ = form['ocena'].value()
				ocena_izpita_ = form['ocena_izpita'].value()
				odjava = form['odjava'].value()
				
				if odjava == True:
					curr.ocena_izpita = -1
					curr.ocena = -1
					curr.odjavitelj = ime_priimek
					curr.cas_odjave = datetime.now()
					curr.save()
				elif ocena_ or ocena_izpita_:
					if (ocena_):
						curr.ocena = ocena_
					if (ocena_izpita_ ):
						curr.ocena_izpita = ocena_izpita_
					curr.save()
				if odjava == False:
					i +=1
				

			
			prijave = Prijava.objects.filter(~Q(ocena = -1), rok__id = rok_id)
			prijave = sort_prijave(prijave)
			formset = formset_factory(ocenaForm, extra = len(prijave))
			context = {
				'arr': prijave,
				'formset': formset,
				'rok_id': rok_id
				}

			return render(request,'vnesi_ocene_predmeta.html',context)
	else:
		return HttpResponse("Nimaš dovoljenja.")

def vnesi_koncne_ocene(request):
#UCITELJ
	if(request.user.groups.all()[0].name == "professors"):
		if request.method == 'POST' and 'vnesi_ocene' in request.POST:
			rok_id = request.POST['id_rok']

			prijave = Prijava.objects.filter(~Q(ocena = -1), rok__id = rok_id)
			prijave = sort_prijave(prijave)
			formset = formset_factory(ocenaForm, extra = len(prijave))
			
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
			prijave = Prijava.objects.filter(~Q(ocena = -1), rok__id = rok_id)
			prijave = sort_prijave(prijave)
			ime_ = request.user.first_name
			priimek_ = request.user.last_name
			ime_priimek = ime_ + " " + priimek_

			i = 0
			for form in formset:
				curr = prijave[i]
				ocena_ = form['ocena'].value()
				ocena_izpita_ = form['ocena_izpita'].value()
				odjava = form['odjava'].value()

				if odjava == True:
					curr.ocena_izpita = -1
					curr.ocena = -1
					curr.odjavitelj = ime_priimek
					curr.cas_odjave = datetime.now()
					curr.save()
				elif ocena_ or ocena_izpita_:
					if (ocena_):
						curr.ocena = ocena_
					if (ocena_izpita_ ):
						curr.ocena_izpita = ocena_izpita_
					curr.save()
				if odjava == False:
					i +=1
				

			
			prijave = Prijava.objects.filter(~Q(ocena = -1), rok__id = rok_id)
			prijave = sort_prijave(prijave)
			formset = formset_factory(ocenaForm, extra = len(prijave))
			
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

			prijave = Prijava.objects.filter(~Q(ocena = -1), rok__id = rok_id)
			
			formset = formset_factory(ocenaForm, extra = len(prijave))
			
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
			prijave = Prijava.objects.filter(rok__id = rok_id, aktivna_prijava = True)
			prijave = sort_prijave(prijave)
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
				

			
			prijave = Prijava.objects.filter(~Q(ocena = -1), rok__id = rok_id)
			prijave = sort_prijave(prijave)
			formset = formset_factory(ocenaForm, extra = len(prijave))
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

def seznam_prijavljenih(request):
	
	if request.method == 'POST' and 'seznam' in request.POST:
		rok_id = request.POST['id_rok']
		prijave = Prijava.objects.filter(rok__id = rok_id,aktivna_prijava = True)
		prijave = sort_prijave(prijave)


		curr_rok = Rok.objects.filter(id = rok_id)[0]
		
		context = {
			'arr': prijave,
			'curr_rok': curr_rok
			}

		return render(request,'seznam_prijavljenih.html',context)

	if request.method == 'POST' and 'natisni_pdf' in request.POST:

		rok_id = request.POST.get('id_rok')

		prijave = Prijava.objects.filter(rok__id = rok_id,aktivna_prijava = True)
		prijave = sort_prijave(prijave)
		rok = Rok.objects.filter(id = rok_id)[0]
		print(rok)

		response = HttpResponse(content_type='application/pdf')
		response['Content-Disposition'] = 'inline; filename="prijave.pdf"'
			
		doc = SimpleDocTemplate(response,pagesize=letter,
					rightMargin=72,leftMargin=72,
					topMargin=72,bottomMargin=18)
		Story=[]
		logo = "student/Logo_UL_FRI.png"
		magName = "Pythonista"
		issueNum = 12
		subPrice = "99.00"


		formatted_time = datetime.now().date()
		formatted_time = str(formatted_time)
		tabela = formatted_time.split("-")
		formatted_time = tabela[2] + "." + tabela[1] + "." + tabela[0]
		#full_name = vpis_.student.ime + " " +  vpis_.student.priimek 
		#address_parts = vpis_.student.naslov_stalno_bivalisce.split(",")

		im = Image(logo, 2*inch, 2*inch)
		Story.append(im)
			
		styles=getSampleStyleSheet()
		styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
		p = ParagraphStyle('MyNormal',parent=styles['Normal'], fontName='Vera')
		p1 = ParagraphStyle('MyNormal',parent=styles['Normal'], fontName='Vera',alignment=TA_RIGHT)
		p2 = ParagraphStyle('MyNormal',parent=styles['Normal'], fontName='Vera',alignment=TA_CENTER)
		ptext = '<font size=12>%s</font>' % formatted_time
		par = Paragraph(ptext, p1)
		Story.append(par)
		Story.append(Spacer(1, 12))

		# Create header
		ptext = '<font size=12>Predmet: %s</font>' % rok.izvedba_predmeta.predmet
		par = Paragraph(ptext, p)
		Story.append(par)

		izprasevalci = ""
		uc1 = rok.izvedba_predmeta.ucitelj_1
		uc2 = rok.izvedba_predmeta.ucitelj_2
		uc3 = rok.izvedba_predmeta.ucitelj_3

		if uc3 != None:
			izprasevalci = uc1 + " / " + uc2 + " / " + " / " + uc3
		elif uc2 != None:
			izprasevalci = uc1 + " / " + uc2 
		elif uc1!= None:
			izprasevalci = uc1

		ptext = '<font size=12>Izpraševalci: %s</font>' % izprasevalci
		par = Paragraph(ptext, p)
		Story.append(par)

		ptext = '<font size=12>Datum in ura izpita: %s</font>' % rok.datum.strftime("%d.%m.%y, %H:%M")
		par = Paragraph(ptext, p)
		Story.append(par)

		ptext = '<font size=12>Prostor izvajanja: %s</font>' % rok.prostor_izvajanja
		par = Paragraph(ptext, p)
		Story.append(par)
		Story.append(Spacer(1, 20))

		header = ["Zaporedna stevilka", "Vpisna stevilka", "Priimek,\nime", "Vrnjena prijava/\ncas odjave/\nodjavitelj", "Stevilo tock\nizpita", "Ocena\nizpita", "Zaporedna\nstevilka\npolaganja"]
		data = [header]
		print(data)
		for i, prijava in enumerate(prijave):
			zap_st = i+1
			zap_st_str = str(zap_st) + "."
			vpisna_st = prijava.predmeti_studenta.vpis.student.vpisna_stevilka
			priimek_ime = prijava.predmeti_studenta.vpis.student.priimek + ", " + prijava.predmeti_studenta.vpis.student.ime
			VP="NE"
			if prijava.ocena == -1:
				cas = prijava.cas_odjave + timedelta(hours=2)
				VP = "VP" + "/\n" + cas.strftime("%d.%m.%y, %H:%M") + "/\n" + prijava.odjavitelj
			
			tocke_izpita = "/"
			if prijava.ocena == None:
				tocke_izpita = "Ni vpisana"
			elif prijava.ocena == -1:
				tocke_izpita = "VP"
			else:
				tocke_izpita = prijava.ocena

			ocena_izpita = "/"
			if prijava.ocena_izpita == None:
				ocena_izpita = "Ni vpisana"
			elif prijava.ocena_izpita == -1:
				ocena_izpita = "VP"
			else:
				ocena_izpita = prijava.ocena_izpita

			zap_st_polaganja = prijava.zaporedna_stevilka_polaganja
			add_data = [zap_st_str, vpisna_st, priimek_ime, VP, tocke_izpita, ocena_izpita, zap_st_polaganja]
			data.append(add_data)
		
		LIST_STYLE = TableStyle([
									('INNERGRID', (0, 0), (-1, -1), 0.2, colors.black),
									('FONT', (0,0), (-1, -1), 'Vera')
								])
		t = Table(data)
		t.setStyle(LIST_STYLE)
		Story.append(t)

			
		Story.append(Spacer(1, 50))

		doc.build(Story)

		return response
	if request.method == 'POST' and 'natisni_csv' in request.POST:

		rok_id = request.POST.get('id_rok')

		response = HttpResponse(content_type='text/csv')
		response['Content-Disposition'] = 'attachment; filename="izpiti.csv"'
		writer = csv.writer(response)

		prijave = Prijava.objects.filter(rok__id = rok_id,aktivna_prijava = True)
		prijave = sort_prijave(prijave)
		header = ["Vpisna stevilka", "Priimek","Ime", "Vrnjena prijava/cas odjave/odjavitelj", "Stevilo tock izpita", "Ocena izpita", "Zaporedna stevilka polaganja"]
		writer.writerow(header)

		for prijava_ in prijave:
			vpisna_st = prijava_.predmeti_studenta.vpis.student.vpisna_stevilka
			priimek_ime = prijava_.predmeti_studenta.vpis.student.priimek + ", " + prijava_.predmeti_studenta.vpis.student.ime
			VP="NE"
			if prijava_.ocena == -1:
				cas = prijava_.cas_odjave + timedelta(hours=2)
				VP = "VP" + "/" + cas.strftime("%d.%m.%y, %H:%M") + "/" + prijava_.odjavitelj
			
			tocke_izpita = "/"
			if prijava_.ocena == None:
				tocke_izpita = "Ni vpisana"
			elif prijava_.ocena == -1:
				tocke_izpita = "VP"
			else:
				tocke_izpita = prijava_.ocena

			ocena_izpita = "/"
			if prijava_.ocena_izpita == None:
				ocena_izpita = "Ni vpisana"
			elif prijava_.ocena_izpita == -1:
				ocena_izpita = "VP"
			else:
				ocena_izpita = prijava_.ocena_izpita

			zap_st_polaganja = prijava_.zaporedna_stevilka_polaganja
			add_data = [vpisna_st, priimek_ime, VP, tocke_izpita, ocena_izpita, zap_st_polaganja]
			writer.writerow(add_data)


		return response

def sort_prijave(prijave):
	
	imena = []
	for prijava_ in prijave:
		p_i = (prijava_.predmeti_studenta.vpis.student.priimek, \
			prijava_.predmeti_studenta.vpis.student.ime, \
			prijava_.predmeti_studenta.vpis.student.vpisna_stevilka)
		imena.append(p_i)
		print(p_i)

	imena = sorted(imena, key=lambda student: (  [alphabet.index(c) for c in student[0].lower()], \
												 [alphabet.index(c) for c in student[1].lower()], \
												 [alphabet.index(c) for c in str(student[2])]))

	new_prijave = []
	while imena:
		print(imena)
		for prijava_ in prijave:
			p_i = (prijava_.predmeti_studenta.vpis.student.priimek, \
				prijava_.predmeti_studenta.vpis.student.ime, \
				prijava_.predmeti_studenta.vpis.student.vpisna_stevilka)
			if p_i == imena[0]:
				new_prijave.append(prijava_)
				del imena[0]
				break

	return new_prijave

def uredi_izpit():
	

def izbrisi_izpit():
	
