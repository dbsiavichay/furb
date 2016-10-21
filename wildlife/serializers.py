from rest_framework import serializers
from .models import *

class KindSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kind
