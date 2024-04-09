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







