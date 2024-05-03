from flask import Flask ,jsonify, request, session
import pymysql
import requests
import logging
from module.acceptedaps import Acceptedaps
from module.admin import Admin
from Misc.functions import *
from module.acv import ACV
import http.client
admin = Admin()

acceptedaps = Acceptedaps()
acv = ACV()

class auction_place_bid: 

    def connect(self):
         # return pymysql.connect(host="localhost", user="carintocash1", password="zkY$$}_vtXO=", database="carintocash1", charset='utf8mb4')
        return pymysql.connect(host="localhost", user="root", password="", database="carintocash", charset='utf8mb4') 

    def acv_auction_place_bid():
        logging.info('-----------cron job place bid started -----------')
        print('-----------cron job place bid started -----------')

        getjwttoken = acv.getjwttoken(acv_user()[0])
                
        getauctions = acv.getauctionsforbid()
        for auction in getauctions:
            # if auction[38] is not None:
                # if auction[38] > auction[36]:
                auction_place_bid.place_auction_proxy_bid(auction[4],auction[36],getjwttoken[0])
                # elif auction[38] == auction[36] or auction[38] < auction[36]:
                #     auction_place_bid.update_data(auction[4])

        logging.info('-----------cron job place bid ended -----------')
        print('-----------cron job place bid ended ------------')
        return 'success'

    def update_data(auctionId):
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

    def place_auction_proxy_bid(auctionId,nextProxyAmount,jwttoken):  
        url = f'https://buy-api.gateway.staging.acvauctions.com/v2/auction/{auctionId}/bid'
        json_data_bid = {
            'amount': nextProxyAmount,
            'proxy': True, 
            'persistent': False
        }
        headers = {
            'Authorization': jwttoken,
            'Content-Type': 'application/json'
        }

        try:
            response = requests.post(url, json=json_data_bid, headers=headers)
            response.raise_for_status()  
            acv.updateproxydata(auctionId,nextProxyAmount)
            print("Response for auction :" + str(auctionId), response.text)
            return 'success'
                    
        except requests.exceptions.RequestException as e:
            print("Error:", e)
            logging.info("Response for auction %s: %s", auctionId, response.text)
            print("Response for auction :" + str(auctionId), response.text)
            return None



