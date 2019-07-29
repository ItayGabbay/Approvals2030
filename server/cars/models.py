from django.db import models


class Approvals(models.Model):
    person_id = models.CharField(max_length=10)
    name = models.CharField(max_length=50)
    license_number = models.CharField(max_length=10)
