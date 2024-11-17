from rest_framework import serializers
from .models import Floor, Pantry, Dispenser
from django.contrib.auth.models import User

class FloorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Floor
        fields = '__all__'

class PantrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Pantry
        fields = '__all__'

class DispenserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dispenser
        fields = '__all__'
