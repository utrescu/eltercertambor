# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse

from .models import Competicio


def principal(request):
    latest_competition_list = Competicio.objects.order_by('-id')[:5]
    return render(request, 'home.html', latest_competition_list)


def llista_competicio(request, competicio_id):

    try:
        competicio = Competicio.objects.get(id=competicio_id)
    except ObjectDoesNotExist:
        return redirect('/')

    problemes = []

    return render(request, 'competicio.html', {'competicio': competicio, 'problemes': problemes})


def prova(request, competicio_id, prova_id):
    return HttpResponse("competicio %s i pregunta %s." % (competicio_id, prova_id))


def estadistiques(request):
    return HttpResponse("Estadistiques")


def classificacio(request):
    return HttpResponse("Not done yet")
