import sys
import os
import django
import shutil, csv, glob, xlrd

sys.path.append('uv_hero')
os.environ['DJANGO_SETTINGS_MODULE'] = 'uv_hero.settings'
django.setup()

from records.models import Pi, Data


def addRawData(fileName):

    workbook = xlrd.open_workbook(fileName)
    sheet = workbook.sheet_by_index(0)

    address = sheet.col_values(1)[0]
    if address == '':
        address = '0:0:0:0:0:0:0'

    code = fileName[40:46:]
    piOb = Pi(code=code, address=address)
    piOb.save()

    rawVol = sheet.col_values(3)[3::]
    rawTimes = sheet.col_values(0)[3::]
    rawTimes = [int((float(x) - 25569) * 86400 + 14400) for x in rawTimes if x != '']

    for i in range(0, len(rawTimes)):
        Data(date_time=rawTimes[i], raw_vol=rawVol[i], cum_vol=0, new_vol=0, las_vol=0, status="raw", pi=piOb).save()


if __name__ == "__main__":

    Data.objects.filter(status="nurse").delete()

    print('starting glob')

    for fileName in glob.glob('/Users/Shikhar/Google Drive/Manual Data/*.xls'):
        workbook = xlrd.open_workbook(fileName)
        sheet = workbook.sheet_by_index(0)

        code = fileName[40:46:]

        print("\nFile is " + code)

        try:
            piid = Pi.objects.filter(code=code)[0]
        except:
            print("This session is not on website" + "\n")
            addRawData(fileName)
            continue

        try:
            cumVol = sheet.col_values(7)[3::]
            cumTimes = [x for x in sheet.col_values(6)[3::]]
        except:
            print("error reading sheet" + "\n")
            continue

        cumTimes = [int((float(x) - 25569) * 86400 + 14400) for x in cumTimes if x != '']

        for i in range(0, len(cumTimes)):
            Data(date_time=cumTimes[i], raw_vol=0, cum_vol=cumVol[i], new_vol=0, las_vol=0, status="nurse",
                 pi=piid).save()

        print("Done!")