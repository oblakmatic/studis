from django.urls import path

from . import views

urlpatterns = [
    #root /studenti/
    path('',views.students,name='students'),
    path('uvoz/',views.upload_file,name='upload_file'),
    path('uvoz/seznam/',views.import_students,name='import_students'),
    path('isci/',views.students_search,name='students_search'),
    path('ustvari-zeton/',views.token_add,name='token_add'),
    path('seznam-zetonov/',views.token_list,name="token_list"),
    path('izbrisi-zeton/<int:del_id>', views.token_delete,name="token_delete")
]
