from django.db import models


class Approvals(models.Model):
    name = models.CharField(max_length=50)
    license_number = models.CharField(max_length=10)
    description = models.CharField(max_length=100)
    picture = models.CharField()
