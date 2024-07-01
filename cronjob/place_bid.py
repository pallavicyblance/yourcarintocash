from flask import Flask ,jsonify, request, session
import pymysql
import requests
import logging
from module.acceptedaps import Acceptedaps
from module.admin import Admin
from Misc.functions import *
# from Misc.dbconnect import *
from module.acv import ACV
import http.client
from module.database import Database
from Misc.common import socketio
from Misc.common import ACV_API_URL

db = Database()
admin = Admin()

acceptedaps = Acceptedaps()
acv = ACV()

class auction_place_bid:

    def connect(self):
        return db.connect()

    def acv_auction_place_bid(self):
        print('-----cron job place bid data started-----')

        getauctions = acv.getauctionsforbid()

        try:
            for auction in getauctions:
                if auction[38] is not None:
                    if auction[38] > auction[36]:
                        self.place_auction_proxy_bid(auction[4], auction[36])
                        self.update_auction(auction[4])
                    elif auction[38] == auction[36] or auction[38] < auction[36]:
                        self.update_data(auction[4])
            print('-----cron job place bid data ended-----')
            return 'success'
        except Exception as e:
            print("Error cron job place bid:", e)

    def update_data(self, auctionId):
        auction_place_bid_instance = auction_place_bid()
        con = auction_place_bid_instance.connect()
        cursor = con.cursor()
        try:
            cursor.execute('UPDATE auctions SET amount_reached = %s WHERE auction_id = %s', (1, auctionId))
            con.commit()
            return 'success'
        except Exception as e:
            print("Error:", e)
            logging.info("%s Error:", e)
            return 'failure'

    def place_auction_proxy_bid(self, auctionId, nextProxyAmount):
        getjwttoken = acv.getjwttoken(acv_user()[0])
        url = f'{ACV_API_URL}/v2/auction/{auctionId}/bid'
        print(f'BID AMOUNT:===>{nextProxyAmount}')
        print(f'AUTO BIDDING AUCTION:===>{auctionId}')

        params = {'amount': nextProxyAmount, 'proxy': True, 'persistent': False}
        headers = {'Authorization': getjwttoken[0], 'Content-Type': 'application/json'}

        try:
            logging.info(f'AUTO BID AUCTION:-{auctionId}')
            response = requests.post(url, json=params, headers=headers)
            response.raise_for_status()
            acv.updateproxydata(auctionId, nextProxyAmount)
            acv.update_bid_by_us(auctionId, 1)
            print(f"Response for auction : {auctionId}")
            print(response.text)
            socketio.emit('auction_bid_placed', {'auctionId': auctionId, 'data': response.text})
            return 'success'

        except requests.exceptions.RequestException as r:
            print("Error BID:", r)
            return None
        except Exception as e:
            print("Error BID E:", e)
            return None

    def update_auction(self, auctionId):
        try:
            getjwttoken = acv.getjwttoken(acv_user()[0])
            auction_data = self.fetch_auction_details(auctionId, getjwttoken[0])
            acv.insertauctiondata(auction_data)
        except Exception as e:
            print("Error:", e)
            logging.info("Error:", e)
            return 'failure'

    def fetch_auction_details(self, auction_id, jwttoken):
        url = f'{ACV_API_URL}/v2/auction/{auction_id}'
        headers = {'Authorization': jwttoken}
        auctiondetails = requests.get(url, headers=headers)
        auctiondetails.raise_for_status()
        return auctiondetails.json()



