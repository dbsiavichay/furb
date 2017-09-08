#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView, TemplateView
from wildlife.models import Animal, Kind
from location.models import Parish

from django.conf import settings
from os.path import isfile, join

from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, TableStyle, Table, Image
from reportlab.lib.units import cm, mm

from wildlife.views import get_letterhead_page, NumberedCanvas

class ParishListView(ListView):
	model = Parish
	template_name = 'reports/animal_by_parish.html'
	queryset = Parish.objects.filter(canton_code='1401')

class StatsListView(ListView):
	model = Parish
	template_name = 'reports/animal_stats.html'
	queryset = Parish.objects.filter(canton_code='1401')

	def get_context_data(self, **kwargs):
		from datetime import date
		context = super(StatsListView, self).get_context_data(**kwargs)
		
		years = range(2017, date.today().year + 1)
		months = [
			(1, 'ENERO'),
			(2, 'FEBRERO'),
			(3, 'MARZO'),
			(4, 'ABRIL'),
			(5, 'MAYO'),
			(6, 'JUNIO'),
			(7, 'JULIO'),
			(8, 'AGOSTO'),
			(9, 'SEPTIEMBRE'),
			(10, 'OCTUBRE'),
			(11, 'NOVIEMBRE'),
			(12, 'DICIEMBRE'),
		]
		context.update({
			'months': months,
			'years':years,
		})

		return context

def get_by_parish(request, parish):
    # Create the HttpResponse object with the appropriate PDF headers.
	response = HttpResponse(content_type='application/pdf')
	response['Content-Disposition'] = 'inline; filename=reporte.pdf'

	sterilized = request.GET.get('sterilized', False)

	pdf = get_animal_by_parish_report(parish, sterilized)

	response.write(pdf)
	return response

def get_animal_stats(request, month, year):
    # Create the HttpResponse object with the appropriate PDF headers.
	response = HttpResponse(content_type='application/pdf')
	response['Content-Disposition'] = 'inline; filename=reporte.pdf'

	pdf = get_chart_by_month(month, year)

	response.write(pdf)
	return response

def get_animal_by_parish_report(parish, sterilized):
	animals = Animal.objects.filter(parish=parish).order_by('owner')
	if sterilized: animals = animals.filter(want_sterilize=True)
	buff = BytesIO()

	doc = SimpleDocTemplate(buff,pagesize=A4,rightMargin=60, leftMargin=40, topMargin=75, bottomMargin=50,)
	styles = getSampleStyleSheet()

	path = join(settings.BASE_DIR, 'static/assets/report/checked.png')

	report = [
		Paragraph("DIRECCIÓN DE GESTION AMBIENTAL Y SERVICIOS PÚBLICOS", styles['Title']),
		Paragraph("REPORTE DE FAUNA POR PARROQUIA", styles['Title']),
	]

	tstyle = TableStyle([
		('LINEBELOW',(0,0),(-1,-1),0.1,colors.gray),
		('TOPPADDING',(0,0),(-1,-1), 5),
		('BOTTOMPADDING',(0,0),(-1,-1), 0),
		('LEFTPADDING',(0,0),(-1,-1), 0),
		('RIGHTPADDING',(0,0),(-1,-1), 0),	
		('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
	])

	# tstyle = TableStyle([
	# 	('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
	# 	('LEFTPADDING',(0,0),(-1,-1), 3),
	# 	('RIGHTPADDING',(0,0),(-1,-1), 3),
	# 	('BOTTOMPADDING',(0,0),(-1,-1), 0),
	# 	('BOX', (0, 0), (-1, -1), 0.5, colors.black),
	# 	('ALIGN',(0,0),(0,-1),'RIGHT'),
	# 	('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
	# 	('BACKGROUND', (0, 0), (-1, 0), colors.gray)
	# ])

	headingStyle = styles['Heading5']
	headingStyle.fontSize = 6

	contentStyle = styles['BodyText']
	contentStyle.fontSize = 5

	columns_width = [0.5*cm, 1.4*cm, 2.5*cm,1.2*cm,1.8*cm,1.5*cm,4.5*cm,3*cm]

	headings = ('N°', 'CÓDIGO', 'NOMBRE','ESPECIE', 'ESTERILIZAR?', 'UBICACIÓN', 'PROPIETARIO', 'CONTACTO')
	headings = (Paragraph(h, headingStyle) for h in headings)	

	content = [(
		Paragraph(str(index + 1), contentStyle),
		Paragraph(animal.code, contentStyle),		
		Paragraph(animal.name.title(), contentStyle),
		Paragraph(animal.breed.kind.name.title(), contentStyle),
		Image(path, width=2.5*mm, height=2.5*mm) if animal.want_sterilize else Paragraph('', contentStyle),
		Paragraph(animal.get_parish_name().title(), contentStyle),
		Paragraph(animal.get_owner_name().title(), contentStyle),
		Paragraph(animal.get_owner_contact().title(), contentStyle),

	) for index, animal in enumerate(animals)] if len(animals) else [('Sin datos.',)]

	table = Table([headings] + content, columns_width, style=tstyle, )
	report.append(table)
	doc.build(report,canvasmaker=NumberedCanvas,onFirstPage=get_letterhead_page,onLaterPages=get_letterhead_page)
	return buff.getvalue()

def get_chart_by_month(month, year):
	buff = BytesIO()

	months = [
		'ENERO','FEBRERO','MARZO','ABRIL',
		'MAYO','JUNIO','JULIO','AGOSTO',
		'SEPTIEMBRE','OCTUBRE','NOVIEMBRE','DICIEMBRE',	
	]

	doc = SimpleDocTemplate(buff,pagesize=A4,rightMargin=60, leftMargin=40, topMargin=75, bottomMargin=50,)
	styles = getSampleStyleSheet()
	
	report = [
		Paragraph("DIRECCIÓN DE GESTION AMBIENTAL Y SERVICIOS PÚBLICOS", styles['Title']),
		Paragraph('REPORTE ESTADISTICO %s %s' % (months[int(month)-1],year), styles['Title']),
	]

	parishes = Parish.objects.filter(canton_code='1401')
	kinds = Kind.objects.all()
		

	for kind in kinds:
		_animals = Animal.objects.filter(
			breed__kind=kind,
			date_joined__year = int(year),
			date_joined__month = int(month)
		)
		
		data = []
		labels = []
		for parish in parishes:
			animals = _animals.filter(parish=parish.code)
			if len(animals) > 0:
				percent = (len(animals) * 100.00) / len(_animals)
				data.append(len(animals))
				labels.append('%s (%0.2f%%)' % (parish.name.encode('utf-8'), percent))

		if len(data) > 0:
			report.append(Paragraph(kind.name, styles['Heading3']))
			chart = create_pie_chart(data, labels, True)			
			report.append(chart)
	
	doc.build(report,canvasmaker=NumberedCanvas,onFirstPage=get_letterhead_page,onLaterPages=get_letterhead_page)
	return buff.getvalue()

colors = [
	colors.HexColor('#7fffd4'),
	colors.HexColor('#0000ff'),        
	colors.HexColor('#a52a2a'),
	colors.HexColor('#ff7f50'),	
	colors.HexColor('#a9a9a9'),
	colors.HexColor('#008b8b'),
	colors.HexColor('#8b0000'),        
	colors.HexColor('#ff00ff'),
	colors.HexColor('#00008b'),         
	colors.HexColor('#008000'),
	colors.HexColor('#adff2f'),                         
	colors.HexColor('#00ff00'),          
	colors.HexColor('#ff00ff'),
	colors.HexColor('#ffa500'),        
	colors.HexColor('#ff0000'),
	colors.HexColor('#ee82ee'),
	colors.HexColor('#ffff00'),
]

def add_legend(draw_obj, chart, data):
	from reportlab.graphics.charts.legends import Legend	
	from reportlab.lib.validators import Auto
    
	legend = Legend()
	legend.alignment = 'right'
	legend.x = 90
	legend.y = 50
	legend.colorNamePairs = [(chart.slices[i].fillColor, (chart.labels[i].split('(')[0], '%s' % chart.data[i])) for i in range(0, len(data))]
	draw_obj.add(legend)

def create_pie_chart(data, labels, legend=False):
	from reportlab.graphics.charts.piecharts import Pie
	from reportlab.graphics.shapes import Drawing

	d = Drawing(250, 275)
	pie = Pie()
	# required by Auto
	pie._seriesCount = len(data)
 
	
 
	pie.x = 175
	pie.y = 100
	pie.width = 150
	pie.height = 150
	pie.data = data
	pie.labels = labels
	pie.simpleLabels = 0
	pie.sideLabels = True    
	pie.slices.strokeWidth = 0.5

	for i in range (0, len(colors)):
		pie.slices[i].fillColor = colors[i]

	if legend:
		add_legend(d, pie, data)

	d.add(pie)

	#d.save(formats=['pdf'], outDir='.', fnRoot='test-pie')
	return d
    