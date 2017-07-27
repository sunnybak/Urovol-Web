from django.shortcuts import render
from records.models import Data, Pi
from django.http import HttpResponse, Http404
import simplejson
from .algorithm import *


def index(request):
    return render(request, 'index.html')


def getData(pi):

    dataObjects = Data.objects.filter(pi=pi)

    if not dataObjects:
        raise Http404("Session does not exist")

    data = []

    for d in dataObjects:
        data.append([int((d.date_time * 1000) - 14400000), float(d.raw_vol)])

    return deepcopy(sorted(data, key=lambda x: x[0]))

def getNurseData(pi):

    dataObjects = Data.objects.filter(pi=pi, status="nurse")

    if not dataObjects:
        raise Http404("Session does not exist")

    data = []

    for d in dataObjects:
        data.append([int((d.date_time * 1000) - 14400000), float(d.raw_vol)])

    return deepcopy(sorted(data, key=lambda x: x[0]))

def params(request):
    params = request.GET
    pi = params.get('pi', 0)
    AVG = float(params.get('AVG', "50"))
    STD = int(params.get('STD', "9"))
    LASTN = int(params.get('LASTN', "6"))
    DIFF_MIN = int(params.get('DIFF_MIN', "-10"))
    DIFF_MAX = int(params.get('DIFF_MAX', "10000"))
    MULT = float(params.get('MULT', "0.9"))
    INTV = int(params.get('INTV', "300"))
    return alg(getData(pi), (AVG, STD, LASTN, DIFF_MIN, DIFF_MAX, MULT, INTV))


# raw data: blue graph
def chart_data_json(request):

    processed_array = getData(request.GET.get('pi', 0))

    return HttpResponse(simplejson.dumps(processed_array), content_type='application/json')


# the algorithm: black
def all_data_json(request):

    processed_array = params(request)

    return HttpResponse(simplejson.dumps(processed_array), content_type='application/json')
