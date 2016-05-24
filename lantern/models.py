import uuid
from django.db import models

class BuoyClient(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    url = models.URLField(max_length=200)

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
