from django import forms
from .models import Trenink

class TreninkForm(forms.ModelForm):
    class Meta:
        model = Trenink
        fields = ['datum','type','doba','pozn']