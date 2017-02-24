from __future__ import unicode_literals

from django.db import models
from records.models import Data,Pi

# Create your models here.

class Stuff(models.Model):
    month = models.IntegerField()
    happiness = models.DecimalField(max_digits=5, decimal_places=1)
