from django.test import TestCase, RequestFactory
from lantern.models import BuoyClient
from uuid import uuid4
import json
import os

class HomeViewTest(TestCase):
    def setUp(self):
        self.sample_data = [{'id': uuid4(), 'name': 'test_c1', 'url': 'https://test_url.fake/1'},
                            {'id': uuid4(), 'name': 'test_c2', 'url': 'https://test_url.fake/2'}]
        for d in self.sample_data:
            client = BuoyClient(d['id'], d['name'], d['url'])
            client.save()

    def test_root_url_uses_correct_template(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('lantern/index.html')

    def test_nonexistent_url_returns_404(self):
        response = self.client.get('/this_url_does_not_go_anywhere')
        self.assertEqual(response.status_code, 404)

    def test_gets_client_list(self):
        response = self.client.get('/')
        # assert that clients are in html 
        self.assertContains(response, self.sample_data[0]['id'])
        self.assertContains(response, self.sample_data[1]['id'])

"""
class ProcessClientDataViewTest(TestCase):
    def setUp(self):
        self.new_client_data_1 = self.from_file('json/new_client_data_1.json')
        self.new_client_data_2 = self.from_file('json/new_client_data_2.json') 
        self.existing_client_data_1 = self.from_file('json/existing_client_data_1.json')
        self.existing_client_data_2 = self.from_file('json/existing_client_data_2.json')

    def from_file(self, filename):
        filename = str("%s/%s" % (os.path.dirname(__file__), filename))
        with open(filename, 'r') as f:
            data = json.load(f)
        return data

    def test_correct_json_gets_added(self):
        pass    

    def test_incorrect_type_gets_rejected(self):
        bad_type = self.from_file('json/bad_type.json')
        print bad_type
        response = self.client.post('/rod/', bad_type, content_type='application/vnd.api+json')
        self.assertEqual(response.status_code, 409)
"""

class ClientInfoViewTest(TestCase):
    def setUp(self):
        self.sample_data = [{'id': uuid4(), 'name': 'test_c1', 'url': 'https://test_url.fake/1'},
                            {'id': uuid4(), 'name': 'test_c2', 'url': 'https://test_url.fake/2'}]
        for d in self.sample_data:
            client = BuoyClient(d['id'], d['name'], d['url'])
            client.save()

    def test_uses_correct_template(self):
        response = self.client.get('/client')
        self.assertTemplateUsed('lantern/client.html')

    def test_uuid_urls_pass_correct_data_to_template(self):
        client_url = str("/client/%s/" % self.sample_data[0]['id'])
        response = self.client.get(client_url)
        self.assertContains(response, self.sample_data[0]['name'])
        self.assertContains(response, self.sample_data[0]['url'])
