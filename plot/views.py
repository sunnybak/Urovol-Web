from django.shortcuts import render, render_to_response
from chartit import DataPool, Chart
from records.models import Data, Pi
from .models import Stuff

# Create your views here.
def records_view(request):
    #Step 1: Create a DataPool with the data we want to retrieve.
    patientdata = \
        DataPool(
           series=
            [{'options': {
               'source': Stuff.objects.all()},
              'terms': [
                'month',
                'happiness']}
             ])

    #Step 2: Create the Chart object
    cht = Chart(
            datasource = patientdata,
            series_options =
              [{'options':{
                  'type': 'line',
                  'stacking': False},
                'terms':{
                  'month': [
                    'happiness']
                  }}],
            chart_options =
              {'title': {
                   'text': 'month'},
               'xAxis': {
                    'title': {
                       'text': 'happiness'}}})

    #Step 3: Send the chart object to the template.
    return render_to_response('plot/plot.html',{'weatherchart': cht})