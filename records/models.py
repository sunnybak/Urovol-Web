from django.db import models
from django.core.urlresolvers import reverse
from datetime import datetime

class Pi(models.Model) :
    address = models.CharField(max_length=100)
    code = models.CharField(max_length=100)

    def get_absolute_url(self):
        return reverse('records:index')

    def __str__(self):
        return self.address + ' - ' + self.code

class Data(models.Model):
    pi = models.ForeignKey(Pi, on_delete=models.CASCADE)
    date_time = models.DecimalField(max_digits=12, decimal_places=1)
    raw_vol = models.DecimalField(max_digits=5, decimal_places=1)
    las_vol = models.DecimalField(max_digits=5, decimal_places=1)
    new_vol = models.DecimalField(max_digits=5, decimal_places=1)
    cum_vol = models.DecimalField(max_digits=5, decimal_places=1)
    status = models.CharField(max_length=10)

    def __str__(self):
        return datetime.fromtimestamp(self.date_time - 14400).strftime('%a %m/%d %I:%M:%S %p')