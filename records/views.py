from .models import Pi, Data
from django.views import generic
from django.views.generic import View
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import UserForm
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required


def index(request):
    if request.user.is_authenticated:
        class piIndex(object):
            def __init__(self, pi):
                self.id = pi.id
                self.code = pi.code
                self.address = pi.address
                # data = Data.objects.filter(pi=pi, status="valid")
                # self.len = len(data)
                # if self.len != 0:
                #     self.latest = max(data, key=lambda d: d.date_time)
                # else:
                #     self.latest = "N/A"
                self.len = ""
                self.latest = ""
        all = []
        for pi in Pi.objects.all()[::-1]:
            all.append(piIndex(pi))
        return render(request, 'records/index.html', {'allpi': all})
    else:
        return HttpResponseRedirect("/records/login_user/")


def detail(request, pi_id):
    if request.user.is_authenticated:
        pi = get_object_or_404(Pi, pk=pi_id)
        dataset = Data.objects.filter(pi=pi, status="valid")
        return render(request, 'records/detail.html',{'pi': pi, 'dataset':dataset})
    else:
        return HttpResponseRedirect("/records/login_user/")


def simul(request, pi_id):
    if request.user.is_authenticated:
        pi = get_object_or_404(Pi, pk=pi_id)
        a1 = request.POST.get('a1', "50")
        a2 = request.POST.get('a2', "1")
        s1 = request.POST.get('s1', "9")
        s2 = request.POST.get('s2', "9")
        n1 = request.POST.get('n1', "6")
        n2 = request.POST.get('n2', "6")
        real = request.POST.get('data', "")

        file = open('data.txt', 'w')
        file.write(real)
        file.close()
        return render(request, 'records/simul.html',{'pi': pi,'a1':a1,'a2':a2,'s1':s1,'s2':s2,'n1':n1,'n2':n2, 'real': real })
    else:
        return HttpResponseRedirect("/records/login_user/")


class PiCreate(generic.CreateView):
    model = Pi
    fields = ['code', 'address']
    # automatically sends the fields to [model]_form.html


class PiUpdate(generic.UpdateView):
    model = Pi
    fields = ['code', 'address']


class PiDelete(generic.DeleteView):
    model = Pi
    success_url = reverse_lazy('records:index')


# admin account:
# username: admsin
# email: ssb2189@columbia.edu
# pass: same as my email
class UserFormView(View):
    form_class = UserForm
    template_name = 'records/registration_form.html'

    # blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    # process the data
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            # saving temporarily
            user = form.save(commit=False)

            # cleaning the fields
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user.set_password(password)
            user.save()

            # returns User objects if correct credentials
            user = authenticate(username= username, password=password)

            if user is not None:

                if user.is_active:
                    login(request, user)

                    return redirect('records:index')


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return index(request)

            else:
                return render(request, 'records/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'records/login.html', {'error_message': 'Invalid login'})
    return render(request, 'records/login.html')


def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'records/login.html', context)




