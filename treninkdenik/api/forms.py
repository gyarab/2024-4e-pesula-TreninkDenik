from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from .models import Uzivatel, Trenink

class UzivatelForm(forms.ModelForm):
    class Meta:
        model = Uzivatel
        fields = ['username','vek','vyska','vaha']
        labels = {
            'username': 'Jméno',
            'vek': 'Věk',
            'vyska': 'Výška',
            'vaha': 'Váha',
        }

class TreninkForm(forms.ModelForm):
    class Meta:
        model = Trenink
        fields = ['nazev','datum','type','doba','pozn']
        widgets = {'datum': forms.DateInput(attrs={'readonly': 'readonly'}), }
        labels = {
            'nazev': 'Název',
            'datum': 'Datum',
            'type': 'Typ tréninku',
            'doba': 'Doba (minuty)',
            'pozn': 'Poznámky'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['datum'].widget = forms.SelectDateWidget() # Vybírá data

Uzivatel = get_user_model()

class RegistraceUseraForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Uzivatel
        fields = ["username", "email", "password"]

    def clean_username(self):
        dejmijmeno = self.cleaned_data.get('username')
        if Uzivatel.objects.filter(username=dejmijmeno).exists():
            raise ValidationError("Toto uživatelské jméno již existuje. Zvolte prosím jiné.")
        return dejmijmeno

class MemoryForm(AuthenticationForm):
    zapamatuj_si = forms.BooleanField(required=False, initial=False, label="Zapamatovat si mě")