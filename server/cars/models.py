from django.db import models


class Approvals(models.Model):
    name = models.CharField(max_length=50)
    license_number = models.CharField(max_length=10, null=True)
    description = models.CharField(max_length=100)
    picture = models.CharField(max_length=200)
    is_authorized = models.BooleanField(default=False)
    chat_id = models.CharField(max_length=50, null=True)