from rest_framework import viewsets
from .models import Uzivatel, Trenink
from .serializers import UzivatelSerializer, TreninkSerializer

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
