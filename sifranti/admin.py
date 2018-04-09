from django.contrib import admin

# Register your models here.
# ENABLES CRUD operations on admin page

from .models import *

admin.site.register(Drzava)
admin.site.register(Posta)