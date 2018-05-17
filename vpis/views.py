from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django import forms
from django.contrib.auth.models import User, Group

import datetime
from reportlab.pdfgen import canvas
from reportlab.platypus import *
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter, A4, landscape
from reportlab.lib import colors 

import time
from reportlab.lib.enums import TA_JUSTIFY, TA_RIGHT, TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from student.forms import TokenForm
from django.db.models import Q

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
pdfmetrics.registerFont(TTFont('Vera', 'Vera.ttf'))

import pdfkit
from django.template.loader import render_to_string
from django.core.files.storage import FileSystemStorage



# Create your views here.
from .forms import *
from student.models import Vpis, Predmetnik, Modul
from sifranti.models import StudijskiProgram, StudijskoLeto, Letnik, Predmet
from izpiti.models import *

nas_leto = "2018/2019"
nas_leto_ob = StudijskoLeto.objects.filter(ime=nas_leto)



def vpisni_list(request, vpisna):
    student = Student.objects.filter(vpisna_stevilka=vpisna)
    vpis = Vpis.objects.filter(student= student[0])
    narediVpisniList(student,vpis)

    name = str(vpisna) +"2018"+'.pdf'
    fs = FileSystemStorage('/tmp')
    with fs.open(name) as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="'+ name+' "'
        return response

    return response


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
                    vrsta_studija=zeton[index].vrsta_studija,
                    oblika_studija=zeton[index].oblika_studija,
                    prosta_izbira = zeton[index].pravica_do_izbire)

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
                ta_datum = form.cleaned_data['datum_rojstva']
                if preveri_emso_datum(ta_emso,ta_datum):
                    #tukaj naredimo iz kandidata studenta in mu dodelimo zeton
                    student1 = form.save(commit=False)
                    student1.vpisna_stevilka = candi.vpisna_stevilka
                    student1.email = candi.email
                    prof_group, status = Group.objects.get_or_create(name='students') 
                    prof_group.user_set.add(request.user)
                    can_group, status = Group.objects.get_or_create(name='candidates')
                    request.user.groups.remove(can_group)
                    request.user.save()
                    student1.save()

                    studentek = vrniStudenta(request.user.email)
                    print(studentek)
                    narediZetonZaKandidata(studentek,candi)
                    return HttpResponseRedirect('/vpis/studij/')
                else:
                    kandidat = vrniKandidata(request.user.email)
                    studentform = None
                    id_kandidata = kandidat[0].vpisna_stevilka
                    data = Kandidat.objects.filter(pk= id_kandidata).values()[0]
                    studentform = NameStudentForm(initial= data)
                    opozorilo = ""
                    
                    if emso_verify(ta_emso) != ta_emso:
                        opozorilo = "EMŠO je nepravilen, ponovno ga vnesite"
                    else:
                        opozorilo = "Datum in EMŠO se ne ujemata"

                    context = {
                    'student' : kandidat[0],
                    'studentform' : form,
                    'opozorilo': opozorilo
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
            if form.is_valid():
                ta_emso = form.cleaned_data['emso']
                ta_datum = form.cleaned_data['datum_rojstva']
                if preveri_emso_datum(ta_emso,ta_datum):
                    form.save()
                    return HttpResponseRedirect('/vpis/studij/')
                else:
                    opozorilo = ""
                    
                    if emso_verify(ta_emso) != ta_emso:
                        opozorilo = "EMŠO je nepravilen, ponovno ga vnesite"
                    else:
                        opozorilo = "Datum in EMŠO se ne ujemata"

                    context = {
                    'vpisi' : Vpis.objects.filter(student=student[0]).filter(dokoncan_vpis=True),
                    'student': student[0],
                    'studentform': form,
                    'opozorilo': opozorilo
                    }
                    return render(request,'vpis/index_vpis.html',context)
            else:
                context = {
                'vpisi' : Vpis.objects.filter(student=student[0]).filter(dokoncan_vpis=True),
                'student': student[0],
                'studentform': form,
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
                'vpisi' : Vpis.objects.filter(student=najden_student[0]).filter(dokoncan_vpis=True),
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

        prosta_izbira = vpis.prosta_izbira

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

                predmet = Predmet.objects.filter(id=i['predmet'])
                if i['obvezen']:
                    predmeti_obvezni.append(predmet)
            
                else:
                    predmeti_izbirni.append(predmet)

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
                    
    
            moduls = Modul.objects.all()
        
    
            for m in moduls:
                temporary.append(m.ime)
                pr = Predmetnik.objects.filter(modul=m)
                temp=[]
                for p in pr:
                    temp.append(p.predmet)

            
                predmeti_modul.append(temp)

        context = {
            'predmeti_o': predmeti_obvezni,
            'predmeti_i': predmeti_izbirni,
            'predmeti_m': predmeti_modul,
            'letnik': letnik,
            'so_moduli': so_moduli
        }
        return render(request,'vpis/predmetnik.html', context)

        context = {
            'predmeti_o': predmeti_obvezni,
            'predmeti_i': zip(predmeti_izbirni, temporary),
            'predmeti_m': zip(predmeti_modul, temporary),
            'letnik': letnik,
            'prosta_izbira': prosta_izbira
        }

        return render(request,'vpis/predmetnik.html', context)


#shrani predmete primernemu studentu
def koncaj_predmetnik(request):

    izbrani_predmeti = request.POST.get('vsi-id', '').split(",")
    izbrani_predmeti = list(map(int, izbrani_predmeti))
    predmeti = Predmet.objects.filter(id__in=izbrani_predmeti)

    izbrani_predmeti = request.POST.get('vsi-id', '').split(",")

    izbrani_predmeti = list(map(int, izbrani_predmeti))
    predmeti = Predmet.objects.filter(id__in=izbrani_predmeti)

    student = vrniStudenta(request.user.email)
    vpis2 = Vpis.objects.filter(potrjen=False).filter(student=student[0])
    vpis1 = vpis2[0]
    
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
    
    vpis1.dokoncan_vpis = True
    vpis1.save()
    return render(request,'vpis/predmetnik_izpis.html', context)


def preveri_emso_datum(emso, datum):

    if emso_verify(emso) == emso and datum[8:10] == emso[0:2] and emso[2:4] == datum[5:7] and emso[4:7] == datum[1:4]:
        return True
    else:
        return False

#naredi zeton za kandidata (ki je pa v tem momentu postal student)
#student, kandidat sta ista oseba, iz kandidat izluscimo kateri studijski
# program hoce delati, zeton dodelimo studentu
def narediZetonZaKandidata(student1,kandidat):
    
    print(student1)
    print(kandidat)
    print("neki")
    if Zeton.objects.filter(student=student1[0]).exists():
        return
    
    print("neki")
    letnik = Letnik.objects.get(ime="1.")
    studij_prog = kandidat.studijski_program
    vrsta_studija = None
    nacin_studija = NacinStudija.objects.get(id=1)
    vrsta_vpisa = VrstaVpisa.objects.get(id=1)
    oblika_studija = OblikaStudija.objects.get(id=1)
    print("neki")
    if studij_prog.id == 1000470:
        vrsta_studija = VrstaStudija.objects.get(id=16203)
    elif studij_prog.id == 1000468:
        vrsta_studija = VrstaStudija.objects.get(id=16204)
    else:
        raise Exception("ne bi se smel tale else izvediti")

    
    
    nov_zeton = Zeton(student = student1[0], 
                    studijski_program = studij_prog,
                    letnik = letnik,
                    vrsta_studija = vrsta_studija,
                    nacin_studija = nacin_studija,
                    vrsta_vpisa = vrsta_vpisa,
                    oblika_studija = oblika_studija
                    )
    nov_zeton.save()
    print("nekisad")
    return
    
#pripeli student in vpis kot queryset
def narediVpisniList(student,vpis):
    #prvoleto = Vpis.objects.filter(student=student).order_by('studijsko_leto')[0]
    #prvoleto = prvoleto.studijsko_leto

    drzava = na(str(student[0].drzava))
    obcina = na(str(student[0].obcina))
    posta = na(str(student[0].posta))
    posta_zacasno = na(str(student[0].posta_zacasno))
    naslov_zacasno_bivalisce = na(str(student[0].naslov_zacasno_bivalisce))
    drzava_zacasno = na(str(student[0].drzava_zacasno))
    obcina_zacasno = na(str(student[0].obcina_zacasno))
    drzava_rojstva = na(str(student[0].drzava_rojstva))
    obcina_rojstva = na(str(student[0].obcina_rojstva))

    #vpis

    studijsko_leto = na(str(vpis[0].studijsko_leto))
    studijski_program = na(str(vpis[0].studijski_program))
    letnik = na(str(vpis[0].letnik))
    vrsta_vpisa = na(str(vpis[0].vrsta_vpisa))
    nacin_studija = na(str(vpis[0].nacin_studija))
    vrsta_studija = na(str(vpis[0].vrsta_studija))
    oblika_studija = na(str(vpis[0].oblika_studija))

    #predmeti

    predmeti = PredmetiStudenta.objects.filter(vpis= vpis[0])[0].predmeti.all()

    vsipod = []

    for predmet in predmeti:
        izvedba = IzvedbaPredmeta.objects.filter(predmet=predmet, studijsko_leto=vpis[0].studijsko_leto)[0]
        ucitelj = na(str(izvedba.ucitelj_1))
        #ucitelj = "test"
        tocke = na(str(predmet.kreditne_tocke))
        predmet_ime = na(str(predmet))

        merge = {'predmet': predmet_ime, 'ucitelj': ucitelj, 'tocke': tocke}
        vsipod.append(merge)


    leto = vpis[0].studijsko_leto.ime[0:4]
    vp = str(vpis[0].student.vpisna_stevilka)



    merge = {** student.values()[0], 
    'drzava' : drzava,
     'obcina': obcina,
     'posta': posta,
     'posta_zacasno':posta_zacasno,
     'naslov_zacasno_bivalisce':naslov_zacasno_bivalisce,
     'drzava_zacasno':drzava_zacasno,
     'obcina_zacasno':obcina_zacasno,
      'drzava_rojstva':drzava_rojstva,
      'obcina_rojstva':obcina_rojstva,}

    merge2 = {** vpis.values()[0],

    'studijsko_leto':studijsko_leto,
     'studijski_program':studijski_program,
     'letnik':letnik,
     'vrsta_vpisa':vrsta_vpisa,
     'nacin_studija':nacin_studija,
     'vrsta_studija':vrsta_studija,
     'oblika_studija':oblika_studija
    }
    context = {
       'student' : merge ,
       'vpis' : merge2,
       'predmetnik': vsipod,

   }


    html_string =  render_to_string('vpis/index3_vpis.html',context)
    pdfkit.from_string( html_string,'/tmp/'+ vp+leto+'.pdf')
    return


def na(objekt):
    if objekt == "None":
        return ""
    else:
        return objekt
    