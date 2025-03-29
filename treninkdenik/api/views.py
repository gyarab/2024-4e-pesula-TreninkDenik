from rest_framework import viewsets
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from api.models import Uzivatel, Trenink
from api.serializers import UzivatelSerializer, TreninkSerializer
from api.forms import UzivatelForm, TreninkForm, RegistraceUseraForm
from datetime import datetime
import calendar

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
    treninky = Trenink.objects.filter(user=request.user) # Pouze tréninky přihlášeného uživatele
    return render(request, 'treninky.html', {'treninky' : treninky})

def uzivatel_udaje(request):
    if request.method == 'POST':
        form = UzivatelForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save() # Uloží údaje o uživateli
            return redirect('kalendar') # Přesměruje na kalendář
    else:
        form = UzivatelForm(instance=request.user)
    
    return render(request, 'uzivatel_udaje.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = RegistraceUseraForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']  

            # Ověří, jestli uživatel se stejným jménem již existuje
            if Uzivatel.objects.filter(username=username).exists():
                messages.error(request, "Toto uživatelské jméno je již obsazené.") # Vyskočí zpráva
                return render(request, 'registrace.html', {'form': form})            
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])  # Zahashování hesla
            user.save() # Uloží uživatele
            request.session['uzivatel_id'] = user.id  # Uloží id uživatele do session

            # Uživatel registrován natrvalo
            login(request, user)  
            request.session.set_expiry(None)
            
            return redirect('kalendar')  # Přesměruje uživatel ke kalendáři

    else:
        form = RegistraceUseraForm()

    return render(request, 'registrace.html', {'form': form})

@login_required
def kalendar(request, rok=None, mesic=None):
    uzivatel = request.user # Přímé načtení uživatele

    if not rok or not mesic:
        dnes = datetime.today() # Dnešní datum
        rok = dnes.year
        mesic = dnes.month
    else:
        rok = int(rok)
        mesic = int(mesic)

    # Výpočítá předchozí a následující rok a měsíc
    predchozi_rok, predchozi_mesic = (rok, mesic - 1) if mesic > 1 else (rok - 1, 12)
    dalsi_rok, dalsi_mesic = (rok, mesic + 1) if mesic < 12 else (rok + 1, 1)

    # Kalendář
    cal = calendar.Calendar()
    kalendar = []

    treninky = Trenink.objects.filter(user=uzivatel, datum__year=rok, datum__month=mesic)
    udelaltrenink = set(treninky.values_list('datum', flat=True)) 

    for tyden in cal.monthdayscalendar(rok, mesic):
        tyden_dny = []
        for den in tyden:
            if den == 0:
                tyden_dny.append(None)  # Prázdné místo pro dny předchozího a následujícícho měsíce
            else:
                tyden_dny.append(f"{rok}-{mesic:02d}-{den:02d}")  # Formát YYY-MM-DD
        kalendar.append(tyden_dny)

    return render(request, 'kalendar.html', {'uzivatel': uzivatel, 'calendar': kalendar, 
                                             'year': rok, 'month': mesic, 'udelaltrenink': udelaltrenink,
                                             'predchozi_rok': predchozi_rok, 'predchozi_mesic': predchozi_mesic,
                                             'dalsi_rok': dalsi_rok, 'dalsi_mesic': dalsi_mesic,})

@login_required
def zapistreninku(request, datum):
    try:
        datum_date = datetime.strptime(datum, '%Y-%m-%d').date()
    except ValueError:
        return redirect('kalendar')

    # Filtrujeme tréninky pouze pro přihlášeného uživatele!
    treninky = Trenink.objects.filter(datum=datum_date, user=request.user) 

    if request.method == "POST":
        form = TreninkForm(request.POST)
        if form.is_valid():
            trenink = form.save(commit=False)
            trenink.user = request.user # Přidá usera k tréninku
            trenink.datum = datum_date # Využije datum vybraného dne
            trenink.save() # Uloží trénink
            return redirect('zapistreninku', datum=datum_date)
    else:
        form = TreninkForm(initial={'datum': datum_date})

    return render(request, 'zapistreninku.html', {'datum': datum_date, 'treninky': treninky, 'form': form})
