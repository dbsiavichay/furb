from __future__ import unicode_literals

from django.db import models

class Parish(models.Model):
    code = models.CharField(primary_key=True, max_length=6, db_column='prrcodigo')
    gencode = models.CharField(max_length=6, db_column='prrcode')
    name = models.CharField(max_length=120, blank=True, null=True, db_column='prrdescri')
    canton_code = models.CharField(max_length=120, blank=True, null=True, db_column='cntcodigo')

    class Meta:
        managed = False
        db_table = 'parroquia'
        ordering = ['name',]

class Owner(models.Model):
    PARISH_CHOICES = (
        (parish.code, parish.name) for parish in Parish.objects.filter(canton_code='1401')
    )

    charter = models.CharField(primary_key=True, max_length=15, db_column='ctrcedula')
    real_charter = models.CharField(primary_key=True,max_length=15, db_column='ctrcedulare')
    name = models.CharField(max_length=120, db_column='ctrnombre')
    address = models.CharField(max_length=60, db_column='ctrdireccion')
    cellphone = models.CharField(max_length=20, blank=True, null=True, db_column='ctrcelular')
    telephone = models.CharField(max_length=20, blank=True, null=True, db_column='ctrtelefono')
    neighborhood = models.CharField(max_length=20, blank=True, null=True, db_column='ctrbarrio')
    reference = models.TextField(blank=True, null=True, db_column='ctrreferencia')
    parish = models.CharField(max_length=16, db_column='prrcodigo', choices=PARISH_CHOICES)
    class Meta:
        managed = False
        db_table = 'contribuyentes'
        ordering = ['name',]
