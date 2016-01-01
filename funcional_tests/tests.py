# -*- coding: utf-8 -*-

from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)


    def tearDown(self):
        self.browser.quit()


    def test_llista_les_competicions(self):
        # Quan algú arriba se li mostra una llista de competicions si no
        # posa cap número de competició...
        self.browser.get(self.live_server_url)
        self.assertIn('Competicions', self.browser.title)

