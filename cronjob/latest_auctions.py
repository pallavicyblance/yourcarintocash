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
from Misc.common import ACV_API_URL

acv = ACV()
admin = Admin()
acceptedaps = Acceptedaps()


def upcoming_auction():
    todaydatetime = datetime.now()
    print('-----cron job runlist auction data started-----', todaydatetime)
    getjwttoken = acv.getjwttoken(acv_user()[0])
    url = f'{ACV_API_URL}/v2/auction/runlist'
    headers = {'Authorization': getjwttoken[0]}

    rows_per_page = 100
    start = 0

    while True:
        params = {'start': start, 'rows': rows_per_page}
        print(f"Requesting runlist auctions with start={start} and rows={rows_per_page}")

        response = requests.get(url, params=params, headers=headers)
        try:
            response.raise_for_status()
            response_data = response.json()
            auctions = response_data.get("auctions", [])

            if not auctions:
                print("No more auctions found runlist.")
                break

            print(f"Fetched {len(auctions)} auctions runlist.")

            for auction in auctions:
                print(f"Processing auction ID: {auction['id']}, Status: {auction['status']}")
                auction_data = fetch_auction_details(auction['id'], getjwttoken[0])
                acv.insertauctiondata(auction_data)

            start += rows_per_page
            print(f"Next runlist start: {start}")
            time.sleep(1)

        except requests.exceptions.HTTPError as r:
            if r.response.status_code == 401:
                # Refresh token and retry the request
                print("Token expired. Refreshing token and retrying runlist...")
                getjwttoken = acv.getjwttoken(acv_user()[0])
                headers['Authorization'] = getjwttoken[0]
                continue
        except Exception as e:
            print(f"Request failed runlist:")
            print(e)
            return None


def live_auctions():
    todaydatetime = datetime.now()

    getjwttoken = acv.getjwttoken(acv_user()[0])
    url = f'{ACV_API_URL}/v2/auction'
    headers = {'Authorization': getjwttoken[0]}

    rows_per_page = 100
    start = 0

    while True:
        params = {'start': start, 'rows': rows_per_page}

        response = requests.get(url, params=params, headers=headers)
        try:
            response.raise_for_status()
            response_data = response.json()
            auctions = response_data.get("auctions", [])

            if not auctions:
                print("No more auctions found.")
                break

            for auction in auctions:
                print(f"Processing auction ID: {auction['id']}, Status: {auction['status']}")
                auction_data = fetch_auction_details(auction['id'], getjwttoken[0])
                acv.insertauctiondata(auction_data)

            start += rows_per_page
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
    url = f'{ACV_API_URL}/v2/auction/{auction_id}'
    headers = {'Authorization': jwttoken}
    auctiondetails = requests.get(url, headers=headers)
    auctiondetails.raise_for_status()
    return auctiondetails.json()


def close_auction():
    acv.close_auction()


def generate_auction_final_status():
    acv.generate_auction_final_status()
