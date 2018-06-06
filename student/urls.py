from django.urls import path

from . import views

urlpatterns = [
    #root /studenti/
    path('',views.students,name='students'),
    path('uvoz/',views.upload_file,name='upload_file'),
    path('uvoz/seznam/',views.import_students,name='import_students'),
    path('isci/',views.students_search,name='students_search'),
    path('ustvari-zeton/<int:id>',views.token_add,name='token_add'),
    path('ustvari-zeton/',views.token_add,name='token_add'),
    path('seznam-zetonov/',views.token_list,name="token_list"),
    path('izbrisi-zeton/<int:del_id>', views.token_delete,name="token_delete"),
    path('uredi-zeton/<int:edit_id>', views.token_edit,name="token_edit"),
    path('izvoz/pdf/',views.export_pdf,name='export_pdf'),
    path('izvoz/csv/',views.export_csv,name='export_csv'),
    path('podatki/', views.student_data, name="student_data"),
    path('podatki/<int:id>', views.all_data, name="all_data"),
    path('potrdi_studente/', views.potrdi_studente, name="potrdi_studente"),
    path('preveri_seznam/', views.preveri_seznam, name="preveri_seznam"),
	path('naroci_potrdila/', views.naroci_potrdila, name="naroci_potrdila"),
	path('natisni_potrdila/', views.natisni_potrdila, name="natisni_potrdila"),
    path('predmeti/', views.students_by_subject, name="students_by_subject"),
    path('predmeti/<int:leto>/<int:id>/', views.subject_data, name="subject_data"),
    path('predmeti/<int:leto>/<int:id>/csv', views.naredi_predmet_csv, name="naredi_predmet_csv"),
    path('predmeti/stevilo/', views.students_by_number, name="students_by_number"),
    path('predmeti/stevilo/<int:leto>/<int:program>/<int:letnik>/csv/', 
        views.naredi_stevilo_csv, name="naredi_stevilo_csv"),

]
