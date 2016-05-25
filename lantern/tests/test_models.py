import uuid
from django.test import TestCase

from lantern.models import BuoyClient

class BuoyClientTest(TestCase):
    def setUp(self):
        client_id = uuid.uuid4()
        self.client = BuoyClient(id=uuid.uuid4(),
                                  name="Donkey Kong 64 was terrible",
                                  url="https://dk64.ssbm.warez")
        self.client.save()

    def test_get_slug(self):
        expected = "donkey-kong-64-was-terrible"
        self.assertEqual(self.client.slug, expected)
