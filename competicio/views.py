# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, Http404
from django.views import generic
from .models import Competicio, Prova

class IndexView(generic.ListView):

    model = Competicio
    template_name = 'home.html'
    context_object_name = 'latest_competition_list'

    def get_queryset(self):
        """Retorna les darreres cinc competicions"""
        return Competicio.objects.order_by('-id')[:5]



# def principal(request):
#     latest_competition_list = Competicio.objects.order_by('-id')[:5]
#     return render(request, 'home.html', latest_competition_list)


def llista_competicio(request, competicio_id):

    try:
        competicio = Competicio.objects.get(id=competicio_id)
    except ObjectDoesNotExist:
        return redirect('/')

    problemes = Prova.objects.filter(competicio_id=competicio_id)

    return render(request, 'competicio.html', {'competicio': competicio, 'problemes': problemes})


def prova(request, competicio_id, prova_id):

    Prova.objects.get(pk=prova_id)

    try:
        prova = Prova.objects.get(pk=prova_id)
    except Prova.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'competicio.html', {'prova': prova})



def estadistiques(request):
    return HttpResponse("Estadistiques")


def classificacio(request):
    return HttpResponse("Not done yet")
