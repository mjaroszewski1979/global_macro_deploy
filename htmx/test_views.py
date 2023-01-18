from django.test import TestCase, Client
from django.urls import reverse, resolve

from . import views


class GlobalMacroTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_home_url_is_resolved(self):
        url = reverse('htmx:home')
        self.assertEquals(resolve(url).func, views.home)

    def test_home_get(self):
        response = self.client.get(reverse('htmx:home'))
        self.assertContains(response, 'Global Macro | Home', status_code=200)
        self.assertTemplateUsed(response, 'home.html')

    def test_gini_url_is_resolved(self):
        url = reverse('htmx:gini')
        self.assertEquals(resolve(url).func, views.gini)

    def test_gini_get(self):
        response = self.client.get(reverse('htmx:gini'))
        self.assertContains(response, 'Global Macro | Gini Index', status_code=200)
        self.assertTemplateUsed(response, 'gini.html')
        self.assertTemplateUsed(response, 'partials/chart.html')
        self.assertIsNotNone(response.context['script'])
        self.assertIsNotNone(response.context['div'])
        self.assertIsNotNone(response.context['years'])

    def test_cpi_url_is_resolved(self):
        url = reverse('htmx:cpi')
        self.assertEquals(resolve(url).func, views.cpi)

    def test_cpi_get(self):
        response = self.client.get(reverse('htmx:cpi'))
        self.assertContains(response, 'Global Macro | CPI Index', status_code=200)
        self.assertTemplateUsed(response, 'cpi.html')
        self.assertTemplateUsed(response, 'partials/chart.html')
        self.assertIsNotNone(response.context['script'])
        self.assertIsNotNone(response.context['div'])
        self.assertIsNotNone(response.context['inputs'])

    def test_stock_url_is_resolved(self):
        url = reverse('htmx:stock')
        self.assertEquals(resolve(url).func, views.stock)

    def test_stock_get(self):
        response = self.client.get(reverse('htmx:stock'))
        self.assertContains(response, 'Global Macro | Stock Index', status_code=200)
        self.assertTemplateUsed(response, 'stock.html')
        self.assertTemplateUsed(response, 'partials/chart.html')
        self.assertIsNotNone(response.context['script'])
        self.assertIsNotNone(response.context['div'])
        self.assertIsNotNone(response.context['inputs'])

    def test_handler404(self):
        response = self.client.get('/some_url/')
        self.assertContains(response, 'Global Macro | Page not found', status_code=404)
        self.assertTemplateUsed(response, '404.html')

    




