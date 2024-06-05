from flask import Flask, flash, session, request
import requests
from datetime import datetime
import pymysql
import logging
import traceback
import http.client
from module.acceptedaps import Acceptedaps
from module.admin import Admin
from Misc.functions import *
from module.acv import ACV

acv = ACV()
admin = Admin()
acceptedaps = Acceptedaps()

def latest_auctions():
    print('-----cron job latest auction data started-----')
    getjwttoken = acv.getjwttoken(acv_user()[0])
    url = 'https://buy-api.gateway.staging.acvauctions.com/v2/auction'
    headers = {'Authorization': getjwttoken[0]}

    rows_per_page = 100
    start = 0

    while True:
        params = {'start': start, 'rows': rows_per_page}
        print(f"Requesting auctions with start={start} and rows={rows_per_page}")
        
        response = requests.get(url, params=params, headers=headers)
        try:
            response.raise_for_status()
            response_data = response.json()
            auctions = response_data.get("auctions", [])

            if not auctions:
                print("No more auctions found.")
                break 

            print(f"Fetched {len(auctions)} auctions.")

            todaydatetime = datetime.now()
            todaydatestr = todaydatetime.strftime("%Y-%m-%d %H:%M:%S")
            for auction in auctions:
                print(f"Processing auction ID: {auction['id']}, Status: {auction['status']}")
                auction_data = fetch_auction_details(auction['id'], headers['Authorization'])
                acv.insertauctiondata(auction_data)
                acv.auctionconditionreport(auction_data)
                acv.countslights(auction['id'])
                
            start += rows_per_page
            print(f"Next start: {start}")
            time.sleep(1)
        
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                # Refresh token and retry the request
                print("Token expired. Refreshing token and retrying...")
                getjwttoken = acv.getjwttoken(acv_user()[0])
                headers['Authorization'] = getjwttoken[0]
                continue  # Retry the current iteration
            else:
                print(f"Request failed: {e}")
                print(response.text)
                return None

    # Second API call to `runlist`
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
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            print("Token expired. Refreshing token and retrying...")
            getjwttoken = acv.getjwttoken(acv_user()[0])
            headers['Authorization'] = getjwttoken[0]
            # Retry the `runlist` request
            response = requests.get(url, params=params, headers=headers)
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
        else:
            print(f"Request failed: {e}")
            print(response.text)
            return None

def fetch_auction_details(auction_id, jwttoken):
    url = f'https://buy-api.gateway.staging.acvauctions.com/v2/auction/{auction_id}'
    headers = {'Authorization': jwttoken}
    auctiondetails = requests.get(url, headers=headers)
    auctiondetails.raise_for_status()
    return auctiondetails.json()
