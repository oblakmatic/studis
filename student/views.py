from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from student.models import Student, Zeton, Vpis
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
	content = request.FILES['students'].read().decode('utf-8')

	str_size = 127
	arr = []
	for i in range(0, len(content), 127):
		data = content[i:i+127];
	
		
		name = data[0:30].rstrip()
		surname = data[30:60].rstrip()
		program = data[60:67]
		email = data[67:].rstrip()

		student = None
		try:
			student = Student.objects.get(email=email)
			student.ime = name
			student.priimek = surname
			student.save()
		except Student.DoesNotExist:
			serial = Student.objects.count()+1
			year = datetime.datetime.today().year % 2000
			vpisna = "63"+ str(year) + format(serial, '04d')
			student = Student.objects.create(vpisna_stevilka=int(vpisna))
			student.email = email
			student.ime = name
			student.priimek = surname
			student.save()



		password = "adminadmin" #User.objects.make_random_password()
		username = email[:6]


		user, created2 = User.objects.get_or_create(username=username, email=email)
		user.first_name = name
		user.last_name = surname
		
		if created2:
			user.set_password(password)
			user.is_staff=False
			user.is_superuser=False
			students_group, status = Group.objects.get_or_create(name='students') 
			students_group.user_set.add(user)

		user.save()

		temp=[]
		temp.append(str(i//127 +1))
		temp.append(surname)
		temp.append(name)
		temp.append(student.vpisna_stevilka)
		temp.append(username)
		temp.append(password)
		

		arr.append(temp)
	


	context = {
		'length': len(arr),
		'students':arr
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

def token_add(request, id):
	if request.method == 'POST':
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
		vpisi = Vpis.objects.select_related().filter(student__pk = id).order_by('-pk')
		print(vpisi)

		context = {
			'id': id
		}
		
		if(vpisi.count() > 0):
			data = {}
			data['prog'] = vpisi[0].studijski_program.ime
			data['letnik'] = '2.' if vpisi[0].letnik.ime == '1.' else '3.'  
			data['vrsta_vp'] = vpisi[0].vrsta_vpisa.ime
			data['nac_stud'] = vpisi[0].nacin_studija
			data['vrst_stud'] = vpisi[0].vrsta_studija
			context['data'] = data
		
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
