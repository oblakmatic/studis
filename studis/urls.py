"""studis URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from django.views.generic.base import TemplateView
from django.contrib.auth import views as auth_views
from studis.views import login, auth_view, logout, invalid, home_view
from sifranti.views import naredi_bazo

urlpatterns = [
	path('', home_view, name='home'),
    path('admin/', admin.site.urls),
    path('sifranti/', include('sifranti.urls')),
    path('vpis/', include('vpis.urls')),
	path('izpiti/', include('izpiti.urls')),
    path('student/', include('student.urls')),
    path('student/potrdi_studente/', include('student.urls')),
    path('user/login/', login, name="login"),
    path('user/logout/', logout, name="logout"),
    path('user/auth/', auth_view, name = "auth_view"),
    path('user/invalid/', invalid, name = "invalid"),
	path('password_reset/', auth_views.password_reset, name='password_reset'),
    path('password_reset/done/', auth_views.password_reset_done, name='password_reset_done'),
    re_path('reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',
        auth_views.password_reset_confirm, name='password_reset_confirm'),
    path('reset/done/', auth_views.password_reset_complete, name='password_reset_complete'),
    path('naredibazo/',naredi_bazo,name='naredibazo'),

]
    