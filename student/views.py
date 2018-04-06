from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from student.models import Student


def add_student(request):

    if(request.POST.get('stud') and request.POST.get('stud_prog') and   )

