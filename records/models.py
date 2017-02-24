from django.db import models
from django.core.urlresolvers import reverse
from django.views.generic.edit import CreateView, UpdateView, DeleteView

class Pi(models.Model) :
    address = models.CharField(max_length=100)
    code = models.CharField(max_length=100)

    def get_absolute_url(self):
        return reverse('records:index')

    def __str__(self):
        return self.address + ' - ' + self.code

class Data(models.Model) :
    pi = models.ForeignKey(Pi, on_delete= models.CASCADE)
    date_time = models.CharField(max_length=50)
    raw_vol = models.CharField(max_length=50)
    las_vol = models.CharField(max_length=10)
    new_vol = models.CharField(max_length=10)
    cum_vol = models.CharField(max_length=50)
    status = models.CharField(max_length=10)

    def __str__(self):
        return self.date_time + ' - ' + str(self.pi.pk)

class Stuff(models.Model):
    month = models.IntegerField()
    lol = models.DecimalField(max_digits=5, decimal_places=1)