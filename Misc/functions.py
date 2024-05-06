import hashlib, binascii

import json

import time

from datetime import date, timedelta, datetime

import uuid

import pytz

# Allowed extension you can set your own

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'svg'])

ALLOWED_EXTENSIONS1 = set(['png', 'jpg', 'jpeg', 'gif','pdf', 'txt', 'docx', 'doc' , 'wps'])

salt=b'$#0x--.\'/\\98'

def hash(string):

    dk = hashlib.pbkdf2_hmac('sha256', b'password', salt, 100000)

    return binascii.hexlify(dk).decode("utf-8")



def b_hash(string):

    dk = hashlib.pbkdf2_hmac('sha256', b'password', salt, 100000)

    return binascii.hexlify(dk)

def gettimezone():

     return (time.strftime("Time Zone: %Z", time.localtime()))



def allowed_file(filename):

    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def allowed_file1(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS1

def filenamegenerator(filename):

    extenstion = filename.rsplit('.').pop()

    ids = uuid.uuid4()

    return ids.hex+'.'+extenstion

def gettimeincst():
     cstnm = datetime.now(pytz.timezone('US/Central'))
     return cstnm
def sessionidgenerator():
     created_at = datetime.now(pytz.timezone('US/Central'))
     sessionid = created_at.strftime("%m%d%y%H%M%S")
     return sessionid

def changeStartDateFormat(date):
    try:
        start_date = datetime.strptime(date, '%m-%d-%Y').strftime('%Y-%m-%d')
    except ValueError:
        start_date = date
    final_date = start_date + ' 00:00:00'
    return final_date

def changeEndDateFormat(date):
    try:
        end_date = datetime.strptime(date, '%m-%d-%Y').strftime('%Y-%m-%d')
    except ValueError:
        end_date = date
    final_date = end_date + ' 23:59:59'
    return final_date

# code added by pallavi
def acv_user():

    # user_1:
    id  = 6422282
    email = 'twincitybuying@twincity.com'
    password = 'TwinCity123!'

    # user_2:
    # id = 6748005
    # email = 'twincitytest2@twincity.com'
    # password = 'TwinCityTest2!'
    
    return id,email,password
# code ended by pallavi







