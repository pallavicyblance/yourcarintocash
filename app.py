from flask import Flask, flash, render_template, redirect, url_for, request, session, json,jsonify 
from apscheduler.schedulers.background import BackgroundScheduler
from werkzeug.utils import secure_filename
import os

import requests

from Misc.functions import *
import socket
from datetime import datetime, timedelta
import schedule
import threading
import sched
import time
import pubnub
from cronjob.acv_login import acv_login
from cronjob.latest_auctions import latest_auctions
from cronjob.place_bid import auction_place_bid
from cronjob.won_auction import won_auction
from cronjob.auction_10_min_left import auction_10_min_left
from cronjob.auction_1_min_left import auction_1_min_left
from cronjob.remove_auction import remove_auction
from cronjob.pub_nub import PubNubNotification
from cronjob.out_bid import OutBid
from cronjob.generate_proqoute import Proqoute

from module.database import Database
from module.admin import Admin


from module.setting import Setting



from module.acceptedaps import Acceptedaps
from module.notes import Notes

from pubnub.pubnub import PubNub
from pubnub.callbacks import SubscribeCallback
from pubnub.pnconfiguration import PNConfiguration

from module.commonarray import Commonarray



from module.qoute import Qoute

from module.offer import Offer

from module.acv import ACV

import smtplib
import logging

from email.message import EmailMessage



from flask import request, g

# from werkzeug.urls import url_parse

logging.basicConfig(filename='cron.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')



app = Flask(__name__)

path = os.getcwd()
UPLOAD_FOLDER = os.path.join(path, 'static/images')
if not os.path.isdir(UPLOAD_FOLDER): os.mkdir(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


app.secret_key = "345t345345343"

db = Database()

admin = Admin()

setting = Setting()


acv = ACV()

acceptedaps = Acceptedaps()
notes= Notes()


commonarray = Commonarray()

qoute = Qoute()

offer = Offer()


@app.route('/google', methods=['GET'])
def referal():
    return render_template('referal.html')


@app.route('/')

def index():

    sharing = request.args.get('amt')
    lang = request.args.get('lang')

    if lang:
        current_lan = lang
    else:
        current_lan = 'en'

    year = setting.getyears(None)



    bodydamage = commonarray.getbodydamage()

    sbodydamage = commonarray.getbodydamagesecondary(current_lan)
    typeoftitle = commonarray.gettypeoftitle(current_lan)



    doeskey = commonarray.getdoeskey(current_lan)



    drive = commonarray.getdrive(current_lan)



    firedamage = commonarray.getfiredamage(current_lan)



    deployedbags = commonarray.getdeployedbags(current_lan)



    state = commonarray.getstate()



    proquotesget = setting.read(1)



    hostname = socket.gethostname()



    #IPAddr = socket.gethostbyname(hostname)

    IPAddr = request.environ['REMOTE_ADDR']





    #flash(location_data)

    locationInfo = acceptedaps.getLocationInfo(IPAddr)

    inquiryget = acceptedaps.autoinquiryget(IPAddr,hostname)



    #datasss = qoute.getqoute()

    if inquiryget :



        inquiryget = inquiryget[0]



    url = request.referrer
    u1 = ''
    # if domain is not mine, save it in the session
    # if url and url_parse(url).host != "http://192.168.1.19:9000":
    #     u1 = url

    # if url and url_parse(url).host != "http://192.168.1.19:9000/":
    #     u1 = url

    param1 = request.args.get('args')

    if param1:
        u1 = param1

    if u1=='http://192.168.1.19:9000/' :
        u1 = ''

    if u1=='http://192.168.1.19:9000' :
        u1 = ''

    if u1=='http://192.168.1.19:9000/?args=' :
        u1 = ''

    if lang:
        labelArr = setting.getTranslateTxt(lang)
    else:
        labelArr = setting.getTranslateTxt('en')

    year_1 = ''
    make_1 = request.args.get('make')
    model_1 = request.args.get('model')

    skip_1 = 'no'
    if request.args.get('year'):
        year_1 = request.args.get('year')
        skip_1 = 'yes'

    sharing = request.args.get('amt')

    # pallavi changes 12-06-24
    param1 = request.args.get('args')
    referrer = ''
    if param1:
        referrer = param1
    else:
        referrer = request.referrer

    utm_source = ''
    if request.args.get('utm_source'):
        utm_source = request.args.get('utm_source')
    
    utm_medium = ''
    if request.args.get('utm_medium'):
        utm_medium = request.args.get('utm_medium')
    
    utm_campaign = ''
    if request.args.get('utm_campaign'):
        utm_campaign = request.args.get('utm_campaign')
    
    currunt_param = request.args.get('current_url')
    currunt_url = ''
    if currunt_param:
        currunt_url = currunt_param
    else:
        currunt_url = request.url
        
    # pallavi changes 12-06-24 close

    return render_template('index.html',lang=lang,labelArr=labelArr[0], u1=referrer ,inquiryget= inquiryget, hostname= hostname, IPAddr= IPAddr, year = year, bodydamage = bodydamage, typeoftitle = typeoftitle, doeskey = doeskey, drives = drive, firedamage = firedamage, deployedbags = deployedbags, states = state, proquotesget =proquotesget , locationInfo=locationInfo,sbodydamage=sbodydamage,skip_1=skip_1,year_1=year_1,make_1=make_1,model_1=model_1 , sharing = sharing, utm_source=utm_source, utm_medium=utm_medium, utm_campaign=utm_campaign,currunt_url=currunt_url)

# darshan added for sharing

@app.route('/sharing_genrate_id' , methods = ['POST', 'GET'])
def sharing_genrate_id():
    if request.method == 'POST':
        sharing =request.args.get('amt')
        data = acceptedaps.insert_sharing(sharing)
        return json.dumps({'data':data});


@app.route('/login/')



def login():
    return render_template('login.html')




@app.route('/signin', methods = ['POST', 'GET'])



def signin():



    if request.method == 'POST' and request.form['login']:



        if admin.adminlogin(request.form):



            data = admin.adminlogin(request.form)



            session['admin_logged_in'] = True



            session['admin_logged_id'] = data[0][0]



            session['admin_logged_username'] = data[0][1]



            session['admin_logged_lastname'] = data[0][2]

            session['role'] = data[0][8]

            session['acv_user_id'] = data[0][9]

            session['acv_user_email'] = data[0][10]
            
            session['acv_user_password'] = data[0][11]

            return redirect(url_for('dashboard'))



        else:



            flash("Username and password is wrong.")



        return redirect(url_for('login'))



    else:



        flash("Username and password is wrong.")



        return redirect(url_for('login'))



@app.route('/signout')



def signout():



     session.clear()



     return redirect(url_for('login'))



@app.route('/discountmanagement/')



def discountmanagement():



    if not session.get('admin_logged_in'):

        return redirect(url_for('login'))
    else:

        data = setting.read(1);
        id = session['admin_logged_id']
        role = admin.role(id)
        return render_template('dashboard.html', data = data,role=role)


# @app.route('/dashboard-old/')



# def dashboardold():



#     if not session.get('admin_logged_in'):



#         return redirect(url_for('login'))



#     else:



#         data1 = setting.getKip();
#         data2 = setting.getKipWeek();
#         data3 = setting.getKipMonth();

#         data5 = setting.getCompleteInquiry();
#         data6 = setting.getInCompleteInquiry();
#         data7 = setting.getAcceptInquiry();
#         data8 = setting.userComesFrom();
#         data9 = setting.userComesFromAll();

#         id = session['admin_logged_id']
#         role = admin.role(id)

#         return render_template('dashboard-new.html', currentDay = data1,currentWeek = data2, currentMonth = data3 , completeInquiry=data5, inCompleteInquiry=data6, acceptInquiry=data7,userfrom=data8,userfromTotal=data9,role=role)

# code added by pallavi
@app.route('/dashboard/',methods = ['POST', 'GET'])
    # This function handles the '/dashboard-new' route.
    # If the user is not logged in as an admin, it redirects to the login page.
    # If the request method is POST, it retrieves the start and end dates from the form,
    # calls the 'getCount' function from the 'setting' module, and returns the result as JSON.
    # If the request method is GET, it sets the start and end dates to the first and last day of the current month,
    # calls the 'getCount' function from the 'setting' module, and renders the 'kpi-dashboard.html' template
    # with the count, start date, and end date as template variables.
def dashboard():
    if not session.get('admin_logged_in'):
        return redirect(url_for('login'))
    else:
        if request.method == 'POST':
            start_date = request.form['start_date']
            end_date = request.form['end_date']
            
            dashboard_count = setting.getCount(start_date,end_date)
            return jsonify(dashboard_count)
        else:
            today = date.today()
            first_day_of_month = today.replace(day=1)
            last_day_of_month = today.replace(day=1, month=today.month % 12 + 1) - timedelta(days=1)
            start_date = first_day_of_month.strftime("%Y-%m-%d")
            end_date = last_day_of_month.strftime("%Y-%m-%d")

            usa_format_start_date = first_day_of_month.strftime("%m-%d-%Y")
            usa_format_end_date = last_day_of_month.strftime("%m-%d-%Y")
            id = session['admin_logged_id']
            role = admin.role(id)
            dashboard_count = setting.getCount(usa_format_start_date,usa_format_end_date)
            return render_template('kpi-dashboard.html',count = dashboard_count, start_date = usa_format_start_date, end_date = usa_format_end_date, role = role)

@app.route('/auction-new-user-bid/', methods = ['POST', 'GET'])
def acvnewuserbid():
    loginurl = 'https://buy-api.gateway.staging.acvauctions.com/v2/login'
    data = {
        'email': 'twincitytest2@twincity.com',  
        'password': 'TwinCityTest2!'
    }
    response = requests.post(loginurl, json=data)
    refresh_token = response.json().get('refreshToken')

    refreshTokenurl = 'https://buy-api.gateway.staging.acvauctions.com/v2/login/refresh'
    data = {
        'refreshToken' : refresh_token
    }
    response = requests.post(refreshTokenurl, json=data)

    jwtToken = response.json().get('jwt')

    # url = 'https://buy-api.gateway.staging.acvauctions.com/v2/auction'
    # params = {'start': 0, 'rows': 10}
    # headers = {'Authorization': jwtToken}

    # response = requests.get(url, params=params, headers=headers)
    # response.raise_for_status()
    # response_data = response.json()

    # for auction in response_data.get("auctions", []):
        # if auction['status'] == 'active':
    auction_data = fetch_auction_details(4422216, jwtToken)
    url = f'https://buy-api.gateway.staging.acvauctions.com/v2/auction/4422216/bid'
    json_data_bid = {
        'amount': auction_data['nextProxyAmount'],
        'proxy': True, 
        'persistent': False
    }
    headers = {
        'Authorization': jwtToken,
        'Content-Type': 'application/json'
    }

    try:
        response = requests.post(url, json=json_data_bid, headers=headers)
        acv.updateproxydata(auction_data['id'],auction_data['nextProxyAmount'])
        print('add bid',auction_data['id'],'bid',auction_data['nextProxyAmount'])
        response.raise_for_status()  
    except requests.exceptions.RequestException as e:
        return ''
                
    return 'success'

def fetch_auction_details(auction, jwttoken):
    url = f'https://buy-api.gateway.staging.acvauctions.com/v2/auction/{auction}'
    params = {'id': auction}
    headers = {'Authorization': jwttoken}
    auctiondetails = requests.get(url, params=params, headers=headers)
    auctiondetails.raise_for_status()
    return auctiondetails.json()
        
@app.route('/place-bid/',methods = ['POST','GET'])
def place_bid():
    
    data = request.json
    auctionId = data['auctionId']
    bidamount = data['bidamount']   

    getjwttoken = acv.getjwttoken(acv_user()[0])

    url = f'https://buy-api.gateway.staging.acvauctions.com/v2/auction/{auctionId}/bid'
    params = {'amount': bidamount}

    headers = {'Authorization': getjwttoken[0],'Content-Type': 'application/json'}

    try:
        
        response = requests.post(url, json=params,headers=headers)
        response.raise_for_status()  
        response_data = response.json() 

        acv.place_bid(auctionId, response_data['amount'])

        url = f'https://buy-api.gateway.staging.acvauctions.com/v2/auction/{auctionId}'
        params = {'id': auctionId}
        headers = {'Authorization': getjwttoken[0]}
        auctiondetails = requests.get(url, params=params, headers=headers)

        ishighbidder = auctiondetails.json().get('isHighBidder')
        nextbidamount = auctiondetails.json().get('nextBidAmount')
        bidAmount = auctiondetails.json().get('bidAmount')
        nextProxyAmount = auctiondetails.json().get('nextProxyAmount')
        bidCount = auctiondetails.json().get('bidCount')
        if ishighbidder:
            acv.update(auctionId,ishighbidder,nextbidamount,bidAmount,nextProxyAmount,bidCount)

        return response_data
    except requests.exceptions.RequestException as e:
        print("Error:", e)
        print("Response:", response.text)
        return jsonify({'error': response.text})

@app.route('/place-proxy-bid/', methods = ['POST','GET'])
def place_proxy_bid():
    data = request.json
    auctionId = data['auctionId']
    bidamount = data['proxyBidAmount']   

    getjwttoken = acv.getjwttoken(acv_user()[0])

    url = f'https://buy-api.gateway.staging.acvauctions.com/v2/auction/{auctionId}/bid'
    json_data_bid = {
        'amount': bidamount,
        'proxy': True, 
        'persistent': False
    }
    headers = {
        'Authorization': getjwttoken[0],
        'Content-Type': 'application/json'
    }

    try:
        response = requests.post(url, json=json_data_bid, headers=headers)
        response.raise_for_status()  
        acv.updateproxydata(auctionId,bidamount)
        return 'success'       
    except requests.exceptions.RequestException as e:
        print("Error:", e)
        print("Response:", response.text)
        return jsonify({'error': response.text})

@app.route('/auction/', methods=['GET'])
def auction():
    if not session.get('admin_logged_in'):
        return redirect(url_for('login'))
    else:
        acv_user_id = session.get('acv_user_id')
        acv_user_email = session.get('acv_user_email')
        acv_user_password = session.get('acv_user_password')
        user_name = session.get('admin_logged_username') + ' ' + session.get('admin_logged_lastname')

        condition_flter = acv.getconditionReport('')
        id = session['admin_logged_id']
        role = admin.role(id)

        return render_template('auction.html', condition_flter=condition_flter,user_name=user_name, role=role)
        
@app.route('/condition-report-details/',methods = ['POST','GET'])
def conditionReportDetails():
    selected_report_id = request.form['id']
    reportfetched = acv.getconditionReport(selected_report_id)
    auctionsfetched = acv.getauctions()
    wonauctions = acv.getwonauction()
    lostauctions = acv.getlostauction()
    countNotificaton = acv.getNotificationCount()

    final_action = {'auctions': [], 'reports': [], 'won_auction': [], 'lost_auction': [], 'count': countNotificaton}

    for auction in auctionsfetched:
        if meets_condition(auction, selected_report_id):
                final_action['auctions'].append(auction)

    for wonauction in wonauctions:
        if meets_condition(wonauction, selected_report_id):
            final_action['won_auction'].append(wonauction)

    for lostauction in lostauctions:
        if meets_condition(lostauction, selected_report_id):
            final_action['lost_auction'].append(lostauction)

    final_action['reports'] = reportfetched
    
    return jsonify(final_action)

@app.route('/liveauction/', methods=['GET'])
def liveauction():
    if not session.get('admin_logged_in'):
        return redirect(url_for('login'))
    else:
        condition_flter = acv.getconditionReport('')
        return render_template('live-auction.html',condition_flter=condition_flter)

@app.route('/live-details/',methods = ['POST','GET'])
def liveconditionReportDetails():
    selected_report_id = request.form['id']
    reportfetched = acv.getconditionReport(selected_report_id)
    auctionsfetched = acv.getliveauctions()
    wonauctions = acv.getlivewonauction()
    lostauctions = acv.getlivelostauction()

    final_action = {'auctions': [], 'reports': [], 'won_auction': [], 'lost_auction': []}

    for auction in auctionsfetched:
        if meets_condition(auction, reportfetched):
                final_action['auctions'].append(auction)

    for wonauction in wonauctions:
        if meets_condition(wonauction, reportfetched):
            final_action['won_auction'].append(wonauction)

    for lostauction in lostauctions:
        if meets_condition(lostauction, reportfetched):
            final_action['lost_auction'].append(lostauction)

    final_action['reports'] = reportfetched
    
    return jsonify(final_action)

@app.route('/save-live-auction',methods = ['POST','GET'])
def saveliveauction():
    loginurl = 'https://buy-api.gateway.acvauctions.com/v2/login'

    data = {
        'email': 'ben@twincitiesautoauctions.com',
        'password': 'E$$BiyfxNx6P'
    }

    try:
        response = requests.post(loginurl, json=data)
        refresh_token = response.json().get('refreshToken')
        
        if refresh_token:
            refreshTokenurl = 'https://buy-api.gateway.acvauctions.com/v2/login/refresh'
            data = {
                'refreshToken' : refresh_token
            }
            try:
                response = requests.post(refreshTokenurl, json=data)
        
                jwtToken = response.json().get('jwt')

                url = 'https://buy-api.gateway.acvauctions.com/v2/auction'
                params = {'start': 0, 'rows': 20}
                headers = {'Authorization': jwtToken}

                try:
                    response = requests.get(url, params=params, headers=headers)
                    response_data = response.json()
                    
                    if response_data.get("auctions", []):
                        for auction in response_data.get("auctions", []):
                            auction_data = fetch_live_auction_details(auction, jwtToken)
                            
                            acv.liveinsertauctiondata(auction_data) 
                            acv.liveauctionconditionreport(auction_data)
                            acv.livecountslights(auction['id'])
                        return 'success'
                    else:
                        return "No live auctions available."
                except requests.exceptions.RequestException as e:
                    print("Error:", e)
                    return None
            except requests.exceptions.RequestException as e:
                print("Error:", e)
                return None
        else:
            print("Login failed. No refresh token received.")
            return None
    except requests.exceptions.RequestException as e:
        print("Error:", e)
        return None

@app.route('/save-live-upcoming-auction',methods = ['POST','GET'])
def saveliveupcomingauction():
    loginurl = 'https://buy-api.gateway.acvauctions.com/v2/login'

    data = {
        'email': 'ben@twincitiesautoauctions.com',
        'password': 'E$$BiyfxNx6P'
    }

    try:
        response = requests.post(loginurl, json=data)
        refresh_token = response.json().get('refreshToken')
        
        if refresh_token:
            refreshTokenurl = 'https://buy-api.gateway.acvauctions.com/v2/login/refresh'
            data = {
                'refreshToken' : refresh_token
            }
            try:
                response = requests.post(refreshTokenurl, json=data)
        
                jwtToken = response.json().get('jwt')

                url = 'https://buy-api.gateway.acvauctions.com/v2/auction/runlist'
                params = {'start': 0, 'rows': 20}
                headers = {'Authorization': jwtToken}

                try:
                    response = requests.get(url, params=params, headers=headers)
                    response_data = response.json()
                    
                    if response_data.get("auctions", []):
                        for auction in response_data.get("auctions", []):
                            auction_data = fetch_live_auction_details(auction, jwtToken)

                            acv.liveinsertauctiondata(auction_data) 
                            acv.liveauctionconditionreport(auction_data)
                            acv.livecountslights(auction['id'])
                        return 'success'
                    else:
                        return "No live upcoming auctions available."
                except requests.exceptions.RequestException as e:
                    print("Error:", e)
                    return None
            except requests.exceptions.RequestException as e:
                print("Error:", e)
                return None
        else:
            print("Login failed. No refresh token received.")
            return None
    except requests.exceptions.RequestException as e:
        print("Error:", e)
        return None
    
def fetch_live_auction_details(auction, jwttoken):
    auction_id = auction['id']
    url = f'https://buy-api.gateway.acvauctions.com/v2/auction/{auction_id}'
    params = {'id': auction_id}
    headers = {'Authorization': jwttoken}
    auctiondetails = requests.get(url, params=params, headers=headers)
    auctiondetails.raise_for_status()
    return auctiondetails.json()

@app.route('/upcoming-live-auction-data/', methods=['GET','POST'])
def upcoming_live_auction_data():
    if not session.get('admin_logged_in'):
        return redirect(url_for('login'))
    else:
        response_upcoming_data = acv.getLiveUpcomingauction()
        return jsonify(response_upcoming_data)

@app.route('/get-live-auction-condition/',methods=['GET','POST'])
def getliveauctioncondition():
    auction_id = request.form['auction_id']
    conditions = acv.getliveauctioncondition(auction_id)
    return jsonify(conditions)
    
@app.route('/match-condition/', methods = ['POST','GET'])
def meets_condition(auction_data, condition_flter):
    # for condition in condition_flter:
        if acv.checkconditonwithauction(auction_data, condition_flter):
            acv.matchauction(auction_data[4],is_match=True)
            return True
        else:
            acv.matchauction(auction_data[4],is_match=False)
            return False

@app.route('/upcoming-auction-data/', methods=['GET','POST'])
def upcoming_auction_data():
    if not session.get('admin_logged_in'):
        return redirect(url_for('login'))
    else:
        response_upcoming_data = acv.getUpcomingauction()
        return jsonify(response_upcoming_data)
      
@app.route('/missed-auction/', methods=['GET','POST'])
def missed_auction():
    if not session.get('admin_logged_in'):
        return redirect(url_for('login'))
    else:
        response_missed_data = acv.getMisseauction()
        return jsonify(response_missed_data)
    
@app.route('/lost-auction/', methods=['GET','POST'])
def lost_auction():
    if not session.get('admin_logged_in'):
        return redirect(url_for('login'))
    else:
        lostauction = acv.getlostauction()
        return jsonify(lostauction)
    
@app.route('/won-auction/', methods=['GET','POST'])
def get_won_auction():
    if not session.get('admin_logged_in'):
        return redirect(url_for('login'))
    else:
        wonauction = acv.getwonauction()
        return jsonify(wonauction)

@app.route('/search-auction/',methods=['GET','POST'])
def searchauction():
    if not session.get('admin_logged_in'):
        return redirect(url_for('login'))
    else:
        auctions = acv.searchauction(request.form['searchval'], request.form['status'])
        return jsonify(auctions)

@app.route('/win-lost-auction/',methods=['GET','POST'])
def winlostauction():
    acv.winlostauctions()
    return 'success'

@app.route('/get-notification-list/', methods=['GET','POST'])
def getNotification():
    notifications = acv.getNotificationList()
    return jsonify(notifications)

@app.route('/get-auction-condition/',methods=['GET','POST'])
def getauctioncondition():
    auction_id = request.form['auction_id']
    conditions = acv.getauctioncondition(auction_id)
    return jsonify(conditions)
# code end by pallavi

@app.route('/settingupdate/', methods = ['POST'])
def settingupdate():
    if not session.get('admin_logged_in'):
        return redirect(url_for('login'))
    else:
        if request.method == 'POST' and request.form['setting']:
            if setting.update(1, request.form):
                flash('Discount Percentage has been updated.')
            else:
                flash('Discount Percentage has not been updated.')



            return redirect(url_for('discountmanagement'))



        else:



            return redirect(url_for('discountmanagement'))



@app.route('/profile-edit/')



def profileEdit():



    if not session.get('admin_logged_in'):

        return redirect(url_for('login'))
    else:

        id  = session['admin_logged_id']
        data = admin.read(id);
        role = admin.role(id)
        return render_template('profileedit.html', data = data,role=role)

@app.route('/change-password/')



def changePassword():



    if not session.get('admin_logged_in'):



        return redirect(url_for('login'))



    else:



        id = session['admin_logged_id']
        data = admin.read(id);
        role = admin.role(id)

        return render_template('change_password.html', data = data,role=role)



@app.route('/getmakes', methods=['POST'])



def getmakes():



        if request.method == 'POST' and request.form['makes']:



            data = setting.getmakes(request.form);



            return json.dumps({'makes':data});



        else:



            return redirect(url_for('dashboard'))



@app.route('/getmodel', methods=['POST'])



def getmodel():



        if request.method == 'POST' and request.form['models']:



            data = setting.getmodels(request.form);



            return json.dumps({'model':data});



        else:



            return redirect(url_for('dashboard'))



@app.route('/getqoute', methods=['POST'])



def getqoute():



        if request.method == 'POST' :



            data = qoute.getqoute(request.form)
            proquotesget1 = setting.read(1)
            return json.dumps({'data':data,'proquotesget1':proquotesget1})



        else:



            return redirect(url_for('dashboard'))

@app.route('/get-offer', methods=['POST'])
def getoffer():
        if request.method == 'POST' :
            data = offer.getoffer(request.form);
            return json.dumps({'data':data});
        else:
            return redirect(url_for('dashboard'))

@app.route('/useracceptbid', methods=['POST'])



def useracceptbid():



        if request.method == 'POST' :



            data = acceptedaps.acceptbidsave(request.form);



            return json.dumps({'data':data});



        else:



            return redirect(url_for('dashboard'))



@app.route('/autoinquirysave', methods=['POST'])



def autoinquirysave():



        if request.method == 'POST' :



            data = acceptedaps.autoinquirysave(request.form);



            return json.dumps({'data':data});



        else:



            return redirect(url_for('dashboard'))



@app.route('/inquiryautoupdate', methods=['POST'])



def inquiryautoupdate():



        if request.method == 'POST' :


            model = request.form.getlist("model")
            data = acceptedaps.autoinquirysave(request.form);



            return json.dumps({'data': data});



        else:



            return redirect(url_for('dashboard'))



@app.route('/updateprofile/', methods = ['POST'])
def updateprofile():
    # darshan chnages 31-08-2023 1
    if request.method == 'POST' :
            email_noti = request.form.get("email_noti")
            email_noti_data = 'no';
            if email_noti:
                email_noti_data = 'yes'
                
            result = admin.update(session['admin_logged_id'], request.form,email_noti_data)
            # return [result]
            # flash('profile has been updated')
            if result:
                 response = {'status': 'success', 'message': 'Profile has been updated'}
            else:
                response = {'status': 'error', 'message': 'Failed to update profile'}

            return jsonify(response)
        # darshan chnages 31-08-2023 1 close
        #session.pop('update', None)
    else:
        return redirect(url_for('profileEdit'))


@app.route('/inquiry-list')



# inquiry page route 
@app.route('/inquiry-list')
def inquirylist():
    if not session.get('admin_logged_in'):  
        return redirect(url_for('login'))
    else:
        param = request.args.get('status')
        param1 = request.args.get('dispatch')
        id = session['admin_logged_id']
        role = admin.role(id)
        role_name = role[0][0]
        current_date = datetime.now()
        date_60_days_ago = current_date - timedelta(days=60)

        end_date = current_date.strftime("%Y-%m-%d")
        start_date = date_60_days_ago.strftime("%Y-%m-%d")

        usa_format_start_date = date_60_days_ago.strftime("%m-%d-%Y")
        usa_format_end_date = current_date.strftime("%m-%d-%Y")

        if param1:
            return render_template('inquiry-dispatch.html',role=role, role_name = role_name, start_date = usa_format_start_date, end_date = usa_format_end_date )
        else :
            return render_template('inquiry-new.html',  role=role ,  role_name=role_name,start_date = usa_format_start_date, end_date = usa_format_end_date)

# inquiry data fetch with datatable route for inquiry
@app.route('/get-inquiry-data', methods = ['POST', 'GET'])
def getInquiryData():
    if request.method == 'POST':
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        status = request.form['status']
        draw = request.form['draw']

        # get limitation for data for inquiry
        start = request.form['start']
        length = request.form['length']

        # get column and order for data sorting for inquiry
        orderByColumnIndex = int(request.form['order[0][column]'])
        orderByColumnNameKey = 'columns[' + str(orderByColumnIndex) + '][data]'
        orderByColumnName = request.form[orderByColumnNameKey]
        orderByColumnDirection = request.form['order[0][dir]']

        searchValue = request.form['search[value]']

        inquiry_data = setting.getInquiryData(start_date,end_date,status,start, length, orderByColumnName, orderByColumnDirection, searchValue)

        total_records = setting.get_total_records(start_date, end_date, status, searchValue)

        id = session.get('admin_logged_id')
        role = admin.role(id)
        data_list = []
        for data in inquiry_data:
            abc = ''
            if data[6] != 'Decline':
                if role == (('Super Admin',),):
                    abc = '<input type="checkbox" name="chkArr[]" class="selectChk" value="' + str(data[0]) + '" onchange="singleSelect()">'
            
            if data[10] == "NaN":
                offerif = ''
            elif data[10] == "none":
                offerif = ''
            else:
                offerif = data[11]
            
            car_info = str(data[1]) + ' ' + str(data[2]) + ' ' + str(data[3])

            location = str(data[7])+','+' '+ str(data[8])+' '+str(data[4])



            if data[10] == "NaN":
                revisedprice = 'Not Finished'
            elif data[10] == None:
                revisedprice = 'Not Finished'
            elif data[10] != "":
               revisedprice = '$' + str(data[10]) 
            else:
                revisedprice = '$0.00'

            if data[6] == 'accept':
                if data[14] != None:
                    offer = data[14] 
                else:
                    offer = 'Accepted'
            else:
                offer = 'Not accepted'

            created_date = changeUSDateFormat(data[9])

            btn = '<a class="btn btn-sm btn-primary" href="/inquiry-fetch/{}/?back=inquiry">View</a>'.format(data[0])
            if role == (('Super Admin',),):
                btn += ' <a class="btn btn-sm btn-primary" href="javascript:void(0)" onclick="deleteInquiry({})">Delete</a>'.format(data[0])
                            
            if data[6] == 'accept':
                if data[12] == 'yes':
                    btn += '<span class="dispatch-btn2">Dispatched to Copart</span>'
                else:
                    btn += '<span class="dispatch-btn3">Awaiting Action to Dispatch</span>'
            
            #pallavi changes 12-06-24
            tracked_form = ''
            url = data[13]
            source = data[15]
            medium = data[16]
            campaign = data[17]

            if url and url.strip() != "" and url != "None":
                if url == 'https://t.co/':
                    url = 'https://www.twitter.com/'
                if source != "":
                    tracked_form = f'<b>{url}</b><br /> <b>Src:</b> {source} <br /> <b>Med:</b> {medium} <br /> <b>Cpn:</b> {campaign}'
                else:
                    tracked_form = url
            elif source != "":
                tracked_form = f'<b>Src:</b> {source} <br /> <b>Med:</b> {medium} <br /> <b>Cpn:</b> {campaign}'
   
            #end pallavi code 12-06-24

            # if data[13] == 'https://t.co/' :
            #     tracked_form = 'https://www.twitter.com/'
            # else:
            #     tracked_form = data[13]

            data_dict = {"chk":abc,"offerif": offerif, "car": car_info,'location':location,'form':tracked_form,'revisedprice':revisedprice, 'offer':offer, 'date':created_date, "btn":btn}
            data_list.append(data_dict)
        response = {
            "draw": int(draw),
            "recordsTotal": total_records,
            "recordsFiltered": total_records,
            "data": data_list
        }
        
        return jsonify(response)

# inquiry data fetch with datatable route for inquiry dispatch
@app.route('/get-dispatch-data', methods = ['POST', 'GET'])
def getDispatchData():

    if request.method == 'POST':
        draw = request.form['draw']
        start_date = request.form['start_date']
        end_date = request.form['end_date']

        # get limitation for data for inquiry dispatch
        start = request.form['start']
        length = request.form['length']

        # grt column and order for data sorting for inquiry dispatch
        orderByColumnIndex = int(request.form['order[0][column]'])
        orderByColumnNameKey = 'columns[' + str(orderByColumnIndex) + '][data]'
        orderByColumnName = request.form[orderByColumnNameKey]
        orderByColumnDirection = request.form['order[0][dir]']

        searchData = request.form['search[value]']

        param = 'accepted'
        param1 = 'no'
        id = session.get('admin_logged_id')
        role = admin.role(id)
        decline_data = acceptedaps.read(None,param,param1,start, length, orderByColumnName, orderByColumnDirection, searchData, start_date, end_date)
        total_records = acceptedaps.total_record(None,param,param1,start_date, end_date, searchData)
        data_list = []

        for data in decline_data:

            abc = ''
            if data[6] != 'Decline':
                if role == (('Super Admin',),):
                    abc = '<input type="checkbox" name="chkArr[]" class="selectChk" value="' + str(data[0]) + '" onchange="singleSelect()">'
            
            if data[10] == "NaN":
                offerif = ''
            elif data[10] == "none":
                offerif = ''
            else:
                offerif = data[11]
            
            car_info = str(data[1]) + ' ' + str(data[3]) + ' ' + str(data[2])

            location = str(data[7])+','+' '+ str(data[8])+' '+str(data[4])

            if data[10] == "NaN":
                revisedprice = 'Not Finished'
            elif data[10] == None:
                revisedprice = 'Not Finished'
            elif data[10] != "":
               revisedprice = '$' + str(data[10]) 
            else:
                revisedprice = '$0.00'

            if data[6] == 'accept':
                if data[14] != None:
                    offer = data[14] 
                else:
                    offer = 'Accepted'
            else:
                offer = 'Not accepted'

            created_date = changeUSDateFormat(data[9])

            btn = '<a class="btn btn-sm btn-primary" href="/inquiry-fetch/{}/?back=inquiry">View</a>'.format(data[0])
            if role == (('Super Admin',),):
                btn += ' <a class="btn btn-sm btn-primary" href="javascript:void(0)" onclick="deleteInquiry({})">Delete</a>'.format(data[0])
                            
            if data[6] == 'accept':
                if data[12] == 'yes':
                    btn += '<br><span class="dispatch-btn2">Dispatched to Copart</span>'
                else:
                    btn += '<br><span class="dispatch-btn3">Awaiting Action to Dispatch</span>'
            
            #pallavi changes 12-06-24
            tracked_form = ''
            url = data[13]
            source = data[15]
            medium = data[16]
            campaign = data[17]

            if url and url.strip() != "" and url != "None":
                if url == 'https://t.co/':
                    url = 'https://www.twitter.com/'
                if source != "":
                    tracked_form = f'<b>{url}</b><br /> <b>Src:</b> {source} <br /> <b>Med:</b> {medium} <br /> <b>Cpn:</b> {campaign}'
                else:
                    tracked_form = url
            elif source != "":
                tracked_form = f'<b>Src:</b> {source} <br /> <b>Med:</b> {medium} <br /> <b>Cpn:</b> {campaign}'

            # tracked_form = ''
            # if data[13] is not None and data[13].strip() != "" and data[13] != "None" and  data[15] != "":
            #     tracked_form = f'<b>{data[13]}</b><br /> <b>Src:</b> {data[15]} <br /> <b>Med:</b> {data[16]} <br /> <b>Cpn:</b> {data[17]}'
            # elif data[13] is not None and data[13].strip() != "" and data[13] != "None":
            #     tracked_form = data[13]
            # elif data[15] != "":
            #     tracked_form = f'<b>Src:</b> {data[15]} <br /> <b>Med:</b> {data[16]} <br /> <b>Cpn:</b> {data[17]}'
            #end pallavi code 12-06-24
                

            # if data[13] == 'https://t.co/' :
            #     tracked_form = 'https://www.twitter.com/'
            # else:
            #     tracked_form = data[13]

            data_dict = {"chk":abc,"offerif": offerif, "car": car_info,'location':location,'form':tracked_form,'revisedprice':revisedprice, 'offer':offer, 'date':created_date, "btn":btn}
            data_list.append(data_dict)

        response = {
            "draw": int(draw),
            "recordsTotal": total_records,
            "recordsFiltered": total_records,
            "data": data_list
        }
        
        return jsonify(response)
@app.route('/inquiry-fetch/<int:id>/')
def inquiryFetch(id):
    
    data = acceptedaps.readnew(id)
    state = commonarray.getstate()
    back = request.args.get('back')
    state_n = ''
    id = session['admin_logged_id']
    role = admin.role(id)
    for number in state:
        if number['id']==data[0][21] :
            state_n = number['name']

    return render_template('inquiry-fetch.html',data=data,state_n=state_n,role=role , user_id =id,back=back)

@app.route('/book')



def book():



    data = db.read(None)



    return render_template('book.html', data = data)



@app.route('/add/')



def add():



    return render_template('add.html')







@app.route('/addphone', methods = ['POST', 'GET'])



def addphone():



    if request.method == 'POST' and request.form['save']:



        if db.insert(request.form):



            flash("A new phone number has been added")



        else:



            flash("A new phone number can not be added")







        return redirect(url_for('book'))



    else:



        return redirect(url_for('book'))







@app.route('/update/<int:id>/')



def update(id):



    data = db.read(id);







    if len(data) == 0:



        return redirect(url_for('book'))



    else:



        session['update'] = id



        return render_template('update.html', data = data)







@app.route('/updatephone', methods = ['POST'])



def updatephone():



    if request.method == 'POST' and request.form['update']:







        if db.update(session['update'], request.form):



            flash('A phone number has been updated')



        else:



            flash('A phone number can not be updated')



        session.pop('update', None)







        return redirect(url_for('book'))



    else:



        return redirect(url_for('book'))







@app.route('/delete/<int:id>/')



def delete(id):



    data = db.read(id);







    if len(data) == 0:



        return redirect(url_for('book'))



    else:



        session['delete'] = id



        return render_template('delete.html', data = data)







@app.route('/deletephone', methods = ['POST'])



def deletephone():



    if request.method == 'POST' and request.form['delete']:







        if db.delete(session['delete']):



            flash('A phone number has been deleted')



        else:



            flash('A phone number can not be deleted')



        session.pop('delete', None)







        return redirect(url_for('book'))



    else:



        return redirect(url_for('book'))



@app.route('/deleteinquiry', methods=['POST'])

def deleteinquiry():

        if request.method == 'POST':

            data = acceptedaps.deleteinquiry(request.form);

            return json.dumps({'model':data});

        else:

            return redirect(url_for('dashboard'))

@app.route('/getnotificationcounter', methods=['POST'])

def getnotificationcounter():

        if request.method == 'POST':

            data = acceptedaps.getnotificationcounter();

            return json.dumps({'model':data});

        else:

            return redirect(url_for('dashboard'))

@app.route('/vehicleinfocheck', methods=['POST'])
def vehicleinfocheck():
    if request.method == 'POST' and request.form['vehicle'] :
        if request.form:
            year_check = acceptedaps.modelYearcheck(request.form)
            make_check = acceptedaps.makecheck(request.form)
            makeID = acceptedaps.getmakeID(request.form)
            year_id = acceptedaps.make_year_check(request.form,makeID)
            model_check = acceptedaps.modelcheck(request.form,year_id)
            return json.dumps({'status': True})
        else:
            return json.dumps({'status': False})

@app.route('/all-delete-inquiry', methods=['POST'])
def deleteinquiryall():
    if request.method == 'POST':

            data = acceptedaps.deleteinquiryall(request.form)

            return json.dumps({'model':data})

    else:
            return redirect(url_for('dashboard'))



@app.route('/emailsent')
def emailsent():

    # msg = Message('Hello from the other side!', sender =   'cyblance.nigam@gmail.com', recipients = ['shadab.cyblance@gmail.com'])
    # msg.body = "Hey Paul, sending you this email from my Flask app, lmk if it works"
    # a= mail.send(msg)
    # flash(a)
    # return redirect(url_for('book'))

    email = "test@yourcarintocash.com"
    password = "0LrxDMAK(sbn"
    to = ["cyblance.nigam@gmail.com"]

    with smtplib.SMTP_SSL('mail.yourcarintocash.com', 465) as smtp:

        smtp.login(email, password)

        subject = "testing mail sending"
        body = "the mail itself"

        msg = "Subject: {}\n\n{}".format(subject, body)

        smtp.sendmail(email, to, msg)





@app.errorhandler(404)



def page_not_found(error):



    return render_template('error.html')


@app.route('/setvinmake', methods=['POST'])
def setvinmake():

        data1 = request.form
        if request.method == 'POST' :

            data = acceptedaps.getvinmake(data1);
            return json.dumps({'data':data});
        else:
            return redirect(url_for('dashboard'))

@app.route('/setvinmodel', methods=['POST'])
def setvinmodel():

        data1 = request.form
        if request.method == 'POST' :

            data = acceptedaps.getvinmodel(data1);
            return json.dumps({'data':data});
        else:
            return redirect(url_for('dashboard'))

@app.route('/add-admin/')
def add_admin():
    if not session.get('admin_logged_in'):
        return redirect(url_for('login'))
    else:
        # darshan changes 31-08-2023 2
        role = session['role']
        if role == 'Super Admin':
            id = session['admin_logged_id']
            role = admin.role(id)
            data = admin.listing()
            return render_template('add_admin.html',data=data,role=role)
        else:
            return redirect(url_for('dashboard'))

@app.route("/admin_insert/" ,methods=['POST'])
def admin_insert():
    if request.method == 'POST' :
        email_noti = request.form.get("email_noti")
        email_noti_data = 'no';
        if email_noti:
            email_noti_data = 'yes'
        data = admin.insert(request.form,email_noti_data)
        return [data]
        flash("inserted succesfulyy")
        return "insertd succees"
    else:
        flash("not inserted")
        return redirect(url_for("add-admin"))

@app.route("/removedata/<int:id>/" , methods = ['POST'])
def removebtn(id):
    data = admin.remove(id)
    return [data]

@app.route("/editdata/<int:id>",methods=['GET'])
def editdata(id):
    data = admin.editdata(id)
    return [data]

@app.route("/validation_email/" , methods=['POST'])
def validation_email():
    if request.method == 'POST':
        data = admin.valid(request.form)
        return [data]

@app.route("/role/")
def role():
    id = session['admin_logged_id']
    role = session['role']
    return render_template("header.html" , role=role)

@app.route("/addusertyps"  , methods=['POST'])
def addusertyps():
    if request.method == 'POST':
        data =admin.updatepass(request.form)
        return [data]

@app.route('/getofferid', methods=['POST'])
def getofferid():

    data1 = request.form
    #return data1
    if request.method == 'POST' :
        data = acceptedaps.getofferid(data1);
        return json.dumps({'data':data});
    else:
        return redirect(url_for('dashboard'))
        
@app.route('/updateofferid', methods=['POST'])
def updateofferid():

    data1 = request.form
    if request.method == 'POST' :
        data = acceptedaps.updateofferid(data1);
        return json.dumps({'data':data});
    else:
        return redirect(url_for('dashboard'))
        
@app.route('/updateofferidcondition', methods=['POST'])
def updateofferidcondition():

    data1 = request.form
    if request.method == 'POST' :
        data = acceptedaps.updateofferidcondition(data1);
        if data1['fetch_type1']=='condition report':    
            fetchPrice = acceptedaps.fetchPriceFrom(data1['id'],'condition report',data1['fet_confition_id1'],data1['condition_title1'])
        else:
            fetchPrice = acceptedaps.fetchPriceFrom(data1['id'],'copart','','')
        return json.dumps({'data':data});
    else:
        return redirect(url_for('dashboard'))

ALLOWED_EXTENSIONS = set(['txt', 'png', 'jpg', 'jpeg', 'gif'])
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/declineinsert" , methods = ['POST'])
def declineinsert():
    if request.method == 'POST':
        data = acceptedaps.d_insert(request.form)
        return [data]
    else:
        return "error"

@app.route("/decline-offer-data/<int:id>" , methods=['Get'])
def decline_offer_data(id):
    decline_data = acceptedaps.decline_data(id)
    return [decline_data]


# get decline offer data route
@app.route('/decline-list')
def declinelist():
    if not session.get('admin_logged_in'):
        return redirect(url_for('login'))
    else:
        id = session['admin_logged_id']
        role = admin.role(id)
        role_name = role[0][0]
        current_date = datetime.now()
        date_60_days_ago = current_date - timedelta(days=60)

        end_date = current_date.strftime("%Y-%m-%d")
        start_date = date_60_days_ago.strftime("%Y-%m-%d")

        usa_format_start_date = date_60_days_ago.strftime("%m-%d-%Y")
        usa_format_end_date = current_date.strftime("%m-%d-%Y")

        # today = date.today()
        # first_day_of_month = today.replace(day=1)
        # last_day_of_month = today.replace(day=1, month=today.month % 12 + 1) - timedelta(days=1)
        # start_date = first_day_of_month.strftime("%Y-%m-%d")
        # end_date = last_day_of_month.strftime("%Y-%m-%d")
        return render_template('decline-inquiry.html', role=role, role_name = role_name, start_date= usa_format_start_date, end_date= usa_format_end_date)

@app.route('/get-decline-data' , methods = ['POST'])
def get_decline_data():
    if request.method == 'POST':
        draw = request.form['draw']

        start_date = request.form['start_date']
        end_date = request.form['end_date']

        # get limitation for data for decline offer
        start = request.form['start']
        length = request.form['length']

        # get column and order for data sorting for decline offer
        orderByColumnIndex = int(request.form['order[0][column]'])
        orderByColumnNameKey = 'columns[' + str(orderByColumnIndex) + '][data]'
        orderByColumnName = request.form[orderByColumnNameKey]
        orderByColumnDirection = request.form['order[0][dir]']
        searchDate = request.form['search[value]']

        decline_data = acceptedaps.getdeclineoffer(start, length, start_date, end_date, orderByColumnName, orderByColumnDirection, searchDate)
        total_records = acceptedaps.get_total_records_decline(start_date, end_date, searchDate)
        id = session.get('admin_logged_id')
        role = admin.role(id)
        data_list = []
        for data in decline_data:
            abc = ''
            if role == (('Super Admin',),):
                abc = '<input type="checkbox" name="chkArr[]" class="selectChk1" value="' + str(data[0]) + '" onchange="singleSelect()">'

            offerif = ''
            if data[6] != 'incomplete':
                offerif = data[11] 
            
            car_info = str(data[1]) + ' ' + str(data[3]) + ' ' + str(data[2])

            location = str(data[7])+','+' '+ str(data[8])+' '+str(data[4])

            # if data[5] == "NaN":
            #     originalprice = 'Not Finished'
            # elif data[5] == None:
            #     originalprice = 'Not Finished'
            # elif data[5] != "":
            #     originalprice = str(data[5])
            # else:
            #     originalprice = '$0.00'

            if data[10] == "NaN":
                revisedprice = 'Not Finished'
            elif data[10] == None:
                revisedprice = 'Not Finished'
            elif data[10] != "":
               revisedprice = str(data[10]) 
            else:
                revisedprice = '$0.00'

            offer = 'Declined'
            
            created_date = changeUSDateFormat(data[9])

            btn = '<a class="btn btn-sm btn-primary" href="/inquiry-fetch/{}/?back=inquiry">View</a>'.format(data[0])
            if role == (('Super Admin',),):
                btn += ' <a class="btn btn-sm btn-primary" href="javascript:void(0)" onclick="deleteInquiry({})">Delete</a>'.format(data[0])
                            
            if data[6] == 'accept':
                if data[12] == 'yes':
                    btn += '<span class="dispatch-btn2">Dispatched to Copart</span>'
                else:
                    btn += '<span class="dispatch-btn3">Awaiting Action to Dispatch</span>'

            #pallavi changes 12-06-24
            tracked_form = ''
            url = data[13]
            source = data[15]
            medium = data[16]
            campaign = data[17]

            if url and url.strip() != "" and url != "None":
                if url == 'https://t.co/':
                    url = 'https://www.twitter.com/'
                if source != "":
                    tracked_form = f'<b>{url}</b><br /> <b>Src:</b> {source} <br /> <b>Med:</b> {medium} <br /> <b>Cpn:</b> {campaign}'
                else:
                    tracked_form = url
            elif source != "":
                tracked_form = f'<b>Src:</b> {source} <br /> <b>Med:</b> {medium} <br /> <b>Cpn:</b> {campaign}'

            # tracked_form = ''
            # if data[13] is not None and data[13].strip() != "" and data[13] != "None" and  data[15] != "":
            #     tracked_form = f'<b>{data[13]}</b><br /> <b>Src:</b> {data[15]} <br /> <b>Med:</b> {data[16]} <br /> <b>Cpn:</b> {data[17]}'
            # elif data[13] is not None and data[13].strip() != "" and data[13] != "None":
            #     tracked_form = data[13]
            # elif data[15] != "":
            #     tracked_form = f'<b>Src:</b> {data[15]} <br /> <b>Med:</b> {data[16]} <br /> <b>Cpn:</b> {data[17]}'
            #end pallavi code 12-06-24
            
            # tracked_form = ""
            
            # if data[13] == 'https://t.co/' :
            #     tracked_form = 'https://www.twitter.com/'
            # else:
            #     tracked_form = data[13]

            data_dict = {"chk":abc,"offerif": offerif, "car": car_info,'location':location,'form':tracked_form,'revisedprice':revisedprice, 'offer':offer, 'date':created_date, "btn":btn}

            data_list.append(data_dict)
        response = {
            "draw": int(draw),
            "recordsTotal": total_records,
            "recordsFiltered": total_records,
            "data": data_list
        }
        
        return jsonify(response)

@app.route('/ajax-image-upload', methods=['POST'])
def ajax_upload_image():
	if 'files[]' not in request.files:
		resp = jsonify({'message' : 'No file part in the request'})
		resp.status_code = 400
		return resp
	files = request.files.getlist('files[]')
	errors = {}
	success = False
	for file in files:
		if file and allowed_file(file.filename):
			#filename = secure_filename(file.filename)
			filename = filenamegenerator(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			errors[filename] = '1'
			success = True
		else:
			errors[file.filename] = '2'

	if success and errors:
		#errors['message'] = 'File(s) successfully uploaded'
		resp = jsonify(errors)
		resp.status_code = 206
		return resp
	if success:
		#resp = jsonify({'message' : 'Files successfully uploaded'})
		resp.status_code = 201
		return resp
	else:
		resp = jsonify(errors)
		resp.status_code = 201
		return resp
@app.template_filter('getjson')
def getjson(data):
   return json.loads(data);    
@app.route('/get-condition-sessionid', methods=['POST'])
def getconditionsessionid():
    sessionid = sessionidgenerator()
    return [sessionid]
@app.route('/condition-filter')
def conditionfilter():

    if not session.get('admin_logged_in'):
        return redirect(url_for('login'))
    else:
        #return 'hi'
        session.pop('sessionid',None)
        modelresult = acceptedaps.getmakes1()
        data = acceptedaps.getConditionalFilter()
        #new code value added start here country
        states = acceptedaps.getState()
        if not session.get('sessionid'):
            session['sessionid'] = sessionidgenerator()
        sessionid = session['sessionid']
        
        idssss = session['admin_logged_id']
        role = admin.role(idssss)
        #new code value added end here country
        return render_template('condition-filter.html',modelresult=modelresult,data=data,states=states,role=role)
    
#11-1-2024 start
@app.route('/condition-filter-softdeleted')
def conditionfiltersoftdeleted():

    if not session.get('admin_logged_in'):
        return redirect(url_for('login'))
    else:
        #return 'hi'
        session.pop('sessionid',None)
        modelresult = acceptedaps.getmakes1()
        data = acceptedaps.getConditionalFilterDeleted()
        #new code value added start here country
        states = acceptedaps.getState()
        if not session.get('sessionid'):
            session['sessionid'] = sessionidgenerator()
        sessionid = session['sessionid']
        #new code value added end here country
        return render_template('condition-filter-deleted.html',modelresult=modelresult,data=data,states=states)
#11-1-2024 end

@app.route('/conditional-report-detail/<int:id>/')

def conditionalReportDetail(id):
    data = acceptedaps.getconditional(id);
    #new code value added start here country
    stateData = acceptedaps.getAllState(data[0][49]);

    stateComma = ''
    if stateData:
        for k1 in stateData:
            stateComma = stateComma+k1[0]+','
    length= len (stateComma)
    stateComma=stateComma[ :length-1]
    #new code value added end here country
    print(data[0][31])
    allzipcode = json.loads(data[0][31])
    print(allzipcode)
    return render_template('conditional-fetch.html',data=data,stateComma=stateComma, allzipcode = allzipcode)

@app.route('/conditional-report-detail-softdeleted/<int:id>/')

def conditionalReportDetailsoftdeleted(id):
    data = acceptedaps.getconditional(id);
    #new code value added start here country
    stateData = acceptedaps.getAllState(data[0][49]);

    stateComma = ''
    if stateData:
        for k1 in stateData:
            stateComma = stateComma+k1[0]+','
    length= len (stateComma)
    stateComma=stateComma[ :length-1]
    #new code value added end here country
    print(data[0][31])
    allzipcode = json.loads(data[0][31])
    print(allzipcode)
    return render_template('conditional-fetch-softdeleted.html',data=data,stateComma=stateComma, allzipcode = allzipcode)




@app.route('/deleteconditionalreporthard', methods=['POST'])
def deleteconditionalreporthard():
    if request.method == 'POST':
        data = acceptedaps.deleteconditionhard(request.form);
        return json.dumps({'model':data});
    else:
        return redirect(url_for('dashboard'))
    
@app.route('/deleteconditionalreport', methods=['POST'])
def deleteconditionalreport():
    if request.method == 'POST':
        data = acceptedaps.deletecondition(request.form);
        return json.dumps({'model':data});
    else:
        return redirect(url_for('dashboard'))
    
@app.route('/restoreconditionalreport', methods=['POST'])
def restoreconditionalreport():
    print('hihihihihihihi')
    if request.method == 'POST':
        data = acceptedaps.restorecondition(request.form);
        return json.dumps({'model':data});
    else:
        return redirect(url_for('dashboard'))



@app.route("/get-conditional-model/<int:id>" , methods=['Get'])
def get_conditional_model(id):
    decline_data = acceptedaps.getmodels1(id)
    #return [decline_data]
    return json.dumps({'data':decline_data});

@app.route("/get-conditional-reoport-data/<int:id>" , methods=['Get'])
def get_conditional_reoport_data(id):
    decline_data = acceptedaps.getConditionalData(id)
    return json.dumps({'data':decline_data});

@app.route("/get-conditional-list" , methods=['Get'])
def get_conditional_list():
    data = acceptedaps.get_conditional_list()
    return json.dumps({'data':data})

#11-1-2024 start
@app.route("/get-conditional-list-deleted" , methods=['Get'])
def get_conditional_list_deleted():
    data = acceptedaps.get_conditional_list_deleted()
    return json.dumps({'data':data})
#11-1-2024 end
@app.route('/get-zipcode-list' , methods = ['POST', 'GET'])
def getzipcodelist():
    if request.method == 'POST':      
        data = acceptedaps.get_zipcode_list(request.form)   
        return json.dumps({'status': True })
@app.route('/condition-filter-add', methods=['POST'])
def conditionfilteradd():
    if request.method == 'POST' :
        modelresult = acceptedaps.saveConditionReportAdd(request.form)
        return json.dumps({'result':modelresult});
@app.route('/condition-filter-submit', methods=['POST'])
def conditionfiltersubmit():
    if request.method == 'POST' :

        dataAll = request.form
        getFilterTitleData = request.form.getlist("filter_title")
        getMakeData = request.form.getlist("make[]")
        getModelData = request.form.getlist("model[]")
        getBodyDamageData = request.form.getlist("damage[]")
        getestimateData = request.form.getlist("Estimate")
        getMakeDatass = request.form.getlist("model[1]")
        getAirBag = request.form.getlist('airbag[]')
        getDrive = request.form.getlist('drive[]')
        getSDamage = request.form.getlist('sdamage[]')
        getKey = request.form.getlist('key[]')
        getTitleType = request.form.getlist('title[]')
        getFireDamage = request.form.getlist('fire_damage[]')
        getDamage = request.form.getlist("damage[]")
        getDamageImg = request.form.getlist("damageimg[]")
        unable_to_verify = request.form.get("unable_to_verify")

        #new code value added start here country
        usa = request.form.get("usa")
        getStateData = request.form.getlist("state[]")
        usa_data = '';
        if usa:
            usa_data = 'USA'

        stateComma = '';
        if getStateData:
            for k1 in getStateData:
                stateComma = stateComma+k1+','
        #new code value added end here country
        
        unable_to_verify_data = 'no';
        if unable_to_verify:
            unable_to_verify_data = 'yes'

        #print(unable_to_verify_data+'unable_to_verify_data')
        
        damageComma = '';
        if getBodyDamageData:
            for k1 in getBodyDamageData:
                damageComma = damageComma+k1+','

        airbagComma = '';
        if getAirBag:
            for k1 in getAirBag:
                airbagComma = airbagComma+k1+','


        driveComma = '';
        if getDrive:
            for k1 in getDrive:
                driveComma = driveComma+k1+','

        getSDamageComma = '';
        if getSDamage:
            for k1 in getSDamage:
                getSDamageComma = getSDamageComma+k1+','

        keyComma = '';
        if getKey:
            for k1 in getKey:
                keyComma = keyComma+k1+','

        titleComma = '';
        if getTitleType:
            for k1 in getTitleType:
                titleComma = titleComma+k1+','
        firDamageComma = '';
        if getFireDamage:
            for k1 in getFireDamage:
                firDamageComma = firDamageComma+k1+','

        

        getDamageImg1 = []
        getDamage1 = ''
        sdamageImg_s = ''
        if getDamage:
            if getDamageImg:
                getDamageImg1 = getDamageImg
                for a11 in getDamageImg1:
                    sdamageImg_s = sdamageImg_s+a11+','
                    #print(sdamageImg_s)

        abc1 = json.dumps(getDamageImg1)

        make_id_s = '';
        model_id_s = '';
        adcostrray = []
        if getMakeData:
            for k in getMakeData:
                make_id = k
                make_id_s = make_id_s+k+','
                model_id = request.form.getlist("model["+k+"]")
                if model_id:
                    model_id1 = model_id
                    for k1 in model_id:
                        model_id_s = model_id_s+k1+','  
                else:
                    model_id1 = 'all'
                adcostrray.append({'make_id' : make_id, 'model_id' : model_id1})
        else:
            adcostrray.append({'make_id' : 'all', 'model_id' : 'all'})

        abc = json.dumps(adcostrray)
        #new code value added start here country
        modelresult = acceptedaps.saveConditionReport(dataAll,getestimateData,abc,getDamage1,abc1,make_id_s,model_id_s,sdamageImg_s,damageComma,airbagComma,driveComma,getSDamageComma,keyComma,titleComma,firDamageComma,unable_to_verify_data,usa_data=usa_data,stateComma=stateComma,getStateData=getStateData)
        #new code value added end here country
        
        makeFlag = 'no'
        if getMakeData:
            makeFlag = 'yes'

        modelFlag = 'no'
        if getModelData:
            modelFlag = 'yes'

        damageFlag = 'no'
        if getBodyDamageData:
            damageFlag = 'yes'

        return json.dumps({'result':modelresult,'getMakeData':getMakeData,'getModelData':getModelData,'dataAll':dataAll,'adcostrray':adcostrray});

@app.route('/getqoute-conditional', methods=['POST'])
def frontend1():
    if request.method == 'POST' :
        unable_to_verify = request.form.get("utv")
        unable_to_verify_data = '';
        if unable_to_verify:
            unable_to_verify_data = 'yes'
            
        dataAll = request.form
        record_id = dataAll['record_id']
        
        conditionalLogic = qoute.frontend1(request.form,unable_to_verify_data)
        return json.dumps({'conditionalLogic':conditionalLogic,'test':'test'});
    else:
        return redirect(url_for('dashboard'))

@app.route('/share')
def share():
    sharing_amt = request.args.get('amt')
    data = acceptedaps.get_price(sharing_amt)
    return render_template('share.html' , data = data,sharing_amt=sharing_amt)

@app.route("/admin/current_location")
def current_location():
    return render_template("current_location.html")

@app.route('/get_location_using_zip' ,methods=['POST','Get'])
def get_location_using_zip():
    if request.method == 'POST':
        data  =  acceptedaps.getzipcode(request.form)
        if data:
            return json.dumps({'status': True , 'data' : data})
        else:
            return json.dumps({'status': False})



@app.route('/insert_location_using_zip' ,methods=['POST','Get'])
def insert_location_using_zip():
    if request.method == 'POST':
        data  =  acceptedaps.insert_zip_code(request.form)
        return [data]

@app.route("/get_location_value" ,methods=['POST','Get'] )
def get_location_value():
    if request.method == 'POST':
        sharing_amt = request.form
        a = sharing_amt['id']
        # print(a)
        data = acceptedaps.get_price(a)
        # print(data)
        return [data]

@app.route('/notesadd', methods=['POST','Get'])
def notesadd():
    if request.method == 'POST':
        print(request.form)
        if notes.noteadd(request.form):
            return json.dumps({'status': True})
        else:
            return json.dumps({'status': False})

@app.route('/get-notes/<id>', methods = ['POST', 'GET'])
def getnotes(id):
    notefile = notes.get_notes(id)
    return jsonify({'data':notefile})


@app.route('/notes-delete/<id>', methods = ['POST', 'GET'])
def notesdelete(id):
    notefile = notes.delete_notes(id)
    if notefile:
        return json.dumps({'status': True})
    else:
        return json.dumps({'status': False})

@app.route('/update_status/', methods=['POST','Get'])
def update_status():
    if request.method == 'POST':
        # a = request.form
        # print("aa")
        # return [a]
        if acceptedaps.update_status(request.form):
            return json.dumps({'status': True})
        else:
            return json.dumps({'status': False})

@app.route('/file-upload', methods=['POST'])
def ajax_upload_file():
    if 'files[]' not in request.files:
        resp = jsonify({'message' : 'No file part in the request'})
        resp.status_code = 400
        return resp
    files = request.files.getlist('files[]')
    errors = {}
    success = False
    for file in files:
        if file and allowed_file1(file.filename):
            filename = filenamegenerator(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            errors[filename] = '1'
            success = True
        else:
            errors[file.filename] = '2'

    if success and errors:
        resp = jsonify(errors)
        resp.status_code = 206
        return resp
    if success:
        resp.status_code = 201
        return resp
    else:
        resp = jsonify(errors)
        resp.status_code = 201
        return resp

@app.route('/file-upload-test-test', methods=['POST', 'GET'])
def ajax_upload_filerrtrtrtrtrtrt():
    token_url = "https://buy-api-staging.gateway.nonprod.acvauctions.com/token"
    #client_id = "your_client_id"
    #client_secret = "your_client_secret"
    username = "twincitybuying@twincity.com"
    password = "TwinCity123!"

    data = {
        "grant_type": "password",
        "username": username,
        "password": password,
        #"client_id": client_id,
        #"client_secret": client_secret
    }

    response = requests.post(token_url, data=data)

    if response.status_code == 200:
        access_token = response.json()["access_token"]
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }
        print(access_token)
    else:
        print(f"Error: Unable to obtain access token. Status Code: {response.status_code}")

    return ''

# code added by pallavi

user_details = admin.getjwttoken(acv_user()[0])

pubnub.set_stream_logger('pubnub', logging.DEBUG)

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
            auction_id = message_data['data']['id']
            return f"Auction launched with ID: {auction_id}"

@app.route('/listen-for-auctions')
def listen_for_auctions():
    pubnub_auth_key = PUBNUB_PUBLISH_KEY
    if not pubnub_auth_key:
        return "Failed to obtain PubNub authKey. Check ACV login API response."
    
    pubnub = configure_pubnub(pubnub_auth_key)

    data = pubnub.add_listener(MyListener())
    pubnub.subscribe().channels("auctions").execute()

    return "Now listening for auction events...",data

@app.template_filter('change_us_date_formate')
def changeUSDateFormat(date,input_format='%Y-%m-%d %H%M%S',time_format='%H%M%S'):
    if isinstance(date, datetime): 
        date_str = date.strftime(input_format)
        time_str = date.strftime(time_format) 
    else:
        date_str = date
        time_str = ''
    date_obj = datetime.strptime(date_str, input_format)
    time_obj = datetime.strptime(time_str, time_format)
    return date_obj.strftime('%m/%d/%Y') + ' ' + time_obj.strftime('%H:%M:%S')

#pallavi changes 12-06-24
@app.route('/remove-zipcode', methods=['POST'])
def remove_zipcode():
    """
    Removes a zipcode from the accepted applications.

    Returns:
        str: JSON response containing the removed zipcode.
    """
    if request.method == 'POST':
        data = acceptedaps.remove_zipcode(request.form)
        return json.dumps({'model':data})
#end pallavi code 12-06-24


# def simulate_task(scheduler):

#     scheduler.enter(40, 1, acv_login, (scheduler))

#     scheduler.enter(60, 1, auction_save.latest_auctions,())

# @app.route('/start_task/')
# def start_task():
#     scheduler = sched.scheduler(time.time, time.sleep)
#     scheduler.enter(0, 1, simulate_task, (scheduler,))
#     thread = threading.Thread(target=scheduler.run)
#     thread.start()
    
#     return 'Task started successfully.'

@app.route('/get-auction-proqoute', methods=['POST','GET'])
def get_proqoute():
    #return 'ninnininini'
    data = acv.get_proqoute()
    return 'dfdsfdfdsfddsffdsfds'

scheduler = BackgroundScheduler()

start_time = datetime.now() + timedelta(hours=6)

# scheduler.add_job(func=refresh_token, trigger='cron', hour='*', minute='*',second='*/30')
scheduler.add_job(func=acv_login, trigger='cron', hour='*', minute='*',second='*/5')
scheduler.add_job(func=latest_auctions, trigger='cron', hour='*', minute='*', second='*/10')
# scheduler.add_job(func=Proqoute.generateproqoute, trigger='cron', hour='*', minute='*',second='*/50')
# scheduler.add_job(func=auction_place_bid.acv_auction_place_bid, trigger='cron', hour='*', minute='*', second='*/30')
# scheduler.add_job(func=remove_auction, trigger='cron', hour=start_time.hour, minute=start_time.minute)
# scheduler.add_job(func=won_auction, trigger='cron', hour='*', minute='*/3')
# scheduler.add_job(func=PubNubNotification.auction_pub_nub_notification, trigger='cron', hour='*', minute='*',second='*/1')
# scheduler.add_job(func=auction_1_min_left, trigger='cron', hour='*', minute='*', second='*/5')
# scheduler.add_job(func=auction_10_min_left, trigger='cron', hour='*', minute='*', second='*/30')
scheduler.start()
    
# @app.route('/run-crone-job/')
# def schedule_cron_job():
#     schedule.every(20).seconds.do(acv_login)
#     schedule.every(30).seconds.do(latest_auctions)
    # schedule.every(1).minutes.do(auction_pub_nub_notification)
    # schedule.every(3).minutes.do(won_auction)
    # schedule.every(45).seconds.do(auction_place_bid.acv_auction_place_bid)
    # schedule.every(30).seconds.do(auction_10_min_left)
    # schedule.every(5).seconds.do(auction_1_min_left)
    # schedule.every(1).minutes.do(remove_auction)
    # schedule.every(1).minutes.do(OutBid.auction_out_bid)
    
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)

# code ended by pallavi

@app.route('/get-light-count/', methods=['POST','GET'])
def get_light_count():
        data = acceptedaps.countslights(4417936)
        return json.dumps({'data':data})

if __name__ == "__main__":
    # code added by pallavi
    # schedule_cron_job()
    # scheduler.start()
    # code ended by pallavi
    app.run(host='192.168.1.179', port=9020)
