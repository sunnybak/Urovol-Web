from django.shortcuts import render_to_response
from records.models import Data
from django.http import HttpResponse
import simplejson
from copy import deepcopy

def index(request):
    return render_to_response('index.html')

def chart_data_json(request):

    params = request.GET

    pi = params.get('pi', 0)

    dataObjects = Data.objects.filter(pi=pi, status="valid")

    data = []

    for d in dataObjects:
        data.append([int((d.date_time * 1000) - 14400000), d.cum_vol])

    data = deepcopy(sorted(data,key=lambda x: x[0]))

    return HttpResponse(simplejson.dumps(data),content_type='application/json')

