from flask import Flask, flash, session

from module.acv import ACV

acv = ACV()

def remove_auction():
    print('-----cron job remove auction started-----')
    acv.deleteAuction()
    print('-----cron job remove auction ended-----')
    return 'success'