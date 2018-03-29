from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.template.context_processors import csrf
from django.contrib.auth.models import User
import datetime

attempts = 0
ip = -1
block_time = datetime.datetime.now() - datetime.timedelta(minutes=1)

def login(request):
	
	#check if ip is blocked 
	print(attempts)
	if attempts >=3:
		is_blocked(request)

	c = {}
	c.update(csrf(request))
	c.update({'error': attempts > 0 })
	return render_to_response('login.html', c)

#checks if usr and pwd are correct and logs in
def auth_view(request):
	username = request.POST.get('usr', '')
	password = request.POST.get('pwd', '')
	user = auth.authenticate(username=username, password=password)
	global attempts
	attempts = attempts + 1

	if user is not None:

		auth.login(request, user)
		attempts=0
		return HttpResponseRedirect('/')
	else:
		if attempts == 3: 
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
	if attempts < 3:
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
	now = datetime.datetime.now()
	global ip
	global attempts

	print(block_time-now)
	#unblock
	if now >= block_time:
		attempts=0
		ip = -1
		print("true")

	#block
	else:
		print("false")
		context = {'ip': ip}
		return render_to_response('invalid.html', context)



