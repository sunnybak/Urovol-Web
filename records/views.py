from django.http import HttpResponse
from .models import Pi, Data
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate, logout
from django.views.generic import View
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.http import Http404
from .forms import UserForm
from django.shortcuts import render, render_to_response
from chartit import DataPool, Chart


def records_view(request):
    #Step 1: Create a DataPool with the data we want to retrieve.
    patientdata = \
        DataPool(
           series=
            [{'options': {
               'source': Data.objects.all()},
              'terms': [
                'raw_vol',
                'cum_vol']}
             ])

    #Step 2: Create the Chart object
    cht = Chart(
            datasource = patientdata,
            series_options =
              [{'options':{
                  'type': 'line',
                  'stacking': False},
                'terms':{
                  'raw_vol': [
                    'cum_vol']
                  }}],
            chart_options =
              {'title': {
                   'text': 'cum_vol'},
               'xAxis': {
                    'title': {
                       'text': 'raw_vol'}}})

    #Step 3: Send the chart object to the template.
    return render_to_response('plot/plot.html',{'weatherchart': cht})

class IndexView(generic.ListView):
    template_name = 'records/index.html'
    context_object_name = 'all_pi'

    def get_queryset(self):
        return Pi.objects.all()

class DetailView(generic.DetailView) :
    model = Pi
    template_name = 'records/detail.html'

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

# class UserFormView(View) :
#     form_class = UserForm
#     template_name = 'records/registration_form.html'
#
#     def get(self, request):
#         form = self.form_class(None)
#         return render(request, self.template_name, {'form' : form})
#
#     def post(self, request):
#         form = self.form_class(request.POST)
#
#         if form.is_valid() :
#             user = form.save(commit=False)
#
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
#             user.set_password(password)
#             user.save()
#
#             user = authenticate(username=username, password=password)
#
#             if user is not None :
#                 if user.is_active :
#                     login(request, user)
#                     return redirect('records:index')
#
#         return render(request, self.template_name, {'form': form})



# def logout_user(request) :
#     logout(request)
#     form = UserForm(request.POST or None)
#     context = {
#         "form": form,
#     }
#     return render(request, 'records/login.html', context)

# def home(request) :
#     if request.method == "POST":
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(username=username, password=password)
#         if user is not None:
#             if user.is_active:
#                 login(request, user)
#                 all_pi = Pi.objects.filter(user=request.user)
#                 return render(request, 'records/home.html', {'all_pi': all_pi})
#             else:
#                 return render(request, 'records/home.html', {'error_message': 'Your account has been disabled'})
#         else:
#             return render(request, 'records/home.html', {'error_message': 'Invalid login'})
#     return render(request, 'records/home.html')

# def login_user(request):
#     if request.method == "POST":
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(username=username, password=password)
#         if user is not None:
#             if user.is_active:
#                 login(request, user)
#                 all_pi = Pi.objects.all()
#                 request.session['username'] = username
#                 return render(request, 'records/index.html', {'all_pi': all_pi})
#             else:
#                 return render(request, 'records/login.html', {'error_message': 'Your account has been disabled'})
#         else:
#             return render(request, 'records/login.html', {'error_message': 'Invalid login'})
#     return render(request, 'records/login.html')

# def formView(request):
#    if request.session.has_key('username'):
#        pass
#       # username = request.session['username']
#       # return render(request, 'index.html', {"username" : username})
#    else:
#       return render(request, 'login.html', {})

