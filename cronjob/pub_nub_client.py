from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory
from module.acv import ACV
from Misc.functions import *
import threading
import logging
import uuid

acv = ACV()
logging.basicConfig(filename='pubnub.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Create a logger object
logger = logging.getLogger(__name__)


class MySubscribeCallback(SubscribeCallback):
    def __init__(self, parent):
        self.parent = parent

    def presence(self, pubnub, presence):
        print(f"Presence event: {presence.event} on channel: {presence.channel}")

    def status(self, pubnub, status):
        print('PUBNUB STATUS')
        if status.is_error():
            print('PUBNUB STATUS IF')
            print(status.category)
            logger.error(f"PUBNUB Error: {status.category}")
        else:
            print('PUBNUB STATUS ELSE')
            print(status.category)
            if status.category == "PNConnectedCategory":
                logger.info("PUBNUB CONNECTED!")
            else:
                logger.info(f"PUBNUB Status update: {status.category}")

    def message(self, pubnub, message):
        print(f"New value: {message.message} on channel: {message.channel}")
        logger.info('PUBNUB NOTIFICATION RECEIVE')
        logger.info(message)
        self.parent.last_value = message.message
        self.parent.handle_notification(message.message)


class PubNubClient:
    def __init__(self):
        pubnub_detail = acv.get_pubnub_auth_key()
        print('PUBNUB DETAILS')
        print(pubnub_detail)
        publish_key = pubnub_detail['pubnub_auth_key']
        subscribe_key = pubnub_detail['pubnub_subscribe_key']
        self.channel = 'auctions'
        self.last_value = None
        self.pubnub = self._initialize_pubnub(subscribe_key, publish_key)
        self._start_subscription()
        self._add_listener()

    def _initialize_pubnub(self, subscribe_key, publish_key):
        pnconfig = PNConfiguration()
        pnconfig.subscribe_key = subscribe_key
        pnconfig.publish_key = publish_key
        pnconfig.uuid = str(uuid.uuid4())
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
