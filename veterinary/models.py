from __future__ import unicode_literals

from django.db import models
from wildlife.models import Kind

class Vaccine(models.Model):
	name = models.CharField(max_length=64)
	kinds = models.ManyToManyField(Kind)

	def __unicode__(self):
		return self.name

class Disease(models.Model):
	name = models.CharField(max_length=128)
	kinds = models.ManyToManyField(Kind)

	def __unicode__(self):
		return self.name
