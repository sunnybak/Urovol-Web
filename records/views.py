from .models import Pi, Data
from django.views import generic
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, get_object_or_404

class IndexView(generic.ListView):
    template_name = 'records/index.html'
    context_object_name = 'all_pi'
    def get_queryset(self):
        return Pi.objects.all()[::-1]

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

