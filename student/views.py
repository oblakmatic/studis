from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from student.models import Student
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

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
