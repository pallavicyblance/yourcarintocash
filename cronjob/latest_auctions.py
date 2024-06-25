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


def upcoming_auction():
    print('-----cron job upcoming auction data started-----')
    getjwttoken = acv.getjwttoken(acv_user()[0])

    # Second API call to `runlist`
    url = 'https://buy-api.gateway.staging.acvauctions.com/v2/auction/runlist'
    params = {'start': 0, 'rows': 10}
    headers = {'Authorization': getjwttoken[0]}
    response = requests.get(url, params=params, headers=headers)

    todaydatetime = datetime.now()
    todaydatestr = todaydatetime.strftime("%Y-%m-%d %H:%M:%S")

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

        print('-----cron job upcoming auction data ended-----')
        return 'success'
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            # Refresh token and retry the request
            print("Token expired. Refreshing token and retrying...")
        else:
            print(f"Request failed: {e}")
            print(response.text)
            return None


def live_auctions():
    todaydatetime = datetime.now()
    print('-----cron job latest auction data started-----', todaydatetime)
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

            for auction in auctions:
                print(f"Processing auction ID: {auction['id']}, Status: {auction['status']}")
                auction_data = fetch_auction_details(auction['id'], getjwttoken[0])
                acv.insertauctiondata(auction_data)

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


def fetch_auction_details(auction_id, jwttoken):
    url = f'https://buy-api.gateway.staging.acvauctions.com/v2/auction/{auction_id}'
    headers = {'Authorization': jwttoken}
    auctiondetails = requests.get(url, headers=headers)
    auctiondetails.raise_for_status()
    return auctiondetails.json()


def bidding_status():
    con = acv.connect()
    cursor = con.cursor()
    cursor1 = acv.connect_index()
    response = []

    try:
        getjwttoken = acv.getjwttoken(acv_user()[0])
        current_datetime = datetime.now()
        auction_end_time = current_datetime.strftime("%Y-%m-%d %H:%M:%S ")

        cursor1.execute('SELECT * FROM auctions WHERE status = "active" AND bid_by_us = %s', (1))
        expire_auctions = cursor1.fetchall()

        for auction in expire_auctions:
            print('-----FETCH AUCTION DETAIL-----', datetime.now())
            auction_data = fetch_auction_details(auction['auction_id'], getjwttoken[0])
            print('-----DONE FETCH AUCTION DETAIL-----', datetime.now())

            ishighbidder = auction_data.get('isHighBidder')
            nextbidamount = auction_data.get('nextBidAmount')
            nextProxyAmount = auction_data.get('nextProxyAmount')
            bidCount = auction_data.get('bidCount')
            bidAmount = auction_data.get('bidAmount')

            response.append({
                'auction_id': auction['auction_id'],
                'isHighBidder': ishighbidder,
                'nextBidAmount': nextbidamount,
                'nextProxyAmount': nextProxyAmount,
                'bidCount': bidCount,
                'bidAmount': bidAmount
            })

            acv.update(auction['auction_id'], ishighbidder, nextbidamount, bidAmount, nextProxyAmount, bidCount)

    except Exception as e:
        print(e)
    finally:
        cursor.close()
        con.close()

    return response


def close_auction():
    print('-----cron job close auction data-----')
    acv.close_auction()
