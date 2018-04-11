from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django import forms

# Create your views here.
from .forms import *
from student.models import Vpis



def index_vpis(request):

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        
        # example Posta --> PostaForm

        possible_student = vrniStudenta(request.user.email)
        form = VpisForm(request.POST)
        

        # check whether it's valid:
        # and saves into database
        if form.is_valid():

            st = form.save(commit=False)
            st.student = possible_student[0]
            st.save()
            context = {
            'form': form,
            'possible_student' : possible_student,
            'opozorilo' : "Uspešno dodan Vpis!"
            }
            return render(request,'vpis/index_vpis.html',context)
        else:
            context = {
            'form': form,
            'possible_student' : possible_student
            }
            return render(request,'vpis/index_vpis.html',context)

    # if a GET (or any other method) we'll create a blank form
    else:
        opozorilo = None
        form = None
        possible_student = vrniStudenta(request.user.email)

        if possible_student:
            zeton = Zeton.objects.filter(student=possible_student[0])

            if zeton:
                form = VpisForm()
                opozorilo = ""
            else:
                opozorilo="Nimaš žetona"
            

        context = {
                'form': form,
                'possible_student' : possible_student.values(),
                'opozorilo' : opozorilo
                }
        
        return render(request,'vpis/index_vpis.html',context)

            

        



# naredi query po studentu z emailom
def vrniStudenta(njegovEmail):
    student = Student.objects.filter(email=njegovEmail)
    return student

