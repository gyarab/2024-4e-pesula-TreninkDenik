"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.shortcuts import redirect
from django.urls import path, include
from api.views import treninky, uzivatel_udaje, register, kalendar, zapistreninku

def domovni_page(request):
    if request.user.is_authenticated: # Pokud se uživatel registroval, se spuětním aplikace zobrazí kalendář
        return redirect('kalendar') # 
    return redirect('register') # V opačném případě zobrazí stránku s registrací

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/', include('api.urls')),
    path('', domovni_page, name='home'), # viz funkce domovni_page (řádek 23)
    path('treninky/', treninky, name='treninky'), # Seznam tréninků uživatele
    path('register/', register, name='register'), # Registrace nových uživatelů
    path('udaje/', uzivatel_udaje, name='uzivatel_udaje'), # Údaje o uživateli
    path('kalendar/', kalendar, name='kalendar'), # Default kalendář
    path('kalendar/<int:rok>/<int:mesic>/', kalendar, name='kalendar'), # URL kalendáře 
    path('zapistreninku/<str:datum>/', zapistreninku, name='zapistreninku'), # URL vybraného dne pro zapisování tréninků
]
