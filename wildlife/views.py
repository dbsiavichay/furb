#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.http import JsonResponse
from django.conf import settings
from os import listdir
from os.path import isfile, join
from django.views.generic import CreateView, ListView, UpdateView
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets
from rest_framework.response import Response
from location.models import Owner, Parish
from .models import *
from .forms import *
from .serializers import *
from django.shortcuts import render, redirect
from django.forms import modelform_factory



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
	model = Kind
	fields = '__all__'
	success_url = '/kind/'

	def get_context_data(self, **kwargs):
		path = join(settings.BASE_DIR, 'static/assets/icons/')
		icons = [f for f in listdir(path) if isfile(join(path, f))]

		context = super(KindCreateView, self).get_context_data(**kwargs)
		context['icons'] = icons
		context['action'] = 'crear'
		return context

class KindUpdateView(UpdateView):
	model = Kind
	fields = '__all__'
	success_url = '/kind/'

	def get_context_data(self, **kwargs):
		path = join(settings.BASE_DIR, 'static/assets/icons/')
		icons = [f for f in listdir(path) if isfile(join(path, f))]

		context = super(KindUpdateView, self).get_context_data(**kwargs)
		context['icons'] = icons
		context['action'] = 'editar'
		return context

class BreedListView(ListView):
	model = Breed

	def get(self, request, *args, **kwargs):
		if request.is_ajax():
			kind = request.GET.get('kind', None)			
			object_list = [{'id': obj.id, 'name': obj.name} for obj in self.model.objects.filter(kind=kind)]
			return JsonResponse(object_list, safe=False)
		else:
			return super(BreedListView, self).get(request, *args, **kwargs)

class BreedCreateView(CreateView):
	model = Breed
	fields = '__all__'
	success_url = '/breed/'

	def get_context_data(self, **kwargs):
		context = super(BreedCreateView, self).get_context_data(**kwargs)		
		context['action'] = 'crear'
		return context

class BreedUpdateView(UpdateView):
	model = Breed
	fields = '__all__'
	success_url = '/breed/'

	def get_context_data(self, **kwargs):
		path = join(settings.BASE_DIR, 'static/assets/icons/')
		icons = [f for f in listdir(path) if isfile(join(path, f))]

		context = super(BreedUpdateView, self).get_context_data(**kwargs)
		context['icons'] = icons
		context['action'] = 'editar'
		return context


class AnimalListView(ListView):
	model = Animal


def animal_first_step_view(request):
	context = {}
	OwnerForm = modelform_factory(Owner, fields = '__all__')

	if request.method == 'POST':		
		charter = request.POST.get('charter', None)
		form = OwnerForm(request.POST)
		if charter is not None:
			try:
				owner = Owner.objects.get(pk=charter)
				form.instance = owner
			except ObjectDoesNotExist:
				pass

		if form.is_valid():
			form.save()
			return redirect('/animal/add/step/2/?owner=%s' % (charter))
	else:
		form = OwnerForm()

	context['form'] = form
	return render(request, 'wildlife/animal_form_first_step.html', context)

class AnimalSecondStepView(CreateView):
	model = Animal
	form_class = AnimalForm
	success_url = '/animal/'
	template_name = 'wildlife/animal_form_second_step.html'

	def get_context_data(self, **kwargs):		
		context = super(AnimalSecondStepView, self).get_context_data(**kwargs)
		context['kinds'] = Kind.objects.all()
		context['owner'] = self.request.GET.get('owner')
		return context

	def form_valid(self, form):	    
		self.object = form.save(commit=False)

		parish = Parish.objects.get(pk=self.object.parish)
		ans = Animal.objects.filter(parish=self.object.parish, gender=self.object.gender, breed__kind=self.object.breed.kind).order_by('id')[:1]
		code = self.object.breed.kind.code + self.object.gender + parish.gencode

		if(len(ans)>0):
			index = ''
			strnum = ans[0].code[4:]
			number = int(strnum)
			zerodigits = 6 - len(str(number))
			for i in range(0, zerodigits):
				index = index + '0';
			index = index + str(number+1);
			code+=index;
		else:
			code+='000001';

		self.object.code = code
		self.object.save()
		return super(AnimalSecondStepView, self).form_valid(form)

class AnimalUpdateView(UpdateView):
	model = Animal
	form_class = AnimalForm
	success_url = '/animal/'
	template_name = 'wildlife/animal_form_second_step.html'

	def get_context_data(self, **kwargs):		
		context = super(AnimalUpdateView, self).get_context_data(**kwargs)
		context['kinds'] = Kind.objects.all()
		context['owner'] = self.request.GET.get('owner')
		return context

	







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
