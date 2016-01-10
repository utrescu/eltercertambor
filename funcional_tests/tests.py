# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class GlobalPageTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()


    def test_llista_les_competicions(self):
        # Quan algú arriba se li mostra una llista de competicions si no
        # posa cap número de competició...

        url = reverse('llista competicions')
        self.browser.get(self.live_server_url + url)

        # Mira que realment estem a la pàgina princial de competició
        self.assertIn('Competicions', self.browser.title)

        enllaz = self.browser.find_element_by_class_name('navbar-brand').get_attribute('href')
        self.assertEquals(self.live_server_url + '/competicio', enllaz)