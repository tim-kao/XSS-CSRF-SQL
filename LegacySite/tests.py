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
        self.assertEqual(response.status_code, 302)

    def test_main(self):
        # test index page
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    # 1- Write the test confirming XSS vulnerability is fixed
    def test_xss(self):
        embedInfo = "<script>alert('XSS');</script>"
        response = self.client.get('/buy', {'director': embedInfo})
        self.assertEqual(response.status_code, 200)
        content = response.content.decode("utf-8")
        self.assertIn("&lt;script&gt;alert(&#x27;XSS&#x27;);&lt;/script&gt;", content)

    # 2- Write the test confirming CSRF vulnerability is fixed
    def test_csrf(self):
        # buy a card to myself
        response = self.client.post('/gift/0', {'amount': ['44'], 'username': ['sk4920']})
        self.assertEqual(response.status_code, 200)
        content = response.content.decode("utf-8")
        self.assertNotIn('Card given to sk4920', content)
    # 3- Write the test confirming SQL Injection attack is fixed
    def test_sql_injection(self):
        response = self.client.post('/login/', self.credentials)
        self.assertEqual(response.status_code, 302)
        # use a card to steal administrator's password
        with open("./testcards/SQLinjection.gftcrd") as card:
            response = self.client.post("/use", {'card_data': card, 'card_supplied': True, 'card_fname': 'test'}, follow=True)
            self.assertEqual(response.status_code, 200)
            content = response.content.decode("utf-8")
            adminPassword = '000000000000000000000000000078d2$18821d89de11ab18488fdc0a01f1ddf4d290e198b0f80cd4974fc031dc2615a3'
            self.assertNotIn(adminPassword, content)

