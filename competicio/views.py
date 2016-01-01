# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse

from .models import Competicio


def index(request):
    latest_competition_list = Competicio.objects.order_by('-id')[:5]
    output = ', '.join([p.competicio_text for p in latest_competition_list])
    return HttpResponse(output)


def competicio(request, competicio_id):
    return HttpResponse("Llista de problemes de la competicio %s" % competicio_id)


def prova(request, competicio_id, prova_id):
    return HttpResponse("competicio %s i pregunta %s." % (competicio_id, prova_id))


def estadistiques(request):
    return HttpResponse("Estadistiques")