import sys
import os
import django
import shutil, csv, glob, xlrd
import numpy as np
from copy import deepcopy
from uv_hero.algorithm import alg

sys.path.append('uv_hero')
os.environ['DJANGO_SETTINGS_MODULE'] = 'uv_hero.settings'
django.setup()

from records.models import Pi, Data


def generateCSVcomparison(code):

    path = '/Users/Shikhar/Google Drive/Combined/'

    data = []

    piReadings = Data.objects.filter(pi=Pi.objects.filter(code=code)[0])

    for d in piReadings.exclude(status="nurse"):
        data.append([int(d.date_time), float(d.raw_vol)])

    par = (50, 14, 60, -10, 10000, 0.9, 300)
    sortedProc = alg(sorted(deepcopy(data), key=lambda x: x[0]), par)

    nurseReadings = sorted(piReadings.filter(status="nurse"), key= lambda x: x.date_time)

    if len(nurseReadings) > 0:
        print("\tGenerating CSV...")

        csvfile = open(path + code + '.csv', 'w', newline='')
        writer = csv.writer(csvfile)
        writer.writerow(['Timestamp', 'Manual', 'Processed'])
        for manualRead in nurseReadings:
            row = []
            proc = []

            for times in range(-60 + int(manualRead.date_time), 61 + int(manualRead.date_time)):
                ds = [x for x in sortedProc if x[0] == times]
                if len(proc) > 6:
                    break
                if len(ds) > 0:
                    for d in ds:
                        proc.append(d[1])

            row.append(manualRead.date_time)
            row.append(manualRead.cum_vol)
            if len(proc) > 0:
                row.append(round(np.mean(proc), 1))
            else:
                row.append('')

            writer.writerow(row)

        csvfile.close()

        print("\tSuccessfully generated CSV!\n")


if __name__ == "__main__":

    Data.objects.filter(status="nurse").delete()
    path = '/Users/Shikhar/Google Drive/Combined/'

    try:
        shutil.rmtree(path) # removes all files from this path
    except:
        print('enter the correct path')

    os.makedirs(path)

    print('starting glob')

    for fileName in glob.glob('/Users/Shikhar/Google Drive/Manual Data/*.xls'):
        workbook = xlrd.open_workbook(fileName)
        sheet = workbook.sheet_by_index(0)

        address = sheet.col_values(1)[0]
        if address == '':
            address = '0:0:0:0:0:0:0'

        code = fileName[40:46:]

        print("\nFile: " + code)

        piOb, created = Pi.objects.get_or_create(code=code)

        if len(piOb.address) <= 10:
            piOb.address = address
            piOb.save()

        if created:
            try:
                rawVol = sheet.col_values(3)[3::]
                rawTimes = sheet.col_values(0)[3::]
                rawTimes = [int((float(x) - 25569) * 86400 + 14400) for x in rawTimes if x != '']

                print("\tNew Pi created. Adding data to database...")
                print('\tThere are ' + str(len(rawTimes)) + ' readings. ETA: ' + str(int(len(rawTimes) / 1000)) + ' mins.')
                for i in range(0, len(rawTimes)):
                    Data(date_time=rawTimes[i], raw_vol=rawVol[i], cum_vol=0, new_vol=0, las_vol=0, status="raw",
                         pi=piOb).save()
                print("\tSuccessfully added all the raw data!\n")
            except:
                print("\t---error reading sheet: adding Raw data---\n")
                pass

        if len(Data.objects.filter(pi=piOb, status="nurse")) == 0:
            try:
                cumVol = sheet.col_values(7)[3::]
                cumTimes = [x for x in sheet.col_values(6)[3::]]
                cumTimes = [int((float(x) - 25569) * 86400 + 14400) for x in cumTimes if x != '']

                print("\tAdding Nurse data...")
                for i in range(0, len(cumTimes)):
                    Data(date_time=cumTimes[i], raw_vol=0, cum_vol=cumVol[i], new_vol=0, las_vol=0, status="nurse",
                         pi=piOb).save()
                print("\tSuccessfully added all the nurse data!\n")
            except IndexError:
                print("\t---No nurse data available for this session---\n")
                continue
            except:
                print("\t---error reading sheet: adding Nurse data---\n")
                continue

            try:
                generateCSVcomparison(code)
            except:
                print("\t---error generating comparison CSV---\n")
                continue

        print("Done!")
