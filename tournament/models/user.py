from django.db import models


class User(models.Model):
    NAME_MAX_LENGTH = 20

    name = models.CharField(max_length=20)
