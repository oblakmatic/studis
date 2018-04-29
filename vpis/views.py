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



        
        if is_kandidat(request.user.email):
            form = VpisForm(request.POST)
        else:




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
        opozorilo = ""
        form = None
        context = None
        #preveri kdo je 
        #p = VpisForm()
        #print(p)
        
        # preveri ce je student 
        if is_kandidat(request.user):
            kandidat = vrniKandidata(request.user.email)
            studentform = None

            form = VpisForm()
            id_kandidata = kandidat[0].vpisna_stevilka
            data = Kandidat.objects.filter(pk= id_kandidata).values()[0]
            studentform = NameStudentForm(initial= data)
            #kandidat 
            context = {
                'form': form,
                'student' : kandidat[0],
                'opozorilo' : opozorilo,
                'studentform' : studentform
                }


        elif is_student(request.user):
            najden_student = vrniStudenta(request.user.email)

            # Preveri, da se lahko vpiše samo študent, ki ima žeton ali je novinec. 
            zeton =  Zeton.objects.filter(student = najden_student[0])
            studentform = None

            if zeton:
                form = VpisForm()
                opozorilo = ""
                id_studenta = najden_student[0].vpisna_stevilka
                data = Student.objects.filter(pk= id_studenta).values()[0]
                data_2 = {
                    'drzava' : najden_student[0].drzava,
                    'posta' : najden_student[0].posta,
                    'obcina' : najden_student[0].obcina,
                 } 
                data = {**data , **data_2}
                #print({**data , **data_2})

                studentform = NameStudentForm(initial= data)
            else:
                opozorilo= "Nimaš žetona"
            
            context = {
                'form': form,
                'student' : najden_student[0],
                'opozorilo' : opozorilo,
                'studentform' : studentform
                }
        else:
            opozorilo="Samo študenti se lahko vpišejo"
            context = {
                    'form': form,
                    'opozorilo' : opozorilo,
                    }
        
        return render(request,'vpis/index_vpis.html',context)

# naredi query po studentu z emailom
def vrniStudenta(njegovEmail):
    student = Student.objects.filter(email=njegovEmail)
    
    if student:
        return student
    else:
        raise Exception('Ni bilo studenta v tabeli')

def vrniKandidata(njegovEmail):
    kandidat = Kandidat.objects.filter(email=njegovEmail)
    
    if kandidat:
        return kandidat
    else:
        raise Exception('Ni bilo studenta v tabeli')

def is_student(user):
    return user.groups.filter(name='students').exists()

def is_kandidat(user):
    #return Kandidat.objects.filter(email=user.email).exists()
    return user.groups.filter(name='candidates').exists()
def emso_verify(emso):
        """
        vnesi emso v stringu in ce dobis rez. isti kot emso je emso kul
        Accepts an iterable of at least 12 digits and returns the number
        as a 13 digit string with a valid 13th control digit.
        Details about computation in
        http://www.uradni-list.si/1/objava.jsp?urlid=19998&stevilka=345
        """
        emso_factor_map = [7, 6, 5, 4, 3, 2, 7, 6, 5, 4, 3, 2]
        emso_digit_list = [int(x) for x in emso]
        emso_sum = sum([emso_digit_list[i] * emso_factor_map[i] for i in range(12)])
        control_digit = 0 if emso_sum % 11 == 0 else 11 - (emso_sum % 11)
        return str(emso)[:12] + str(control_digit)