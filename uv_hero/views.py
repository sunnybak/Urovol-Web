from django.shortcuts import render
from records.models import Data, Pi
from django.http import HttpResponse, Http404
import simplejson
from copy import deepcopy
import numpy as np
import time, datetime
from .algorithm import *


def index(request):
    return render(request, 'index.html')


def getData(pi):

    dataObjects = Data.objects.filter(pi=pi)

    if not dataObjects:
        raise Http404("Session does not exist")

    data = []

    for d in dataObjects:
        data.append([int((d.date_time * 1000) - 14400000), d.raw_vol])

    return deepcopy(sorted(data, key=lambda x: x[0]))


def params(request):
    params = request.GET
    pi = params.get('pi', 0)
    AVG = float(params.get('AVG', "50"))
    STD = int(params.get('STD', "9"))
    LASTN = int(params.get('lN', "6"))
    DIFF_MIN = int(params.get('MIN', "-10"))
    DIFF_MAX = int(params.get('MAX', "10000"))
    return alg(getData(pi), (AVG, STD, LASTN, DIFF_MIN, DIFF_MAX))


# raw data without processing
def chart_data_json(request):

    processed_array = params(request)

    return HttpResponse(simplejson.dumps(processed_array), content_type='application/json')


# the algorithm: black
def all_data_json(request):

    processed_array = params(request)

    return HttpResponse(simplejson.dumps(processed_array), content_type='application/json')


# real data upload
def real_data_json(request):

    file = open('./data.txt', 'r')
    text = file.readlines()
    data = [line.split('\t') for line in text]
    info = []
    for d in data:
        info.append([time.mktime(datetime.datetime.strptime(d[0], "%m/%d/%y %H:%M").timetuple())*1000,
                     round(float(d[-1].replace('\n', '')), 1)])

    return HttpResponse(simplejson.dumps(info), content_type='application/json')






