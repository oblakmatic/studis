from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from student.models import Student, Zeton
from sifranti.models import *
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
import csv
from reportlab.pdfgen import canvas
from reportlab.platypus import *
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter, A4, landscape
from reportlab.lib import colors 

# Create your views here.
def upload_file(request):

    return render(request,'import_students.html')

def students(request):
	all_students = Student.objects.values('id', 'ime', 'priimek', 'email')
	context = {
		'arr': all_students
	}
	return render(request,'students.html', context)

def import_students(request):
	content = request.FILES['students'].read().splitlines()

	arr = []
	for i in range(0, len(content), 4):
		name = content[i].decode('utf-8')
		surname = content[i+1].decode('utf-8')
		program = content[i+2].decode('utf-8')
		email = content[i+3].decode('utf-8')

		student = Student(ime=name, priimek=surname, email=email)
		student.save()
		password = "adminadmin"#User.objects.make_random_password()
		username = surname+str(student.id)

		user = User.objects.create_user(username=username,
                                 email=email,
                                 password=password,
                                 is_staff=False,
                                 is_superuser=False)


		students_group, status = Group.objects.get_or_create(name='students') 
		students_group.user_set.add(user)

		temp=[]
		temp.append(name)
		temp.append(surname)
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
			context = {
				'message': 'Žeton uspešno dodan!'
			}
			return token_list(request, context)
	else:
		context = {
			'id': id
		}
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
			'student': token.student.id,
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

		context = {
			'message': 'Žeton uspešno urejen!'
		}

		return redirect('/student/seznam-zetonov/', context)

	else:
		try:
			zeton = Zeton.objects.select_related().get(pk=edit_id)
		except Zeton.DoesNotExist:
			zeton = None
		if(zeton == None):
			context = {
				'message': 'Ta žeton ne obstaja!'
			}
			return redirect('/student/seznam-zetonov/', context)
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

	doc = SimpleDocTemplate(response, pagesize=landscape(A4))
	
	elements = []
	all_students = Student.objects.values()
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
	elements.append(t)

	doc.build(elements)
	return response