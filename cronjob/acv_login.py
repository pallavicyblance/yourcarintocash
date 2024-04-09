from flask import Flask, flash, session

import requests
from module.acceptedaps import Acceptedaps
from module.admin import Admin
from Misc.functions import *
import logging
admin = Admin()

acceptedaps = Acceptedaps()

def acv_login():

    logging.info('-----cron job acv login started-----')
    print('-----cron job acv login started-----')
    loginurl = 'https://buy-api.gateway.staging.acvauctions.com/v2/login'

    data = {
        'email': acv_user()[1],
        'password': acv_user()[2]
    }
    
    response = requests.post(loginurl, json=data)

    refresh_token = response.json().get('refreshToken')
    pubnum_auth_key = response.json().get('pubnub').get('authKey')
    pubnum_expiration = response.json().get('pubnub').get('expiration')
    pubnum_subscribe_key = response.json().get('pubnub').get('subscribeKey')
    
    refreshTokenurl = 'https://buy-api.gateway.staging.acvauctions.com/v2/login/refresh'
    data = {
        'refreshToken' : refresh_token
    }
    response = requests.post(refreshTokenurl, json=data)
    
    jwtToken = response.json().get('jwt')
    

    admin.storeToken(jwtToken,acv_user()[0],pubnum_auth_key,pubnum_expiration,pubnum_subscribe_key)
    
    logging.info('-----cron job acv login ended-----')
    print('-----cron job acv login ended-----')

