from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django import forms
from django.contrib.auth.models import User, Group

# Create your views here.
from .forms import *
from student.models import Vpis, Predmetnik, Modul
from sifranti.models import StudijskiProgram, StudijskoLeto, Letnik, Predmet
from izpiti.models import PredmetiStudenta

nas_leto = "2018/2019"
nas_leto_ob = StudijskoLeto.objects.filter(ime=nas_leto)



def vpisni_list(request, ind_student, ind_studleto,ind_studleto2):

    student = Student.objects.filter(vpisna_stevilka= ind_student)
    ime_stud = ind_studleto+"/"+ind_studleto2
    stud_leto = StudijskoLeto.objects.filter(ime=ime_stud)
    vpis1 = Vpis.objects.filter(student= student[0]).filter(studijsko_leto=stud_leto[0])[0]

    predmentiStudenta = PredmetiStudenta.objects.filter(vpis=vpis1)[0]
    
    

    context ={
        'student' : student,
        'vpis': vpis1,
        'predmeti_studenta' : predmentiStudenta,

    }

    return render(request,'vpis/vpisni_list.html',context) 


def index2_vpis_post(request,index):
    #index je index zetona od nekega studenta, ki ga dobimo po querysetu
    if request.method == 'POST':
        # create a form instance and populate it with data from the request
        if is_kandidat(request.user):
            return HttpResponseRedirect('/vpis/')
        elif is_student(request.user):
            student = vrniStudenta(request.user.email)
            zeton = Zeton.objects.filter(student= student[0])
            
            # ce vpis za to studijsko leto ze obstaja, ga skensli
            if Vpis.objects.filter(studijsko_leto=nas_leto_ob[0]).filter(student=student[0]).exists():
                return HttpResponseRedirect('/vpis/')
            else:
                nov_vpis = Vpis(student=student[0], 
                    studijsko_leto=StudijskoLeto.objects.filter(ime=nas_leto)[0],
                    studijski_program=zeton[index].studijski_program,
                    letnik=zeton[index].letnik,
                    vrsta_vpisa=zeton[index].vrsta_vpisa,
                    nacin_studija=zeton[index].nacin_studija,
                    vrsta_studija=zeton[index].vrsta_studija)

                nov_vpis.save()
                zeton[index].izkoriscen = True
                zeton[index].save()
                return HttpResponseRedirect('/vpis/predmetnik/')

def index2_vpis(request):

    if request.method == 'POST':
        # create a form instance and populate it with data from the request
        raise Exception('POST na vpis/studij!')

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

            if zeton:
                if len(zeton) == 2:
                    context={
                        'info':'Izbiraš lahko med dvema vpisoma',
                        'zeton1': zeton[0],
                        'zeton2': zeton[1],
                    }
                    return render(request,'vpis/index2_vpis.html',context)
                elif len(zeton) == 1:
                    context={
                        'info':'Izbereš lahko en vpis',
                        'zeton1': zeton[0],
                    }
                    return render(request,'vpis/index2_vpis.html',context)
                else:
                    context={
                        'info':'Zakaj imaš toliko žetonov?',
                    }
                    return render(request,'vpis/index2_vpis.html',context)
        else:
            opozorilo="Samo študenti se lahko vpišejo"
            context = {
                    'info' : opozorilo,
                    }
            return render(request,'vpis/index_vpis2.html',context) 
         

def index_vpis(request):

    if request.method == 'POST':
        # create a form instance and populate it with data from the request

        if is_kandidat(request.user):

            candi = vrniKandidata(request.user.email)[0]
            form = NameStudentForm(request.POST)

            if form.is_valid():

                ta_emso = form.cleaned_data['emso']
                if emso_verify(str(ta_emso)) == str(ta_emso):
                    student1 = form.save(commit=False)
                    student1.vpisna_stevilka = candi.vpisna_stevilka
                    student1.email = candi.email
                    prof_group, status = Group.objects.get_or_create(name='students') 
                    prof_group.user_set.add(request.user)
                    can_group, status = Group.objects.get_or_create(name='candidates')
                    request.user.groups.remove(can_group)
                    request.user.save()
                    student1.save()
                    return HttpResponseRedirect('/vpis/')
                else:
                    kandidat = vrniKandidata(request.user.email)
                    studentform = None
                    id_kandidata = kandidat[0].vpisna_stevilka
                    data = Kandidat.objects.filter(pk= id_kandidata).values()[0]
                    studentform = NameStudentForm(initial= data)
                    #kandidat 
           
                    context = {
                    'student' : kandidat[0],
                    'studentform' : form,
                    'opozorilo': 'EMŠO je nepravilen, ponovno ga vnesite'
                    }
                    return render(request,'vpis/index_vpis.html',context)

                
            else:
                context = {
                'studentform': form,
                'opozorilo': 'Prišlo je do napake, ponovno vnesite podatke'
                }
                return render(request,'vpis/index_vpis.html',context)

        elif is_student(request.user):
            student = vrniStudenta(request.user.email)
            form = NameStudentForm(request.POST, instance=student[0])
            print("eno")
            if form.is_valid():
                print("dva")
                form.save()
                return HttpResponseRedirect('/vpis/studij/')
                
            else:
                context = {
                'form': form,
                'opozorilo': 'Prišlo je do napake, ponovno vnesite podatke'
                }
                return render(request,'vpis/index_vpis.html',context)
        else:
            context = {
                'opozorilo': 'Niste študent pa ste vseeno nekaj POST-al'
                }
            return render(request,'vpis/index_vpis.html',context)

    # if a GET (or any other method) we'll create a blank form
    else:
        opozorilo = ""
        context = None
        #preveri kdo je 
        #p = VpisForm()
        #print(p)
        
        # preveri ce je student 
        if is_kandidat(request.user):
            kandidat = vrniKandidata(request.user.email)
            studentform = None
            id_kandidata = kandidat[0].vpisna_stevilka
            data = Kandidat.objects.filter(pk= id_kandidata).values()[0]
            studentform = NameStudentForm(initial= data)
            #kandidat 
            context = {
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
                form.fields["studijski_program"].queryset = StudijskiProgram.objects.filter(id=1000475)

                opozorilo = ""
                id_studenta = najden_student[0].vpisna_stevilka
                data = Student.objects.filter(pk= id_studenta).values()[0]
                data_2 = {
                    'drzava' : najden_student[0].drzava,
                    'posta' : najden_student[0].posta,
                    'obcina' : najden_student[0].obcina,
                    'drzava_rojstva' : najden_student[0].drzava_rojstva,
                    'obcina_rojstva' : najden_student[0].obcina_rojstva,
                 } 
                data = {**data , **data_2}
                #print({**data , **data_2})

                studentform = NameStudentForm(initial= data)
            else:
                opozorilo= "Nimaš žetona"
            
            context = {
                'vpisi' : Vpis.objects.filter(student=najden_student[0]),
                'student' : najden_student[0],
                'opozorilo' : opozorilo,
                'studentform' : studentform
                }
        else:
            opozorilo="Samo študenti se lahko vpišejo"
            context = {
                    'opozorilo' : "",
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

def predmetnik(request):

    #A preko request.POST dobis spodnje vrednosti in jih das v get
    #p_id = request.POST.get('program-id', '') namesto 1000468 npr
    if is_student(request.user):

        student = vrniStudenta(request.user.email)
        vpis = Vpis.objects.filter(potrjen=False).filter(student=student[0])[0]
        '''program = StudijskiProgram.objects.get(id=1000468)
        leto = StudijskoLeto.objects.get(ime="2018/2019")
        letnik = Letnik.objects.get(ime="2.")'''
        program = vpis.studijski_program
        leto = vpis.studijsko_leto
        letnik = vpis.letnik



        predmeti_obvezni = []
        predmeti_izbirni = []
        predmeti_modul = []
    
        so_moduli = False

        #1 in 2 letnik
        if letnik != Letnik.objects.get(ime="3."):
        
            predmeti_id = Predmetnik.objects.filter(studijski_program=program, studijsko_leto=leto, letnik=letnik).values('predmet', 'obvezen')
            
    
            for i in predmeti_id:

                predmet = Predmet.objects.filter(id=i['predmet'])
                if i['obvezen']:
                    predmeti_obvezni.append(predmet)
            
                else:
                    predmeti_izbirni.append(predmet)
        #3 letnik
        else:
            so_moduli = True
            predmeti_id = Predmetnik.objects.filter(studijski_program=program, studijsko_leto=leto, letnik=letnik, ima_modul=False).values('predmet', 'obvezen')
            for i in predmeti_id:

                predmet = Predmet.objects.filter(id=i['predmet'])
                if i['obvezen']:
                    predmeti_obvezni.append(predmet)

                else:
                    predmeti_izbirni.append(predmet)

            num = Modul.objects.count()
        
            for m in range(1, num+1):
                modul = Modul.objects.get(id=m)

                temp=[]
                for p in modul.predmetniki.all().values():
        
                    temp.append(Predmet.objects.filter(id=p["predmet_id"]))

                predmeti_modul.append(temp)


        context = {
            'predmeti_o': predmeti_obvezni,
            'predmeti_i': predmeti_izbirni,
            'predmeti_m': predmeti_modul,
            'letnik': letnik,
            'so_moduli': so_moduli
        }
        return render(request,'vpis/predmetnik.html', context)


#shrani predmete primernemu studentu
def koncaj_predmetnik(request):

    izbrani_predmeti = request.POST.get('vsi-id', '').split(",")
    izbrani_predmeti = list(map(int, izbrani_predmeti))
    predmeti = Predmet.objects.filter(id__in=izbrani_predmeti)

    student = vrniStudenta(request.user.email)
    vpis1 = Vpis.objects.filter(potrjen=False).filter(student=student[0])[0]

    #TODO manjka vpis key, treba ga je preko predmetnik.html dati sem ali pa kako drugace
    predmetiStudenta = PredmetiStudenta()
    predmetiStudenta.vpis = vpis1
    predmetiStudenta.save()

    #shrani predmete
    for p in predmeti:
        predmetiStudenta.predmeti.add(p)

    predmetiStudenta.save()
    context = {
        'predmeti': predmeti,
    }

    return render(request,'vpis/predmetnik_izpis.html', context)