from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader

# Create your views here.
from .forms import *
from student.models import Vpis



def index(request):

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        
        # example Posta --> PostaForm

        possible_student = vrniStudenta(request.user.email)
        form = VpisForm(request.POST)
        

        # check whether it's valid:
        # and saves into database
        if form.is_valid():

            vpis = form.save(commit=False)
            vpis.student = possible_student[0]
            vpis.save()
            #student requesta stran, naredim query po njegovem emailu
            
            
            return HttpResponseRedirect('/vpis/')
        else:
            print("NI SAFE")

    # if a GET (or any other method) we'll create a blank form
    else:
        
        
        #print(student[0]["id"])
        form = VpisForm()
        context = {
        'form': form,
        }
        return render(request,'vpis/index.html',context)



# naredi query po studentu z emailom
def vrniStudenta(njegovEmail):
    student = Student.objects.filter(email=njegovEmail)
    return student

