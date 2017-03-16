from django.shortcuts import render_to_response
from records.models import Data, Pi
from django.http import HttpResponse
import simplejson

def index(request):
    return render_to_response('index.html')

def chart_data_json(request):

    params = request.GET

    pi = params.get('pi', 0)
    print(pi)

    dataObjects = Data.objects.filter(pi=pi)

    data = []

    for datum in dataObjects:
        data.append([int((datum.date_time - 14400) * 1000),
                     datum.cum_vol])

    return HttpResponse(simplejson.dumps(data),content_type='application/json')

