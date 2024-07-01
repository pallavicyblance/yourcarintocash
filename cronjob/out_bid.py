from flask import Flask, request
import pymysql
import requests
import logging
from Misc.functions import *
from module.acceptedaps import Acceptedaps
from module.admin import Admin
from module.acv import ACV
from module.database import Database
from Misc.common import ACV_API_URL

db = Database()
acceptedaps = Acceptedaps()
admin = Admin()
acv = ACV()


class OutBid:

    def connect(self):
        return db.connect()

    def auction_out_bid():
        logging.info('-----cron job out bid started-----')
        print('-----cron job out bid started-----')
        active_auction = acv.getauctionsbid()
        getjwttoken = acv.getjwttoken(acv_user()[0])
        for auction in active_auction:
            user_bid = OutBid.bid_amount(auction[4], acv_user()[0])
            if auction[9] >= user_bid:
                if auction[38] is not None:
                    if auction[38] > auction[25]:
                        OutBid.place_auction_bid(auction[4], auction[25], getjwttoken[0])
                    elif auction[38] == auction[25] or auction[38] < auction[25]:
                        OutBid.update_data(auction[4])

        logging.info('-----cron job out bid ended-----')
        print('-----cron job out bid ended-----')
        return 'success'

    def bid_amount(auctionId, userId):
        out_bid_instance = OutBid()
        con = out_bid_instance.connect()
        cursor = con.cursor()
        try:
            cursor.execute("SELECT * FROM bids WHERE auction_id = %s AND user_id = %s", (auctionId, userId))
            bid = cursor.fetchone()
            return bid[2]
        except:
            return 0

    def place_auction_bid(auctionId, bidamount, jwttoken):

        url = f'{ACV_API_URL}/v2/auction/{auctionId}/bid'
        json_data = {'amount': bidamount}
        headers = {'Authorization': jwttoken, 'Content-Type': 'application/json'}

        try:
            response = requests.post(url, json=json_data, headers=headers)
            response.raise_for_status()
            if response.status_code == 200:
                acv.place_bid(auctionId, bidamount)
                acv.update_bid_by_us(auctionId)
                logging.info("auction %s: placed bid with amount %s", auctionId, bidamount)
                print('auction ' + str(auctionId) + ' placed bid with amount ' + str(bidamount))
                return 'status'

        except requests.exceptions.RequestException as e:
            logging.info("Response for auction %s: %s", auctionId, response.text)
            print("Response for auction :" + str(auctionId), response.text)
            return None

    def update_data(auctionId):
        out_bid_instance = OutBid()
        con = out_bid_instance.connect()
        cursor = con.cursor()
        try:
            cursor.execute('UPDATE auctions SET amount_reached = %s WHERE auction_id = %s', (1, auctionId))
            con.commit()
            return 'success'
        except Exception as e:
            print("Error:", e)
            logging.info("%s Error:", e)
            return 'failure'
