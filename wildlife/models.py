#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime
from PIL import Image, ImageOps, ImageDraw
from django.db import models
from location.models import Parish

class Kind(models.Model):
	class Meta:
		ordering = ['code',]

	code = models.CharField(max_length=2)
	name = models.CharField(max_length=128)
	image = models.CharField(max_length=100)

	def __unicode__(self):
		return self.name

class Breed(models.Model):
	name = models.CharField(max_length=128)
	kind = models.ForeignKey(Kind)

	def __unicode__(self):
		return self.name

class Animal(models.Model):
	GENDER_CHOICES = (		
        ('F', 'Femenino'),
        ('M', 'Masculino'),        
    )

	PARISH_CHOICES = (
		(parish.code, parish.name) for parish in Parish.objects.filter(canton_code='1401')
	)

	code = models.CharField(max_length=32)
	name = models.CharField(max_length=128)
	birthday = models.DateField()
	primary_color = models.CharField(max_length=64)
	secondary_color = models.CharField(max_length=64, blank=True, null=True)
	gender = models.CharField(max_length=4, choices = GENDER_CHOICES)
	weight = models.DecimalField(max_digits=6, decimal_places=2)
	is_sterilized = models.BooleanField(default=False)
	is_vaccinated = models.BooleanField(default=False)
	want_sterilize = models.BooleanField(default=False)
	image = models.ImageField(upload_to='animals', blank=True, null=True)
	contraindications = models.TextField(blank=True, null=True)
	owner = models.CharField(max_length=15)
	parish = models.CharField(max_length=6, choices = PARISH_CHOICES)
	breed = models.ForeignKey(Breed)
	
	def age(self):
		birthday = str(self.birthday)[:10].split('-')
		diff = (datetime.now() - datetime(int(birthday[0]), int(birthday[1]), int(birthday[2]))).days
		years = int(diff/365)

		diffmonths = diff%365
		months = int(diffmonths/30)

		periods = (
			(years, "año", "años"),
			(months, "mes", "meses"),		    
		)

		age = ''
		for period, singular, plural in periods:
			if period >= 1:
				age +=  '%d %s ' % (period, singular if period == 1 else plural)

		return age

	def save(self, *args, **kwargs):
		super(Animal, self).save(*args, **kwargs)
		if self.image:
			process_image(self.image, 600)
		#circle_image(self.image)		


def process_image(image_field, size):		
		image = Image.open(image_field)
		width, height = image.size
		box = (0,0,width, height)
		if width > height:
			value = (width - height) / 2
			box = (value, 0, width - value, height)
		else:
			value = (height - width) / 2
			box = (0, value, width, height - value)
		cut_image = image.crop(box)
		new_size = cut_image.width
		if new_size > size:
			cut_image = cut_image.resize((size, size), Image.ANTIALIAS)		
		cut_image.save(image_field.path)

def circle_image(image_field):
	im = Image.open(image_field)
	bigsize = (im.size[0] * 3, im.size[1] * 3)
	mask = Image.new('L', bigsize, 0)
	draw = ImageDraw.Draw(mask) 
	draw.ellipse((0, 0) + bigsize, fill=255)
	mask = mask.resize(im.size, Image.ANTIALIAS)
	im.putalpha(mask)
	output = ImageOps.fit(im, mask.size, centering=(0.5, 0.5))
	output.putalpha(mask)
	output.save(image_field.path)