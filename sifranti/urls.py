from django.urls import path

from . import views

urlpatterns = [
    #example /sifranti/
    path('',views.index,name='index'),
    path('<str:diff>/',views.changesif,name='changesif'),

]