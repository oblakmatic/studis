from django.urls import path

from . import views

urlpatterns = [
    #root /izpiti/
    path('',views.index_izpiti,name='index_izpiti'),
    path('izpiti-message/',views.dodaj_izpit,name='izpiti_message'),
    path('napolni-bazo/',views.fill_database,name='napolni_bazo'),
]
