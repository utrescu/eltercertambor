# coding=utf-8
import urllib
import os

try:
    from unittest import mock
except ImportError:
    import mock

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client, RequestFactory
from django.http import HttpRequest

from competicio.views import *

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

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

PATH_FILE = os.path.join(BASE_DIR, 'images/images/none.png')


def crear_usuari():
    Usuari.objects.create_user(username=USERNAME, password=PASSWORD)


def crear_competicio(autor, nom):
    competicio1 = Competicio(author=autor)
    competicio1.text = nom
    competicio1.save()
    return competicio1


def crear_prova(competicio, text):
    compe = Prova(competicio=competicio, titol=text,
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
        response = client.get(reverse('llista competicions'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

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
        request = RequestFactory().get(reverse('llista competicions'))
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

    # @classmethod
    # def setUpClass(cls):
    #     crearUsuari()

    def setUp(self):
        crear_usuari()
        self.autor = Usuari()
        self.autor.save()
        crear_competicio(self.autor, "Competicio per emplenar")

    def test_recupera_competicio_amb_id(self):
        """
        Comprova si es recupera la competició correcta
        en el cas en que existeixi
        :return:
        """
        competicio1 = crear_competicio(self.autor, PRIMERA_COMPETICIO)

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

    def test_recupera_competicio_amb_id_i_te_proves(self):

        competicio1 = crear_competicio(self.autor, PRIMERA_COMPETICIO)

        crear_prova(competicio1, TITOL_1)
        crear_prova(competicio1, TITOL_2)

        request = HttpRequest()
        resposta = llista_competicio(request, competicio1.id)
        self.assertIn(PRIMERA_COMPETICIO, resposta.content.decode())
        self.assertIn(TITOL_1, resposta.content.decode())
        self.assertIn(TITOL_2, resposta.content.decode())

    def test_formulari_correcte(self):
        """
        Comprovar que és correcte un formulari amb imatge i text
        :return:
        """
        post = {'text': PRIMERA_COMPETICIO}
        fitxer = {'imatge': SimpleUploadedFile(name='none2.png',
                                               content=open(PATH_FILE, 'rb').read(),
                                               content_type='image/png')}
        formulari = CompeticioForm(post, fitxer)
        self.assertTrue(formulari.is_valid())

    def test_formulari_sense_imatge_es_correcte(self):
        """
        Comprovar que accepta formularis sense imatge
        :return:
        """
        post = {'text': PRIMERA_COMPETICIO}
        fitxer = {'imatge': None}
        formulari = CompeticioForm(post, fitxer)
        self.assertTrue(formulari.is_valid())

    def test_formulari_sense_text_no_es_correcte(self):
        """
        Les competicions han de tenir nom
        :return:
        """
        post = {'text': ''}
        fitxer = {'imatge': None}
        formulari = CompeticioForm(post, fitxer)
        self.assertFalse(formulari.is_valid())

    def test_formulari_amb_text_repetit_no_es_correcte(self):
        """
        Comprova que no es poden crear competicions amb el mateix nom
        que un que ja existeix
        :return:
        """
        crear_competicio(self.autor, PRIMERA_COMPETICIO)
        post = {'text': PRIMERA_COMPETICIO}
        fitxer = {'imatge': None}
        formulari = CompeticioForm(post, fitxer)
        self.assertFalse(formulari.is_valid())

    def test_es_pot_crear_una_competicio(self):
        # Login
        self.client = Client()
        self.client.login(username=USERNAME, password=PASSWORD)
        # Creo una competició amb la vista
        text = PRIMERA_COMPETICIO
        imatge = None

        resposta = self.client.post(reverse("nova competicio"), {'text': text, 'imatge': imatge})

        self.assertEqual(resposta.status_code, 302)
        expected_url = reverse('competicio', args=(1,)).rsplit('/', 1)[1]
        self.assertIn(expected_url, resposta['location'])

        # self.assertFormError(response, 'form', 'some_field', 'This field is required.')

    def test_anonymous_no_crea_competicions(self):
        """
        Si no ha entrat cap usuari la part de crear competicions no funciona
        :return:
        """
        text = PRIMERA_COMPETICIO
        imatge = None
        expected_url = reverse('login') + "?next=" + urllib.quote(reverse("nova competicio"), "")

        resposta = self.client.post(reverse("nova competicio"), {'text': text, 'imatge': imatge}, follow=True)
        self.assertRedirects(resposta, expected_url)

        resposta = self.client.get(reverse("nova competicio"), follow=True)
        self.assertRedirects(resposta, expected_url)

    def test_no_es_pot_crear_la_mateixa_competicio_dos_cops(self):
        """
        Comprovem que si s'intenta crear una competició amb el mateix nom dues
        vegades no permet fer-la.
        :return:
        """
        # Creo la competició
        usuari = Usuari(username="tom")
        usuari.save()
        crear_competicio(usuari, PRIMERA_COMPETICIO)
        # Login
        self.client = Client()
        self.client.login(username=USERNAME, password=PASSWORD)
        # Creo una competició amb un nom que ja hi era
        text = PRIMERA_COMPETICIO
        imatge = None

        # No aconsegueixo capturar els Raises
        # with self.assertRaises(ValidationError):
        resposta = self.client.post(reverse("nova competicio"), {'text': text, 'imatge': imatge})
        self.assertContains(resposta, 'Repeticions no acceptades', status_code=200)


class LoginTest(TestCase):

    def setUp(self):
        # Crear un usuari
        crear_usuari()

    def test_usuari_correcte_pot_entrar(self):
        """
        Comprovar que l'usuari amb les credencials correctes pot entrar en el
        sistema i queda registrada en la plantilla
        :return:
        """
        # Fer login
        self.client = Client()
        haentrat = self.client.login(username=USERNAME, password=PASSWORD)
        self.assertTrue(haentrat)

        # Anar a la pàgina d'inici
        url = reverse('llista competicions')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_authenticated())
        # Comprovar si l'usuari és a la pàgina
        self.assertIn(USERNAME, response.content.decode())

    def test_usuari_i_contrasenya_incorrecta_no_entra(self):
        """
        Comprovar que si es falla la contrasenya si l'usuari va a la pàgina
        principal encara és anonymous
        :return:
        """
        # Fer login
        self.client = Client()
        haentrat = self.client.login(username=USERNAME, password=PASSWORD_NO_CORRECTE)
        self.assertFalse(haentrat)
        # Anar a la pàgina d'inici (i pot fer-ho)
        url = reverse('llista competicions')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_authenticated())
        # Però no està identificat
        self.assertIn(ANONYMOUS, response.content.decode())


class ProvaViewTest(TestCase):

    def setUp(self):
        # Crear un usuari
        crear_usuari()
        # Un usuari per crear una competició
        self.usuari = Usuari()
        self.usuari.save()
        # Crear una competició
        self.competicio = crear_competicio(self.usuari, PRIMERA_COMPETICIO)
        self.prova = crear_prova(self.competicio, TITOL_1)

    def test_no_es_pot_anar_a_proves_no_existents(self):
        """
        Comprovar que ningú pot accedir a una pàgina de proves que no existeixen
        :return:
        """
        self.client = Client()
        self.client.login(username=USERNAME, password=PASSWORD)
        # with self.assertRaises(Http404):
        url = reverse('llista prova', args=(self.competicio.id, 999999))
        resposta = self.client.get(url)
        self.assertEqual(resposta.status_code, 404)

    def test_usuari_correcte_pot_entrar(self):
        """
        Comprovar que un usuari que existeix pot entrar en el sistema i
        arribar a una pàgina de proves
        :return:
        """
        # Fer login
        self.client = Client()
        self.client.login(username=USERNAME, password=PASSWORD)

        # Anar a la pàgina de la prova
        url = reverse('llista prova', args=(self.competicio.id, self.prova.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_usuari_correcte_resposta_suma(self):
        """
        Comprovar que quan un usuari contesta una prova s'incrementa el valor
        dels intents en el registre
        :return:
        """
        # Fer login
        self.client = Client()
        self.client.login(username=USERNAME, password=PASSWORD)

        # Enviar POST a la pàgina de la prova
        url = reverse('llista prova', args=(self.competicio.id, self.prova.id,))
        response = self.client.post(url, {'resultat': RESPOSTA_CORRECTA}, follow=True)
        expeted_url = reverse('resultat prova', args=(self.competicio.id, self.prova.id,))

        # És redirigit a la pàgina de resultats
        self.assertRedirects(response, expeted_url)

        # TODO - comprovar que ha creat un registre
        # TODO - comprovar que ha sumat un més

    def test_usuari_incorrecte_no_pot_entrar(self):
        """
        Comprovar que no es pot entrar en una pàgina d'una prova si no
        s'ha fet login
        :return:
        """
        # Fer login malament
        self.client = Client()
        haentrat = self.client.login(username=USERNAME, password=PASSWORD_NO_CORRECTE)
        self.assertFalse(haentrat)

        # Anar a la pàgina de la prova
        url = reverse('llista prova', args=(self.competicio.id, self.prova.id,))
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

        crear_competicio(autor, PRIMERA_COMPETICIO)
        crear_competicio(autor, SEGONA_COMPETICIO)

        desats = Competicio.objects.all()
        self.assertEqual(desats.count(), 2)

        self.assertEqual(desats[0].text, PRIMERA_COMPETICIO)
        self.assertEqual(desats[1].text, SEGONA_COMPETICIO)



