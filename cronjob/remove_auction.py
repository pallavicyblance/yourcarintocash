from flask import Flask, flash, session

from module.acceptedaps import Acceptedaps

acceptedaps = Acceptedaps()

def remove_auction():
    print('-----cron job remove auction started-----')
    acceptedaps.deleteAuction()
    print('-----cron job remove auction ended-----')
    return 'success'