from django.shortcuts import get_object_or_404
from django.views.generic import DetailView
from django.http import JsonResponse
from django.forms.models import model_to_dict
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from suds.client import Client
from .models import *

class OwnerDetailView(DetailView):
	model = Owner
	pk_url_kwarg = 'charter'

	def get(self, request, *args, **kwargs):		
		self.object = self.get_object()
		data = model_to_dict(self.object)
		return JsonResponse(data)


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
