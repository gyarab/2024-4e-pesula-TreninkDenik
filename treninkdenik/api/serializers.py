from rest_framework import serializers
from .models import Uzivatel, Trenink

class UzivatelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Uzivatel
        fields = '__all__'

class TreninkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trenink
        fields = '__all__'