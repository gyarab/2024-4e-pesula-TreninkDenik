from rest_framework import viewsets
from django.shortcuts import redirect, render, get_object_or_404
from .models import Uzivatel, Trenink
from .serializers import UzivatelSerializer, TreninkSerializer
from .forms import UzivatelForm, TreninkForm

# Create your views here.
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

#def index(request):
   # return render(request, 'index.html')

def treninky(request):
    treninky = Trenink.objects.all()
    return render(request, 'treninky.html', {'treninky' : treninky})

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

def kalendar(request):
    uzivatel_id = request.session.get('uzivatel_id')
    if not uzivatel_id:
        return redirect ('login')
    
    uzivatel = get_object_or_404(Uzivatel, pk=uzivatel_id)

    return render(request, 'base.html', {'uzivatel': uzivatel})