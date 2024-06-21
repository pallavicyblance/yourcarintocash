from flask import Flask, flash, session

import requests
from module.acceptedaps import Acceptedaps
from module.acv import ACV
from Misc.functions import *
import logging
import jwt

acv = ACV()

acceptedaps = Acceptedaps()


def acv_login():
    loginurl = 'https://buy-api.gateway.staging.acvauctions.com/v2/login'
    data = {
        'email': acv_user()[1],
        'password': acv_user()[2]
    }
    response = requests.post(loginurl, json=data)
    refresh_token = response.json().get('refreshToken')
    pubnub_auth_key = response.json().get('pubnub').get('authKey')
    pubnub_expiration = response.json().get('pubnub').get('expiration')
    pubnub_subscribe_key = response.json().get('pubnub').get('subscribeKey')

    refreshTokenurl = 'https://buy-api.gateway.staging.acvauctions.com/v2/login/refresh'
    data = {
        'refreshToken': refresh_token
    }
    response = requests.post(refreshTokenurl, json=data)
    jwtToken = response.json().get('jwt')

    refresh_token = response.json().get('refreshToken')
    acv.storeToken(acv_user()[0], pubnub_auth_key, pubnub_expiration, pubnub_subscribe_key, refresh_token)
    acv.storeRefreshToken(jwtToken, acv_user()[0])

    print('acv_login')

