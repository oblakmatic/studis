from django.urls import path

from . import views

urlpatterns = [
    #root /sifranti/
    path('',views.index_vpis,name='index_vpis'),
    #path('<str:diff>/',views.changesif,name='changesif'),
    #path('<str:diff>/<int:index>/',views.update,name='update'),
    #path('<str:diff>/<int:index>/delete/',views.delete,name='delete')
]
