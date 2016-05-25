from django.test import TestCase, RequestFactory
from lantern.models import BuoyClient
from uuid import uuid4
import json
import os
import mock

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
        self.assertContains(response, self.sample_data[0]['name'])
        self.assertContains(response, self.sample_data[1]['name'])

class ProcessClientDataViewTest(TestCase):
    def setUp(self):
        self.new_client_data_1 = self.from_file('json/new_client_data_1.json')
        self.new_client_data_2 = self.from_file('json/new_client_data_2.json') 
        self.existing_client_data_1 = self.from_file('json/existing_client_data_1.json')
        self.existing_client_data_2 = self.from_file('json/existing_client_data_2.json')

    def from_file(self, filename):
        filename = str("%s/%s" % (os.path.dirname(__file__), filename))
        data = open(filename, 'r').read()
        return data

    def test_new_json_with_id_returns_forbidden(self):
        client_data = '{"data": { "type": "client", "id": "d3efef58-80a7-4728-8cb6-257800fb630d", "attributes": { "name": "New Client With ID", "url": "https://testclient.fake/" } } }'
        response = self.client.post('/rod/', client_data, content_type='application/vnd.api+json')
        self.assertEqual(response.status_code, 403)

    def test_non_existent_attributes_return_bad_request(self):
        incorrect_data = self.from_file('json/incorrect_attributes.json')
        response = self.client.post('/rod/', incorrect_data, content_type='application/vnd.api+json')
        self.assertEqual(response.status_code, 400)

    def test_correct_new_json_replies_with_id(self):
        response_1 = self.client.post('/rod/', self.new_client_data_1, content_type='application/vnd.api+json')
        response_2 = self.client.post('/rod/', self.new_client_data_2, content_type='application/vnd.api+json')

        self.assertEqual(response_1.status_code, 201)
        self.assertEqual(response_2.status_code, 201)

        response_json_1 = json.loads(response_1.content)
        response_json_2 = json.loads(response_2.content)

        self.assertTrue('id' in response_json_1['data'])
        self.assertTrue('id' in response_json_2['data'])

    @mock.patch('lantern.views.BuoyClient', autospec=True)
    def test_correct_new_json_is_saved(self, mock_client):
        response_1 = self.client.post('/rod/', self.new_client_data_1, content_type='application/vnd.api+json')
        response_2 = self.client.post('/rod/', self.new_client_data_2, content_type='application/vnd.api+json')

        mock_client.return_value.save.assert_called_with()

    def test_correct_update_json_returns_404_if_not_existing(self):
        response_1 = self.client.patch('/rod/', self.existing_client_data_1, content_type='application/vnd.api+json')
        response_2 = self.client.patch('/rod/', self.existing_client_data_2, content_type='application/vnd.api+json')

        self.assertEqual(response_1.status_code, 404)
        self.assertEqual(response_2.status_code, 404)

    def test_correct_update_json_updates(self):
        client_data = json.loads(self.existing_client_data_1)
        client_id = client_data['data']['id']
        client_model = BuoyClient(id=client_id, name="test", url="test")
        client_model.save()

        response = self.client.patch('/rod/', self.existing_client_data_1, content_type='application/vnd.api+json')

        updated_model = BuoyClient.objects.get(id=client_id)

        self.assertEqual(response.status_code, 200)
        attributes = client_data['data']['attributes']
        self.assertEqual(attributes['name'], updated_model.name)
        self.assertEqual(attributes['url'], updated_model.url)
        self.assertEqual(attributes['country'], updated_model.country)
        self.assertEqual(attributes['province'], updated_model.province)
        self.assertEqual(attributes['city'], updated_model.city)
        self.assertEqual(attributes['registrations'], updated_model.registrations)
        self.assertEqual(attributes['is_https'], updated_model.is_https)
        self.assertEqual(attributes['population'], updated_model.population)

    def test_incorrect_type_gets_rejected(self):
        bad_type = self.from_file('json/bad_type.json')
        response = self.client.post('/rod/', bad_type, content_type='application/vnd.api+json')
        self.assertEqual(response.status_code, 409)

class ClientInfoViewTest(TestCase):
    def setUp(self):
        self.sample_data = [{'id': uuid4(), 'name': 'Test C1', 'url': 'https://test_url.fake/1'},
                            {'id': uuid4(), 'name': 'Test C2', 'url': 'https://test_url.fake/2'}]
        for d in self.sample_data:
            buoy = BuoyClient(d['id'], d['name'], d['url'])
            buoy.save()

    def test_uses_correct_template(self):
        response = self.client.get('/client')
        self.assertTemplateUsed('lantern/client.html')

    def test_client_urls_pass_correct_data_to_template(self):
        buoy = BuoyClient.objects.get(id=self.sample_data[0]['id'])
        client_url = buoy.get_absolute_url()
        response = self.client.get(client_url)
        self.assertContains(response, self.sample_data[0]['name'])
        self.assertContains(response, self.sample_data[0]['url'])
