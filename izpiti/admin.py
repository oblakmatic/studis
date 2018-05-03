from django.contrib import admin


# Register your models here.
from .models import *

admin.site.register(Ucitelj)
admin.site.register(IzvedbaPredmeta)
admin.site.register(Rok)
admin.site.register(PredmetiStudenta)
admin.site.register(Prijava)
admin.site.register(PrijaveStudenta)
