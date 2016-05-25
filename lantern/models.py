import uuid
import re
from django.db import models
from django.core.urlresolvers import reverse

class BuoyClient(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    url = models.URLField(max_length=200)
    slug = models.SlugField(max_length=40, default="")

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
        return reverse('client_info', args=[self.slug])

    def save(self, *args, **kwargs):
        slug = re.sub(r"[^\w]+", " ", self.name)
        slug = "-".join(slug.lower().strip().split())
        self.slug = slug
        super(BuoyClient, self).save(*args, **kwargs)
