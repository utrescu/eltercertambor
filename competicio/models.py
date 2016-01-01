# -*- coding: utf-8 -*-
import datetime

from django.db import models
from django.utils import timezone

# Create your models here.

class Competicio(models.Model):
    competicio_text = models.CharField(max_length=200)
    competicio_imatge = models.ImageField(upload_to='images/',default='images/none.png')

    def __unicode__(self):
        return self.competicio_text
    
    def __str__(self):
        return self.competicio_text

#    vots = models.IntegerField(default=0)

class Prova(models.Model):
    competicio = models.ForeignKey(Competicio)
    prova_titol = models.CharField(max_length=200)
    prova_text = models.CharField(max_length=200)
    prova_resposta = models.CharField(max_length=200)
    prova_date = models.DateTimeField('date published')
    prova_intents = models.BigIntegerField()
    
    def isEnabled(self):
        return self.prova_date >= timezone.now()
    
    def __unicode__(self):
        return self.competicio + " " + self.prova_titol

    def __str__(self):
        return self.competicio + " " + self.prova_titol
