# coding=utf-8
import urllib

from django.core.urlresolvers import resolve
from django.test import TestCase, Client, RequestFactory
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string
from django.http import HttpRequest

from competicio.models import Competicio
from competicio.views import *


USERNAME = 'pep'
ANONYMOUS = 'AnonymousUser'
PASSWORD = 'contrasenya'
PASSWORD_NO_CORRECTE = 'error'

TITOL_1 = 'Titol 1'
TITOL_2 = 'Titol 2'
RESPOSTA_CORRECTA = 'Correcta'
RESPOSTA_INCORRECTA = 'Incorrecta'

PRIMERA_COMPETICIO = 'Primera Competicio'
SEGONA_COMPETICIO = 'Segona Competicio'


def crearCompeticio(autor, nom):
    competicio1 = Competicio(author=autor)
    competicio1.text = nom
    competicio1.save()
    return competicio1

def crearProva(competicio, text):
    compe = Prova(competicio=competicio, titol = text,
                  resposta=RESPOSTA_CORRECTA, datainici=timezone.now())
    compe.save()
    return compe

class HomePageTest(TestCase):

    def test_arrel(self):
        """
        Comprova si s'arriba a la pàgina principal
        :return:
        """
        client = Client()
        response = client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

        # response = client.get(reverse('competicio:index'))
        # self.assertEqual(response.status_code, 200)
        # found = resolve('/')
        # self.assertEqual(found.func, principal)

    def test_competicio_page_correct(self):
        """
        Comprova si al carregar la pàgina principal
        s'obté el document correcte
        :return:
        """
        request = RequestFactory().get(reverse('index'))
        view = IndexView.as_view()
        # Run.
        resposta = view(request)

        # contingut = resposta.render()

        self.assertEqual(resposta.status_code, 200)
        # self.assertEqual(contingut.content, render_to_string('home.html'))
        # self.assertEqual(resposta.context_data['name'], name)

        # client = Client()
        # request = HttpRequest()
        # resposta = client.get(reverse('competicio:llista_competicio'))
        # expected_html = render_to_string('home.html')
        # self.assertEqual(resposta.content.decode(), expected_html)


class LlistaCompeticioTest(TestCase):

    def setUp(self):
        self.autor = Usuari()
        self.autor.save()
        crearCompeticio(self.autor, "Competicio per emplenar")

    def test_recupera_competicio_amb_id(self):
        """
        Comprova si es recupera la competició correcta
        en el cas en que existeixi
        :return:
        """
        competicio1 = crearCompeticio(self.autor, PRIMERA_COMPETICIO)

        request = HttpRequest()
        resposta = llista_competicio(request, competicio1.id)
        self.assertEqual(resposta.status_code, 200)
        self.assertIn(PRIMERA_COMPETICIO, resposta.content.decode())



    def test_recupera_competicio_amb_id_erroni(self):
        """
        Comprova si va a l'arrel quan es posa un ID que no existeix
        :return:
        """
        request = HttpRequest()
        resposta = llista_competicio(request, 2)
        self.assertEqual(resposta.status_code, 302)
        self.assertEqual(resposta['location'], '/')

    def test_recupera_competicio_amb_id_i_problemes(self):

        competicio1 = crearCompeticio(self.autor, PRIMERA_COMPETICIO)

        crearProva(competicio1, TITOL_1)
        crearProva(competicio1, TITOL_2)

        request = HttpRequest()
        resposta = llista_competicio(request, competicio1.id)
        self.assertIn(PRIMERA_COMPETICIO, resposta.content.decode())
        self.assertIn(TITOL_1, resposta.content.decode())
        self.assertIn(TITOL_2, resposta.content.decode())


class LoginTest(TestCase):

    def setUp(self):
        # Crear un usuari
        self.usuari = Usuari.objects.create_user(username=USERNAME, password=PASSWORD)
        # Crear una competició
        self.competicio = crearCompeticio(self.usuari, PRIMERA_COMPETICIO)
        # Afegir-li una prova
        self.prova = crearProva(self.competicio, TITOL_1)

    def test_usuari_correcte_pot_entrar(self):
        # Fer login
        self.client = Client()
        haEntrat = self.client.login(username=USERNAME, password=PASSWORD)
        self.assertTrue(haEntrat)

        # Anar a la pàgina d'inici
        url = reverse('index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_authenticated())
        # Comprovar si l'usuari és a la pàgina
        self.assertIn(USERNAME, response.content.decode())

    def test_usuari_i_contrasenya_incorrecta_no_entra(self):
        # Fer login
        self.client = Client()
        haEntrat = self.client.login(username=USERNAME, password=PASSWORD_NO_CORRECTE)
        self.assertFalse(haEntrat)
        # Anar a la pàgina d'inici (i pot fer-ho)
        url = reverse('index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_authenticated())
        # Però no està identificat
        self.assertIn(ANONYMOUS, response.content.decode())

class ProvaViewTest(TestCase):

    def setUp(self):
        # Crear un usuari
        self.usuari = Usuari.objects.create_user(username=USERNAME, password=PASSWORD)
        # Crear una competició
        self.competicio = crearCompeticio(self.usuari, PRIMERA_COMPETICIO)
        self.prova = crearProva(self.competicio, TITOL_1)

    def test_usuari_correcte_pot_entrar(self):
        # Fer login
        self.client = Client()
        haEntrat = self.client.login(username=USERNAME, password=PASSWORD)

        # Anar a la pàgina de la prova
        url = reverse('llista prova', args=(self.competicio.id,self.prova.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_usuari_correcte_resposta_suma(self):
        # Fer login
        self.client = Client()
        haEntrat = self.client.login(username=USERNAME, password=PASSWORD)

        # Enviar POST a la pàgina de la prova
        url = reverse('llista prova', args=(self.competicio.id,self.prova.id,))
        response = self.client.post(url,{'resultat': RESPOSTA_CORRECTA}, follow=True)
        expeted_url = reverse('resultat prova',args=(self.competicio.id,self.prova.id,))

        # És redirigit a la pàgina de resultats
        self.assertRedirects(response, expeted_url)

        #  - comprovar que ha creat un registre
        #  - comprovar que ha sumat un més


    def test_usuari_incorrecte_no_pot_entrar(self):
        # Fer login malament
        self.client = Client()
        haEntrat = self.client.login(username=USERNAME, password=PASSWORD_NO_CORRECTE)
        self.assertFalse(haEntrat)

        # Anar a la pàgina de la prova
        url = reverse('llista prova', args=(self.competicio.id,self.prova.id,))
        response = self.client.get(url, follow=True)
        # Es redirigeix a la pàgina de login perquè no està identificat
        expected_url = reverse('login') + "?next=" + urllib.quote(url, "")
        self.assertRedirects(response, expected_url)

class CompeticioModelTest(TestCase):

    def test_desa_i_recupera_competitions(self):
        """
        Comprova que es pot emmagatzemar i recuperar
        dades correctament
        :return:
        """
        autor = Usuari()
        autor.save()

        crearCompeticio(autor, PRIMERA_COMPETICIO)
        crearCompeticio(autor, SEGONA_COMPETICIO)

        desats = Competicio.objects.all()
        self.assertEqual(desats.count(), 2)

        self.assertEqual(desats[0].text, PRIMERA_COMPETICIO)
        self.assertEqual(desats[1].text, SEGONA_COMPETICIO)



