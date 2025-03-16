from django.db import IntegrityError
from rest_framework import viewsets
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Uzivatel, Trenink
from .serializers import UzivatelSerializer, TreninkSerializer
from .forms import UzivatelForm, TreninkForm, RegistraceUseraForm
import calendar
from datetime import datetime

class UzivatelViewSet(viewsets.ModelViewSet):
    queryset = Uzivatel.objects.all()
    serializer_class = UzivatelSerializer

    def get_queryset(self):
        return Uzivatel.objects.filter(active=True)

class TreninkViewSet(viewsets.ModelViewSet):
    queryset = Trenink.objects.all()
    serializer_class = TreninkSerializer    

    def get_queryset(self):
        return Trenink.objects.filter(active=True)

def treninky(request):
    treninky = Trenink.objects.all()
    return render(request, 'treninky.html', {'treninky' : treninky})

def prijmuti(request):
    if request.user.is_authenticated:
        return redirect('kalendar')
    return render(request, 'login.html')

def uzivatel_udaje(request):
    if request.method == 'POST':
        form = UzivatelForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save() # Uloží údaje
            return redirect('kalendar') # Přesměruje na kalendář
    else:
        form = UzivatelForm(instance=request.user)
    
    return render(request, 'uzivatel_udaje.html', {'form': form})

def pridat_trenink(request):
    if request.method == "POST":
        form = TreninkForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('treninky')
    else:
        form = TreninkForm()

    return render(request, 'pridat_trenink.html', {'form' : form})

def login(request):
    if request.method == 'POST':
        form = UzivatelForm(request.POST)
        if form.is_valid():
            uzivatel = form.save() # Uloží uživatele
            request.session['uzivatel_id'] = uzivatel.id
            return redirect('kalendar') # Přesměruje na kalendář
    else:
        form = UzivatelForm()
    
    return render(request, 'login.html', {'form': form}) 

def register(request):
    if request.method == 'POST':
        form = RegistraceUseraForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["jmeno"]  # Ujistěte se, že máte pole pro uživatelské jméno v rámci formuláře
            if Uzivatel.objects.filter(username=username).exists():

                # Pokud uživatelské jméno existuje, přidejte chybovou zprávu
                messages.error(request, "Toto uživatelské jméno již existuje. Zvolte prosím jiné.")
                return render(request, 'registrace.html', {'form': form})  # Zobrazte formulář znovu

            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])  # Zahashování hesla
            try:
                user.save()
                login(request, user)
                return redirect('kalendar')  # Přesměrování na kalendář
            except IntegrityError as e:
                # Zpracování chyby, např. logování, informování uživatele
                print("Chyba při ukládání uživatele:", e)
            
    else:
        form = RegistraceUseraForm()
    
    return render(request, 'registrace.html', {'form': form})

def kalendar(request):
    uzivatel_id = request.session.get('uzivatel_id')
    if not uzivatel_id:
        return redirect ('register')
    
    uzivatel = get_object_or_404(Uzivatel, pk=uzivatel_id)

    dnes = datetime.today()
    rok = dnes.year
    mesic = dnes.month

    cal = calendar.Calendar()
    kalendar = []
    for tyden in cal.monthdayscalendar(rok, mesic):
        tyden_dny = []
        for den in tyden:
            if den == 0:
                tyden_dny.append(None)  # Prázdné místo pro dny mimo měsíc
            else:
                tyden_dny.append(f"{rok}-{mesic:02d}-{den:02d}")  # Formát Y-m-d
        kalendar.append(tyden_dny)

    return render(request, 'kalendar.html', {'uzivatel': uzivatel, 'calendar': kalendar, 'year': rok, 'month': mesic})

def zapistreninku(request, datum):
    try: # Ujistíme se, že datum je ve správném formátu (YYYY-MM-DD)
        datum_ber = str(datum)  # Převedeme datum na řetězec
        datum_date = datetime.strptime(datum_ber, '%Y-%m-%d').date()  # Převedeme na datum
        
    except ValueError:
        return redirect('kalendar')  # Pokud je formát špatný, přesměrujeme zpět
    
    treninky = Trenink.objects.filter(datum=datum_date, user=request.user)
    if request.method == "POST":
        form = TreninkForm(request.POST)
        if form.is_valid():
            trenink = form.save(commit=False)
            trenink.user = request.user # Přidá usera k tréninku
            trenink.datum = datum_date
            trenink.save()
            return redirect('zapistreninku', datum=datum_date)
    else:
        form = TreninkForm(initial={'datum': datum_date})

    return render(request, 'zapistreninku.html', {'datum': datum_date, 'treninky': treninky, 'form': form})