"""
The following information is CONFIDENTIAL. If you are NOT an admin, and if you are seeing this,
e-mail ssb2189@columbia.edu
"""
import psycopg2.extras
# import os
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "uv_hero.settings")

import sys
import os
import django

sys.path.append('uv_hero')
os.environ['DJANGO_SETTINGS_MODULE'] = 'uv_hero.settings'
django.setup()

from records.models import Pi, Data

# Final Database - Storing patient records
DBNAME = 'd5nq5opbhumdlr'
USER = 'kznrowmqsnyetc'
PASSWORD = 'RRjBYCRf8crRhzrpHmk-HcPvnb'
HOST = 'ec2-54-163-253-94.compute-1.amazonaws.com'
PORT = '5432'

# Temporary Database - Testing
# DBNAME = 'd2i3vppivu81og'
# USER = 'cmukqvlzfirmnq'
# PASSWORD = 'Dc2dad3DKM8fFovofn8otZ099p'
# HOST = 'ec2-54-235-179-112.compute-1.amazonaws.com'
# PORT = '5432'

#This connects to the database
try:
    conn = psycopg2.connect("\
    dbname = '" + DBNAME + "'       \
    user = '" + USER + "'           \
    password = '" + PASSWORD + "'   \
    host = '" + HOST + "'           \
    port = '" + PORT + "'           \
                   ")
    conn.autocommit = True
except:
    print("Can't connect to the database :/ Check Wi-Fi.")


# Defining the cursor
try:
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
except:
    print("Error while importing psycopgy2")


# This adds the pi to the records_pi table
def add_pi(pi_code) :

    # this gets the RaspberryPi's MAC address
    try:
        str = open('/sys/class/net/eth0/address').read()
    except:
        str = "00:00:00:00:00:00"
    address = str[0:17]

    cur.execute("""SELECT records_pi.id FROM records_pi WHERE records_pi.code = (%s) """, (pi_code,))
    rows = cur.fetchall()

    if len(rows) == 0 :
        # Inserts the pi code and address into the records_pi table
        try:
            cur.execute("""INSERT INTO records_pi(code,address) VALUES(%s, %s)""", (pi_code, address))
        except :
            print("Error while inserting into records_pi")
    else :
        print("Code already exists.")



# This adds data to that particular pi
# def add_data(time,vol,last,new,cumul,status,pi_code) :

def add_data(all_data):

    time,vol,last,new, cumul, status, pi_code = all_data

    time = round(float(time), 1) - 3600
    vol = round(float(str(vol)),1)
    last = round(float(str(last)),1)
    new = round(float(str(new)),1)
    cumul = round(float(str(cumul)),1)
    status = str(status)
    pi_code = str(pi_code)


    # gets the pi_id from the records_pi table after matching the code
    try:
        cur.execute("""SELECT records_pi.id FROM records_pi WHERE records_pi.code = (%s) """,(pi_code,))
        rows = cur.fetchall()
        pi_id = str(rows[0][0])
    except:
        print("The Pi with that code does not exist")

    # Inserts the row into the data table
    try:
        cur.execute("""INSERT INTO records_data(date_time,raw_vol, las_vol,new_vol, cum_vol, status, pi_id) VALUES(%s, %s, %s, %s, %s, %s, %s)""", (time,vol,last,new,cumul,status,pi_id))
        all_data.pop(0)
    except:
        print("Error while inserting into records_data")


def findPi(code):
    return Pi.objects.filter(code=code)[0].id

if __name__ == "__main__":
    piid = findPi("ZE18YE")

    # d = Data(date_time=1501170473.2, raw_vol=5000, las_vol=5000, new_vol=5000, cum_vol=5000, status="nurse", pi_id=piid)
    # d.save()
    d = Data(date_time=1501134805.3, raw_vol=5000, las_vol=5000, new_vol=5000, cum_vol=5000, status="nurse", pi_id=piid)
    d.save()

