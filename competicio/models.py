# -*- coding: utf-8 -*-
import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class Usuari(AbstractUser):
    # followers = models.ManyToManyField('self', related_name='followees', symmetrical=False)
    pass


class Competicio(models.Model):
    author = models.ForeignKey(Usuari, related_name='competicions')
    text = models.CharField(max_length=200)
    imatge = models.ImageField(upload_to='images/', default='images/none.png')

    def __unicode__(self):
        return self.text
    
    def __str__(self):
        return self.text


class Prova(models.Model):
    """
    Exercici a fer en una determinada competició
    """
    competicio = models.ForeignKey(Competicio)
    titol = models.CharField(max_length=200)
    text = models.TextField(blank=True, null=True)
    resposta = models.CharField(max_length=200)
    datacreacio = models.DateField(auto_now_add=True)
    datamodificacio = models.DateField(auto_now=True)
    datainici = models.DateTimeField()
    intents = models.IntegerField(default=0)
    
    def enabled(self):
        return self.datainici <= timezone.now()

    def __unicode__(self):
        return self.competicio + " " + self.titol

    def __str__(self):
        return self.competicio + " " + self.titol


class UserResolutions(models.Model):
    """
    Classe per portar el compte de les proves que ha solucionat
    un determinat usuari
    """
    user = models.ForeignKey(Usuari)
    prova = models.ForeignKey(Prova)
    datacreacio = models.DateTimeField(auto_now_add=True)
    intents = models.BigIntegerField(default=0)
    dataresolucio = models.DateTimeField(null=True, blank=True)
    solucionat = models.BooleanField(default=False)

    def solved(self):
        return self.solucionat

    def __unicode__(self):
        return self.user.get_username() + ' ' + self.prova.id + ' : ' + self.solved()

    def __str__(self):
        return self.user.get_username() + ' ' + self.prova.id + ' : ' + self.solved()
