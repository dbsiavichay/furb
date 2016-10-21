from rest_framework import serializers
from .models import *

class KindSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kind

class BreedSerializer(serializers.ModelSerializer):
    kind_name = serializers.SerializerMethodField()

    class Meta:
        model = Breed
        fields = ('id', 'name', 'kind', 'kind_name')

    def get_kind_name(self, obj):
        return obj.kind.name
