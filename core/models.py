from django.db import models


class City(models.Model):
    external_id = models.IntegerField()
    name = models.CharField(max_length=255, db_index=True)
