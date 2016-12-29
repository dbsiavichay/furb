from __future__ import unicode_literals

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
        ('H', 'Hembra'),
        ('M', 'Macho'),        
    )

	PARISH_CHOICES = (
		(parish.code, parish.name) for parish in Parish.objects.filter(canton_code='1401')
	)

	code = models.CharField(max_length=32)
	name = models.CharField(max_length=128)
	birthday = models.DateTimeField()
	primary_color = models.CharField(max_length=64)
	secondary_color = models.CharField(max_length=64, blank=True, null=True)
	gender = models.CharField(max_length=4, choices = GENDER_CHOICES)
	weight = models.DecimalField(max_digits=6, decimal_places=2)
	is_sterilized = models.BooleanField(default=False)
	is_vaccinated = models.BooleanField(default=False)
	image = models.ImageField(upload_to='animals', blank=True, null=True)
	contraindications = models.TextField(blank=True, null=True)
	owner = models.CharField(max_length=15)
	parish = models.CharField(max_length=6, choices = PARISH_CHOICES)
	breed = models.ForeignKey(Breed)
