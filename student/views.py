from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from student.models import Student, Zeton, Vpis, Kandidat
from sifranti.models import *
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
import csv
import datetime
from reportlab.pdfgen import canvas
from reportlab.platypus import *
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter, A4, landscape
from reportlab.lib import colors 

import time
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from student.forms import TokenForm

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
pdfmetrics.registerFont(TTFont('Vera', 'Vera.ttf'))


# Create your views here.
def upload_file(request):

	return render(request,'import_students.html')

def students(request):
	all_students = Student.objects.values('priimek', 'ime', 'vpisna_stevilka', 'email').order_by('priimek')
	context = {
		'arr': all_students
	}
	return render(request,'students.html', context)

def import_students(request):
	content = request.FILES['students'].read().splitlines()

	arr = []
	updated = 0
	new = 0
	for i in range(0, len(content)):
		data = content[i].decode('utf-8');
		
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
	id_filtered_students = Student.objects.values('id', 'ime', 'priimek', 'email').filter(id__startswith=search_query)
	# print(id_filtered_students)
	name_filtered_students = Student.objects.values('id', 'ime', 'priimek', 'email').filter(ime__startswith=search_query)
	surname_filtered_students = Student.objects.values('id', 'ime', 'priimek', 'email').filter(priimek__startswith=search_query)
	context = {
		'students_id': id_filtered_students,
		'students_name': name_filtered_students,
		'students_surname': surname_filtered_students
	}
	'''
	else:
		id_filtered_students = Student.objects.values('id', 'ime', 'priimek', 'email')
		name_filtered_students = Student.objects.values('id', 'ime', 'priimek', 'email')
		surname_filtered_students = Student.objects.values('id', 'ime', 'priimek', 'email')
		context = {
			'students_id': id_filtered_students,
			'students_name': name_filtered_students,
			'students_surname': surname_filtered_students
		}
	'''
	return render(request,'search.html', context)

def token_add(request):
	if request.method == 'POST':
		print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ pridemo do posta ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
		student = Student.objects.filter(id=request.POST.get('stud'))
		program = StudijskiProgram.objects.filter(ime=request.POST.get('stud_prog'))
		letnik = Letnik.objects.filter(ime=request.POST.get('letnik'))
		vrsta_vpisa = VrstaVpisa.objects.filter(ime=request.POST.get('vrsta_vpisa'))
		nacin_studija = NacinStudija.objects.filter(ime=request.POST.get('nac_stud'))
		vrsta_studija = VrstaStudija.objects.filter(ime=request.POST.get('vrst_stud'))
		prosta_izbira = request.POST.get('predmet_choice', False)

		if prosta_izbira == 'on':
			prosta_izbira = True

		data = {
			'student': student,
			'program': program,
			'letnik': letnik,
			'vrsta_vpisa': vrsta_vpisa,
			'nacin_studija': nacin_studija,
			'prosta_izbira': prosta_izbira
		}
		# print(data)
		if(student.count() != 1 or program.count() != 1 or letnik.count() != 1 or vrsta_vpisa.count() != 1 or nacin_studija.count() != 1):
			context = {
				'message': 'Prosimo, vnesite vse zahtevane podatke!'
			}
			return render(request, 'token_add.html', context)
		

		else:
			
			if Zeton.objects.filter(student=student[0]).count() >= 2:
				context = {
					'message': 'Student že ima 2 žetona!'
				}
				return render(request, 'token_add.html', context)
			zeton = Zeton(student=student[0], studijski_program=program[0], letnik=letnik[0], vrsta_vpisa=vrsta_vpisa[0], nacin_studija=nacin_studija[0], vrsta_studija=vrsta_studija[0], pravica_do_izbire=prosta_izbira)
			zeton.save()
			return token_list(request, 'Žeton uspešno dodan!')
	else:
		# vpisi = Vpis.objects.select_related().filter(student__pk = id).order_by('-pk')
		# print(vpisi)

		# context = {
		# 	'id': id
		# }
		context =  {}
		tokenForm = TokenForm()
		context['tokenForm'] = tokenForm
		'''if(vpisi.count() > 0):
			data = {}
			data['prog'] = vpisi[0].studijski_program.ime
			data['letnik'] = '2.' if vpisi[0].letnik.ime == '1.' else '3.'  
			data['vrsta_vp'] = vpisi[0].vrsta_vpisa.ime
			data['nac_stud'] = vpisi[0].nacin_studija
			data['vrst_stud'] = vpisi[0].vrsta_studija
			context['data'] = data'''
		
		return render(request, 'token_add.html', context )

def token_list(request, msg=None):
	all_tokens = Zeton.objects.select_related()
	zetoni = []
	for token in all_tokens:
		# print(token)
		# print(token.student)
		# print(dir(token))
		zeton = {
			'id': token.pk,
			'student': token.student.pk,
			'studijski_program': token.studijski_program.ime,
			'letnik': token.letnik.ime,
			'vrsta_vpisa': token.vrsta_vpisa.ime,
			'nacin_studija': token.nacin_studija.ime,
			'vrsta_studija': token.vrsta_studija.ime,
			'pravica_do_izbire': 'DA' if token.pravica_do_izbire else 'NE' if token.letnik.ime == '3.' else '/'
		}
		zetoni.append(zeton)
	# print(all_tokens)
	context = {
		'arr': zetoni
	}
	if (not msg is None):
		context['message'] = msg
	return render(request,'token_list.html', context)

def token_delete(request, del_id):
	try:
		zeton = Zeton.objects.get(pk=del_id)
		print(zeton)
	except Zeton.DoesNotExist:
		zeton = None
	if(zeton == None):
		return token_list(request, 'Ta žeton ne obstaja!')
	else:
		zeton.delete()
		return token_list(request, 'Žeton uspešno izbrisan!')

def token_edit(request, edit_id):
	print(request.method)
	if request.method == 'POST':
		# print(request.POST)
		token = Zeton.objects.get(pk=edit_id)
		# print('neurejeni token')
		# print(token.studijski_program)
		token.studijski_program = StudijskiProgram.objects.filter(ime=request.POST.get('stud_prog'))[0]
		token.letnik = Letnik.objects.filter(ime=request.POST.get('letnik'))[0]
		token.vrsta_vpisa = VrstaVpisa.objects.filter(ime=request.POST.get('vrsta_vpisa'))[0]
		token.nacin_studija = NacinStudija.objects.filter(ime=request.POST.get('nac_stud'))[0]
		token.vrsta_studija = VrstaStudija.objects.filter(ime=request.POST.get('vrst_stud'))[0]
		token.prosta_izbira = True if request.POST.get('predmet_choice') == 'on' else False
		token.save()
		# print('urejeni token')
		# print(token.program)


		return redirect('/student/seznam-zetonov/', 'Žeton uspešno urejen!')

	else:
		try:
			zeton = Zeton.objects.select_related().get(pk=edit_id)
		except Zeton.DoesNotExist:
			zeton = None
		if(zeton == None):
			return redirect('/student/seznam-zetonov/', 'Ta žeton ne obstaja!')
		else:
			context = {
				'data': {
					'vpisna': zeton.student.pk,
					'prog': zeton.studijski_program.ime,
					'letnik': zeton.letnik.ime,
					'vrsta_vp': zeton.vrsta_vpisa.ime,
					'nac_stud': zeton.nacin_studija.ime,
					'vrst_stud': zeton.vrsta_studija.ime,
					'izbira': zeton.pravica_do_izbire
				}
			}
			return render(request, 'token_edit.html', context)

def all_data(request, id):
	student = Student.objects.get(pk = id)
	vpisi = Vpis.objects.filter(student = student)
	# if student.naslov_zacasno_bivalisce == '':
	# 	student.naslov_stalno_bivalisce = student.naslov_zacasno_bivalisce
	
	context = {
		'student': student,
		'vpisi': vpisi
	}

	return render(request, 'student_data.html', context)
	
def export_csv(request):
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="studenti.csv"'

	writer = csv.writer(response)
	all_students = Student.objects.values()
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
			vpis_ = None
			for vpis in Vpis.objects.all():
				if str(vpis.student.email) == vpis_student_email:
					vpis_ = vpis


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
			full_name = vpis_.student.ime + " " +  vpis_.student.priimek 
			address_parts = vpis_.student.naslov_stalno_bivalisce.split(",")
 
			im = Image(logo, 2*inch, 2*inch)
			Story.append(im)
			
			styles=getSampleStyleSheet()
			styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
			p = ParagraphStyle('MyNormal',parent=styles['Normal'], fontName='Vera')
			ptext = '<font size=12>%s</font>' % formatted_time
			par = Paragraph(ptext, p)
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
			
			Story.append(Spacer(1, 12))
			ptext = '<font size=12>POTRDILO O VPISU</font>'
			par = Paragraph(ptext, p)
			Story.append(par)
			Story.append(Spacer(1, 12))
 
			ptext = '<font size=12>Vpisna številka : %d <br/>Priimek, ime: %s, %s<br/>Država rojstva: %s<br/>Študijsko leto: %s<br/>Vrsta vpisa: %s<br/>Način in oblika študija: %s<br/>Letnik,dodatno leto: %s<br/>Študijski program: %s<br/>Vrsta in stopnja študija: %d %s</font>' % (vpis_.student.vpisna_stevilka,vpis_.student.priimek,vpis_.student.ime,vpis_.student.drzava_rojstva.slovenski_naziv,vpis_.studijsko_leto.ime,vpis_.vrsta_vpisa.opis,vpis_.nacin_studija.opis,vpis_.letnik.ime,vpis_.studijski_program.naziv,vpis_.studijski_program.id,vpis_.studijski_program.stopnja)
			par = Paragraph(ptext, p)
			Story.append(par)
			Story.append(Spacer(1, 48))
 
 
			ptext = '<font size=12>prof. dr. Bojan Orel<br/>dekan</font>'
			par = Paragraph(ptext, p)
			Story.append(par)
			Story.append(Spacer(1, 12))

			
			
			doc.build(Story)
			return response

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