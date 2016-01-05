# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.utils import timezone
from .models import Competicio, Prova, Usuari, UserResolutions


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

    return render(request, 'competicio.html', {'titol_competicio': competicio, 'problemes': problemes})


@login_required
def valorar_prova(request, competicio_id, prova_id):

    try:
        prova_actual = Prova.objects.get(pk=prova_id)
    except Prova.DoesNotExist:
        raise Http404("Question does not exist")

    if request.method == 'GET':
        return render(request, 'prova.html', {'competicio': prova_actual.competicio.text,
                                              'prova': prova_actual,
                                              'origen': request.get_full_path().rsplit("/",2)[0]
                                              })
    elif request.method == 'POST':
        # Mirar si hi ha resposta ...
        usuari = Usuari.objects.get(id=request.user.id)
        solucio, _ = UserResolutions.objects.get_or_create(user=usuari, prova=prova_actual)
        solucio.intents += 1

        resposta_donada = request.POST.get("resultat", "")
        if prova_actual.resposta == resposta_donada:
            # Assignar el punt a l'usuari
            solucio.solucionat = True
            solucio.dataresolucio = timezone.now()

        solucio.save()
        request.session['resposta'] = resposta_donada
        return HttpResponseRedirect('resposta')


@login_required
def resultat_prova(request, competicio_id, prova_id):

    resposta = request.session['resposta']
    try:
        resultat = UserResolutions.objects.get(user_id=request.user.id, prova_id=prova_id)
        if (resultat.solucionat):
            resposta = resultat.prova.resposta
    except Prova.DoesNotExist:
        raise Http404("Petició no correcta")

    return render(request, 'resultat.html', {'encert':resultat.solucionat,
                                             'prova': resultat.prova.text,
                                             'resposta':resposta,
                                             'origen': request.get_full_path().rsplit("/",1)[0]
                                             })


def estadistiques(request):
    return HttpResponse("Estadistiques")


def classificacio(request):
    return HttpResponse("Not done yet")
