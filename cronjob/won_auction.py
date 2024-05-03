from flask import Flask 

from module.acv import ACV

acv = ACV()

def won_auction():
    print('-----cron job won auction started-----')
    acv.winlostauctions()
    print('-----cron job won auction ended-----')
    return 'success'