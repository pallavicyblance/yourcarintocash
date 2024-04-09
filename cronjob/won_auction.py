from flask import Flask 

from module.acceptedaps import Acceptedaps

acceptedaps = Acceptedaps()

def won_auction():
    print('-----cron job won auction started-----')
    acceptedaps.winlostauctions()
    print('-----cron job won auction ended-----')
    return 'success'