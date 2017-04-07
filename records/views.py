from .models import Pi, Data
from django.views import generic
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, get_object_or_404

def index(request):
    class piIndex(object):
        def __init__(self, pi):
            data = Data.objects.filter(pi=pi)
            self.id = pi.id
            self.code = pi.code
            self.address = pi.address
            self.len = len(data)
            if self.len != 0:
                self.latest = max(data, key=lambda d: d.date_time)
            else:
                self.latest = "N/A"
    all = []
    for pi in Pi.objects.all()[::-1]:
        all.append(piIndex(pi))
    return render(request, 'records/index.html', {'allpi': all })

def detail(request, pi_id):
    pi = get_object_or_404(Pi, pk=pi_id)
    dataset = Data.objects.filter(pi=pi, status="valid")
    return render(request, 'records/detail.html',{'pi': pi, 'dataset':dataset})

class PiCreate(generic.CreateView) :
    model = Pi
    fields = ['code', 'address']
    # automatically sends the fields to [model]_form.html

class PiUpdate(generic.UpdateView) :
    model = Pi
    fields = ['code', 'address']

class PiDelete(generic.DeleteView) :
    model = Pi
    success_url = reverse_lazy('records:index')

