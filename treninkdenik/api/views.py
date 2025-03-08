from rest_framework import viewsets
from django.shortcuts import redirect, render
from .models import Uzivatel, Trenink
from .serializers import UzivatelSerializer, TreninkSerializer
from .forms import TreninkForm

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

def index(request):
    return render(request, 'index.html')

def treninky(request):
    treninky = Trenink.objects.all()
    return render(request, 'treninky.html', {'treninky' : treninky})

def pridat_trenink(request):
    if request.method == "POST":
        form = TreninkForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('treninky')
    else:
        form = TreninkForm()

    return render(request, 'pridat_trenink.html', {'form' : form})