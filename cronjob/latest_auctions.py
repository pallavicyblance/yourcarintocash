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


admin = Admin()
acceptedaps = Acceptedaps()
def latest_auctions():
        
    # logging.info('-----cron job latest auction data started-----')
    # print('-----cron job latest auction data started-----')
    # getjwttoken = session.get('jwt_token')
    getjwttoken = admin.getjwttoken(acv_user()[0])

    url = 'https://buy-api.gateway.staging.acvauctions.com/v2/auction'
    params = {'start': 0, 'rows': 10}
    headers = {'Authorization': getjwttoken[0]}

    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()
    response_data = response.json()

    todaydatetime = datetime.now()
    todaydatestr = todaydatetime.strftime("%Y-%m-%d %H:%M:%S")

    for auction in response_data.get("auctions", []):

        auctiondate = auction['endTime']
        auctiondate = datetime.strptime(auctiondate[:-1], "%Y-%m-%dT%H:%M:%S")
        auctionenddatestr = auctiondate.strftime("%Y-%m-%d %H:%M:%S")

        if auctionenddatestr > todaydatestr and auction['status'] == 'active':
            auction_data = fetch_auction_details(auction, getjwttoken[0])
            nextproxybidamount = auction_data['nextProxyAmount'] 
            acceptedaps.insertauctiondata(auction_data,auction_data['nextProxyAmount']) 
            acceptedaps.auctionconditionreport(auction_data)
            acceptedaps.countslights(auction['id'])
            # logging.info("%s -----auction data inserted-----", int(auction_data['id']))
            # print(str(auction_data['id']),'-----auction data inserted-----')

    url = 'https://buy-api.gateway.staging.acvauctions.com/v2/auction/runlist'
    params = {'start': 0, 'rows': 10}
    headers = {'Authorization': getjwttoken[0]}

    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()
    response_data = response.json()
    for auction in response_data.get("auctions", []):

        auctiondate = auction['startTime']
        auctiondate = datetime.strptime(auctiondate[:-1], "%Y-%m-%dT%H:%M:%S")
        auctionstartdatestr = auctiondate.strftime("%Y-%m-%d %H:%M:%S")

        if auctionstartdatestr > todaydatestr:

            # proxybidamount = auction['price']
            # nextproxybidamount = auction['price'] + 50

            auction_data = fetch_auction_details(auction, getjwttoken[0])
            nextproxybidamount = auction_data['nextProxyAmount'] 
            acceptedaps.insertauctiondata(auction_data,nextproxybidamount)
            acceptedaps.auctionconditionreport(auction_data)
            acceptedaps.countslights(auction['id'])
            # logging.info("%s -----upcoming auction data inserted-----", int(auction_data['id']))
            # print(str(auction_data['id']), '-----upcoming auction data inserted-----')

    # logging.info('-----cron job latest auction data ended-----')
    # print('-----cron job latest auction data ended-----')
    return 'success'

def fetch_auction_details(auction, jwttoken):
    auction_id = auction['id']
    url = f'https://buy-api.gateway.staging.acvauctions.com/v2/auction/{auction_id}'
    params = {'id': auction_id}
    headers = {'Authorization': jwttoken}
    auctiondetails = requests.get(url, params=params, headers=headers)
    auctiondetails.raise_for_status()
    return auctiondetails.json()



    
    