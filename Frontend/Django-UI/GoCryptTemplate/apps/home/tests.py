# -*- encoding: utf-8 -*-
"""
Copyright (c) 2022 - present GoCrypt
"""

from django.test import TestCase
from django.urls import reverse
from apps.home.models import FavList

class cryptoCoinViewTest(TestCase):

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/cryptodetails.html/Bitcoin')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('cryptodetails', kwargs={'id':"Bitcoin"}))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('cryptodetails', kwargs={'id':"Bitcoin"}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/cryptodetails.html')

    def test_result_present(self):
        response = self.client.get(reverse('cryptodetails', kwargs={'id':"Bitcoin"}))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('apidata' in response.context)
        self.assertTrue('id' in response.context)
        self.assertTrue('SAPrediction' in response.context)
        self.assertTrue('LSTM' in response.context)

class marketListTest(TestCase):

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/portfolio.html')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('market'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('market'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/market.html')

    def test_result_present(self):
        response = self.client.get(reverse('market'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('apidata' in response.context)
        self.assertTrue('favarray' in response.context)

class portfolioTest(TestCase):

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/portfolio.html')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('portfolio'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('portfolio'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/portfolio.html')

    def test_result_present(self):
        response = self.client.get(reverse('portfolio'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('apidata' in response.context)
        self.assertTrue('favarray' in response.context)

class checkInFavTest(TestCase):
    
    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('checkinfavourites', kwargs={'crypto':"bitcoin"}))
        self.assertEqual(response.status_code, 200)

    def test_result_present(self):
        response = self.client.get(reverse('checkinfavourites', kwargs={'crypto':"bitcoin"}))
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'success': True, 'isFavourite': True})

class newsTest(TestCase):

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/index.html')
        self.assertEqual(response.status_code, 200)

    def test_result_present(self):
        response = self.client.get('/index.html')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('api' in response.context)
