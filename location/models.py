from __future__ import unicode_literals

from django.db import models

class Parish(models.Model):
    code = models.CharField(primary_key=True, max_length=16, db_column='prrcode')
    name = models.CharField(max_length=120, blank=True, null=True, db_column='prrdescri')
    canton_code = models.CharField(max_length=120, blank=True, null=True, db_column='cntcodigo')

    class Meta:
        managed = False
        db_table = 'parroquia'
        ordering = ['name',]

class Owner(models.Model):
    charter = models.CharField(primary_key=True, max_length=15, db_column='ctrcedula')
    name = models.CharField(max_length=120, blank=True, null=True, db_column='ctrnombre')
    address = models.CharField(max_length=60, blank=True, null=True, db_column='ctrdireccion')
    cellphone = models.CharField(max_length=20, blank=True, null=True, db_column='ctrcelular')
    telephone = models.CharField(max_length=20, blank=True, null=True, db_column='ctrtelefono')

    class Meta:
        managed = False
        db_table = 'contribuyentes'
        ordering = ['name',]
