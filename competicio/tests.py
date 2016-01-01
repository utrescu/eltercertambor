# coding=utf-8
from django.core.urlresolvers import resolve
from django.test import TestCase
from django.template.loader import render_to_string
from django.http import HttpRequest

from competicio.models import Competicio
from competicio.views import *

# Create your tests here.


class HomePageTest(TestCase):

    def test_arrel(self):
        """
        Comprova si s'arriba a la pàgina principal
        :return:
        """
        found = resolve('/')
        self.assertEqual(found.func, principal)


    def test_competicio_page_correct(self):
        """
        Comprova si al carregar la pàgina principal
        s'obté el document correcte
        :return:
        """
        request = HttpRequest()
        resposta = principal(request)
        expected_html = render_to_string('home.html')
        self.assertEqual(resposta.content.decode(), expected_html)

    def test_recupera_competicio_amb_id(self):
        """
        Comprova si es recupera la competició correcta
        en el cas en que existeixi
        :return:
        """
        competicio1 = Competicio()
        competicio1.text = 'Primera competicio'
        competicio1.save()

        request = HttpRequest()
        resposta = llista_competicio(request, competicio1.id)
        self.assertEqual(resposta.status_code, 200)
        self.assertIn('Primera', resposta.content.decode())


    def test_recupera_competicio_amb_id_erroni(self):
        """
        Comprova si va a l'arrel quan es posa un ID que no existeix
        :return:
        """
        request = HttpRequest()
        resposta = llista_competicio(request, 2)
        self.assertEqual(resposta.status_code, 302)
        self.assertEqual(resposta['location'], '/')

class CompeticioModelTest(TestCase):

    def test_desa_i_recupera_competitions(self):
        """
        Comprova que es pot emmagatzemar i recuperar
        dades correctament
        :return:
        """
        competicio1 = Competicio()
        competicio1.text = 'Primera competicio'
        competicio1.save()

        competicio2 = Competicio()
        competicio2.text = 'Segona competicio'
        competicio2.save()

        desats = Competicio.objects.all()
        self.assertEqual(desats.count(), 2)

        self.assertEqual(desats[0].text, 'Primera competicio')
        self.assertEqual(desats[1].text, 'Segona competicio')



