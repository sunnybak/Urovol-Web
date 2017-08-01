from .models import Pi, Data
from django.views import generic
from django.views.generic import View
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import UserForm
from django.http import HttpResponseRedirect
from params import getParams, setParams


class const(object):
    def __init__(self, name, val, desc):
        self.n = name
        self.v = val
        self.d = desc

    @staticmethod
    def listOfConstants(p=None):
        if p is None:
            p = getParams()

        AVG, STD, LASTN, DIFF_MIN, DIFF_MAX, MULT, INTV = p

        # format: const([name], [default value], [description])
        consts = [const('AVG', AVG, "Average Threshold:"), const('STD', STD, "Standard Deviation Threshold:"),
                  const('LASTN', LASTN, "Number of running readings:"), const('DIFF_MIN', DIFF_MIN, "Min Difference:"),
                  const('DIFF_MAX', DIFF_MAX, "Max Difference:"), const('MULT', MULT, "Multiplier:"),
                  const('INTV', INTV, "Interval:")]

        return consts

def index(request):
    if request.user.is_authenticated:
        class piIndex(object):
            def __init__(self, pi):
                self.id = pi.id
                self.code = pi.code
                self.address = pi.address
                self.latest = ''
                self.len = ''

        all = [piIndex(pi) for pi in Pi.objects.order_by('code')]

        p = getParams()
        params = request.GET

        AVG = int(params.get('AVG', p[0]))
        STD = int(params.get('STD', p[1]))
        LASTN = int(params.get('LASTN', p[2]))
        DIFF_MIN = int(params.get('DIFF_MIN', p[3]))
        DIFF_MAX = int(params.get('DIFF_MAX', p[4]))
        MULT = float(params.get('MULT', p[5]))
        INTV = int(params.get('INTV', p[6]))
        setParams((AVG, STD, LASTN, DIFF_MIN, DIFF_MAX, MULT, INTV))

        consts = const.listOfConstants((AVG, STD, LASTN, DIFF_MIN, DIFF_MAX, MULT, INTV))

        return render(request, 'records/index.html', {'allpi': all, 'consts': consts})
    else:
        return HttpResponseRedirect("/records/login_user/")


def detail(request, pi_id):
    if request.user.is_authenticated:
        pi = get_object_or_404(Pi, pk=pi_id)
        dataset = Data.objects.filter(pi=pi, status="valid")
        return render(request, 'records/detail.html', {'pi': pi, 'dataset': dataset})
    else:
        return HttpResponseRedirect("/records/login_user/")


def simul(request, pi_id):
    if request.user.is_authenticated:
        consts = const.listOfConstants()
        cont = dict()
        cont['pi'] = get_object_or_404(Pi, pk=pi_id)

        for k in consts:
            k.v = request.POST.get(k.n, str(k.v))

        cont['consts'] = consts

        return render(request, 'records/simul.html', cont)
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




