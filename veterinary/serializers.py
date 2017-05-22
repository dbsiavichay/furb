from rest_framework import serializers
from .models import *

class VaccineSerializer(serializers.ModelSerializer):
    str_kinds = serializers.SerializerMethodField()

    class Meta:
        model = Vaccine
        fields = ('id', 'name', 'kinds', 'str_kinds')

    def get_str_kinds(self, obj):
        k = ''
        if len(obj.kinds.all()) < 1:
            return k

        for kind in obj.kinds.all():
            k = k + kind.name + ','
        return k[:len(k)-1]

class DiseaseSerializer(serializers.ModelSerializer):
    str_kinds = serializers.SerializerMethodField()

    class Meta:
        model = Disease
        fields = ('id', 'name', 'kinds', 'str_kinds')

    def get_str_kinds(self, obj):
        k = ''
        if len(obj.kinds.all()) < 1:
            return k

        for kind in obj.kinds.all():
            k = k + kind.name + ','
        return k[:len(k)-1]
