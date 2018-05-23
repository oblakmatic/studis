from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from student.models import Student, Zeton, Vpis, Kandidat, Predmetnik
from izpiti.models import PredmetiStudenta, Ucitelj
from sifranti.models import *
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
import csv
import datetime
import codecs
from reportlab.pdfgen import canvas
from reportlab.platypus import *
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter, A4, landscape
from reportlab.lib import colors 

import time
from reportlab.lib.enums import TA_JUSTIFY, TA_RIGHT, TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from student.forms import TokenForm
from django.db.models import Q

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
pdfmetrics.registerFont(TTFont('Vera', 'Vera.ttf'))

import pdfkit
from django.template.loader import render_to_string
from django.core.files.storage import FileSystemStorage

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from operator import itemgetter, attrgetter

alphabet = 'abcčdefghijklmnopqrsštuvwxyzž0123456789'

# Create your views here.
def upload_file(request):

	return render(request,'import_students.html')

def students(request):
	if(request.user.groups.all()[0].name == "students"):
		return redirect('/student/podatki')
	else:
		if(request.user.groups.all()[0].name == "referent"):
			all_students_list = Student.objects.values('priimek', 'ime', 'vpisna_stevilka', 'email')#.order_by('priimek')
			print('unsorted', all_students_list)
			all_students_list = sorted(all_students_list, key=lambda student: ([alphabet.index(c) for c in student['priimek'].lower()], \
																			   [alphabet.index(c) for c in student['ime'].lower()], \
																			   [alphabet.index(c) for c in str(student['vpisna_stevilka'])]))
			print('sorted', all_students_list)
			paginator = Paginator(all_students_list, 10)
			page = request.GET.get('page')
			all_students = paginator.get_page(page)
			

		elif(request.user.groups.all()[0].name == "professors"):
			# student <- vpis ->  predmeti studenta -> predmet -> izvedba predmeta -> ucitelj 1, 2, 3
			all_students_list = Student.objects.filter(Q(vpis__predmetistudenta__predmeti__izvedbapredmeta__ucitelj_1__email = request.user.email) \
												| Q(vpis__predmetistudenta__predmeti__izvedbapredmeta__ucitelj_2__email = request.user.email) \
												| Q(vpis__predmetistudenta__predmeti__izvedbapredmeta__ucitelj_3__email = request.user.email))\
												.distinct().values('priimek', 'ime', 'vpisna_stevilka', 'email')#.order_by('priimek')
			all_students_list = sorted(all_students_list, key=lambda student: ([alphabet.index(c) for c in student['priimek'].lower()], [alphabet.index(c) for c in student['ime'].lower()], [alphabet.index(c) for c in str(student['vpisna_stevilka'])]))

			paginator = Paginator(all_students_list, 10)
			page = request.GET.get('page')
			all_students = paginator.get_page(page)

		context = {
			'students': all_students
		}
		return render(request,'students.html', context)

def import_students(request):
	content = request.FILES['students'].read().splitlines()

	arr = []
	updated = 0
	new = 0
	for i in range(0, len(content)):
		data = content[i].decode('utf-8')
		
		name = data[0:30].rstrip()
		surname = data[30:60].rstrip()
		program = data[60:67]
		email = data[67:].rstrip()

		kandidat = None
		try:
			kandidat = Kandidat.objects.get(email=email)
			kandidat.ime = name
			kandidat.priimek = surname
			kandidat.studijski_program=StudijskiProgram.objects.filter(pk=int(program))[0]
			kandidat.save()
			updated = updated + 1
		except Kandidat.DoesNotExist:

			serial = Kandidat.objects.count()+1
			year = datetime.datetime.today().year % 2000
			vpisna = "63"+ str(year) + format(serial, '04d')
			kandidat = Kandidat.objects.create(vpisna_stevilka=int(vpisna))
			kandidat.email = email
			kandidat.ime = name
			kandidat.studijski_program = StudijskiProgram.objects.filter(pk=int(program))[0]
			kandidat.priimek = surname
			kandidat.save()
			
			new = new + 1


		password = "adminadmin" #User.objects.make_random_password()
		username = email[:6]


		user, created2 = User.objects.get_or_create(username=username, email=email)
		user.first_name = name
		user.last_name = surname
		
		if created2:
			user.set_password(password)
			user.is_staff=False
			user.is_superuser=False
			students_group, status = Group.objects.get_or_create(name='candidates') 
			students_group.user_set.add(user)

		user.save()

		temp=[]
		temp.append(str(i + 1))
		temp.append(kandidat.vpisna_stevilka)
		temp.append(surname)
		temp.append(name)
		temp.append(username)
		temp.append(password)
		

		arr.append(temp)
	


	context = {
		'length': len(arr),
		'students':arr,
		'new': new,
		'updated': updated
	}

	return render(request,'import_msg.html', context)

def students_search(request): 
	# print(request.body)
	search_query = request.POST.get('search_text', '')
	# print("Iskalni niz:" + search_query)
	# if (search_query != ''):
	id_filtered_students = Student.objects.values('vpisna_stevilka', 'ime', 'priimek', 'email').filter(vpisna_stevilka__startswith=search_query)
	id_filtered_students = sorted(id_filtered_students, key=lambda student: (  [alphabet.index(c) for c in student['priimek'].lower()], \
																			   [alphabet.index(c) for c in student['ime'].lower()], \
																			   [alphabet.index(c) for c in str(student['vpisna_stevilka'])]))
	# print(id_filtered_students)
	name_filtered_students = Student.objects.values('vpisna_stevilka', 'ime', 'priimek', 'email').filter(ime__startswith=search_query)
	name_filtered_students = sorted(name_filtered_students, key=lambda student: (  [alphabet.index(c) for c in student['priimek'].lower()], \
																			   [alphabet.index(c) for c in student['ime'].lower()], \
																			   [alphabet.index(c) for c in str(student['vpisna_stevilka'])]))
	surname_filtered_students = Student.objects.values('vpisna_stevilka', 'ime', 'priimek', 'email').filter(priimek__startswith=search_query)
	surname_filtered_students = sorted(surname_filtered_students, key=lambda student: (  [alphabet.index(c) for c in student['priimek'].lower()], \
																			   [alphabet.index(c) for c in student['ime'].lower()], \
																			   [alphabet.index(c) for c in str(student['vpisna_stevilka'])]))
	context = {
		'students_id': id_filtered_students,
		'students_name': name_filtered_students,
		'students_surname': surname_filtered_students
	}
	return render(request,'search.html', context)

def token_add(request, id):
	if request.method == 'POST':
		form = TokenForm(request.POST)
		if (form.is_valid()):
			# print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ pridemo do posta ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
			student = form.cleaned_data['student']
			program = form.cleaned_data['studijski_program']
			letnik = form.cleaned_data['letnik']
			vrsta_vpisa = form.cleaned_data['vrsta_vpisa']
			nacin_studija = form.cleaned_data['nacin_studija']
			# vrsta_studija = form.cleaned_data['vrsta_studija']
			prosta_izbira = form.cleaned_data['pravica_do_izbire']

			context = {}
			tokenForm = TokenForm(initial={
				'student': student.vpisna_stevilka,
				'studijski_program': program.id,
				'letnik': letnik.id,
				'vrsta_vpisa': vrsta_vpisa.id,
				'nacin_studija': nacin_studija.id,
				# 'vrsta_studija': token.vrsta_studija.id,
				'pravica_do_izbire': prosta_izbira})
			
			

				
			if Zeton.objects.filter(student=student).count() >= 2:
				context = {
					'message': 'Student že ima 2 žetona!',
					'msg_type': 'alert-warning',
					'tokenForm': tokenForm
				}
				return render(request, 'token_add.html', context)
			if (program.id == 1000471 and letnik.ime == "3."):
				context = {
					'message': 'Neveljavna kombinacija program / letnik!',
					'msg_type': 'alert-warning',
					'tokenForm': tokenForm
				}
				return render(request, 'token_add.html', context)
			zeton = Zeton(student=student, studijski_program=program, letnik=letnik, vrsta_vpisa=vrsta_vpisa, nacin_studija=nacin_studija, pravica_do_izbire = prosta_izbira)# vrsta_studija=vrsta_studija, pravica_do_izbire=prosta_izbira)
			zeton.save()
			return token_list(request, 'Žeton uspešno dodan!', 'alert-success')
		else:
			context = {}
			tokenForm = TokenForm(initial={
				'student': id})
			
			context = {
				'message': 'Prosimo, vnesite vse zahtevane podatke!',
				'msg_type': 'alert-warning',
				'tokenForm': tokenForm
			}
			return render(request, 'token_add.html', context)
		
	else:
		# vpisi = Vpis.objects.select_related().filter(student__pk = id).order_by('-pk')
		# print(vpisi)

		# context = {
		# 	'id': id
		# }
		context =  {}
		if (id):
			tokenForm = TokenForm(initial={'student': str(id)})
		else:
			tokenForm = TokenForm()
		context['tokenForm'] = tokenForm
		
		return render(request, 'token_add.html', context )

def token_list(request, msg=None, msgType = None):
	all_tokens = Zeton.objects.select_related()
	
	zetoni = []
	for token in all_tokens:
		# print(token)
		# print(token.student)
		# print(dir(token))
		zeton = {
			'id': token.pk,
			'student': token.student,
			'studijski_program': token.studijski_program,
			'letnik': token.letnik,
			'vrsta_vpisa': token.vrsta_vpisa,
			'nacin_studija': token.nacin_studija,
			'vrsta_studija': token.vrsta_studija,
			'pravica_do_izbire': 'DA' if token.pravica_do_izbire else 'NE' if token.letnik.ime == '3.' else '/'
		}
		zetoni.append(zeton)
	# print(all_tokens)
	paginator = Paginator(zetoni, 10)
	page = request.GET.get('page')
	ostranjeni_zetoni = paginator.get_page(page)
	context = {
		'arr': ostranjeni_zetoni
	}
	if (not msg is None):
		context['message'] = msg
		context['msg_type'] = msgType
	return render(request,'token_list.html', context)

def token_delete(request, del_id):
	try:
		zeton = Zeton.objects.get(pk=del_id)
		print(zeton)
	except Zeton.DoesNotExist:
		zeton = None
	if(zeton == None):
		return token_list(request, 'Ta žeton ne obstaja!', 'alert-warning')
	else:
		zeton.delete()
		return token_list(request, 'Žeton uspešno izbrisan!', 'alert-success')

def token_edit(request, edit_id):
	print(request.method)
	if request.method == 'POST':
		# print(request.POST)
		token = Zeton.objects.get(pk=edit_id)
		form = TokenForm(request.POST)
		

		if (form.is_valid()):
			# print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ pridemo do posta ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
			
			token.studijski_program = form.cleaned_data['studijski_program']
			token.letnik = form.cleaned_data['letnik']
			token.vrsta_vpisa = form.cleaned_data['vrsta_vpisa']
			token.nacin_studija = form.cleaned_data['nacin_studija']
			# token.vrsta_studija = form.cleaned_data['vrsta_studija']
			token.prosta_izbira = form.cleaned_data['pravica_do_izbire']

			context = {}
			tokenForm = TokenForm(initial={
				'student': token.student.vpisna_stevilka,
				'studijski_program': token.studijski_program.id,
				'letnik': token.letnik.id,
				'vrsta_vpisa': token.vrsta_vpisa.id,
				'nacin_studija': token.nacin_studija.id,
				# 'vrsta_studija': token.vrsta_studija.id,
				'pravica_do_izbire': token.pravica_do_izbire})
			
			context['tokenForm'] = tokenForm
			if (token.studijski_program.id == 1000471 and letnik.ime == "3."):
				context = {
					'message': 'Neveljavna kombinacija program / letnik!',
					'msg_type': 'alert-warning',
					'form': tokenForm
				}
				return render(request, 'token_edit.html', context)
			token.save()
			return token_list(request, 'Žeton uspešno urejen!', 'alert-success')
		else:
			return token_list(request, 'Neveljavna forma!', 'alert-warning')
	else:
		try:
			zeton = Zeton.objects.select_related().get(pk=edit_id)
		except Zeton.DoesNotExist:
			zeton = None
		if(zeton == None):
			return token_list(request, 'Ta žeton ne obstaja!', 'alert-warning')
		else:
			'''context = {
				'data': {
					'vpisna': zeton.student,
					'prog': zeton.studijski_program,
					'letnik': zeton.letnik,
					'vrsta_vp': zeton.vrsta_vpisa,
					'nac_stud': zeton.nacin_studija,
					'vrst_stud': zeton.vrsta_studija,
					'izbira': zeton.pravica_do_izbire
				}
			}
			return render(request, 'token_edit.html', context)'''
			context = {}
			tokenForm = TokenForm(initial={
				'student': zeton.student.vpisna_stevilka,
				'studijski_program': zeton.studijski_program.id,
				'letnik': zeton.letnik.id,
				'vrsta_vpisa': zeton.vrsta_vpisa.id,
				'nacin_studija': zeton.nacin_studija.id,
				'vrsta_studija': zeton.vrsta_studija.id,
				'pravica_do_izbire': zeton.pravica_do_izbire})
			
			context['tokenForm'] = tokenForm
			
			return render(request, 'token_edit.html', context )

def all_data(request, id):
	student = Student.objects.get(pk = id)
	if(student.naslov_zacasno_bivalisce is None):
		student.naslov_zacasno_bivalisce = '/'
	print(student)
	vpisi = Vpis.objects.filter(student = student).order_by('-studijsko_leto').select_related()
	'''.values('studijsko_leto',\
								 'studijski_program', 'letnik', 'vrsta_vpisa', \
								 'nacin_studija', 'vrsta_studija')'''
	print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~",vpisi)
	
	context = {
		'student': student,
		'vpisi': vpisi
	}

	return render(request, 'student_data.html', context)
	
def student_data(request):
	

	if(request.user.groups.all()[0].name == "students"):
		student = Student.objects.get(email = request.user.email)
		vpisi = Vpis.objects.filter(student = student.vpisna_stevilka)
		print(vpisi)
		if(student.naslov_zacasno_bivalisce is None):
			student.naslov_zacasno_bivalisce = '/'
		context = {
			'student': student,
			'vpisi': vpisi
		}

		return render(request, 'student_data.html', context)

	else:
		return redirect('/student/')

def export_csv(request):
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="studenti.csv"'

	writer = csv.writer(response)
	all_students = Student.objects.values()
	all_students = sorted(all_students, key=lambda student: (  [alphabet.index(c) for c in student['priimek'].lower()], \
															   [alphabet.index(c) for c in student['ime'].lower()], \
															   [alphabet.index(c) for c in str(student['vpisna_stevilka'])]))
	writer.writerow(all_students[0].keys())

	for student in all_students:
		 writer.writerow(student.values())

	return response

def export_pdf(request):
	# Create the HttpResponse object with the appropriate PDF headers.
	response = HttpResponse(content_type='application/pdf')
	response['Content-Disposition'] = 'attachment; filename="studenti.pdf"'
	styles = getSampleStyleSheet()
	doc = SimpleDocTemplate(response, pagesize=landscape(A4))
	header = Paragraph('Tabela študentov na dan: ' + str(datetime.date.today()), styles['title'])
	elements = []
	all_students = Student.objects.values().order_by('priimek')
	all_students = sorted(all_students, key=lambda student: (  [alphabet.index(c) for c in student['priimek'].lower()], \
															   [alphabet.index(c) for c in student['ime'].lower()], \
															   [alphabet.index(c) for c in str(student['vpisna_stevilka'])]))
	k = list(all_students[0].keys())
	
	for l in range(len(k)):
		if len(k[l]) > 10:
			k[l] = k[l][:10] + ".."	
			

	data = [k]
	
	for student in all_students:
		 data.append(list(student.values()))
	LIST_STYLE = TableStyle([('INNERGRID', (0, 0), (-1, -1), 0.2, colors.black)])
	t=Table(data)
	t.setStyle(LIST_STYLE)
	elements.append(header)
	elements.append(t)

	doc.build(elements)
	return response

def potrdi_studente(request):
	if(request.user.groups.all()[0].name == "referent"):
		if request.method == 'POST' and 'potrdi_studenta' in request.POST:

			vpis_student_email = request.POST.get('vpis_email')
			
			for vpis in Vpis.objects.all():
				if str(vpis.student.email) == vpis_student_email:
					
					if vpis.potrjen == False:
						vpis.potrjen = True
						vpis.save()


	else:
		return HttpResponse("Nimaš dovoljenja.")

	all_vpis = Vpis.objects.all()
	potrjeni = []
	for vpis in all_vpis:
		if vpis.potrjen == False:
			potrjeni.append(vpis)
	
	context = {
		'arr': potrjeni
		}

	return render(request, 'potrdi_studente.html',context)

def preveri_seznam(request):

	if(request.user.groups.all()[0].name == "referent"):
		
		if request.method == 'POST' and 'natisni' in request.POST:
			
			vpis_student_email = request.POST.get('vpis_email')
			studijsko_leto_ime = request.POST.get('vpis_leto')

			return natisni_potrdilo(vpis_student_email,studijsko_leto_ime, 6)
			

		if request.method == 'POST' and 'prikaz_seznama' in request.POST:

			seznam = []
			for vpis in Vpis.objects.all():
				if vpis.potrjen == True:
					seznam.append(vpis)

			context = {
				'arr': seznam
				}

			return render(request, 'preveri_seznam.html',context)
	else:
		return HttpResponse("Nimaš dovoljenja.")

def naroci_potrdila(request):
	if request.method == 'POST' and 'naroci' in request.POST:
		studijsko_leto_ime = request.POST.get('studijsko_leto')
		st_potrdil = request.POST.get('st_potrdil')
		student = Student.objects.get(email = request.user.email)
		#print(student)
		#print(studijsko_leto_)
		vpis_ = Vpis.objects.filter(studijsko_leto__ime = studijsko_leto_ime, student = student.vpisna_stevilka)[0]
		print(vpis_)
		if st_potrdil:
			vpis_.st_narocenih_potrdil = st_potrdil
			vpis_.save()

	student = Student.objects.get(email = request.user.email)
	vpisi = Vpis.objects.filter(student = student.vpisna_stevilka)
	
def students_by_subject(request):

	if(request.user.groups.all()[0].name == "referent"):
		predmeti_list = Predmet.objects.all().order_by('ime')
	elif(request.user.groups.all()[0].name == "professors"):
		ucitelj = Ucitelj.objects.get(email=request.user.email)

		predmeti_list = ucitelj.predmeti.all()
		print(predmeti_list)
	else:
		return redirect('')

	leto = StudijskoLeto.objects.latest('id')

	if request.POST.get('izbrano-leto') != None:
		leto = StudijskoLeto.objects.get(ime=request.POST.get('izbrano-leto'))

	

	paginator = Paginator(predmeti_list, 24)
	page = request.GET.get('page')
	predmeti = paginator.get_page(page)
			
	leta = StudijskoLeto.objects.all()
	context = {
		'predmeti': predmeti,
		'leta': leta,
		'leto': leto
	}

	return render(request, 'all_subjects.html',context)

def subject_data(request, leto, id):

	predmet = Predmet.objects.get(id=id)

	leto = StudijskoLeto.objects.get(id=leto)		

	predmetiStudenta = PredmetiStudenta.objects.all()

	student_list = []


	for pr in predmetiStudenta:
		if pr.vpis.studijsko_leto==leto and pr.vpis.potrjen :
			for p in pr.predmeti.all():
				if p == predmet:
					student_list.append(pr.vpis)

	
	student_list = sorted(student_list, key=lambda x: ([alphabet.index(c) for c in x.student.priimek.lower()], \
																	   [alphabet.index(c) for c in x.student.ime.lower()], \
																	   [alphabet.index(c) for c in str(x.student.vpisna_stevilka)]))
	paginator = Paginator(student_list, 15)
	page = request.GET.get('page')
	students = paginator.get_page(page)

	#naredi pdf tabelo vpisanih študentov v predmet
	if request.method == "POST":
		naredi_predmet_pdf(predmet, leto, student_list)

		name = str(predmet.id) +'.pdf'
		fs = FileSystemStorage('/tmp')
		with fs.open(name) as pdf:
			response = HttpResponse(pdf, content_type='application/pdf')
			response['Content-Disposition'] = 'attachment; filename="'+ name+' "'
			return response

	context = {
		'predmet': predmet,
		'students': students,
		'leto': leto
	}

	return render(request, 'subject.html',context)

def natisni_potrdila(request): # dodaj se da izbrise stevilo narocenih potrdil.
	if request.method == 'POST' and 'natisni' in request.POST:
		st_potrdil = request.POST.get('st_potrdil_')
		email_ = request.POST.get('email_')
		stud_leto = request.POST.get('stud_leto')
		print(email_)
		print(stud_leto)
		print(st_potrdil)

		return natisni_potrdilo(email_,stud_leto,st_potrdil)

	vpisi = Vpis.objects.filter(~Q(st_narocenih_potrdil = 0))
	context= {
		'vpisi': vpisi
		}

	return render(request, 'natisni_potrdila.html',context)

def natisni_potrdilo(vpis_student_email, studijsko_leto_ime, st_potrdil):
	print(studijsko_leto_ime)
	vpis_ = Vpis.objects.filter(student__email = vpis_student_email, studijsko_leto__ime = studijsko_leto_ime)[0]
	print(vpis_)

	response = HttpResponse(content_type='application/pdf')
	response['Content-Disposition'] = 'inline; filename="studenti.pdf"'
			
	doc = SimpleDocTemplate(response,pagesize=letter,
				rightMargin=72,leftMargin=72,
				topMargin=72,bottomMargin=18)
	Story=[]
	logo = "student/Logo_UL_FRI.png"
	magName = "Pythonista"
	issueNum = 12
	subPrice = "99.00"


	formatted_time = datetime.date.today()
	formatted_time = str(formatted_time)
	tabela = formatted_time.split("-")
	formatted_time = tabela[2] + "." + tabela[1] + "." + tabela[0]
	full_name = vpis_.student.ime + " " +  vpis_.student.priimek 
	address_parts = vpis_.student.naslov_stalno_bivalisce.split(",")
 
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
 
	# Create return address
	ptext = '<font size=12>%s</font>' % full_name
	par = Paragraph(ptext, p)
	Story.append(par)
	for part in address_parts:
		ptext = '<font size=12>%s</font>' % part.strip()
		par = Paragraph(ptext, p)
		Story.append(par)
			
	Story.append(Spacer(1, 50))

	text = "POTRDILO O VPISU"
	ptext = '<font size=13>%s</font>' % text
	par = Paragraph(ptext, p2)
	Story.append(par)
	Story.append(Spacer(1, 20))
 
	ptext = '<font size=12>Vpisna številka : %d <br/>Priimek, ime: %s, %s<br/>Država rojstva: %s<br/>Študijsko leto: %s<br/>Vrsta vpisa: %s<br/>Način in oblika študija: %s<br/>Letnik,dodatno leto: %s<br/>Študijski program: %s<br/>Vrsta in stopnja študija: %d %s</font>' % (vpis_.student.vpisna_stevilka,vpis_.student.priimek,vpis_.student.ime,vpis_.student.drzava_rojstva.slovenski_naziv,vpis_.studijsko_leto.ime,vpis_.vrsta_vpisa.opis,vpis_.nacin_studija.opis,vpis_.letnik.ime,vpis_.studijski_program.naziv,vpis_.studijski_program.id,vpis_.studijski_program.stopnja)
	par = Paragraph(ptext, p)
	Story.append(par)
	Story.append(Spacer(1, 48))
			
			
	ptext = '<font size=12>prof. dr. Bojan Orel, dekan</font>'
	par = Paragraph(ptext, p1)
	Story.append(par)
	Story.append(Spacer(1, 12))
	Story.append(PageBreak())


	add_story = int(st_potrdil)*Story

	doc.build(add_story)
	return response


def students_by_number(request):


	leto = StudijskoLeto.objects.latest('id')
	program = StudijskiProgram.objects.get(id=1000468)
	letnik = Letnik.objects.get(ime="1.")

	if request.POST.get('izbrano-leto') != None:
		leto = StudijskoLeto.objects.get(ime=request.POST.get('izbrano-leto'))

	if request.POST.get('izbran-program') != None:
		program = StudijskiProgram.objects.get(naziv=request.POST.get('izbran-program'))

	if request.POST.get('izbran-letnik') != None:
		letnik = Letnik.objects.get(ime=request.POST.get('izbran-letnik'))


	predmetnik_list = Predmetnik.objects.filter(studijski_program=program, studijsko_leto=leto, letnik=letnik).values('predmet')

	predmeti_list=[]
	for p in predmetnik_list:
		predmeti_list.append(p['predmet'])

	predmeti_list=Predmet.objects.filter(id__in=predmeti_list).order_by('ime').values()

	predmetiStudenta = PredmetiStudenta.objects.all()

	student_list = []

	predmeti_number = [0] * predmeti_list.count()

	#prestej predmete
	for pr in predmetiStudenta:
		if pr.vpis.studijsko_leto==leto and pr.vpis.studijski_program==program and pr.vpis.letnik==letnik and pr.vpis.potrjen :
			for p in pr.predmeti.all():
				for i, p2 in enumerate(predmeti_list):
					if p.ime == p2['ime']:
						predmeti_number[i]+=1
						break

	for i, p in enumerate(predmeti_list):
		p['number'] = predmeti_number[i]


	#PDF		

	if request.POST.get("save_pdf"):
		naredi_stevilo_pdf(leto, letnik, program, predmeti_list)
		name = str(program.id) +'.pdf'
		fs = FileSystemStorage('/tmp')
		with fs.open(name) as pdf:
			response = HttpResponse(pdf, content_type='application/pdf')
			response['Content-Disposition'] = 'attachment; filename="'+ name+' "'
			return response
	
	#pages
	paginator = Paginator(predmeti_list, 40)
	page = request.GET.get('page')
	predmeti = paginator.get_page(page)
			
	leta = StudijskoLeto.objects.all()
	programi = StudijskiProgram.objects.all()
	letniki = Letnik.objects.all()

	context = {
		'predmeti': predmeti,
		'numbers': predmeti_number,
		'leta': leta,
		'leto': leto,
		'programi': programi,
		'program': program,
		'letniki': letniki,
		'letnik': letnik
	}

	return render(request, 'all_subjects_number.html',context)

def naredi_predmet_pdf(predmet, leto, student_list):
	
	context = {
	   'predmet' : predmet,
	   'leto' : leto,
	   'students': student_list,
	}

	options = {
    	'page-size': 'A4',
        'dpi': 600,
        '--footer-right': '[page]',
	}

	html_string =  render_to_string('pdf_predmet.html',context)
	pdfkit.from_string( html_string,'/tmp/'+ str(predmet.id) + '.pdf', options=options)
	return

def naredi_stevilo_pdf(leto, letnik, program, predmeti):
	
	context = {
	   'leto': leto,
	   'program': program,
	   'letnik': letnik,
	   'predmeti': predmeti
	}

	options = {
    	'page-size': 'A4',
        'dpi': 600,
        '--footer-right': '[page]',
	}

	html_string =  render_to_string('pdf_stevilo.html',context)
	pdfkit.from_string( html_string,'/tmp/'+ str(program.id) + '.pdf', options=options)
	return

def naredi_predmet_csv(request, leto, id):

	predmet = Predmet.objects.get(id=id)

	leto = StudijskoLeto.objects.get(id=leto)		

	predmetiStudenta = PredmetiStudenta.objects.all()

	student_list = []


	for pr in predmetiStudenta:
		if pr.vpis.studijsko_leto==leto and pr.vpis.potrjen :
			for p in pr.predmeti.all():
				if p == predmet:
					student_list.append(pr.vpis)

	
	student_list = sorted(student_list, key=lambda x: ([alphabet.index(c) for c in x.student.priimek.lower()], \
																	   [alphabet.index(c) for c in x.student.ime.lower()], \
																	   [alphabet.index(c) for c in str(x.student.vpisna_stevilka)]))
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="studenti.csv"'
	response.write(codecs.BOM_UTF8)

	writer = csv.writer(response)

	writer.writerow([str(predmet)])
	writer.writerow([str(leto)])
	writer.writerow(['#', 'Priimek', 'Ime', 'Vpisna številka', "Email", "Vrsta vpisa"])

	for num, student in enumerate(student_list):
		 writer.writerow([str(num), student.student.priimek, 
		 	student.student.ime, 
		 	student.student.vpisna_stevilka, student.student.email, 
		 	str(student.vrsta_vpisa)])

	return response

def naredi_stevilo_csv(request, leto, program, letnik):

	leto = StudijskoLeto.objects.get(id=leto)
	program = StudijskiProgram.objects.get(id=program)
	letnik = Letnik.objects.get(id=letnik)


	predmetnik_list = Predmetnik.objects.filter(studijski_program=program, studijsko_leto=leto, letnik=letnik).values('predmet')

	predmeti_list=[]
	for p in predmetnik_list:
		predmeti_list.append(p['predmet'])

	predmeti_list=Predmet.objects.filter(id__in=predmeti_list).order_by('ime').values()

	predmetiStudenta = PredmetiStudenta.objects.all()

	student_list = []

	predmeti_number = [0] * predmeti_list.count()

	#prestej predmete
	for pr in predmetiStudenta:
		if pr.vpis.studijsko_leto==leto and pr.vpis.studijski_program==program and pr.vpis.letnik==letnik and pr.vpis.potrjen :
			for p in pr.predmeti.all():
				for i, p2 in enumerate(predmeti_list):
					if p.ime == p2['ime']:
						predmeti_number[i]+=1
						break

	for i, p in enumerate(predmeti_list):
		p['number'] = predmeti_number[i]

	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="stevilo_studentov.csv"'
	response.write(codecs.BOM_UTF8)

	writer = csv.writer(response)

	writer.writerow([str(program)])
	writer.writerow([str(leto)])
	writer.writerow([str(letnik) + "letnik"])

	for num, p in enumerate(predmeti_list):
		 writer.writerow([str(num), str(p['id']), str(p['ime']), str(p['number'])])


	return response



