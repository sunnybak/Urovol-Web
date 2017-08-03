import os, sys, django
sys.path.append('uv_hero')
os.environ['DJANGO_SETTINGS_MODULE'] = 'uv_hero.settings'
os.environ['DATABASE_URL'] = 'postgres://u82igt0qtftuee:p2a86c1e8c0bdc274664b9fae1a3507a97a6d7c4be5b6475fa82996799202968a@ec2-34-230-191-133.compute-1.amazonaws.com:5432/d8b1o1r9gidjh0'
django.setup()
RED   = "\033[1;31m"
BLUE  = "\033[1;34m"
CYAN  = "\033[1;36m"
GREEN = "\033[0;32m"
RESET = "\033[0;0m"
BOLD    = "\033[;1m"
REVERSE = "\033[;7m"

from records.models import Pi, Data
from uv_hero.algorithm import alg
from params import getParams
import numpy as np
import time

def binary_search(a, x, lo, hi=None):
    """Return the index where to insert item x in list a, assuming a is sorted.

    The return value i is such that all e in a[:i] have e < x, and all e in
    a[i:] have e >= x.  So if x already appears in the list, a.insert(x) will
    insert just before the leftmost x already there.

    Optional args lo (default 0) and hi (default len(a)) bound the
    slice of a to be searched.
    """
    if hi is None:
        hi = len(a)
    while lo < hi:
        mid = (lo+hi)//2
        if a[mid][0] < x: lo = mid+1
        else: hi = mid

    if lo != len(a) and a[lo][0] == x:
        return lo
    return None

error_dict = dict()
total = 0

for pi in Pi.objects.order_by('code'):
# for pi in Pi.objects.filter(code='BJ01LD'):
    print(pi.code + ':', end='  ')

    if Data.objects.filter(pi=pi, status="nurse").exists() is False:
        sys.stdout.write(RED)
        print('No nurse data')
        sys.stdout.write(RESET)
        continue


    # print('\tReadings:', len(Data.objects.filter(pi=pi)))


    t0 = time.time()

    processed_data = []
    nurse_data = []


    for d in Data.objects.filter(pi=pi).order_by('date_time'):
        if d.status == "nurse":
            nurse_data.append((int(d.date_time), float(d.cum_vol)))
        else:
            processed_data.append((int(d.date_time), float(d.raw_vol)))

    td = time.time()
    # print("Time to fetch raw data:", str(round(td - t0, 2)), "seconds\n")
    params = getParams()
    processed_data = alg(processed_data, params)
    tp = time.time()
    # print("\nTime to process data:", str(round(tp - td, 2)), "seconds\n")

    errors = []
    for n in nurse_data:
        proc_avg = []
        low = 0
        # hi = len(processed_data)
        for time_range in range(n[0] - 60, n[0] + 61):
            i = binary_search(processed_data, time_range, low)
            if i is not None:
                proc_avg.append(processed_data[i][1])
                low = i
                # hi = i + 70
        if len(proc_avg) > 0 and n[1] != 0:
            errors.append(abs(np.mean(proc_avg) - n[1])/n[1])

    # print("Time to process error:", str(round(time.time() - td, 2)), "seconds")
    if len(errors) > 0:
        errors = round(np.mean(errors) * 100, 2)
        sys.stdout.write(GREEN)
        print("Error " + str(errors) + "%")
        sys.stdout.write(RESET)
        error_dict[pi.code] = errors
    else:
        sys.stdout.write(BLUE)
        print("Weird graph, check website.")
        sys.stdout.write(RESET)

    total += round(time.time() - t0, 2)

print(error_dict)
print("\tTotal Processing Time: ", str(total), "seconds")

