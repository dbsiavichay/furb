#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.http import JsonResponse
from django.conf import settings
from os import listdir
from os.path import isfile, join
from django.views.generic import CreateView, ListView, UpdateView, DetailView
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
from PIL import Image as PilImage


from pure_pagination.mixins import PaginationMixin

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


class AnimalListView(PaginationMixin, ListView):
	model = Animal
	paginate_by = 12


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
	template_name = 'wildlife/animal_form_second_step.html'

	def get_context_data(self, **kwargs):		
		context = super(AnimalSecondStepView, self).get_context_data(**kwargs)		
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
		self.success_url = '/animal/%s/confirm/' % (self.object.id)
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

class AnimalThirdStepView(DetailView):
	model = Animal	
	success_url = '/animal/'
	template_name = 'wildlife/animal_confirm_third_step.html'	


def get_animal_report(request, pk):
    # Create the HttpResponse object with the appropriate PDF headers.
	response = HttpResponse(content_type='application/pdf')
	response['Content-Disposition'] = 'inline; filename=padron.pdf'

	pdf = pdf_animal_report(pk, request.user)

    # Get the value of the StringIO buffer and write it to the response.
	response.write(pdf)
	return response


def pdf_animal_report(pk, user):
	animal = Animal.objects.get(pk=pk)
	owner = Owner.objects.get(pk=animal.owner)
	animal_parish = Parish.objects.get(code=animal.parish)
	owner_parish = Parish.objects.get(code=owner.parish)
	buff = BytesIO()

	doc = SimpleDocTemplate(buff,pagesize=A4,rightMargin=60, leftMargin=40, topMargin=75, bottomMargin=20,)
	styles = getSampleStyleSheet()
	report = [
		Paragraph("DIRECCIÓN DE GESTION AMBIENTAL Y SERVICIOS PÚBLICOS", styles['Title']),
		Paragraph("REGISTRO DE FAUNA URBANA", styles['Title']),
	]

	spanc = styles['Heading1']
	spanc.alignment = TA_CENTER
	spanc.spaceAfter = 0;

	span = styles['Heading6']
	span.alignment = TA_CENTER
	span.spaceBefore = 0;
	span.fontSize = 10

	path = join(settings.BASE_DIR, 'static/assets/icons/')
	figure = [
		Paragraph(animal.name.upper(), styles['Title']),
		Image(animal.image.path if animal.image else path + animal.breed.kind.image, width=5*cm, height=5*cm),
		Paragraph(animal.code, spanc),
		Paragraph('Código', span),
	]
	

	table_content2 = [		
		(figure,'Especie', animal.breed.kind.name.upper()),
		(None,'Raza', animal.breed.name.upper()),
		(None,'Color primario', animal.primary_color.upper()),
		(None,'Color secundario', animal.secondary_color.upper()),
		(None,'Fecha de nacimiento', str(animal.birthday)[:10]),
		(None,'Edad', animal.age().upper()),
		(None,'Sexo', 'MASCULINO' if animal.gender=='M' else 'FEMENINO'),
		(None,'Peso (Kg)', animal.weight),
		(None,'Residencia', animal_parish.name.upper()),
		(None,'Vacunado?', 'SI' if animal.is_vaccinated else 'NO'),
		(None,'Esterilizado?', 'SI' if animal.is_sterilized else 'NO'),
	]

	table2 = Table(table_content2, [8*cm, 5*cm,4*cm],hAlign='RIGHT')

	table2.setStyle(
		TableStyle([			
			('SPAN',(0,0),(0,-1)),
			('ALIGN',(0,0),(0,-1),'CENTER'),
			('ALIGN',(2,0),(2,-1),'RIGHT'),
			('LINEBELOW',(1,0),(2,-1),0.1,colors.gray),
			('TOPPADDING',(0,0),(0,-1), 10),
			('TOPPADDING',(1,0),(2,-1), 10),
			('LEFTPADDING',(1,0),(1,-1), 0),
			('RIGHTPADDING',(2,0),(2,-1), 0),
			('VALIGN', (0, 0), (0, -1), 'TOP'),	
			('VALIGN', (1, 0), (1, -1), 'MIDDLE'),			
		])
	)
	report.append(table2)

	titleStyle = styles['Heading2']
	titleStyle.spaceBefore = 20

	report.append(Paragraph('DATOS DEL PROPIETARIO', titleStyle))

	tstyle = TableStyle([
			('LINEBELOW',(0,0),(-1,3),0.1,colors.gray),
			('LEFTPADDING',(0,0),(-1,-1), 0),
			('RIGHTPADDING',(0,0),(-1,-1), 0),	
	])

	pstyle = getSampleStyleSheet()['BodyText']
	pstyle.textColor = colors.gray
	pstyle.spaceAfter = 5

	cpropietario1 = [
		([Paragraph('', styles['BodyText']),Paragraph(owner.name.upper(), styles['BodyText'])],),
		([Paragraph('Nombre', pstyle),Paragraph(owner_parish.name.upper(), styles['BodyText'])],),
		([Paragraph('Parroquia', pstyle),Paragraph(owner.neighborhood.upper(), styles['BodyText'])],),
		([Paragraph('Barrio', pstyle),Paragraph(owner.address.upper(), styles['BodyText'])],),
		([Paragraph('Dirección', pstyle),Paragraph('', styles['BodyText'])],),
	]

	tablepropietario1 = Table(cpropietario1, style=tstyle)

	cpropietario2 = [
		([Paragraph('', pstyle),Paragraph(owner.charter, styles['BodyText'])],),
		([Paragraph('Cédula', pstyle),Paragraph(owner.telephone if owner.telephone else '---', styles['BodyText'])],),
		([Paragraph('Telefono', pstyle),Paragraph(owner.cellphone if owner.cellphone else '---', styles['BodyText'])],),
		([Paragraph('Celular', pstyle),Paragraph(owner.reference.upper() if owner.reference else '---', styles['BodyText'])],),
		([Paragraph('Referencia', pstyle),Paragraph('', styles['BodyText'])],),
	]
	tablepropietario2 = Table(cpropietario2, style=tstyle)

	
	table = Table([(tablepropietario1, tablepropietario2)])
	report.append(table)

	con = [
		('__________________________','__________________________'),
		(user.get_full_name(), owner.name.title()),
		('FUNCIONARIO MUNICIPAL', 'PROPIETARIO')
	]
	tfirmas = Table(con, spaceBefore=40)
	tfirmas.setStyle(
		TableStyle([						
			('ALIGN',(0,0),(-1,-1),'CENTER'),
			('RIGHTPADDING',(0,0),(0,-1), 30),
			('LEFTPADDING',(1,0),(1,-1), 30),
		])
	)
	report.append(tfirmas)


	doc.build(report, onFirstPage=get_letterhead_page,onLaterPages=get_letterhead_page)
	return buff.getvalue()


def get_letterhead_page(canvas, doc):
        # Save the state of our canvas so we can draw on it
		canvas.saveState()
		styles = getSampleStyleSheet()
		base_path = join(settings.BASE_DIR, 'static/assets/report/')

		escudo = Image(base_path + 'escudo_morona.png', width=6*cm,height=2*cm)
		logo = Image(base_path + 'logo_morona.jpg', width=2*cm,height=2*cm)
		aside = Image(base_path + 'aside.png', width=1*cm,height=10*cm)
		footer_caption = Image(base_path + 'footer-caption.png', width=6.5*cm,height=1.5*cm)
		footer_image = Image(base_path + 'footer-image.png', width=3*cm,height=1.5*cm)

		w, h = escudo.wrap(doc.width, doc.topMargin)
		escudo.drawOn(canvas, doc.leftMargin, doc.height + doc.topMargin - 60)

		w, h = logo.wrap(doc.width, doc.topMargin)
		logo.drawOn(canvas, doc.leftMargin + 480, doc.height + doc.topMargin - 60)

		w, h = aside.wrap(doc.width, doc.topMargin)
		aside.drawOn(canvas, doc.leftMargin + 510, doc.height + doc.topMargin - 375)
		
		w, h = footer_caption.wrap(doc.width, doc.topMargin)
		footer_caption.drawOn(canvas, doc.leftMargin, doc.height + doc.topMargin - 800)

		w, h = footer_image.wrap(doc.width, doc.topMargin)
		footer_image.drawOn(canvas, doc.leftMargin + 430, doc.height + doc.topMargin - 800)

        # Release the canvas
		canvas.restoreState()

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        """add page info to each page (page x of y)"""
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        self.setFont("Helvetica", 10)
        self.drawRightString(200*mm, 5*mm,
            "Pagina %d de %d" % (self._pageNumber, page_count))