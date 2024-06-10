from flask import Flask, flash, session, json
import logging
import pymysql
import datetime
import requests
import traceback
from pubnub.pubnub import PubNub
from datetime import date
from pubnub.callbacks import SubscribeCallback
from pubnub.pnconfiguration import PNConfiguration
from Misc.functions import *
from module.admin import Admin
from module.acceptedaps import Acceptedaps
from module.acv import ACV

acv = ACV()
admin = Admin()
acceptedaps = Acceptedaps()

class PubNubNotification:

    def connect(self):
        return pymysql.connect(host="localhost", user="root", password="", database="carcash", charset='utf8mb4') 

    def auction_pub_nub_notification():
        try:
            print('-----cron job auction_pub_nub_notification started-----')
            user_details = acv.getjwttoken(acv_user()[0])

            PUBNUB_PUBLISH_KEY = user_details[2]
            PUBNUB_SUBSCRIBE_KEY = user_details[3]
            USER_ID = str(user_details[1])
            getjwttoken = acv.getjwttoken(acv_user()[0])

            def configure_pubnub(auth_key):
                pnconfig = PNConfiguration()
                pnconfig.subscribe_key = PUBNUB_SUBSCRIBE_KEY
                pnconfig.auth_key = auth_key
                pnconfig.uuid = USER_ID  
                return PubNub(pnconfig)
            
            class MyListener(SubscribeCallback):
                def message(self, pubnub, message):
                    message_data = message.message

                    if 'type' in message_data:
                        
                        if message_data['type'] == 'LAUNCHED':
                            PubNubNotification.insertNotification(message_data)
                        
                            auctionId = message_data['data']['id']
                            auction_data = PubNubNotification.fetch_auction_details(auctionId, getjwttoken[0])
                            
                            if isinstance(auction_data, dict):
                                auction_end_date = auction_data['endTime']
                                print('end_date', auction_end_date)

                                # auctiondate = datetime.strptime(auction_end_date[:-1], "%Y-%m-%dT%H:%M:%S")
                                # auctionenddatestr = auctiondate.strftime("%Y-%m-%d %H:%M:%S")

                                if auction_data['status'] == 'active':    
                                    acv.insertAuctionsUsingPubnub(auction_data) 
                            else:
                                print('Unexpected data type for auction_data:', type(auction_data))

                        elif message_data['type'] == 'UPDATED':
                            print('update')
                            auction_id = message_data['data']['id']
                            print(auction_id)
                        
                        else:
                            print("Unknown message type:", message_data)
                    
                    else:
                        print("Message type not specified:", message_data)

            pubnub_auth_key = PUBNUB_PUBLISH_KEY
            if not pubnub_auth_key:
                return "Failed to obtain PubNub authKey. Check ACV login API response."
            
            pubnub = configure_pubnub(pubnub_auth_key)

            pubnub.add_listener(MyListener())
            pubnub.subscribe().channels('auctions').execute()
            
            print('-----cron job auction_pub_nub_notification ended-----')
            return "Now listening for auction events..."
        except Exception as e:
            print("Error:", e)
            logging.info("%s Error:", e)
            return 'failure'
    
    def insertNotification(message_data):
        notification_instance = PubNubNotification() 
        con = notification_instance.connect()
        cursor = con.cursor()
        try:
            auction_id = message_data['data']['id']
            print('auction_id',auction_id)
            if not auction_id:
                return 'Auction ID is missing'
            
            cursor.execute("SELECT auction_id FROM pubnub WHERE auction_id = %s", (auction_id,))
            existing_auction = cursor.fetchone()
            print('existing_auction',existing_auction)
            if existing_auction is None:
                print('Auction does not exist in the database')
                message_data_str = json.dumps(message_data)
                cursor.execute('INSERT INTO pubnub (auction_id, massage, created_at) VALUES (%s, %s, %s)', (auction_id, message_data_str, datetime.now()))
                con.commit()
                return 'success'
            else:
                print('Auction already exists in the database')
                return 'Auction already exists'
        
        except Exception as e:
            print(f"Error during database operation: {str(e)}")
            traceback.print_exc()
            return False
    
    def fetch_auction_details(auction_id, jwttoken):
        try:
            url = f'https://buy-api.gateway.staging.acvauctions.com/v2/auction/{auction_id}'
            params = {'id': auction_id}
            headers = {'Authorization': jwttoken}
            auctiondetails = requests.get(url, params=params, headers=headers)
            auctiondetails.raise_for_status()
            return auctiondetails.json()
        except Exception as e:
            print(f"Error during database operation: {str(e)}")
            traceback.print_exc()
            return False
