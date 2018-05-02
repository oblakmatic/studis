from django.shortcuts import render_to_response, render
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.template.context_processors import csrf
import datetime

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



