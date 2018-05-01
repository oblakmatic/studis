from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django import forms

# Create your views here.
from .forms import *
from student.models import Vpis, Predmetnik, Modul
from sifranti.models import StudijskiProgram, StudijskoLeto, Letnik, Predmet

def index_vpis(request):

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        
        # example Posta --> PostaForm

        possible_student = vrniStudenta(request.user.email)
        print(request.POST)

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
        context = None
        #preveri kdo je 
        #p = VpisForm()
        #print(p)
        
        # preveri ce je student 
        if is_student(request.user):
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
                
                print({**data , **data_2})

                studentform = NameStudentForm(initial= {**data , **data_2})
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

def is_student(user):
    return user.groups.filter(name='student').exists()

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

def predmetnik(request):
    program = StudijskiProgram.objects.get(id=1000468)
    leto = StudijskoLeto.objects.get(ime="2018/2019")
    letnik = Letnik.objects.get(ime="2.")

    predmeti_obvezni = []
    predmeti_izbirni = []
    predmeti_modul = []
    KT = 0
    so_moduli = False

    #1 in 2 letnik
    if letnik != Letnik.objects.get(ime="3."):
       
        predmeti_id = Predmetnik.objects.filter(studijski_program=program, studijsko_leto=leto, letnik=letnik).values('predmet', 'obvezen')
        
 
        for i in predmeti_id:

            predmet = Predmet.objects.get(id=i['predmet'])
            if i['obvezen']:
                predmeti_obvezni.append(predmet)
                KT=KT+6
            else:
                predmeti_izbirni.append(predmet)
    #3 letnik
    else:
        so_moduli = True
        predmeti_id = Predmetnik.objects.filter(studijski_program=program, studijsko_leto=leto, letnik=letnik, ima_modul=False).values('predmet', 'obvezen')
        for i in predmeti_id:

            predmet = Predmet.objects.get(id=i['predmet'])
            if i['obvezen']:
                predmeti_obvezni.append(predmet)
                KT=KT+6
            else:
                predmeti_izbirni.append(predmet)

        num = Modul.objects.count()
    
        for m in range(1, num+1):
            modul = Modul.objects.get(id=m)

            temp=[]
            for p in modul.predmetniki.all().values():
    
                temp.append(Predmet.objects.get(id=p["predmet_id"]))

            predmeti_modul.append(temp)


    context = {
        'predmeti_o': predmeti_obvezni,
        'predmeti_i': predmeti_izbirni,
        'predmeti_m': predmeti_modul,
        'letnik': letnik,
        'so_moduli': so_moduli,
        'KT': KT
    }
    return render(request,'vpis/predmetnik.html', context)
