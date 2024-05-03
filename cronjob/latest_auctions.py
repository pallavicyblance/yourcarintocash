from flask import Flask, flash, session, request

import requests
import datetime
import pymysql
import logging
import traceback
import http.client
from datetime import date
from module.acceptedaps import Acceptedaps
from module.admin import Admin
from Misc.functions import *
from module.acv import ACV

acv = ACV()
admin = Admin()
acceptedaps = Acceptedaps()
def latest_auctions():
    
    # logging.info('-----cron job latest auction data started-----')
    print('-----cron job latest auction data started-----')
    getjwttoken = acv.getjwttoken(acv_user()[0])
    url = 'https://buy-api.gateway.staging.acvauctions.com/v2/auction'
    params = {'start': 0, 'rows': 10}
    headers = {'Authorization': getjwttoken[0]}

    response = requests.get(url, params=params, headers=headers)
    try:
        response.raise_for_status()
        response_data = response.json()

        todaydatetime = datetime.now()
        todaydatestr = todaydatetime.strftime("%Y-%m-%d %H:%M:%S")
        for auction in response_data.get("auctions", []):
            auctiondate = auction['endTime']
            auctiondate = datetime.strptime(auctiondate[:-1], "%Y-%m-%dT%H:%M:%S")
            auctionenddatestr = auctiondate.strftime("%Y-%m-%d %H:%M:%S")
            # if auctionenddatestr > todaydatestr and auction['status'] == 'active':
            auction_data = fetch_auction_details(auction['id'], getjwttoken[0])
            acv.insertauctiondata(auction_data) 
            acv.auctionconditionreport(auction_data)
            acv.countslights(auction['id'])
    except requests.exceptions.RequestException as e:
        print(response.text)
        return None 

    url = 'https://buy-api.gateway.staging.acvauctions.com/v2/auction/runlist'
    params = {'start': 0, 'rows': 10}
    headers = {'Authorization': getjwttoken[0]}

    response = requests.get(url, params=params, headers=headers)
    try:
        response.raise_for_status()
        response_data = response.json()
        for auction in response_data.get("auctions", []):

            auctiondate = auction['startTime']
            auctiondate = datetime.strptime(auctiondate[:-1], "%Y-%m-%dT%H:%M:%S")
            auctionstartdatestr = auctiondate.strftime("%Y-%m-%d %H:%M:%S")

            if auctionstartdatestr > todaydatestr:
                auction_data = fetch_auction_details(auction['id'], getjwttoken[0])
                acv.insertauctiondata(auction_data)
                acv.auctionconditionreport(auction_data)
                acv.countslights(auction['id'])

        print('-----cron job latest auction data ended-----')
        return 'success'
    except requests.exceptions.RequestException as e:
        print(response.text)
        return None 

def fetch_auction_details(auction_id, jwttoken):
    url = f'https://buy-api.gateway.staging.acvauctions.com/v2/auction/{auction_id}'
    params = {'id': auction_id}
    headers = {'Authorization': jwttoken}
    auctiondetails = requests.get(url, params=params, headers=headers)
    auctiondetails.raise_for_status()
    return auctiondetails.json()



    
    