#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView
from wildlife.models import Animal
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

def get_by_parish(request, parish):
    # Create the HttpResponse object with the appropriate PDF headers.
	response = HttpResponse(content_type='application/pdf')
	response['Content-Disposition'] = 'inline; filename=reporte.pdf'

	sterilized = request.GET.get('sterilized', False)

	pdf = get_animal_by_parish_report(parish, sterilized)

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

	columns_width = [0.5*cm, 2.5*cm,1.3*cm,1.5*cm,1.6*cm,1.8*cm,1.7*cm,5*cm]

	headings = ('N°','NOMBRE','ESPECIE', 'PESO', 'VACUNADO?', 'ESTERILIZAR?', 'UBICACIÓN', 'PROPIETARIO')
	headings = (Paragraph(h, headingStyle) for h in headings)	

	content = [(
		Paragraph(str(index + 1), contentStyle),
		Paragraph(animal.name.title(), contentStyle),
		Paragraph(animal.breed.kind.name.title(), contentStyle),
		Paragraph('%s kg' % (animal.weight,), contentStyle),
		Image(path, width=2.5*mm, height=2.5*mm) if animal.is_vaccinated else Paragraph('', contentStyle),
		Image(path, width=2.5*mm, height=2.5*mm) if animal.want_sterilize else Paragraph('', contentStyle),
		Paragraph(animal.get_parish_name().title(), contentStyle),
		Paragraph(animal.get_owner_name().title(), contentStyle),

	) for index, animal in enumerate(animals)] if len(animals) else [('Sin datos.',)]

	table = Table([headings] + content, columns_width, style=tstyle, )
	report.append(table)
	doc.build(report,canvasmaker=NumberedCanvas,onFirstPage=get_letterhead_page,onLaterPages=get_letterhead_page)
	return buff.getvalue()