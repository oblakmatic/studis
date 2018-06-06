from django.urls import path

from . import views

urlpatterns = [
    #root /vpis/
    path('',views.index_vpis,name='index_vpis'),
    path('studij/',views.index2_vpis,name='index2_vpis'),
    path('studij/<int:index>/',views.index2_vpis_post,name='index2_vpis_post'),
    path('vpisni_list/<int:vpisna>/<str:ind_studleto>/<str:ind_studleto2>/',views.vpisni_list,name='vpisni_list'),
    #path('<str:diff>/',views.changesif,name='changesif'),
    #path('<str:diff>/<int:index>/',views.update,name='update'),
    #path('<str:diff>/<int:index>/delete/',views.delete,name='delete')
    path('predmetnik/',views.predmetnik,name='predmetnik'),
    path('predmetnik/izpis/',views.koncaj_predmetnik,name='koncaj_predmetnik'),
    path('kartotecni/<int:vpisna>/<int:storitev>/',views.narediKartotecniList,name='narediKartotecniList'),
    #path('vpisni_list/<int:vpisna>/', views.vpisni_list, name='vpisni_list'),
]
