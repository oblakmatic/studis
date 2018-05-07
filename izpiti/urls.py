from django.urls import path

from . import views


urlpatterns = [
    #root /izpiti/
    path('',views.index_izpiti,name='index_izpiti'),
    path('izpiti-message/',views.dodaj_izpit,name='izpiti_message'),
    path('prijava/',views.prijava,name='prijava'),
    path('vnesi_ocene/',views.izberi_rok,name='vnesi_ocene'),
    path('vnesi_ocene_predmeta/',views.vnesi_ocene_predmeta,name='vnesi_ocene_predmeta'),
    path('seznam_ocen/',views.seznam_ocen,name='seznam_ocen')
]
