from django.contrib import admin

# Register your models here.
# ENABLES CRUD operations on admin page

from .models import *

admin.site.register(Drzava)
admin.site.register(Posta)
admin.site.register(Obcina)
admin.site.register(VrstaStudija)
admin.site.register(Letnik)
admin.site.register(StudijskiProgram)
admin.site.register(StudijskoLeto)
admin.site.register(NacinStudija)
admin.site.register(OblikaStudija)