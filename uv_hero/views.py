from django.shortcuts import render
from records.models import Data, Pi
from django.http import HttpResponse, Http404
import simplejson
from copy import deepcopy
import numpy as np
import time, datetime

def index(request):
    return render(request, 'index.html')

# Data with the old algorithm with pre-set initial conditions
# def chart_data_json(request):
#
#     params = request.GET
#
#     pi = params.get('pi', 0)
#
#     dataObjects = Data.objects.filter(pi=pi, status="valid")
#
#     if not dataObjects:
#         raise Http404("Session does not exist")
#
#     data = []
#
#     for d in dataObjects:
#         data.append([int((d.date_time * 1000) - 14400000), d.cum_vol]) # change to cum_vol
#
#     data = deepcopy(sorted(data, key=lambda x: x[0]))
#
#     return HttpResponse(simplejson.dumps(data), content_type='application/json')


# raw data without processing

def chart_data_json(request):

    params = request.GET

    pi = params.get('pi', 0)

    dataObjects = Data.objects.filter(pi=pi)

    if not dataObjects:
        raise Http404("Session does not exist")

    data = []

    for d in dataObjects:
        data.append([int((d.date_time * 1000) - 14400000), d.raw_vol])

    data = deepcopy(sorted(data, key=lambda x: x[0]))

    data = []

    return HttpResponse(simplejson.dumps(data), content_type='application/json')


# the original algorithm
def all_data_json_original(request):

    params = request.GET

    pi = params.get('pi', 0)
    AVG = int(params.get('AVG', "50"))
    STD = int(params.get('STD', "9"))
    lastN = int(params.get('lN', "6"))

    dataObjects = Data.objects.filter(pi=pi)

    if not dataObjects:
        raise Http404("Session does not exist")

    data = []

    for d in dataObjects:
        data.append([int((d.date_time * 1000) - 14400000), d.raw_vol])

    data = deepcopy(sorted(data, key=lambda x: x[0]))

    tick = 0
    last = 100000
    new = 0
    cumul = 0

    readings = []
    readings.append((data[0][0] - 1, 0, last, new, cumul, "init"))

    for i in range(0,len(data)):
        timestamp = data[i][0]
        reading = data[i][1]
        status = "raw"

        if tick % 3 == 0 and tick > 0:
            last_six = [x[1] for x in readings[-1*(lastN-1):]]
            last_six.append(reading)
            avg = float(np.mean(last_six))
            std = float(np.std(last_six))

            if avg > AVG and std < STD:
                last = avg
                new = avg - readings[-1][2]
                if new > 0:
                    cumul += new
                else:
                    new = 0
                status = "valid"
            else:
                status = "rejected"

        vol = reading
        last = round(last, 3)
        new = round(new, 3)
        cumul = round(cumul, 3)

        readings.append((timestamp, vol, last, new, round(cumul, 1), status))

        tick += 1

    data = deepcopy([])

    for x in readings:
        if x[-1] == "valid":
            data.append([x[0], x[-2]])

    return HttpResponse(simplejson.dumps(data), content_type='application/json')

# the new algorithm
def all_data_json(request):
    params = request.GET

    pi = params.get('pi', 0)
    MUL = float(params.get('AVG', "1"))
    STD = int(params.get('STD', "9"))
    lastN = int(params.get('lN', "6"))

    dataObjects = Data.objects.filter(pi=pi)

    if not dataObjects:
        raise Http404("Session does not exist")

    data = []

    for d in dataObjects:
        data.append([int((d.date_time * 1000) - 14400000), d.raw_vol])

    data = deepcopy(sorted(data, key=lambda x: x[0]))

    last = 100000
    new = 0
    cumul = 0

    readings = []
    readings.append((data[0][0] - 1, 0, last, new, cumul, "init"))


    for i in range(5, len(data)):
        timestamp = data[i][0]
        reading = data[i][1]

        # last_ten = [x[1] for x in readings[-5:]]
        # last_ten.append(reading)
        # avg = float(np.mean(last_ten))
        # std = float(np.std(last_ten))

        last_six = [x[1] for x in readings[-6:]]
        last_six.append(reading)
        last = float(np.mean(last_six))
        std = float(np.std(last_six))

        # if avg > AVG and std < STD:
        #     last = avg
        #     new = avg - readings[-1][2]
        #     # prev = readings[-1][2]
        #     if cumul + new < 0 or abs(new) > 30:
        #         new = 0
        #         status = "rejected"
        #     else:
        #         status = "valid"
        #     if new > 0:
        #         new *= 0.9
        #     cumul += new
        # else:
        #     status = "rejected"

        if last > 50 and std < 5:
            if abs(last - readings[-1][2]) > 10:
                new = 0
            else:
                new = (last - readings[-1][2])*MUL

            cumul += new
            status = "valid"
        else:
            status = "rejected"
            cumul = readings[-1][4]
            new = 0

        vol = reading
        last = round(last, 3)
        new = round(new, 3)
        if cumul < 0:
            cumul = 0
        cumul = round(cumul, 3)

        readings.append((timestamp, vol, last, new, round(cumul, 1), status))

    data = deepcopy([])

    for x in readings:
        if x[-1] == "valid":
            data.append([x[0], x[-2]])

    return HttpResponse(simplejson.dumps(data), content_type='application/json')


# real data upload`
def real_data_json(request):

    file = open('./data.txt', 'r')
    text = file.readlines()
    data = [line.split('\t') for line in text]
    info = []
    for d in data:
        info.append([time.mktime(datetime.datetime.strptime(d[0], "%m/%d/%y %H:%M").timetuple())*1000, round(float(d[-1].replace('\n', '')), 1)])

    return HttpResponse(simplejson.dumps(info), content_type='application/json')






