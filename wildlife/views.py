from rest_framework import viewsets
from .models import *
from .serializers import *

class KindViewSet(viewsets.ModelViewSet):
	queryset = Kind.objects.all()
	serializer_class = KindSerializer
