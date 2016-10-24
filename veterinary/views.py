from rest_framework import viewsets
from .models import *
from .serializers import *

class VaccineViewSet(viewsets.ModelViewSet):
	queryset = Vaccine.objects.all()
	serializer_class = VaccineSerializer

class DiseaseViewSet(viewsets.ModelViewSet):
	queryset = Disease.objects.all()
	serializer_class = DiseaseSerializer
