from django.urls import path

from . import views

urlpatterns = [
    #root /studenti/
    path('',views.students,name='students'),
    path('uvoz/',views.upload_file,name='upload_file'),
    path('uvoz/seznam/',views.import_students,name='import_students'),
    path('isci/',views.students_search,name='students_search'),
]
