from django import forms
from .models import Uzivatel, Trenink

class UzivatelForm(forms.ModelForm):
    class Meta:
        model = Uzivatel
        fields = ['jmeno','vek','vyska','vaha']

class TreninkForm(forms.ModelForm):
    class Meta:
        model = Trenink
        fields = ['datum','type','doba','pozn']