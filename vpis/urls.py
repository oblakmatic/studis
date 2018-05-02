from django.urls import path

from . import views

urlpatterns = [
    #root /vpis/
    path('',views.index_vpis,name='index_vpis'),
    path('studij/',views.index2_vpis,name='index2_vpis'),
    path('studij/<int:index>/',views.index2_vpis_post,name='index2_vpis_post'),
    #path('<str:diff>/',views.changesif,name='changesif'),
    #path('<str:diff>/<int:index>/',views.update,name='update'),
    #path('<str:diff>/<int:index>/delete/',views.delete,name='delete')
]
