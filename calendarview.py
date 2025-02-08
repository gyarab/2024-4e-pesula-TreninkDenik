from django.shortcuts import render
from .models import Training

def calendar_view(request):
    trainings = Training.objects.all()
    return render(request, 'calendar.html', {'trainings': trainings})
