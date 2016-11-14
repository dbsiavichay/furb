from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from suds.client import Client
from .models import *
from .serializers import *

class ParishViewSet(viewsets.ModelViewSet):
	queryset = Parish.objects.using('sim').filter(canton_code='1401')
	serializer_class = ParishSerializer

class OwnerViewSet(viewsets.ModelViewSet):
	queryset = Owner.objects.using('sim').all()
	serializer_class = OwnerSerializer

	def create(self, request):
		data = {attr: request.data[attr] for attr in request.data if attr!='csrfmiddlewaretoken'}
		data['charter'] = data['real_charter']
		owner = Owner.objects.using('sim').create(**data)
		serializer = OwnerSerializer(owner)
		return Response(serializer.data)

	def update(self, request, pk=None):
		owner = get_object_or_404(self.queryset, pk=pk)
		owner.cellphone = request.data.get('cellphone', owner.cellphone)
		owner.parish = request.data.get('parish', owner.parish)
		owner.neighborhood = request.data.get('neighborhood', owner.neighborhood)
		owner.address = request.data.get('address', owner.address)
		owner.save()
		serializer = OwnerSerializer(owner)
		return Response(serializer.data)


@api_view(['GET',])
def search_charter(request, charter):
    if charter is None:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    response = get_data_registro_civil(charter)

    if response is None:
        return Response('Not found',status=status.HTTP_404_NOT_FOUND)

    return Response(response, status=status.HTTP_200_OK)

def get_data_registro_civil(cedula):
    url = 'http://webservice02.registrocivil.gob.ec:8080/WEBRegistroCivilUniversal/WSRegistroCivilConsulta?wsdl'
    user = 'amorona1'
    password = 'A1Cm0r$Na'
    proxy = {'http': '172.16.8.1:3128', 'https': '172.16.8.1:3128'}
    client = Client(url, proxy=proxy)
    result = client.service.BusquedaPorCedula(cedula, user, password)
    return result
