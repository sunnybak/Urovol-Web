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
            data.append([x[0],x[-2]])


    return HttpResponse(simplejson.dumps(data),content_type='application/json')


# the new algorithm
def all_data_json(request):

    params = request.GET

    pi = params.get('pi', 0)

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
                new = (last - readings[-1][2])*0.8

            # if cumul + new < 0:
            #     new = 0

            cumul += new
            status = "valid"
        else:
            status = "rejected"
            cumul = readings[-1][4]
            new = 0


        vol = reading
        last = round(last, 3)
        new = round(new, 3)
        cumul = round(cumul, 3)

        readings.append((timestamp, vol, last, new, round(cumul, 1), status))

    data = deepcopy([])

    for x in readings:
        if x[-1] == "valid":
            data.append([x[0], x[-2]])

    csv_sections(threshold=50)

    return HttpResponse(simplejson.dumps(data), content_type='application/json')


# real data upload
def real_data_json(request):

    file = open('./data.txt', 'r')
    text = file.readlines()
    data = [line.split('\t') for line in text]
    info = []
    for d in data:
        if "valid" in d[-1]:
            info.append([time.mktime(datetime.datetime.strptime(d[0], "%m/%d/%y %H:%M").timetuple())*1000, round(float(d[-2]), 1)])

    return HttpResponse(simplejson.dumps(info),content_type='application/json')


# create CSV sections based on gradient spikes
def csv_sections(threshold):

    import shutil, os, csv, glob, xlrd
    shutil.rmtree('/Users/shikhar/dev/uv_hero/Sections/')
    os.makedirs('Sections')
    print('starting glob')

    piObjects = Pi.objects.all()
    error = ''
    for pi in piObjects:
        # create a folder by the session name
        for fileName in glob.glob('Combined/*.xls'):
            # There is a match. Start CSV creation
            if pi.code in fileName:

                # initializations
                os.makedirs('Sections/' + pi.code)
                secCounter = 0
                csvfile = open('Sections/' + pi.code + '/section_0.csv', 'w',
                               newline='')
                writer = csv.writer(csvfile)
                writer.writerow(
                    ['Timestamp', 'Raw Volume', 'Manual Volume', 'Grad'])
                csvfile.close()
                csvfile = open('Sections/' + pi.code + '/section_0.csv', 'a',
                               newline='')
                writer = csv.writer(csvfile)

                all_data = []

                # getting the raw data
                all_data.extend([[float(x.date_time), float(x.raw_vol), 'RAW'] for x in Data.objects.filter(pi=pi.id)])

                # getting the processed data
                # all_data.extend([[x.date_time, x.raw_vol, 'PROC'] for x in Data.objects.filter(pi=pi.id, status='valid')])


                # getting the manual data
                print('Found:' + fileName)
                xl_workbook = xlrd.open_workbook(fileName)
                xl_sheet = xl_workbook.sheet_by_index(0)
                numReadings = xl_sheet.col_values(5).index('', 3)
                times = xl_sheet.col_values(4)[3:numReadings:]
                times = [int((x-25569)*86400) for x in times]
                man_cum = xl_sheet.col_values(5)[3:numReadings:]
                all_data.extend([[times[i], float(man_cum[i]), 'MAN'] for i in range(0, len(times))])

                # sorting data chronologically
                all_data = deepcopy(sorted(all_data, key=lambda x: x[0]))

                prev = 0.0
                writen = False

                for x in all_data:
                    if x[2] == 'RAW':
                        if abs(x[1] - prev) < threshold:
                            writer.writerow(x)
                            writen = True
                        else:
                            if writen:
                                csvfile.close()
                                secCounter += 1
                                print('\tStarting section', secCounter)
                                csvfile = open(
                                    'Sections/' + pi.code + '/section_' + str(
                                        secCounter) + '.csv',
                                    'w', newline='')
                                writer = csv.writer(csvfile)
                                writer.writerow(
                                    ['Timestamp', 'Volume', 'Type'])
                                csvfile.close()
                                csvfile = open(
                                    'Sections/' + pi.code + '/section_' + str(
                                        secCounter) + '.csv',
                                    'a', newline='')
                                writer = csv.writer(csvfile)
                                writen = False
                        prev = x[1]
                    else:
                        writer.writerow(x)
                csvfile.close()
                break
        else:
            error += 'error: ' + pi.code + ' on database but not offline \n'
    print(error)











