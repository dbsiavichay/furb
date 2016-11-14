from rest_framework import serializers
from .models import *

class ParishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parish
        fields = ('code', 'name')

class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Owner
