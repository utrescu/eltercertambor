# -*- coding: utf-8 -*-
import datetime

from django.db import models
from django.utils import timezone

# Create your models here.

class Competicio(models.Model):
    text = models.CharField(max_length=200)
    imatge = models.ImageField(upload_to='images/', default='images/none.png')

    def __unicode__(self):
        return self.text
    
    def __str__(self):
        return self.text

#    vots = models.IntegerField(default=0)


class Prova(models.Model):
    competicio = models.ForeignKey(Competicio)
    titol = models.CharField(max_length=200)
    text = models.TextField(default="prova")
    resposta = models.CharField(max_length=200)
    datainici = models.DateTimeField('date published')
    intents = models.BigIntegerField()
    
    def enabled(self):
        return True
        # return self.datainici >= timezone.now()
    
    def __unicode__(self):
        return self.competicio + " " + self.titol

    def __str__(self):
        return self.competicio + " " + self.titol
