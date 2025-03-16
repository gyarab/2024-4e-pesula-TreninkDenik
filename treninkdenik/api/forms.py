from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from .models import Uzivatel, Trenink

class UzivatelForm(forms.ModelForm):
    class Meta:
        model = Uzivatel
        fields = ['jmeno','vek','vyska','vaha']

class TreninkForm(forms.ModelForm):
    class Meta:
        model = Trenink
        fields = ['datum','type','doba','pozn']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['datum'].widget = forms.SelectDateWidget() # Vybírá data

Uzivatel = get_user_model()

class RegistraceUseraForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Uzivatel
        fields = ["jmeno", "email", "password"]

    def clean_username(self):
        dejmijmeno = self.cleaned_data.get('jmeno')
        if Uzivatel.objects.filter(username=dejmijmeno).exists():
            raise ValidationError("Toto uživatelské jméno již existuje. Zvolte prosím jiné.")
        return dejmijmeno