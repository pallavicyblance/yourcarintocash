from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory
from module.acv import ACV
from Misc.functions import *
import threading
import logging

acv = ACV()
logging.basicConfig(filename='pubnub.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Create a logger object
logger = logging.getLogger(__name__)


class MySubscribeCallback(SubscribeCallback):
    def __init__(self, parent):
        self.parent = parent

    def presence(self, pubnub, presence):
        print(f"Presence event: {presence.event} on channel: {presence.channel}")

    def status(self, pubnub, status):
        if status.category == PNStatusCategory.PNConnectedCategory:
            print("Connected to PubNub")

    def message(self, pubnub, message):
        print(f"New value: {message.message} on channel: {message.channel}")
        logger.info('PUBNUB NOTIFICATION RECEIVE')
        logger.info(message)
        self.parent.last_value = message.message
        self.parent.handle_notification(message.message)


class PubNubClient:
    def __init__(self):
        user_details = acv.getjwttoken(acv_user()[0])
        user_id = str(user_details[1])
        publish_key = user_details[2]
        subscribe_key = user_details[3]
        self.channel = 'auctions'
        self.last_value = None
        self.pubnub = self._initialize_pubnub(subscribe_key, publish_key, user_id)
        self._add_listener()
        self._start_subscription()

    def _initialize_pubnub(self, subscribe_key, publish_key, user_id):
        pnconfig = PNConfiguration()
        pnconfig.subscribe_key = subscribe_key
        pnconfig.publish_key = publish_key
        pnconfig.uuid = user_id
        return PubNub(pnconfig)

    def _add_listener(self):
        self.pubnub.add_listener(MySubscribeCallback(self))

    def _start_subscription(self):
        def run():
            self.pubnub.subscribe().channels(self.channel).execute()

        subscription_thread = threading.Thread(target=run)
        subscription_thread.start()

    def handle_notification(self, message):
        # Custom function to handle the notification
        print(f"Handling notification with message: {message}")
        acv.handle_pubnub_notification(message)

    def publish_message(self, message):
        self.pubnub.publish().channel(self.channel).message(message).sync()

    def get_last_value(self):
        return self.last_value
