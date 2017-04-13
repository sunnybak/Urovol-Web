from .models import Pi, Data
from django.views import generic
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, get_object_or_404

def index(request):
    class piIndex(object):
        def __init__(self, pi):
            data = Data.objects.filter(pi=pi, status="valid")
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

def simul(request, pi_id):
    pi = get_object_or_404(Pi, pk=pi_id)
    a1 = request.POST.get('a1', "50")
    a2 = request.POST.get('a2', "50")
    s1 = request.POST.get('s1', "9")
    s2 = request.POST.get('s2', "9")
    n1 = request.POST.get('n1', "6")
    n2 = request.POST.get('n2', "6")
    real = request.POST.get('data', "")

    file = open('data.txt', 'w')
    file.write(real)
    file.close()
    return render(request, 'records/simul.html',{'pi': pi,'a1':a1,'a2':a2,'s1':s1,'s2':s2,'n1':n1,'n2':n2, 'real': real })

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
