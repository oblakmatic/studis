from django.shortcuts import render_to_response, render, redirect
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.template.context_processors import csrf
import datetime
from student.models import *
from sifranti.models import *
from student.forms import *

max_attempts = 6
attempts = 0
ip = -1
block_time = datetime.datetime.now() - datetime.timedelta(minutes=1)


def home_view(request):

	if request.user.is_authenticated:
		return render(request, 'home.html')

	return HttpResponseRedirect('/user/login')

def login(request):
	
	#check if ip is blocked 
	print(attempts)
	if is_blocked(request):
		return HttpResponseRedirect('/user/invalid')


	c = {}
	c.update(csrf(request))
	c.update({'error': attempts > 0 })
	return render_to_response('login.html', c)

#checks if usr and pwd are correct and logs in
#else +1 to attempts
def auth_view(request):
	username = request.POST.get('usr', '')
	password = request.POST.get('pwd', '')
	user = auth.authenticate(username=username, password=password)
	global attempts
	attempts = attempts + 1

	if user is not None and attempts<max_attempts:

		auth.login(request, user)
		attempts=0
		return HttpResponseRedirect('/')
	else:
		if attempts == max_attempts: 
			global ip
			ip = get_client_ip(request)

			#block ip for 1 minute
			global block_time
			block_time = datetime.datetime.now() + datetime.timedelta(minutes=1)
			return HttpResponseRedirect('/user/invalid')

		context = {}
		context.update(csrf(request))
		context.update({'error': 'True'})
		context.update({'attempts': attempts})
		return HttpResponseRedirect('/user/login')


def logout(request):
	auth.logout(request)
	return HttpResponseRedirect('/user/login')

#if ip is blocked redirect here
def invalid(request):
	print("attempts %d", attempts)
	if attempts < max_attempts:
		return HttpResponseRedirect('/user/login')
	else:
		context = {'ip': ip}
		return render_to_response('invalid.html', context )


def get_client_ip(request):
	x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
	if x_forwarded_for:
		ip = x_forwarded_for.split(',')[0]
	else:
		ip = request.META.get('REMOTE_ADDR')
	return ip

#checks if ip is being blocked
def is_blocked(request):
	global attempts
	if attempts < max_attempts:
		return False

	now = datetime.datetime.now()

	global ip

	print(block_time-now)
	#unblock
	if now > block_time:
		attempts=0
		ip = -1
		print("true")
		return False

	return True

def vzdr_pred(request, _program, _leto, _letnik):

	program = StudijskiProgram.objects.get(id=_program)
	leto = StudijskoLeto.objects.get(id=_leto)
	letnik = Letnik.objects.get(id=_letnik)

	if request.POST.get('izbrano-leto') != None:
		leto = StudijskoLeto.objects.get(ime=request.POST.get('izbrano-leto'))

	if request.POST.get('izbran-program') != None:
		program = StudijskiProgram.objects.get(naziv=request.POST.get('izbran-program'))

	if request.POST.get('izbran-letnik') != None:
		letnik = Letnik.objects.get(ime=request.POST.get('izbran-letnik'))

	if request.method == "POST" and (request.POST.get('izbrano-leto') != None or 
		request.POST.get('izbran-program') != None or
		request.POST.get('izbran-letnik') != None):
		print("redirecting")
		return redirect("/predmetnik/"+str(program.id)+"/"+str(leto.id)+"/"+str(letnik.id)+"/")

	predmeti_obvezni = []
	predmeti_izbirni = []
	predmeti_modul = []
	#za imena modulov in
	temporary = []

	#1
	if letnik == Letnik.objects.get(ime="1."):
	
		predmetniki = Predmetnik.objects.filter(studijski_program=program, studijsko_leto=leto, letnik=letnik)
		
		for p in predmetniki:
			if  p.obvezen:
				predmeti_obvezni.append(p.predmet)



	#2 letnik
	elif letnik == Letnik.objects.get(ime="2."):
	
		predmetniki = Predmetnik.objects.filter(studijski_program=program, studijsko_leto=leto, letnik=letnik)
		
		for p in predmetniki:
			if  p.obvezen:
				predmeti_obvezni.append(p.predmet)

			else:
				temporary.append(p.strokoven)
				predmeti_izbirni.append(p.predmet)

	#3 letnik
	else:
	
		predmetniki = Predmetnik.objects.filter(studijski_program=program, studijsko_leto=leto, letnik=letnik, modul=None)
		
		for p in predmetniki:
			if  p.obvezen:
				predmeti_obvezni.append(p.predmet)

			else:
				predmeti_izbirni.append(p.predmet)
				

		moduls = Modul.objects.filter(studijsko_leto=leto, studijski_program=program)
	

		for m in moduls:
			temporary.append(m.ime)
			pr = Predmetnik.objects.filter(modul=m, studijsko_leto=leto, studijski_program=program)
			temp=[]
			for p in pr:
				temp.append(p.predmet)

		
			predmeti_modul.append(temp)

	leta = StudijskoLeto.objects.all()
	programi = StudijskiProgram.objects.all()
	letniki = Letnik.objects.all()

	data= {'studijski_program': program, 'studijsko_leto': leto, 'letnik': letnik}

	form = PredmetnikForm(leto, program, initial=data)

	context = {
		'predmeti_o': predmeti_obvezni,
		'predmeti_i': zip(predmeti_izbirni, temporary),
		'predmeti_m': zip(predmeti_modul, temporary),
		'letnik': letnik,
		'leto': leto,
		'program': program,
		'leta': leta,
		'programi': programi,
		'letniki': letniki,
		'form': form
		

	}

		
	return render(request, 'vzdr_pred.html', context)

def del_pred(request, _program, _leto, _letnik, predmet):
	predmetnik = Predmetnik.objects.get(studijski_program=_program, 
		studijsko_leto=_leto, letnik=_letnik, predmet=predmet).delete()

	return redirect("/predmetnik/"+str(_program)+"/"+str(_leto)+"/"+str(_letnik)+"/")

def add_pred(request, _program, _leto, _letnik):
	leto = StudijskoLeto.objects.get(id=_leto)
	program = StudijskiProgram.objects.get(id=_program)
	form = PredmetnikForm(leto, program, request.POST)
	if form.is_valid():
		form.save()
	return redirect("/predmetnik/"+str(_program)+"/"+str(_leto)+"/"+str(_letnik)+"/")


