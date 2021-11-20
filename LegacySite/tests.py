from django.test import Client
from django.db import connection
from django.test import TestCase
from django.contrib.auth.models import User, AnonymousUser
from django.urls import reverse
import time

# Create your tests here.
# Please view: https://docs.djangoproject.com/en/3.2/topics/testing/overview/
class securityTest(TestCase):
    def setUp(self):
        cred = 'sk' + str(time.time()).split('.')[0]
        self.credentials = {'uname': cred, 'pword': cred, 'pword2':cred}
        self.client = Client()
        response = self.client.post('/register', self.credentials)
        print(response)


    def test_main(self):
        # test index page
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    # 1- Write the test confirming XSS vulnerability is fixed

    # 2- Write the test confirming CSRF vulnerability is fixed

    # 3- Write the test confirming SQL Injection attack is fixed
    def test_sql_injection(self):
        # register
        # response = self.client.post('/register/', self.credentials, follow=True)
        # self.assertEqual(response.status_code, 200)
        # login with username: sk4920 and password: sk4920
        response = self.client.post('/login/', self.credentials, follow=True)
        #self.assertEqual(response.status_code, 302)
        # use a card to steal administrator's password

        with open("./testcards/SQLinjection.gftcrd") as card:
            response = self.client.post("/use", {'card_data': card, 'card_supplied': True, 'card_fname': 'test'}, follow=True)
        #card = SimpleUploadedFile("./testcards/SQLinjection.gftcrd", 'application/octet-stream')
            self.assertEqual(response.status_code, 200)

