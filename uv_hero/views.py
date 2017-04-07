from django.shortcuts import render_to_response
from records.models import Data, Pi
from django.http import HttpResponse
import simplejson
from copy import deepcopy

def index(request):
    return render_to_response('index.html')

def chart_data_json(request):

    params = request.GET

    pi = params.get('pi', 0)

    dataObjects = Data.objects.filter(pi=pi, status="valid")

    objects = []

    for d in dataObjects:
        objects.append([int(d.date_time - 14400)* 1000, d.cum_vol])

    objects = sorted(objects,key=lambda x: x[0])

    data = deepcopy(objects)


    return HttpResponse(simplejson.dumps(data),content_type='application/json')

