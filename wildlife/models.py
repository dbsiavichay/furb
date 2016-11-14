from __future__ import unicode_literals

from django.db import models

class Kind(models.Model):
	code = models.CharField(max_length=2)
	name = models.CharField(max_length=128)

	def __unicode__(self):
		return self.name

class Breed(models.Model):
	name = models.CharField(max_length=128)
	kind = models.ForeignKey(Kind)

	def __unicode__(self):
		return self.name

class Animal(models.Model):
	code = models.CharField(max_length=32)
	name = models.CharField(max_length=128)
	birthday = models.DateTimeField()
	primary_color = models.CharField(max_length=64)
	secondary_color = models.CharField(max_length=64, blank=True, null=True)
	gender = models.CharField(max_length=4)
	weight = models.DecimalField(max_digits=6, decimal_places=2)
	is_sterilized = models.BooleanField(default=False)
	contraindications = models.TextField(blank=True, null=True)
	owner = models.CharField(max_length=15)
	parish = models.CharField(max_length=6)
	breed = models.ForeignKey(Breed)

class AnimalVaccine(models.Model):
	animal = models.ForeignKey(Animal)
	vaccine = models.PositiveIntegerField()
	date = models.DateTimeField()

class AnimalDesease(models.Model):
	animal = models.ForeignKey(Animal)
	disease = models.PositiveIntegerField()
