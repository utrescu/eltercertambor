# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.utils import timezone

from .models import Competicio, Prova, Usuari, UserResolutions
from .forms import CompeticioForm


class IndexView(generic.ListView):
    """
    Vista de la pàgina principal.

    Faig servir una classe per veure si entenc com ho fan. Però
    no sembla que m'aporti gaire res interessant...
    """
    model = Competicio
    template_name = 'home.html'
    context_object_name = 'latest_competition_list'

    def get_queryset(self):
        """Retorna les darreres cinc competicions"""
        return Competicio.objects.order_by('-id')[:5]

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['titol_competicio'] = 'Competicions'
        return context


# def principal(request):
#     latest_competition_list = Competicio.objects.order_by('-id')[:5]
#     return render(request, 'home.html', latest_competition_list)


@login_required
def nova_competicio(request):
    """
    Crear una nova competicio
    :param request:
    :return:
    """
    if request.method == 'POST':
        form = CompeticioForm(request.POST, request.FILES)
        if form.is_valid():
            # Comprovar que la competició no existia... (ho fa el formulari)

            # Crear la competicio
            nova = Competicio()
            nova.author = Usuari.objects.get(id=request.user.id)
            nova.text = form.cleaned_data['text']
            nova.imatge = form.cleaned_data['imatge']
            nova.save()

            # Redirigir a la llista de competicions
            return redirect(reverse('competicio', args=(nova.id,)))
        else:
            return HttpResponse('Repeticions no acceptades')

    return HttpResponse('allowed only via POST')


def llista_competicio(request, competicio_id):
    """
    Llista les proves de la competició especificada en el 'id'
    :param request:
    :param competicio_id:
    :return:
    """

    try:
        competicio = Competicio.objects.get(id=competicio_id)
    except ObjectDoesNotExist:
        return redirect('/')

    problemes = Prova.objects.filter(competicio_id=competicio_id)

    return render(request, 'competicio.html', {'titol_competicio': competicio,
                                               'imatge': competicio.imatge.url,
                                               'problemes': problemes})


@login_required
def valorar_prova(request, competicio_id, prova_id):
    """
    llista la prova que es demana i mostra o bé el quadre de text
    que demana quin és el resultat o si ja l'havia resposta li dóna
    el que havia respost.
    :param request:
    :param competicio_id:
    :param prova_id:
    :return:
    """

    # No permetre proves no existents
    try:
        prova_actual = Prova.objects.get(pk=prova_id)
    except Prova.DoesNotExist:
        raise Http404("Question does not exist")

    # Mirar si ja havia llegit l'enunciat
    usuari = Usuari.objects.get(id=request.user.id)
    solucio, _ = UserResolutions.objects.get_or_create(user=usuari, prova=prova_actual)

    if request.method == 'GET':
        return render(request, 'prova.html', {'titol_competicio': prova_actual.competicio.text,
                                              'prova': prova_actual,
                                              'origen': request.get_full_path().rsplit("/", 2)[0],
                                              'resolta': solucio.solucionat,
                                              'resposta': prova_actual.resposta
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
    """
    Comprova si la resposta proporcionada és la correcta
    i si ho emmagatzema (tant si està bé com si no)
    :param request:
    :param competicio_id:
    :param prova_id:
    :return:
    """

    resposta = request.session['resposta']
    try:
        resultat = UserResolutions.objects.get(user_id=request.user.id, prova_id=prova_id)
        if resultat.solucionat:
            resposta = resultat.prova.resposta
    except UserResolutions.DoesNotExist:
        raise Http404("Petició no correcta")

    return render(request, 'resultat.html',
                  {'encert': resultat.solucionat,
                   'prova': resultat.prova.text,
                   'resposta': resposta,
                   'origen': request.get_full_path().rsplit("/", 1)[0]
                   })


def estadistiques(request):
    """
    Mostra les estadístiques globals de la competició.
    :param request:
    :return:
    """
    return HttpResponse("Estadistiques")


def classificacio(request):
    """
    Mostra la classifació de la competició (els que l'han resolt primer
    per davant)
    :param request:
    :return:
    """
    return HttpResponse("Not done yet")
