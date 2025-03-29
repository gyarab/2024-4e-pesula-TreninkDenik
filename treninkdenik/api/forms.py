from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from .models import Uzivatel, Trenink

# Formulář pro vyplnění údajů o uživateli
class UzivatelForm(forms.ModelForm):
    class Meta:
        model = Uzivatel
        fields = ['vek','vyska','vaha']
        labels = {
            'vek': 'Věk',
            'vyska': 'Výška',
            'vaha': 'Váha',
        }

# Formulář pro zapsání tréninku
class TreninkForm(forms.ModelForm):
    class Meta:
        model = Trenink
        fields = ['nazev','datum','type','doba','pozn']
        labels = {
            'nazev': 'Název',
            'datum': 'Datum',
            'type': 'Typ tréninku',
            'doba': 'Doba (minuty)',
            'pozn': 'Poznámky'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['datum'].widget.attrs['readonly'] = True
        self.fields['pozn'].widget.attrs.update({'rows': 3, 'cols': 30, 'style': 'resize: none;'})

Uzivatel = get_user_model()

# Formulář pro registraci uživatele
class RegistraceUseraForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Uzivatel
        fields = ["username", "email", "password"]
        labels = {
            'username': 'Uživatelské jméno',
            'email': 'E-mail',
            'password': 'Heslo'
        }
    
    # Kontrola jména uživatele
    def clean_username(self):
        dejmijmeno = self.cleaned_data.get('username')
        if Uzivatel.objects.filter(username=dejmijmeno).exists():
            raise ValidationError("Uživatelské jméno již existuje. Zvolte jiné.")
        return dejmijmeno