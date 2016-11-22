#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.views.generic import CreateView, ListView
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.response import Response
from location.models import Owner, Parish
from .models import *
from .serializers import *

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, TableStyle, Table, Image
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER
from reportlab.lib.units import cm, mm
from io import BytesIO

class KindListView(ListView):
	model = Kind

class KindCreateView(CreateView):
	pass

class KindViewSet(viewsets.ModelViewSet):
	queryset = Kind.objects.all()
	serializer_class = KindSerializer

class BreedViewSet(viewsets.ModelViewSet):
	queryset = Breed.objects.all()
	serializer_class = BreedSerializer

	def get_queryset(self):
		queryset = self.queryset
		kind = self.request.query_params.get('kind', None)
		if kind is not None:
			queryset = queryset.filter(kind=kind)
		return queryset

class AnimalViewSet(viewsets.ModelViewSet):
	queryset = Animal.objects.all()
	serializer_class = AnimalSerializer

	def create(self, request):
		data = {attr: request.data[attr] for attr in request.data if attr!='csrfmiddlewaretoken'}
		parish = data['parish']
		gender = data['gender']
		data['breed'] = Breed.objects.get(pk=data['breed'])
		kind_id = data.pop('kind', None)
		kind = Kind.objects.get(pk=kind_id) if kind_id is not None else '';
		data['code'] = parish + gender + kind.code

		ans = Animal.objects.filter(parish=parish, gender=gender, breed__kind=kind).order_by('id')[:1]

		if(len(ans)>0):
			index = ''
			strnum = ans[0].code[9:]
			number = int(strnum)
			zerodigits = 6 - len(str(number))
			for i in range(0, zerodigits):
				index = index + '0';
			index = index + str(number+1);
			data['code']+=index;
		else:
			data['code']+='000001';

		animal = Animal.objects.create(**data)
		serializer = AnimalSerializer(animal)
		return Response(serializer.data)

def create_animal_report(request):
    # Create the HttpResponse object with the appropriate PDF headers.
	response = HttpResponse(content_type='application/pdf')
	response['Content-Disposition'] = 'inline; filename=padron.pdf'

	animal = request.GET.get('animal', None)

	pdf = None
	if animal is not None:
		pdf = pdf_animal_report(animal)

    # Get the value of the StringIO buffer and write it to the response.
	response.write(pdf)
	return response


def pdf_animal_report(id):
	animal = Animal.objects.get(pk=id)
	owner = Owner.objects.using('sim').get(pk=animal.owner)
	animal_parish = Parish.objects.using('sim').get(code=animal.parish)
	owner_parish = Parish.objects.using('sim').get(code=owner.parish)
	buff = BytesIO()
	doc = SimpleDocTemplate(buff,pagesize=A4,rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=20,)
	styles = getSampleStyleSheet()
	report = [Paragraph("FICHA DE FAUNA URBANA DEL CANTON MORONA", styles['Title']),]
	report.append(Paragraph('CODIGO: %s' % (animal.code,), styles['Heading2']))

	report.append(Paragraph('DATOS DEL PROPIETARIO', styles['Heading2']))

	table_content = [('Nombre:', owner.name, 'Direccion:', owner.address),]
	table_content.append(('Cedula:', owner.charter, 'Barrio:', owner.neighborhood))
	table_content.append(('Celular:', owner.cellphone, 'Parroquia:', owner_parish.name))
	table = Table(table_content)
	report.append(table)

	report.append(Paragraph('DATOS INFORMATIVOS DEL ANIMAL', styles['Heading2']))

	table_content2 = [('Especie:', animal.breed.kind.name, 'Color primario:', animal.primary_color),]
	table_content2.append(('Raza:', animal.breed.name, 'Color secundario:', animal.secondary_color))
	table_content2.append(('Nombre:', animal.name, 'Peso:', animal.weight))
	table_content2.append(('Fecha de nacimiento:', animal.birthday, 'Peso:', animal.weight))
	table_content2.append(('Residencia:', animal_parish.name, 'Esta esterilizado?:', 'SI' if animal.is_sterilized else 'NO'))
	table_content2.append(('Sexo:', 'HEMBRA' if animal.gender=='0' else 'MACHO', '', ''))
	table2 = Table(table_content2)
	report.append(table2)

	doc.build(report)
	return buff.getvalue()
