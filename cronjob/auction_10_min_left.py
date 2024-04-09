
from flask import Flask, flash, session
from datetime import datetime
import requests
import logging
from module.acceptedaps import Acceptedaps
from module.admin import Admin

from Misc.functions import *

admin = Admin()
acceptedaps = Acceptedaps()

def auction_10_min_left():
    logging.info('-----cron job auction 10 min left started-----')
    print('-----cron job auction 10 min left started-----')
    auctionsfetched = acceptedaps.getauctionsbid()
    getjwttoken = admin.getjwttoken(acv_user()[0])
    for auction in auctionsfetched:
        current_datetime = datetime.now()
        time_left = auction[7] - current_datetime

        minutes_left = max(time_left.total_seconds() / 60, 0)
    
        if minutes_left <= 10:
            logging.info("%s auction left 10 minutes to end", auction[4])
            print(auction[4],'auction left 10 minutes to end')
            auction_data = fetch_auction_details(auction[4], getjwttoken[0])
            place_auction_bid(auction[4],auction_data['nextBidAmount'],getjwttoken[0])

    logging.info('-----cron job auction 10 min left ended-----')
    print('-----cron job auction 10 min left ended-----')


def fetch_auction_details(auction, jwttoken):
    auction_id = auction
    url = f'https://buy-api.gateway.staging.acvauctions.com/v2/auction/{auction_id}'
    params = {'id': auction_id}
    headers = {'Authorization': jwttoken}
    auctiondetails = requests.get(url, params=params, headers=headers)
    auctiondetails.raise_for_status()
    return auctiondetails.json()


def place_auction_bid(auctionId, bidamount, jwttoken):

    url = f'https://buy-api.gateway.staging.acvauctions.com/v2/auction/{auctionId}/bid'
    params = {'amount': bidamount}
    headers = {'Authorization': jwttoken,'Content-Type': 'application/json'}
    try:
        response = requests.post(url, json=params,headers=headers)
        response.raise_for_status()  
        response_data = response.json() 

        acceptedaps.addbid(auctionId,response_data['amount'],acv_user()[0])
        acceptedaps.place_bid(auctionId, response_data['amount'])
        logging.info("auction %s: placed bid with amount %s", auctionId, response_data['amount'])
        print('auction ' + str(auctionId) + ' placed bid with amount ' + str(response_data['amount']))

        return response_data
    except requests.exceptions.RequestException as e:
        logging.info("Response for auction %s: %s", auctionId, response.text)
        print("Response for auction :" + str(auctionId), response.text)
        return None 