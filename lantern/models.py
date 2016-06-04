import base64
import uuid
import re
from django.db import models
from django.core.urlresolvers import reverse

class BuoyClient(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    url = models.URLField(max_length=200)
    link = models.CharField(max_length=200, default="") # can a malicious client use this default value collision for something?

    # locations
    country = models.CharField(max_length=200, default="")
    province = models.CharField(max_length=200, default="")
    city = models.CharField(max_length=200, default="")

    # what registrations are allowed?
    registrations = models.CharField(max_length=200, default="")

    # does the client support HTTPS?
    is_https = models.BooleanField(default=False)

    # number of users
    population = models.IntegerField(default=0)

    # add more fields for other pieces of client data

    def get_absolute_url(self):
        return reverse('client_info', args=[self.link])

    def save(self, *args, **kwargs):
        link_id = str(uuid.uuid4())
        self.link = base64.urlsafe_b64encode(link_id)
        super(BuoyClient, self).save(*args, **kwargs)
