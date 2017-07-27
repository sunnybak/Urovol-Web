import sys
import os
import django
import csv, glob, xlrd
import time, datetime
from copy import deepcopy

sys.path.append('uv_hero')
os.environ['DJANGO_SETTINGS_MODULE'] = 'uv_hero.settings'
django.setup()

from records.models import Pi, Data



def findPi(code):
    return Pi.objects.filter(code=code)[0]

if __name__ == "__main__":
    # piid = findPi("ZE18YE")
    # Data.objects.filter(status="nurse").delete()
    print('starting glob')

    Data.objects.filter(status="nurse").delete()

    for fileName in glob.glob('/Users/Shikhar/Google Drive/Manual Data/*.xls'):
        workbook = xlrd.open_workbook(fileName)
        sheet = workbook.sheet_by_index(0)

        code = sheet.col_values(0)[0]

        print("File is " + fileName[40:46:] + "\n\n\n\n")

        all_data = []
        try:
            piid = Pi.objects.filter(code=fileName[40:46:])[0]
        except:
            continue

        if code == "":
            print("Couldn't find code in " + fileName)

        # getting the man data
        try:
            cumVol = sheet.col_values(7)[3::]
            cumTimes = [x for x in sheet.col_values(6)[3::]]
        except:
            continue

        cumTimes = [int((float(x)-25569)*86400 + 14400) for x in cumTimes if x != '']

        for i in range(0, len(cumTimes)):
            Data(date_time=cumTimes[i], raw_vol=0, cum_vol=cumVol[i], new_vol=0, las_vol=0, status="nurse", pi=piid).save()
            print(cumTimes[i], cumVol[i])

