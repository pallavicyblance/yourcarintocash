from flask import Flask, flash, session
import logging

import pubnub

from pubnub.pubnub import PubNub
from pubnub.callbacks import SubscribeCallback
from pubnub.pnconfiguration import PNConfiguration
from Misc.functions import *
from module.admin import Admin

admin = Admin()

def auction_pub_nub_notification():

    print('-----cron job auction_pub_nub_notification started-----')
    user_details = admin.getjwttoken(acv_user()[0])

    PUBNUB_PUBLISH_KEY = user_details[2]
    PUBNUB_SUBSCRIBE_KEY = user_details[3]
    USER_ID = str(user_details[1])

    def configure_pubnub(auth_key):
        pnconfig = PNConfiguration()
        pnconfig.subscribe_key = PUBNUB_SUBSCRIBE_KEY
        pnconfig.auth_key = auth_key
        pnconfig.uuid = USER_ID  
        return PubNub(pnconfig)
    
    class MyListener(SubscribeCallback):
        def message(self, pubnub, message):
            message_data = message.message
            if 'type' in message_data and message_data['type'] == 'LAUNCHED':
                print('message_data',message_data)
                session['message_data'] = message_data
                auction_id = message_data['data']['id']
                print(f"Auction launched with ID: {auction_id}")
    
    pubnub_auth_key = PUBNUB_PUBLISH_KEY
    if not pubnub_auth_key:
        return "Failed to obtain PubNub authKey. Check ACV login API response."
    
    pubnub = configure_pubnub(pubnub_auth_key)

    pubnub.add_listener(MyListener())
    pubnub.subscribe().channels("auctions").execute()
    
    print('-----cron job auction_pub_nub_notification ended-----')
    return "Now listening for auction events..."
