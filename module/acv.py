import pymysql
import datetime
import json
import http.client
import traceback
from datetime import date

class ACV:
    def connect(self):
        return pymysql.connect(host="localhost", user="root", password="", database="carintocash", charset='utf8mb4')

    def storeToken(self, id, pubnub_auth_key, pubnub_expiration, pubnub_subscribe_key, refresh_token):
        con = ACV.connect(self)
        cursor = con.cursor()
        try:

            cursor.execute("SELECT * FROM acv_jwt_token where user_id = %s", (id,))
            fetchone = cursor.fetchone()

            if fetchone is not None:
                cursor.execute("UPDATE acv_jwt_token set pubnub_auth_key = %s, pubnub_expiration = %s, pubnub_subscribe_key = %s, refresh_token = %s where user_id = %s", (pubnub_auth_key, pubnub_expiration, pubnub_subscribe_key,refresh_token,id))
            else:
                cursor.execute("INSERT INTO acv_jwt_token (user_id,pubnub_auth_key,pubnub_expiration,pubnub_subscribe_key,refresh_token) VALUES (%s, %s, %s, %s, %s)", (id,pubnub_auth_key, pubnub_expiration, pubnub_subscribe_key,refresh_token))
            con.commit()
            return "Token has been stored successfully."
        except:
            return "error"
        finally:
            con.close()
    
    def storeRefreshToken(self,token,id):
        con = ACV.connect(self)
        cursor = con.cursor()
        try:
            cursor.execute("SELECT * FROM acv_jwt_token where user_id = %s", (id,))
            fetchone = cursor.fetchone()
            if fetchone is not None:
                cursor.execute("UPDATE acv_jwt_token set jwt_token = %s where user_id = %s", (token, id))
            else:
                cursor.execute("INSERT INTO acv_jwt_token (jwt_token) VALUES (%s) where user_id = %s", (token,id))
            con.commit()
            return "Token has been stored successfully."
        except:
            return "error"
        finally:
            con.close()

    def getjwttoken(self,id):
        con = ACV.connect(self)
        cursor = con.cursor()
        try:
            cursor.execute("SELECT jwt_token,user_id,pubnub_auth_key,pubnub_subscribe_key,refresh_token FROM acv_jwt_token where user_id = %s",(id))
            return cursor.fetchone()
        except:
            return "error"
        finally:
            con.close()

    def insertauctiondata(self, data):
        con = ACV.connect(self)
        cursor = con.cursor()
        try:     
            body_damage = ""
            # major, moderate, minor body damage are false
            if data['conditionReport']['sections'][0]['questions'][2]['selected'] == 0 and data['conditionReport']['sections'][0]['questions'][1]['selected'] == 0 and data['conditionReport']['sections'][0]['questions'][0]['selected'] == 0:
                body_damage = 'No, my vehicle is in good shape!'

            # major body damage is true and moderate body damage is false
            elif data['conditionReport']['sections'][0]['questions'][2]['selected'] == 1 and data['conditionReport']['sections'][0]['questions'][1]['selected'] == 0:
                body_damage = 'FR,RR,SD,TP'
            
            # moderate body damage is true and minor body damage is false
            elif data['conditionReport']['sections'][0]['questions'][1]['selected'] == 1 and data['conditionReport']['sections'][0]['questions'][0]['selected'] == 0:
                body_damage = 'FR'
            
            # major body damage is true and minor body damage is false
            elif data['conditionReport']['sections'][0]['questions'][2]['selected'] == 1 and data['conditionReport']['sections'][0]['questions'][0]['selected'] == 0:
                body_damage = 'FR,RR,SD,TP'
            
            #major body damage is true
            elif data['conditionReport']['sections'][0]['questions'][2]['selected'] == 1:
                body_damage = 'FR,RR,SD,TP'
            
            #moderate body damage is true
            elif data['conditionReport']['sections'][0]['questions'][1]['selected'] == 1:
                body_damage = 'FR'
            
            #minor body damage is true
            elif data['conditionReport']['sections'][0]['questions'][0]['selected'] == 1:
                body_damage = 'No, my vehicle is in good shape!'
                
            airbag_value = 'N'
            if data['conditionReport']['sections'][5]['questions'][13]['selected'] == 1:
                airbag_value = 'Y'

            start_and_drive = ''
            # if engine_does_not_start is false and engine_does_not_crank is false
            if data['conditionReport']['sections'][2]['questions'][2]['selected'] == 0 and data['conditionReport']['sections'][2]['questions'][1]['selected'] == 0:
                # engine_does_not_stay_running is true or vehicle inoperable is true
                if data['conditionReport']['sections'][2]['questions'][3]['selected'] == 1 or data['conditionReport']['sections'][3]['questions'][0]['selected'] == 1:
                    start_and_drive = 'S'
                
                # engine_does_not_stay_running is true or vehicle inoperable is false
                elif data['conditionReport']['sections'][2]['questions'][3]['selected'] == 1 or data['conditionReport']['sections'][3]['questions'][0]['selected'] == 0:
                    start_and_drive = 'S'

                # engine_does_not_stay_running is false or vehicle inoperable is true
                elif data['conditionReport']['sections'][2]['questions'][3]['selected'] == 0 or data['conditionReport']['sections'][3]['questions'][0]['selected'] == 1:
                    start_and_drive = 'S'
                
                # engine_does_not_stay_running is false or vehicle inoperable is false
                elif data['conditionReport']['sections'][2]['questions'][3]['selected'] == 0 or data['conditionReport']['sections'][3]['questions'][0]['selected'] == 0:
                    if data['conditionReport']['sections'][2]['questions'][3]['selected'] == 0 and data['conditionReport']['sections'][3]['questions'][0]['selected'] == 0:
                        start_and_drive = 'D'

            # if engine_does_not_start is true or engine_does_not_crank is true
            elif data['conditionReport']['sections'][2]['questions'][2]['selected'] == 1 or data['conditionReport']['sections'][2]['questions'][1]['selected'] == 1:
                start_and_drive = 'N'
            
            # if engine_does_not_start is true or engine_does_not_crank is false
            elif data['conditionReport']['sections'][2]['questions'][2]['selected'] == 1 or data['conditionReport']['sections'][2]['questions'][1]['selected'] == 0:
                start_and_drive = 'N'
            
            # if engine_does_not_start is false or engine_does_not_crank is true
            elif data['conditionReport']['sections'][2]['questions'][2]['selected'] == 0 or data['conditionReport']['sections'][2]['questions'][1]['selected'] == 1:
                start_and_drive = 'N'

            trasmission_issue = "No my vehicle is in good shape!"

            if (data['conditionReport']['sections'][3]['questions'][2]['selected'] == 1 or data['conditionReport']['sections'][3]['questions'][1]['selected'] == 1) and (data['conditionReport']['sections'][2]['questions'][4]['selected'] == 1 or data['conditionReport']['sections'][2]['questions'][5]['selected'] == 1 or data['conditionReport']['sections'][2]['questions'][6]['selected'] == 1 or data['conditionReport']['sections'][2]['questions'][7]['selected'] == 1 or data['conditionReport']['sections'][2]['questions'][8]['selected'] == 1) and (data['conditionReport']['sections'][1]['questions'][3]['selected'] == 1 or data['conditionReport']['sections'][1]['questions'][0]['selected'] == 1):
                trasmission_issue = 'Yes major engine issues,Yes major transmission issues,Yes major frame issues'

            elif ((data['conditionReport']['sections'][3]['questions'][2]['selected'] == 1 or data['conditionReport']['sections'][3]['questions'][1]['selected'] == 1) and (data['conditionReport']['sections'][2]['questions'][4]['selected'] == 1 or data['conditionReport']['sections'][2]['questions'][5]['selected'] == 1 or data['conditionReport']['sections'][2]['questions'][6]['selected'] == 1 or data['conditionReport']['sections'][2]['questions'][7]['selected'] == 1 or data['conditionReport']['sections'][2]['questions'][8]['selected'] == 1)):
                trasmission_issue = 'Yes major transmission issues,Yes major engine issues'

            elif ((data['conditionReport']['sections'][2]['questions'][4]['selected'] == 1 or data['conditionReport']['sections'][2]['questions'][5]['selected'] == 1 or data['conditionReport']['sections'][2]['questions'][6]['selected'] == 1 or data['conditionReport']['sections'][2]['questions'][7]['selected'] == 1 or data['conditionReport']['sections'][2]['questions'][8]['selected'] == 1) and (data['conditionReport']['sections'][1]['questions'][3]['selected'] == 1 or data['conditionReport']['sections'][1]['questions'][0]['selected'] == 1)):
                trasmission_issue = 'Yes major engine issues,Yes major frame issues'

            elif ((data['conditionReport']['sections'][3]['questions'][2]['selected'] == 1 or data['conditionReport']['sections'][3]['questions'][1]['selected'] == 1) and (data['conditionReport']['sections'][1]['questions'][3]['questionTitle']['selected'] == 1 or data['conditionReport']['sections'][1]['questions'][0]['selected'] == 1)):
                trasmission_issue = 'Yes major transmission issues,Yes major frame issues'
            
            elif (data['conditionReport']['sections'][3]['questions'][2]['selected'] == 1 or data['conditionReport']['sections'][3]['questions'][1]['selected'] == 1):
                trasmission_issue = 'Yes major transmission issues'

            elif (data['conditionReport']['sections'][2]['questions'][4]['selected'] == 1 or data['conditionReport']['sections'][2]['questions'][5]['selected'] == 1 or data['conditionReport']['sections'][2]['questions'][6]['selected'] == 1 or data['conditionReport']['sections'][2]['questions'][7]['selected'] == 1 or data['conditionReport']['sections'][2]['questions'][8]['selected'] == 1):
                trasmission_issue = 'Yes major engine issues'
            
            elif (data['conditionReport']['sections'][1]['questions'][3]['selected'] == 1 or data['conditionReport']['sections'][1]['questions'][0]['selected'] == 1):
                trasmission_issue = 'Yes major frame issues'
            
            title_type = ""
            # if sold on bill sale is true
            if data['conditionReport']['sections'][7]['questions'][10]['selected'] == 1:
                title_type = "Unknown"
            else:
                # if branded title is true
                if data['conditionReport']['sections'][7]['questions'][1]['selected'] == 1:
                    title_type = 'Salvage Rebuilt'
                else:
                    # hail damage is true
                    if data['conditionReport']['sections'][0]['questions'][9]['selected'] == 1:
                        title_type = 'Salvage Rebuilt'
                    else:
                        title_type = 'Clean Title'

            print('title_type',title_type)
            fire_water_damage = 'no'
            if data['conditionReport']['sections'][7]['questions'][3]['selected'] == 1:
                fire_water_damage = 'W'
            
            lights = []
            if data['blueLight'] == 1:
                lights.append('blue')
            
            if data['yellowLight'] == 1:
                lights.append('yellow')
            
            if data['redLight'] == 1:
                lights.append('red')
            
            if data['greenLight'] == 1:
                lights.append('green')
        
            lights_str = ' '.join(lights)
         
            cursor.execute('SELECT auction_id from auctions WHERE auction_id = %s',data['id'])
            fetchone = cursor.fetchone()

            if fetchone is None:
                print('insert auction')
                cursor.execute('INSERT INTO auctions (year,make,model,auction_id,location,odometer,action_end_datetime,zip_code,bid_amount,bid_count,vin,status,minor_body_type_ans,modrate_body_type_ans,major_body_type_ans,airbag_deployed_ans,engine_start_or_not,engine_start_not_run,transmission_issue_ans,frame_issue_ans,title_absent_ans,title_branded_ans,vehicle_display_name,start_and_drive_ans,next_bid_amount,start_price,is_high_bidder,created_at,body_damage,reserve_met,next_proxy_bid_amount,action_start_datetime,lights,auction_image_url,auction_url, distance,transmission,trim,drivetrain,engine,fuel_type,basic_color,water_or_fire_damage) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', 
                            (data['year'],data['make'],data['model'],data['id'],data['location'],data['odometer'],data['endTime'],data['postalCode'],data['bidAmount'],data['bidCount'],data['vin'],data['status'],
                                # body type damage
                                data['conditionReport']['sections'][0]['questions'][0]['selected'],
                                data['conditionReport']['sections'][0]['questions'][1]['selected'],
                                data['conditionReport']['sections'][0]['questions'][2]['selected'],

                                # airbag issue
                                airbag_value,

                                # engine start 
                                data['conditionReport']['sections'][2]['questions'][2]['selected'],
                                data['conditionReport']['sections'][2]['questions'][3]['selected'],

                                # transmission issue
                                trasmission_issue,

                                # frame issue
                                data['conditionReport']['sections'][1]['questions'][0]['selected'],
                
                                # title issue
                                title_type,
                                data['conditionReport']['sections'][7]['questions'][1]['selected'],

                                data['vehicleDisplayName'],

                                start_and_drive,
                                data['nextBidAmount'],
                                data['startPrice'],
                                data['isHighBidder'],
                                datetime.datetime.now(),
                                body_damage,
                                data['reserveMet'],
                                data['nextProxyAmount'],
                                data['startTime'],
                                lights_str,
                                data['primaryImage']['url'],
                                data['auctionLink'],
                                data['distance'],
                                data['transmission'],
                                data['trim'],
                                data['drivetrain'],
                                data['engine'],
                                data['fuelType'],
                                data['basicColor'],
                                fire_water_damage
                                )),
                con.commit()
            else:
                print('update auction')
                cursor.execute('UPDATE auctions SET bid_amount = %s, next_bid_amount = %s, is_high_bidder = %s, next_proxy_bid_amount = %s where auction_id = %s',(data['bidAmount'], data['nextBidAmount'], data['isHighBidder'], data['nextProxyAmount'], data['id']))
                con.commit()
        except:
            return ()
        finally:
            con.close()

    def auctionconditionreport(self, data):
        con = ACV.connect(self)
        cursor = con.cursor()
        
        try:
            cursor.execute('SELECT auction_id from auction_condition_report WHERE auction_id = %s',data['id'])
            fetchone = cursor.fetchone()

            if fetchone is None:

                # section - 0 - Exterior

                minor_body_type = {
                    "questionTitle": data['conditionReport']['sections'][0]['questions'][0]['questionTitle'],
                    "selected": data['conditionReport']['sections'][0]['questions'][0]['selected'],
                    "answer": data['conditionReport']['sections'][0]['questions'][0]['answer']
                }

                moderate_body_type = {
                    "questionTitle": data['conditionReport']['sections'][0]['questions'][1]['questionTitle'],
                    "selected": data['conditionReport']['sections'][0]['questions'][1]['selected'],
                    "answer": data['conditionReport']['sections'][0]['questions'][1]['answer']
                }

                major_body_type = {
                    "questionTitle": data['conditionReport']['sections'][0]['questions'][2]['questionTitle'],
                    "selected": data['conditionReport']['sections'][0]['questions'][2]['selected'],
                    "answer": data['conditionReport']['sections'][0]['questions'][2]['answer']
                }

                scratches = {
                    "questionTitle": data['conditionReport']['sections'][0]['questions'][3]['questionTitle'],
                    "selected": data['conditionReport']['sections'][0]['questions'][3]['selected'],
                    "answer": data['conditionReport']['sections'][0]['questions'][3]['answer']
                }
                
                glass_damage = {
                    "questionTitle": data['conditionReport']['sections'][0]['questions'][4]['questionTitle'],
                    "selected": data['conditionReport']['sections'][0]['questions'][4]['selected'],
                    "answer": data['conditionReport']['sections'][0]['questions'][4]['answer']
                }

                lights_damage = {
                    "questionTitle": data['conditionReport']['sections'][0]['questions'][5]['questionTitle'],
                    "selected": data['conditionReport']['sections'][0]['questions'][5]['selected'],
                    "answer": data['conditionReport']['sections'][0]['questions'][5]['answer']
                }

                minor_body_rust = {
                    "questionTitle": data['conditionReport']['sections'][0]['questions'][6]['questionTitle'],
                    "selected": data['conditionReport']['sections'][0]['questions'][6]['selected'],
                    "answer": data['conditionReport']['sections'][0]['questions'][6]['answer']
                }

                modrate_body_rust = {
                    'questionTitle': data['conditionReport']['sections'][0]['questions'][7]['questionTitle'],
                    'selected': data['conditionReport']['sections'][0]['questions'][7]['selected'],
                    'answer': data['conditionReport']['sections'][0]['questions'][7]['answer']
                }

                major_body_rust = {
                    'questionTitle': data['conditionReport']['sections'][0]['questions'][8]['questionTitle'],
                    'selected': data['conditionReport']['sections'][0]['questions'][8]['selected'],
                    'answer': data['conditionReport']['sections'][0]['questions'][8]['answer']
                }

                hail_damage = {
                    'questionTitle': data['conditionReport']['sections'][0]['questions'][9]['questionTitle'],
                    'selected': data['conditionReport']['sections'][0]['questions'][9]['selected'],
                    'answer': data['conditionReport']['sections'][0]['questions'][9]['answer']
                }

                aftermarket_parts_exterior = {
                    "questionTitle": data['conditionReport']['sections'][0]['questions'][10]['questionTitle'], 
                    "selected": data['conditionReport']['sections'][0]['questions'][10]['selected'],
                    "answer": data['conditionReport']['sections'][0]['questions'][10]['answer']
                }

                mismatched_paint = {
                    "questionTitle": data['conditionReport']['sections'][0]['questions'][11]['questionTitle'],
                    "selected": data['conditionReport']['sections'][0]['questions'][11]['selected'],
                    "answer": data['conditionReport']['sections'][0]['questions'][11]['answer']
                }

                paint_meter_readings = {
                    "questionTitle": data['conditionReport']['sections'][0]['questions'][12]['questionTitle'],
                    "selected": data['conditionReport']['sections'][0]['questions'][12]['selected'],
                    "answer": data['conditionReport']['sections'][0]['questions'][12]['answer']
                }

                poor_quality_repairs = {
                    "questionTitle": data['conditionReport']['sections'][0]['questions'][13]['questionTitle'],
                    "selected": data['conditionReport']['sections'][0]['questions'][13]['selected'],
                    "answer": data['conditionReport']['sections'][0]['questions'][13]['answer']
                }

                previous_paint_work = {
                    "questionTitle": data['conditionReport']['sections'][0]['questions'][14]['questionTitle'],
                    "selected": data['conditionReport']['sections'][0]['questions'][14]['selected'],
                    "answer": data['conditionReport']['sections'][0]['questions'][14]['answer']
                }   

                # section - 1 = Frame & Unibody       
                frame_damage = {
                    "questionTitle": data['conditionReport']['sections'][1]['questions'][0]['questionKey'],
                    "selected": data['conditionReport']['sections'][1]['questions'][0]['selected'],
                    "answer": data['conditionReport']['sections'][1]['questions'][0]['answer']
                }

                surface_rust = {
                    "questionTitle": data['conditionReport']['sections'][1]['questions'][1]['questionTitle'],
                    "selected": data['conditionReport']['sections'][1]['questions'][1]['selected'],
                    "answer": data['conditionReport']['sections'][1]['questions'][1]['answer']
                } 

                heavy_rust = {
                    "questionTitle": data['conditionReport']['sections'][1]['questions'][2]['questionTitle'],
                    "selected": data['conditionReport']['sections'][1]['questions'][2]['selected'],
                    "answer": data['conditionReport']['sections'][1]['questions'][2]['answer']
                } 

                penetrating_rust = {
                    "questionTitle": data['conditionReport']['sections'][1]['questions'][3]['questionTitle'],
                    "selected": data['conditionReport']['sections'][1]['questions'][3]['selected'],
                    "answer": data['conditionReport']['sections'][1]['questions'][3]['answer']
                }

                # section - 2 - Mechanicals

                jump_start_required = {
                    "questionTitle": data['conditionReport']['sections'][2]['questions'][0]['questionTitle'],
                    "selected": data['conditionReport']['sections'][2]['questions'][0]['selected'],
                    "answer": data['conditionReport']['sections'][2]['questions'][0]['answer']
                }

                engine_does_not_crank = {
                    "questionTitle": data['conditionReport']['sections'][2]['questions'][1]['questionTitle'],
                    "selected": data['conditionReport']['sections'][2]['questions'][1]['selected'],
                    "answer": data['conditionReport']['sections'][2]['questions'][1]['answer']
                }

                engine_does_not_start = {
                    "questionTitle": data['conditionReport']['sections'][2]['questions'][2]['questionTitle'],
                    "selected": data['conditionReport']['sections'][2]['questions'][2]['selected'],
                    "answer": data['conditionReport']['sections'][2]['questions'][2]['answer']
                }

                engine_does_not_stay_running = {
                    "questionTitle": data['conditionReport']['sections'][2]['questions'][3]['questionTitle'],
                    "selected": data['conditionReport']['sections'][2]['questions'][3]['selected'],
                    "answer": data['conditionReport']['sections'][2]['questions'][3]['answer']
                }

                engine_noise = {
                    "questionTitle": data['conditionReport']['sections'][2]['questions'][4]['questionTitle'],
                    "selected": data['conditionReport']['sections'][2]['questions'][4]['selected'],
                    "answer": data['conditionReport']['sections'][2]['questions'][4]['answer']
                }

                engine_hesitation = {
                    "questionTitle": data['conditionReport']['sections'][2]['questions'][5]['questionTitle'],
                    "selected": data['conditionReport']['sections'][2]['questions'][5]['selected'],
                    "answer": data['conditionReport']['sections'][2]['questions'][5]['answer']
                }

                engine_overheats = {
                    "questionTitle": 'Engine Problem: Engine Overheats',
                    "selected": 'false',
                    "answer": ''
                }

                timing_chain_issue = {
                    "questionTitle": data['conditionReport']['sections'][2]['questions'][6]['questionTitle'],
                    "selected": data['conditionReport']['sections'][2]['questions'][6]['selected'],
                    "answer": data['conditionReport']['sections'][2]['questions'][6]['answer']
                }

                supercharger_issue = {
                    "questionTitle": 'Turbo/Supercharger Issue',
                    "selected": 'false',
                    "answer": ''
                }

                abnormal_exhaust_smoke = {
                    "questionTitle": data['conditionReport']['sections'][2]['questions'][7]['questionTitle'],
                    "selected": data['conditionReport']['sections'][2]['questions'][7]['selected'],
                    "answer": data['conditionReport']['sections'][2]['questions'][7]['answer']
                }

                head_gasket_issue = {
                    "questionTitle": data['conditionReport']['sections'][2]['questions'][8]['questionTitle'],
                    "selected": data['conditionReport']['sections'][2]['questions'][8]['selected'],
                    "answer": data['conditionReport']['sections'][2]['questions'][8]['answer']
                }

                exhaust_noise = {
                    "questionTitle": data['conditionReport']['sections'][2]['questions'][9]['questionTitle'],
                    "selected": data['conditionReport']['sections'][2]['questions'][9]['selected'],
                    "answer": data['conditionReport']['sections'][2]['questions'][9]['answer']
                }

                exhaust_modifications = {
                    "questionTitle": data['conditionReport']['sections'][2]['questions'][10]['questionTitle'],
                    "selected": data['conditionReport']['sections'][2]['questions'][10]['selected'],
                    "answer": data['conditionReport']['sections'][2]['questions'][10]['answer']
                }

                suspension_modifications = {
                    "questionTitle": data['conditionReport']['sections'][2]['questions'][11]['questionTitle'],  
                    "selected": data['conditionReport']['sections'][2]['questions'][11]['selected'],
                    "answer": data['conditionReport']['sections'][2]['questions'][11]['answer']
                }

                emissions_modifications = {
                    "questionTitle": data['conditionReport']['sections'][2]['questions'][12]['questionTitle'],
                    "selected": data['conditionReport']['sections'][2]['questions'][12]['selected'],
                    "answer": data['conditionReport']['sections'][2]['questions'][12]['answer']
                }
                

                emissions_issue = {
                    "questionTitle": 'Emissions Sticker Issue',
                    "selected": 'false',
                    "answer": ''
                }


                catalytic_converters_missing = {
                    "questionTitle": data['conditionReport']['sections'][2]['questions'][13]['questionTitle'],
                    "selected": data['conditionReport']['sections'][2]['questions'][13]['selected'],
                    "answer": data['conditionReport']['sections'][2]['questions'][13]['answer']
                }

                aftermarket_mechanical = {
                    'questionTitle': data['conditionReport']['sections'][2]['questions'][14]['questionTitle'],
                    'selected': data['conditionReport']['sections'][2]['questions'][14]['selected'],
                    'answer': data['conditionReport']['sections'][2]['questions'][14]['answer']
                }

                engine_accessory_issue = {
                    'questionTitle': data['conditionReport']['sections'][2]['questions'][15]['questionTitle'],
                    'selected': data['conditionReport']['sections'][2]['questions'][15]['selected'],
                    'answer': data['conditionReport']['sections'][2]['questions'][15]['answer']
                }

                fluid_leaks = {
                    'questionTitle': data['conditionReport']['sections'][2]['questions'][16]['questionTitle'],
                    'selected': data['conditionReport']['sections'][2]['questions'][16]['selected'],
                    'answer': data['conditionReport']['sections'][2]['questions'][16]['answer']
                }

                oil_level_issue = {
                    "questionTitle": 'Oil Level Issue',
                    "selected": 'false',
                    "answer": ''
                }

                oil_condition_issue = {
                    "questionTitle": 'Oil Condition Issue',
                    "selected": 'false',
                    "answer": ''
                }

                oil_intermix_dipstick_v2 = {
                    'questionTitle': data['conditionReport']['sections'][2]['questions'][17]['questionTitle'],
                    'selected': data['conditionReport']['sections'][2]['questions'][17]['selected'],
                    'answer': data['conditionReport']['sections'][2]['questions'][17]['answer']
                }

                coolant_level_issue = {
                    "questionTitle": 'Coolant Level Issue',
                    "selected": 'false',
                    "answer": ''
                }

                # section 3 Driveability
                vehicle_inop = {
                    "questionTitle": data['conditionReport']['sections'][3]['questions'][0]['questionTitle'],
                    "selected": data['conditionReport']['sections'][3]['questions'][0]['selected'],
                    "answer": data['conditionReport']['sections'][3]['questions'][0]['answer']
                }

                transmission_issue = {
                    "questionTitle": data['conditionReport']['sections'][3]['questions'][1]['questionTitle'],
                    "selected": data['conditionReport']['sections'][3]['questions'][1]['selected'],
                    "answer": data['conditionReport']['sections'][3]['questions'][1]['answer']
                }

                drivetrain_issue = {
                    "questionTitle": data['conditionReport']['sections'][3]['questions'][2]['questionTitle'],
                    "selected": data['conditionReport']['sections'][3]['questions'][2]['selected'],
                    "answer": data['conditionReport']['sections'][3]['questions'][2]['answer']
                }

                steering_issue = {
                    "questionTitle": data['conditionReport']['sections'][3]['questions'][3]['questionTitle'],
                    "selected": data['conditionReport']['sections'][3]['questions'][3]['selected'],
                    "answer": data['conditionReport']['sections'][3]['questions'][3]['answer']
                }

                break_issue = {
                    "questionTitle": data['conditionReport']['sections'][3]['questions'][4]['questionTitle'],
                    "selected": data['conditionReport']['sections'][3]['questions'][4]['selected'],
                    "answer": data['conditionReport']['sections'][3]['questions'][4]['answer']
                }

                suspension_issue = {
                    "questionTitle": data['conditionReport']['sections'][3]['questions'][5]['questionTitle'],
                    "selected": data['conditionReport']['sections'][3]['questions'][5]['selected'],
                    "answer": data['conditionReport']['sections'][3]['questions'][5]['answer']
                }

                # section - 4 - Warning Lights"

                check_engine_light = {
                    "questionTitle": data['conditionReport']['sections'][4]['questions'][0]['questionTitle'],
                    "selected": data['conditionReport']['sections'][4]['questions'][0]['selected'],
                    "answer": data['conditionReport']['sections'][4]['questions'][0]['answer']
                }

                airbag_light = {
                    "questionTitle": data['conditionReport']['sections'][4]['questions'][1]['questionTitle'],
                    "selected": data['conditionReport']['sections'][4]['questions'][1]['selected'],
                    "answer": data['conditionReport']['sections'][4]['questions'][1]['answer']
                }
                
                brake_light = {
                    "questionTitle": data['conditionReport']['sections'][4]['questions'][2]['questionTitle'],
                    "selected": data['conditionReport']['sections'][4]['questions'][2]['selected'],
                    "answer": data['conditionReport']['sections'][4]['questions'][2]['answer']
                }

                traction_control_light = {
                    "questionTitle": data['conditionReport']['sections'][4]['questions'][3]['questionTitle'],
                    "selected": data['conditionReport']['sections'][4]['questions'][3]['selected'],
                    "answer": data['conditionReport']['sections'][4]['questions'][3]['answer']
                }

                tpms_light = {
                    "questionTitle": data['conditionReport']['sections'][4]['questions'][4]['questionTitle'],
                    "selected": data['conditionReport']['sections'][4]['questions'][4]['selected'],
                    "answer": data['conditionReport']['sections'][4]['questions'][4]['answer']
                }

                battery_light = {
                    "questionTitle": data['conditionReport']['sections'][4]['questions'][5]['questionTitle'],
                    "selected": data['conditionReport']['sections'][4]['questions'][5]['selected'],
                    "answer": data['conditionReport']['sections'][4]['questions'][5]['answer']
                }

                other_warning_light = {
                    "questionTitle": data['conditionReport']['sections'][4]['questions'][6]['questionTitle'],
                    "selected": data['conditionReport']['sections'][4]['questions'][6]['selected'],
                    "answer": data['conditionReport']['sections'][4]['questions'][6]['answer']
                }

                obdii_codes = {
                    "questionTitle": data['conditionReport']['sections'][4]['questions'][7]['questionTitle'],
                    "selected": data['conditionReport']['sections'][4]['questions'][7]['selected'],
                    "answer": data['conditionReport']['sections'][4]['questions'][7]['answer']
                }

                incomplete_readiness_monitors = {
                    "questionTitle": data['conditionReport']['sections'][4]['questions'][8]['questionTitle'],
                    "selected": data['conditionReport']['sections'][4]['questions'][8]['selected'],
                    "answer": data['conditionReport']['sections'][4]['questions'][8]['answer']
                }


                #section - 5 - Interior

                seat_damage = {
                    "questionTitle": data['conditionReport']['sections'][5]['questions'][0]['questionTitle'],
                    "selected": data['conditionReport']['sections'][5]['questions'][0]['selected'],
                    "answer": data['conditionReport']['sections'][5]['questions'][0]['answer']
                }

                carpet_damage = {
                    "questionTitle": data['conditionReport']['sections'][5]['questions'][1]['questionTitle'],
                    "selected": data['conditionReport']['sections'][5]['questions'][1]['selected'],
                    "answer": data['conditionReport']['sections'][5]['questions'][1]['answer']
                }

                dashboard_damage = {
                    "questionTitle": data['conditionReport']['sections'][5]['questions'][2]['questionTitle'],
                    "selected": data['conditionReport']['sections'][5]['questions'][2]['selected'],
                    "answer": data['conditionReport']['sections'][5]['questions'][2]['answer']
                }

                headliner_damage = {
                    "questionTitle": data['conditionReport']['sections'][5]['questions'][3]['questionTitle'],
                    "selected": data['conditionReport']['sections'][5]['questions'][3]['selected'],
                    "answer": data['conditionReport']['sections'][5]['questions'][3]['answer']
                }

                interior_trim_damage = {
                    "questionTitle": data['conditionReport']['sections'][5]['questions'][4]['questionTitle'],
                    "selected": data['conditionReport']['sections'][5]['questions'][4]['selected'],
                    "answer": data['conditionReport']['sections'][5]['questions'][4]['answer']
                }

                interior_order = {
                    "questionTitle": data['conditionReport']['sections'][5]['questions'][5]['questionTitle'],
                    "selected": data['conditionReport']['sections'][5]['questions'][5]['selected'],
                    "answer": data['conditionReport']['sections'][5]['questions'][5]['answer']
                }

                crank_windows = {
                    "questionTitle": data['conditionReport']['sections'][5]['questions'][6]['questionTitle'],
                    "selected": data['conditionReport']['sections'][5]['questions'][6]['selected'],
                    "answer": data['conditionReport']['sections'][5]['questions'][6]['answer']
                }

                no_factory_ac = {
                    "questionTitle": data['conditionReport']['sections'][5]['questions'][7]['questionTitle'],
                    "selected": data['conditionReport']['sections'][5]['questions'][7]['selected'],
                    "answer": data['conditionReport']['sections'][5]['questions'][7]['answer']
                }

                electronics_issue = {
                    "questionTitle": data['conditionReport']['sections'][5]['questions'][8]['questionTitle'],
                    "selected": data['conditionReport']['sections'][5]['questions'][8]['selected'],
                    "answer": data['conditionReport']['sections'][5]['questions'][8]['answer']
                }

                five_digit_odometer = {
                    "questionTitle": data['conditionReport']['sections'][5]['questions'][9]['questionTitle'],
                    "selected": data['conditionReport']['sections'][5]['questions'][9]['selected'],
                    "answer": data['conditionReport']['sections'][5]['questions'][9]['answer']
                }

                sunroof = {
                    "questionTitle": data['conditionReport']['sections'][5]['questions'][10]['questionTitle'],
                    "selected": data['conditionReport']['sections'][5]['questions'][10]['selected'],
                    "answer": data['conditionReport']['sections'][5]['questions'][10]['answer']
                }

                aftermarket_sunroof = {
                    "questionTitle": 'Aftermarket Sunroof',
                    "selected": '',
                    "answer": ''
                }

                backup_camera = {
                    "questionTitle": 'Backup camera',
                    "selected": '',
                    "answer": ''
                }

                charging_cable = {
                    "questionTitle": 'Charging Cable',
                    "selected": '',
                    "answer": ''
                }
                navigation = {
                    "questionTitle": data['conditionReport']['sections'][5]['questions'][11]['questionTitle'],
                    "selected": data['conditionReport']['sections'][5]['questions'][11]['selected'],
                    "answer": data['conditionReport']['sections'][5]['questions'][11]['answer']
                }

                aftermarket_stereo = {
                    "questionTitle": data['conditionReport']['sections'][5]['questions'][12]['questionTitle'],
                    "selected": data['conditionReport']['sections'][5]['questions'][12]['selected'],
                    "answer": data['conditionReport']['sections'][5]['questions'][12]['answer']
                }

                airbag_json_value = {
                    "questionTitle": data['conditionReport']['sections'][5]['questions'][13]['questionTitle'],
                    "selected": data['conditionReport']['sections'][5]['questions'][13]['selected'],
                    "answer": data['conditionReport']['sections'][5]['questions'][13]['answer']
                } 

                hvac_not_working = {
                    "questionTitle": data['conditionReport']['sections'][5]['questions'][14]['questionTitle'],
                    "selected": data['conditionReport']['sections'][5]['questions'][14]['selected'],
                    "answer": data['conditionReport']['sections'][5]['questions'][14]['answer']
                } 

                leather_seats = {
                    "questionTitle": data['conditionReport']['sections'][5]['questions'][15]['questionTitle'],
                    "selected": data['conditionReport']['sections'][5]['questions'][15]['selected'],
                    "answer": data['conditionReport']['sections'][5]['questions'][15]['answer']
                }

                #section - 6 - Wheels & Tires

                aftermarket_wheels = {
                    "questionTitle": data['conditionReport']['sections'][6]['questions'][0]['questionTitle'],
                    "selected": data['conditionReport']['sections'][6]['questions'][0]['selected'],
                    "answer": data['conditionReport']['sections'][6]['questions'][0]['answer']
                }

                damaged_wheels = {
                    'questionTitle': data['conditionReport']['sections'][6]['questions'][1]['questionTitle'],
                    'selected': data['conditionReport']['sections'][6]['questions'][1]['selected'],
                    'answer': data['conditionReport']['sections'][6]['questions'][1]['answer']
                }

                oversized_tires = {
                    'questionTitle': data['conditionReport']['sections'][6]['questions'][2]['questionTitle'],
                    'selected': data['conditionReport']['sections'][6]['questions'][2]['selected'],
                    'answer': data['conditionReport']['sections'][6]['questions'][2]['answer']
                }

                damaged_tires = {
                    'questionTitle': data['conditionReport']['sections'][6]['questions'][3]['questionTitle'],
                    'selected': data['conditionReport']['sections'][6]['questions'][3]['selected'],
                    'answer': data['conditionReport']['sections'][6]['questions'][3]['answer']
                }

                uneven_tread_wear = {
                    'questionTitle': data['conditionReport']['sections'][6]['questions'][4]['questionTitle'],
                    'selected': data['conditionReport']['sections'][6]['questions'][4]['selected'],
                    'answer': data['conditionReport']['sections'][6]['questions'][4]['answer']
                }

                mismatched_tires = {
                    'questionTitle': data['conditionReport']['sections'][6]['questions'][5]['questionTitle'],
                    'selected': data['conditionReport']['sections'][6]['questions'][5]['selected'],
                    'answer': data['conditionReport']['sections'][6]['questions'][5]['answer']
                }

                missing_spare_tire = {
                    'questionTitle': data['conditionReport']['sections'][6]['questions'][6]['questionTitle'],
                    'selected': data['conditionReport']['sections'][6]['questions'][6]['selected'],
                    'answer': data['conditionReport']['sections'][6]['questions'][6]['answer']
                }

                tire_measurements = {
                    'questionTitle': data['conditionReport']['sections'][6]['questions'][7]['questionTitle'],
                    'selected': data['conditionReport']['sections'][6]['questions'][7]['selected'],
                    'answer': data['conditionReport']['sections'][6]['questions'][7]['answer']
                }
                
                # section - 7 - Title & History
                questions = data['conditionReport']['sections'][7]['questions']

                title_absent = {
                    'questionTitle': data['conditionReport']['sections'][7]['questions'][0]['questionTitle'],
                    'selected': data['conditionReport']['sections'][7]['questions'][0]['selected'],
                    'answer': data['conditionReport']['sections'][7]['questions'][0]['answer']
                }
            
                title_branded = {
                    'questionTitle': data['conditionReport']['sections'][7]['questions'][1]['questionTitle'],
                    'selected': data['conditionReport']['sections'][7]['questions'][1]['selected'],
                    'answer': data['conditionReport']['sections'][7]['questions'][1]['answer']
                }
            
                true_mileage_unknown = {
                    'questionTitle': data['conditionReport']['sections'][7]['questions'][2]['questionTitle'],
                    'selected': data['conditionReport']['sections'][7]['questions'][2]['selected'],
                    'answer': data['conditionReport']['sections'][7]['questions'][2]['answer']
                }
            
                flood_damage = {
                    'questionTitle': data['conditionReport']['sections'][7]['questions'][3]['questionTitle'],
                    'selected': data['conditionReport']['sections'][7]['questions'][3]['selected'],
                    'answer': data['conditionReport']['sections'][7]['questions'][3]['answer']
                }
        
                off_lease_vehicle = {
                    'questionTitle': data['conditionReport']['sections'][7]['questions'][4]['questionTitle'],
                    'selected': data['conditionReport']['sections'][7]['questions'][4]['selected'],
                    'answer': data['conditionReport']['sections'][7]['questions'][4]['answer']
                }
                
                repair_order_attached = {
                    'questionTitle': data['conditionReport']['sections'][7]['questions'][5]['questionTitle'],
                    'selected': data['conditionReport']['sections'][7]['questions'][5]['selected'],
                    'answer': data['conditionReport']['sections'][7]['questions'][5]['answer']
                }
                
                repossession = {
                    'questionTitle': data['conditionReport']['sections'][7]['questions'][6]['questionTitle'],
                    'selected': data['conditionReport']['sections'][7]['questions'][6]['selected'],
                    'answer': data['conditionReport']['sections'][7]['questions'][6]['answer']
                }
                
                repossession_papers_wo_title = {
                    'questionTitle': data['conditionReport']['sections'][7]['questions'][7]['questionTitle'],
                    'selected': data['conditionReport']['sections'][7]['questions'][7]['selected'],
                    'answer': data['conditionReport']['sections'][7]['questions'][7]['answer']
                }
                
                mobility = {
                    'questionTitle': data['conditionReport']['sections'][7]['questions'][8]['questionTitle'],
                    'selected': data['conditionReport']['sections'][7]['questions'][8]['selected'],
                    'answer': data['conditionReport']['sections'][7]['questions'][8]['answer']
                }

                if len(questions) > 9:
                    transferrable_registration = {
                        "questionTitle": data['conditionReport']['sections'][7]['questions'][9]['questionTitle'],
                        "selected": data['conditionReport']['sections'][7]['questions'][9]['selected'],
                        "answer": data['conditionReport']['sections'][7]['questions'][9]['answer']
                    }
                else:
                    transferrable_registration = {
                        "questionTitle": 'Transferrable Registration',
                        "selected": 'false',
                        "answer": ''
                    }
                
                if len(questions) > 10:
                    sold_on_bill_of_sale = {
                        "questionTitle": data['conditionReport']['sections'][7]['questions'][10]['questionTitle'],
                        "selected": data['conditionReport']['sections'][7]['questions'][10]['selected'],
                        "answer": data['conditionReport']['sections'][7]['questions'][10]['answer']
                    }
                else:
                    sold_on_bill_of_sale = {
                    "questionTitle": 'Sold on Bill of Sale',
                    "selected": "false",
                    "answer": ""
                    }
                
                airbag_json_string = json.dumps(airbag_json_value)
                vehicle_json_string = json.dumps(vehicle_inop)
                engine_does_not_crank_json_string = json.dumps(engine_does_not_crank)
                engine_does_not_start_json_string = json.dumps(engine_does_not_start)
                penetrating_rust_json_string = json.dumps(penetrating_rust)
                unbody_damage_json_string = json.dumps(frame_damage)
                engine_noise_json_string = json.dumps(engine_noise)
                engine_hesitation_json_string = json.dumps(engine_hesitation)
                timing_chain_issue_json_string = json.dumps(timing_chain_issue)
                abnormal_exhaust_smoke_json_string = json.dumps(abnormal_exhaust_smoke)
                head_gasket_issue_json_string = json.dumps(head_gasket_issue)
                drivetrain_issue_json_string = json.dumps(drivetrain_issue)
                transmission_issue_json_string = json.dumps(transmission_issue)
                minor_body_type_json_string = json.dumps(minor_body_type)
                moderate_body_type_json_string = json.dumps(moderate_body_type)
                major_body_type_json_string = json.dumps(major_body_type)
                glass_damage_json_string = json.dumps(glass_damage)
                lights_damage_json_string = json.dumps(lights_damage)
                aftermarket_parts_exterior_json_string = json.dumps(aftermarket_parts_exterior)
                poor_quality_repairs_json_string = json.dumps(poor_quality_repairs)
                surface_rust_json_string = json.dumps(surface_rust)
                heavy_rust_json_string = json.dumps(heavy_rust)
                obdii_codes_json_string = json.dumps(obdii_codes)   
                incomplete_readiness_monitors_json_string = json.dumps(incomplete_readiness_monitors)
                seat_damage_json_string = json.dumps(seat_damage)
                dashboard_damage_json_string = json.dumps(dashboard_damage)
                interior_trim_damage_json_string = json.dumps(interior_trim_damage)
                electronics_issue_json_string = json.dumps(electronics_issue)
                break_issue_json_string = json.dumps(break_issue)
                suspension_issue_json_string = json.dumps(suspension_issue)
                steering_issue_json_string = json.dumps(steering_issue)
                aftermarket_wheels_json_string = json.dumps(aftermarket_wheels)
                damaged_wheels_json_string = json.dumps(damaged_wheels)
                damaged_tiles_json_string = json.dumps(damaged_tires)
                tire_measurements_json_string = json.dumps(tire_measurements)
                aftermarket_mechanical_json_string = json.dumps(aftermarket_mechanical)
                engine_accessory_issue_json_string = json.dumps(engine_accessory_issue)
                title_absent_json_string = json.dumps(title_absent)
                title_branded_json_string = json.dumps(title_branded)
                modrate_body_rust_json_string = json.dumps(modrate_body_rust)
                flood_damage_json_string = json.dumps(flood_damage)
                scratches_json_string = json.dumps(scratches)
                hail_damage_json_string = json.dumps(hail_damage)
                mismatched_paint_json_string = json.dumps(mismatched_paint)
                paint_meter_readings_json_string = json.dumps(paint_meter_readings)
                previous_paint_work_json_string = json.dumps(previous_paint_work)
                major_body_rust_json_string = json.dumps(major_body_rust)
                minor_body_rust_json_string = json.dumps(minor_body_rust)
                jump_start_required_json_string = json.dumps(jump_start_required)
                oil_intermix_dipstick_v2_json_string = json.dumps(oil_intermix_dipstick_v2)
                fluid_leaks_json_string = json.dumps(fluid_leaks)
                emissions_modifications_json_string = json.dumps(emissions_modifications)
                catalytic_converters_missing_json_string = json.dumps(catalytic_converters_missing)
                exhaust_modifications_json_string = json.dumps(exhaust_modifications)
                exhaust_noise_json_string = json.dumps(exhaust_noise)
                suspension_modifications_json_string = json.dumps(suspension_modifications)
                engine_does_not_stay_running_json_string = json.dumps(engine_does_not_stay_running)
                check_engine_light_json_string = json.dumps(check_engine_light)
                airbag_light_json_string = json.dumps(airbag_light)
                brake_light_json_string = json.dumps(brake_light)
                traction_control_light_json_string = json.dumps(traction_control_light)
                tpms_light_json_string = json.dumps(tpms_light)
                battery_light_json_string = json.dumps(battery_light)
                other_warning_light_json_string = json.dumps(other_warning_light)
                oversized_tires_json_string = json.dumps(oversized_tires)
                uneven_tread_wear_json_string = json.dumps(uneven_tread_wear)
                mismatched_tires_json_string = json.dumps(mismatched_tires)
                missing_spare_tire_json_string = json.dumps(missing_spare_tire)
                carpet_damage = json.dumps(carpet_damage)
                headliner_damage = json.dumps(headliner_damage)
                interior_order = json.dumps(interior_order)
                crank_windows = json.dumps(crank_windows)
                no_factory_ac = json.dumps(no_factory_ac)
                five_digit_odometer = json.dumps(five_digit_odometer)
                sunroof = json.dumps(sunroof)
                navigation = json.dumps(navigation)
                aftermarket_stereo = json.dumps(aftermarket_stereo)
                hvac_not_working = json.dumps(hvac_not_working)
                leather_seats = json.dumps(leather_seats)
                true_mileage_unknown = json.dumps(true_mileage_unknown)
                off_lease_vehicle = json.dumps(off_lease_vehicle)
                repair_order_attached = json.dumps(repair_order_attached)
                repossession = json.dumps(repossession)
                repossession_papers_wo_title = json.dumps(repossession_papers_wo_title)
                mobility = json.dumps(mobility)
                transferrable_registration = json.dumps(transferrable_registration)
                sold_on_bill_of_sale = json.dumps(sold_on_bill_of_sale)
                aftermarket_sunroof = json.dumps(aftermarket_sunroof)
                backup_camera = json.dumps(backup_camera)
                charging_cable = json.dumps(charging_cable)
                engine_overheats = json.dumps(engine_overheats)
                supercharger_issue = json.dumps(supercharger_issue)
                emissions_issue = json.dumps(emissions_issue)
                oil_level_issue = json.dumps(oil_level_issue)
                oil_condition_issue = json.dumps(oil_condition_issue)
                coolant_level_issue = json.dumps(coolant_level_issue)

                cursor.execute('INSERT into auction_condition_report (auction_id, air_bag, vehicle_inop, engine_does_not_start, engine_does_not_crank, penetrating_rust,frame_damage,engine_noise,engine_hesitation,timing_chain_issue,abnormal_exhaust_smoke,head_gasket_issue,drivetrain_issue,transmission_issue,minor_body_type,moderate_body_type,major_body_type,glass_damage,lights_damage,aftermarket_parts_exterior,poor_quality_repairs,surface_rust,heavy_rust,obdii_codes,incomplete_readiness_monitors,seat_damage,dashboard_damage,interior_trim_damage,electronics_issue,break_issue,suspension_issue,steering_issue,aftermarket_wheels,damaged_wheels,damaged_tiles,tire_measurements,aftermarket_mechanical,engine_accessory_issue,title_absent,title_branded,modrate_body_rust,flood_damage,scratches, minor_body_rust, major_body_rust, hail_damage, mismatched_paint, paint_meter_readings, previous_paint_work, jump_start_required,oil_intermix_dipstick_v2,fluid_leaks,emissions_modifications,catalytic_converters_missing,exhaust_modifications,exhaust_noise,suspension_modifications,engine_does_not_stay_running,check_engine_light,airbag_light,brake_light,traction_control_light,tpms_light,battery_light,other_warning_light,oversized_tires,uneven_tread_wear,mismatched_tires,missing_spare_tire, carpet_damage, headliner_damage, interior_order, crank_windows, no_factory_ac,five_digit_odometer, sunroof, navigation, aftermarket_stereo, hvac_not_working, leather_seats, true_mileage_unknown,off_lease_vehicle,repair_order_attached, repossession, repossession_papers_wo_title, mobility, transferrable_registration, sold_on_bill_of_sale,aftermarket_sunroof,backup_camera,charging_cable,engine_overheats,supercharger_issue, emissions_issue, oil_level_issue, oil_condition_issue, coolant_level_issue) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (data['id'],airbag_json_string,vehicle_json_string,engine_does_not_start_json_string,engine_does_not_crank_json_string,penetrating_rust_json_string,unbody_damage_json_string,engine_noise_json_string,engine_hesitation_json_string,timing_chain_issue_json_string,abnormal_exhaust_smoke_json_string,head_gasket_issue_json_string,drivetrain_issue_json_string,transmission_issue_json_string,minor_body_type_json_string,moderate_body_type_json_string,major_body_type_json_string,glass_damage_json_string,lights_damage_json_string,aftermarket_parts_exterior_json_string,poor_quality_repairs_json_string,surface_rust_json_string,heavy_rust_json_string,obdii_codes_json_string,incomplete_readiness_monitors_json_string,seat_damage_json_string,dashboard_damage_json_string,interior_trim_damage_json_string,electronics_issue_json_string,break_issue_json_string,suspension_issue_json_string,steering_issue_json_string,aftermarket_wheels_json_string,damaged_wheels_json_string,damaged_tiles_json_string,tire_measurements_json_string,aftermarket_mechanical_json_string,engine_accessory_issue_json_string,title_absent_json_string,title_branded_json_string,modrate_body_rust_json_string,flood_damage_json_string,scratches_json_string, minor_body_rust_json_string, major_body_rust_json_string, hail_damage_json_string, mismatched_paint_json_string, paint_meter_readings_json_string, previous_paint_work_json_string, jump_start_required_json_string,oil_intermix_dipstick_v2_json_string,fluid_leaks_json_string,emissions_modifications_json_string,catalytic_converters_missing_json_string,exhaust_modifications_json_string,exhaust_noise_json_string,suspension_modifications_json_string,engine_does_not_stay_running_json_string,check_engine_light_json_string,airbag_light_json_string,brake_light_json_string,traction_control_light_json_string,tpms_light_json_string,battery_light_json_string,other_warning_light_json_string,oversized_tires_json_string,uneven_tread_wear_json_string,mismatched_tires_json_string,missing_spare_tire_json_string, carpet_damage, headliner_damage, interior_order, crank_windows, no_factory_ac,five_digit_odometer, sunroof, navigation, aftermarket_stereo, hvac_not_working, leather_seats,true_mileage_unknown,off_lease_vehicle,repair_order_attached, repossession, repossession_papers_wo_title, mobility,transferrable_registration,sold_on_bill_of_sale,aftermarket_sunroof,backup_camera,charging_cable,engine_overheats,supercharger_issue, emissions_issue, oil_level_issue, oil_condition_issue, coolant_level_issue))

                con.commit()
            return True
        except:
            return ()
        finally:
            con.close()

    def insertAuctionsUsingPubnub(self, data):
        con = ACV.connect(self)
        cursor = con.cursor()
        try:     

            body_damage = ""
            # major, moderate, minor body damage are false
            if data['conditionReport']['sections'][0]['questions'][2]['selected'] == 0 and data['conditionReport']['sections'][0]['questions'][1]['selected'] == 0 and data['conditionReport']['sections'][0]['questions'][0]['selected'] == 0:
                body_damage = 'No, my vehicle is in good shape!'

            # major body damage is true and moderate body damage is false
            elif data['conditionReport']['sections'][0]['questions'][2]['selected'] == 1 and data['conditionReport']['sections'][0]['questions'][1]['selected'] == 0:
                body_damage = 'FR,RR,SD,TP'
            
            # moderate body damage is true and minor body damage is false
            elif data['conditionReport']['sections'][0]['questions'][1]['selected'] == 1 and data['conditionReport']['sections'][0]['questions'][0]['selected'] == 0:
                body_damage = 'FR'
            
            # major body damage is true and minor body damage is false
            elif data['conditionReport']['sections'][0]['questions'][2]['selected'] == 1 and data['conditionReport']['sections'][0]['questions'][0]['selected'] == 0:
                body_damage = 'FR,RR,SD,TP'
            
            #major body damage is true
            elif data['conditionReport']['sections'][0]['questions'][2]['selected'] == 1:
                body_damage = 'FR,RR,SD,TP'
            
            #moderate body damage is true
            elif data['conditionReport']['sections'][0]['questions'][1]['selected'] == 1:
                body_damage = 'FR'
            
            #minor body damage is true
            elif data['conditionReport']['sections'][0]['questions'][0]['selected'] == 1:
                body_damage = 'No, my vehicle is in good shape!'

            airbag_value = 'N'
            if data['conditionReport']['sections'][5]['questions'][13]['selected'] == 1:
                airbag_value = 'Y'

            start_and_drive = ''
            # if engine_does_not_start is false and engine_does_not_crank is false
            if data['conditionReport']['sections'][2]['questions'][2]['selected'] == 0 and data['conditionReport']['sections'][2]['questions'][1]['selected'] == 0:
                # engine_does_not_stay_running is true or vehicle inoperable is true
                if data['conditionReport']['sections'][2]['questions'][3]['selected'] == 1 or data['conditionReport']['sections'][3]['questions'][0]['selected'] == 1:
                    start_and_drive = 'S'
                
                # engine_does_not_stay_running is true or vehicle inoperable is false
                elif data['conditionReport']['sections'][2]['questions'][3]['selected'] == 1 or data['conditionReport']['sections'][3]['questions'][0]['selected'] == 0:
                    start_and_drive = 'S'

                # engine_does_not_stay_running is false or vehicle inoperable is true
                elif data['conditionReport']['sections'][2]['questions'][3]['selected'] == 0 or data['conditionReport']['sections'][3]['questions'][0]['selected'] == 1:
                    start_and_drive = 'S'
                
                # engine_does_not_stay_running is false or vehicle inoperable is false
                elif data['conditionReport']['sections'][2]['questions'][3]['selected'] == 0 or data['conditionReport']['sections'][3]['questions'][0]['selected'] == 0:
                    if data['conditionReport']['sections'][2]['questions'][3]['selected'] == 0 and data['conditionReport']['sections'][3]['questions'][0]['selected'] == 0:
                        start_and_drive = 'D'

            # if engine_does_not_start is true or engine_does_not_crank is true
            elif data['conditionReport']['sections'][2]['questions'][2]['selected'] == 1 or data['conditionReport']['sections'][2]['questions'][1]['selected'] == 1:
                start_and_drive = 'N'
            
            # if engine_does_not_start is true or engine_does_not_crank is false
            elif data['conditionReport']['sections'][2]['questions'][2]['selected'] == 1 or data['conditionReport']['sections'][2]['questions'][1]['selected'] == 0:
                start_and_drive = 'N'
            
            # if engine_does_not_start is false or engine_does_not_crank is true
            elif data['conditionReport']['sections'][2]['questions'][2]['selected'] == 0 or data['conditionReport']['sections'][2]['questions'][1]['selected'] == 1:
                start_and_drive = 'N'

            trasmission_issue = "No my vehicle is in good shape!"

            if (data['conditionReport']['sections'][3]['questions'][2]['selected'] == 1 or data['conditionReport']['sections'][3]['questions'][1]['selected'] == 1) and (data['conditionReport']['sections'][2]['questions'][4]['selected'] == 1 or data['conditionReport']['sections'][2]['questions'][5]['selected'] == 1 or data['conditionReport']['sections'][2]['questions'][6]['selected'] == 1 or data['conditionReport']['sections'][2]['questions'][7]['selected'] == 1 or data['conditionReport']['sections'][2]['questions'][8]['selected'] == 1) and (data['conditionReport']['sections'][1]['questions'][3]['selected'] == 1 or data['conditionReport']['sections'][1]['questions'][0]['selected'] == 1):
                trasmission_issue = 'Yes major engine issues,Yes major transmission issues,Yes major frame issues'

            elif ((data['conditionReport']['sections'][3]['questions'][2]['selected'] == 1 or data['conditionReport']['sections'][3]['questions'][1]['selected'] == 1) and (data['conditionReport']['sections'][2]['questions'][4]['selected'] == 1 or data['conditionReport']['sections'][2]['questions'][5]['selected'] == 1 or data['conditionReport']['sections'][2]['questions'][6]['selected'] == 1 or data['conditionReport']['sections'][2]['questions'][7]['selected'] == 1 or data['conditionReport']['sections'][2]['questions'][8]['selected'] == 1)):
                trasmission_issue = 'Yes major transmission issues,Yes major engine issues'

            elif ((data['conditionReport']['sections'][2]['questions'][4]['selected'] == 1 or data['conditionReport']['sections'][2]['questions'][5]['selected'] == 1 or data['conditionReport']['sections'][2]['questions'][6]['selected'] == 1 or data['conditionReport']['sections'][2]['questions'][7]['selected'] == 1 or data['conditionReport']['sections'][2]['questions'][8]['selected'] == 1) and (data['conditionReport']['sections'][1]['questions'][3]['selected'] == 1 or data['conditionReport']['sections'][1]['questions'][0]['selected'] == 1)):
                trasmission_issue = 'Yes major engine issues,Yes major frame issues'

            elif ((data['conditionReport']['sections'][3]['questions'][2]['selected'] == 1 or data['conditionReport']['sections'][3]['questions'][1]['selected'] == 1) and (data['conditionReport']['sections'][1]['questions'][3]['questionTitle']['selected'] == 1 or data['conditionReport']['sections'][1]['questions'][0]['selected'] == 1)):
                trasmission_issue = 'Yes major transmission issues,Yes major frame issues'
            
            elif (data['conditionReport']['sections'][3]['questions'][2]['selected'] == 1 or data['conditionReport']['sections'][3]['questions'][1]['selected'] == 1):
                trasmission_issue = 'Yes major transmission issues'

            elif (data['conditionReport']['sections'][2]['questions'][4]['selected'] == 1 or data['conditionReport']['sections'][2]['questions'][5]['selected'] == 1 or data['conditionReport']['sections'][2]['questions'][6]['selected'] == 1 or data['conditionReport']['sections'][2]['questions'][7]['selected'] == 1 or data['conditionReport']['sections'][2]['questions'][8]['selected'] == 1):
                trasmission_issue = 'Yes major engine issues'
            
            elif (data['conditionReport']['sections'][1]['questions'][3]['selected'] == 1 or data['conditionReport']['sections'][1]['questions'][0]['selected'] == 1):
                trasmission_issue = 'Yes major frame issues'
            
            title_type = ""
            # if sold on bill sale is true
            if data['conditionReport']['sections'][7]['questions'][10]['selected'] == 1:
                title_type = "Unknown"
            else:
                # if branded title is true
                if data['conditionReport']['sections'][7]['questions'][1]['selected'] == 1:
                    title_type = 'Salvage Rebuilt'
                else:
                    # hail damage is true
                    if data['conditionReport']['sections'][0]['questions'][9]['selected'] == 1:
                        title_type = 'Salvage Rebuilt'
                    else:
                        title_type = 'Clean Title'
            
            fire_water_damage = 'no'
            if data['conditionReport']['sections'][7]['questions'][3]['selected'] == 1:
                fire_water_damage = 'W'

            lights = []
            if data['blueLight'] == 1:
                lights.append('blue')
            
            if data['yellowLight'] == 1:
                lights.append('yellow')
            
            if data['redLight'] == 1:
                lights.append('red')
            
            if data['greenLight'] == 1:
                lights.append('green')
        
            lights_str = ' '.join(lights)
         
            cursor.execute('SELECT auction_id from auctions WHERE auction_id = %s',data['id'])
            fetchone = cursor.fetchone()

            if fetchone is None:
                print('Inserting Auctions')
                cursor.execute('INSERT INTO auctions (year,make,model,auction_id,location,odometer,action_end_datetime,zip_code,bid_amount,bid_count,vin,status,minor_body_type_ans,modrate_body_type_ans,major_body_type_ans,airbag_deployed_ans,engine_start_or_not,engine_start_not_run,transmission_issue_ans,frame_issue_ans,title_absent_ans,title_branded_ans,vehicle_display_name,start_and_drive_ans,next_bid_amount,start_price,is_high_bidder,created_at,body_damage,reserve_met,next_proxy_bid_amount,action_start_datetime,lights,auction_image_url,auction_url, distance,transmission,trim,drivetrain,engine,fuel_type,basic_color,fire_water_damage) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', 
                    (data['year'],data['make'],data['model'],data['id'],data['location'],data['odometer'],data['endTime'],data['postalCode'],data['bidAmount'],data['bidCount'],data['vin'],data['status'],
                        # body type damage
                        data['conditionReport']['sections'][0]['questions'][0]['selected'],
                        data['conditionReport']['sections'][0]['questions'][1]['selected'],
                        data['conditionReport']['sections'][0]['questions'][2]['selected'],

                        # airbag issue
                        airbag_value,

                        # engine start 
                        data['conditionReport']['sections'][2]['questions'][2]['selected'],
                        data['conditionReport']['sections'][2]['questions'][3]['selected'],

                        # transmission issue
                        trasmission_issue,

                        # frame issue
                        data['conditionReport']['sections'][1]['questions'][0]['selected'],

                        # title issue
                        title_type,
                        data['conditionReport']['sections'][7]['questions'][1]['selected'],

                        data['vehicleDisplayName'],

                        start_and_drive,
                        data['nextBidAmount'],
                        data['startPrice'],
                        data['isHighBidder'],
                        datetime.datetime.now(),
                        body_damage,
                        data['reserveMet'],
                        data['nextProxyAmount'],
                        data['startTime'],
                        lights_str,
                        data['primaryImage']['url'],
                        data['auctionLink'],
                        data['distance'],
                        data['transmission'],
                        data['trim'],
                        data['drivetrain'],
                        data['engine'],
                        data['fuelType'],
                        data['basicColor'],
                        fire_water_damage
                        )),
            con.commit()
        
        except:
            return ()
        finally:
            con.close()
    
    def insertConditionreportUsingPubnub(self, data):
        con = ACV.connect(self)
        cursor = con.cursor()
        
        try:
            cursor.execute('SELECT auction_id from auction_condition_report WHERE auction_id = %s',data['id'])
            fetchone = cursor.fetchone()

            # section - 0 - Exterior

            minor_body_type = {
                "questionTitle": data['conditionReport']['sections'][0]['questions'][0]['questionTitle'],
                "selected": data['conditionReport']['sections'][0]['questions'][0]['selected'],
                "answer": data['conditionReport']['sections'][0]['questions'][0]['answer']
            }

            moderate_body_type = {
                "questionTitle": data['conditionReport']['sections'][0]['questions'][1]['questionTitle'],
                "selected": data['conditionReport']['sections'][0]['questions'][1]['selected'],
                "answer": data['conditionReport']['sections'][0]['questions'][1]['answer']
            }

            major_body_type = {
                "questionTitle": data['conditionReport']['sections'][0]['questions'][2]['questionTitle'],
                "selected": data['conditionReport']['sections'][0]['questions'][2]['selected'],
                "answer": data['conditionReport']['sections'][0]['questions'][2]['answer']
            }

            scratches = {
                "questionTitle": data['conditionReport']['sections'][0]['questions'][3]['questionTitle'],
                "selected": data['conditionReport']['sections'][0]['questions'][3]['selected'],
                "answer": data['conditionReport']['sections'][0]['questions'][3]['answer']
            }
            
            glass_damage = {
                "questionTitle": data['conditionReport']['sections'][0]['questions'][4]['questionTitle'],
                "selected": data['conditionReport']['sections'][0]['questions'][4]['selected'],
                "answer": data['conditionReport']['sections'][0]['questions'][4]['answer']
            }

            lights_damage = {
                "questionTitle": data['conditionReport']['sections'][0]['questions'][5]['questionTitle'],
                "selected": data['conditionReport']['sections'][0]['questions'][5]['selected'],
                "answer": data['conditionReport']['sections'][0]['questions'][5]['answer']
            }

            minor_body_rust = {
                "questionTitle": data['conditionReport']['sections'][0]['questions'][6]['questionTitle'],
                "selected": data['conditionReport']['sections'][0]['questions'][6]['selected'],
                "answer": data['conditionReport']['sections'][0]['questions'][6]['answer']
            }

            modrate_body_rust = {
                'questionTitle': data['conditionReport']['sections'][0]['questions'][7]['questionTitle'],
                'selected': data['conditionReport']['sections'][0]['questions'][7]['selected'],
                'answer': data['conditionReport']['sections'][0]['questions'][7]['answer']
            }

            major_body_rust = {
                'questionTitle': data['conditionReport']['sections'][0]['questions'][8]['questionTitle'],
                'selected': data['conditionReport']['sections'][0]['questions'][8]['selected'],
                'answer': data['conditionReport']['sections'][0]['questions'][8]['answer']
            }

            hail_damage = {
                'questionTitle': data['conditionReport']['sections'][0]['questions'][9]['questionTitle'],
                'selected': data['conditionReport']['sections'][0]['questions'][9]['selected'],
                'answer': data['conditionReport']['sections'][0]['questions'][9]['answer']
            }

            aftermarket_parts_exterior = {
                "questionTitle": data['conditionReport']['sections'][0]['questions'][10]['questionTitle'], 
                "selected": data['conditionReport']['sections'][0]['questions'][10]['selected'],
                "answer": data['conditionReport']['sections'][0]['questions'][10]['answer']
            }

            mismatched_paint = {
                "questionTitle": data['conditionReport']['sections'][0]['questions'][11]['questionTitle'],
                "selected": data['conditionReport']['sections'][0]['questions'][11]['selected'],
                "answer": data['conditionReport']['sections'][0]['questions'][11]['answer']
            }

            paint_meter_readings = {
                "questionTitle": data['conditionReport']['sections'][0]['questions'][12]['questionTitle'],
                "selected": data['conditionReport']['sections'][0]['questions'][12]['selected'],
                "answer": data['conditionReport']['sections'][0]['questions'][12]['answer']
            }

            poor_quality_repairs = {
                "questionTitle": data['conditionReport']['sections'][0]['questions'][13]['questionTitle'],
                "selected": data['conditionReport']['sections'][0]['questions'][13]['selected'],
                "answer": data['conditionReport']['sections'][0]['questions'][13]['answer']
            }

            previous_paint_work = {
                "questionTitle": data['conditionReport']['sections'][0]['questions'][14]['questionTitle'],
                "selected": data['conditionReport']['sections'][0]['questions'][14]['selected'],
                "answer": data['conditionReport']['sections'][0]['questions'][14]['answer']
            }   

            # section - 1 = Frame & Unibody       
            frame_damage = {
                "questionTitle": data['conditionReport']['sections'][1]['questions'][0]['questionKey'],
                "selected": data['conditionReport']['sections'][1]['questions'][0]['selected'],
                "answer": data['conditionReport']['sections'][1]['questions'][0]['answer']
            }

            surface_rust = {
                "questionTitle": data['conditionReport']['sections'][1]['questions'][1]['questionTitle'],
                "selected": data['conditionReport']['sections'][1]['questions'][1]['selected'],
                "answer": data['conditionReport']['sections'][1]['questions'][1]['answer']
            } 

            heavy_rust = {
                "questionTitle": data['conditionReport']['sections'][1]['questions'][2]['questionTitle'],
                "selected": data['conditionReport']['sections'][1]['questions'][2]['selected'],
                "answer": data['conditionReport']['sections'][1]['questions'][2]['answer']
            } 

            penetrating_rust = {
                "questionTitle": data['conditionReport']['sections'][1]['questions'][3]['questionTitle'],
                "selected": data['conditionReport']['sections'][1]['questions'][3]['selected'],
                "answer": data['conditionReport']['sections'][1]['questions'][3]['answer']
            }

            # section - 2 - Mechanicals

            jump_start_required = {
                "questionTitle": data['conditionReport']['sections'][2]['questions'][0]['questionTitle'],
                "selected": data['conditionReport']['sections'][2]['questions'][0]['selected'],
                "answer": data['conditionReport']['sections'][2]['questions'][0]['answer']
            }

            engine_does_not_crank = {
                "questionTitle": data['conditionReport']['sections'][2]['questions'][1]['questionTitle'],
                "selected": data['conditionReport']['sections'][2]['questions'][1]['selected'],
                "answer": data['conditionReport']['sections'][2]['questions'][1]['answer']
            }

            engine_does_not_start = {
                "questionTitle": data['conditionReport']['sections'][2]['questions'][2]['questionTitle'],
                "selected": data['conditionReport']['sections'][2]['questions'][2]['selected'],
                "answer": data['conditionReport']['sections'][2]['questions'][2]['answer']
            }

            engine_does_not_stay_running = {
                "questionTitle": data['conditionReport']['sections'][2]['questions'][3]['questionTitle'],
                "selected": data['conditionReport']['sections'][2]['questions'][3]['selected'],
                "answer": data['conditionReport']['sections'][2]['questions'][3]['answer']
            }

            engine_noise = {
                "questionTitle": data['conditionReport']['sections'][2]['questions'][4]['questionTitle'],
                "selected": data['conditionReport']['sections'][2]['questions'][4]['selected'],
                "answer": data['conditionReport']['sections'][2]['questions'][4]['answer']
            }

            engine_hesitation = {
                "questionTitle": data['conditionReport']['sections'][2]['questions'][5]['questionTitle'],
                "selected": data['conditionReport']['sections'][2]['questions'][5]['selected'],
                "answer": data['conditionReport']['sections'][2]['questions'][5]['answer']
            }

            engine_overheats = {
                "questionTitle": 'Engine Problem: Engine Overheats',
                "selected": 'false',
                "answer": ''
            }

            timing_chain_issue = {
                "questionTitle": data['conditionReport']['sections'][2]['questions'][6]['questionTitle'],
                "selected": data['conditionReport']['sections'][2]['questions'][6]['selected'],
                "answer": data['conditionReport']['sections'][2]['questions'][6]['answer']
            }

            supercharger_issue = {
                "questionTitle": 'Turbo/Supercharger Issue',
                "selected": 'false',
                "answer": ''
            }

            abnormal_exhaust_smoke = {
                "questionTitle": data['conditionReport']['sections'][2]['questions'][7]['questionTitle'],
                "selected": data['conditionReport']['sections'][2]['questions'][7]['selected'],
                "answer": data['conditionReport']['sections'][2]['questions'][7]['answer']
            }

            head_gasket_issue = {
                "questionTitle": data['conditionReport']['sections'][2]['questions'][8]['questionTitle'],
                "selected": data['conditionReport']['sections'][2]['questions'][8]['selected'],
                "answer": data['conditionReport']['sections'][2]['questions'][8]['answer']
            }

            exhaust_noise = {
                "questionTitle": data['conditionReport']['sections'][2]['questions'][9]['questionTitle'],
                "selected": data['conditionReport']['sections'][2]['questions'][9]['selected'],
                "answer": data['conditionReport']['sections'][2]['questions'][9]['answer']
            }

            exhaust_modifications = {
                "questionTitle": data['conditionReport']['sections'][2]['questions'][10]['questionTitle'],
                "selected": data['conditionReport']['sections'][2]['questions'][10]['selected'],
                "answer": data['conditionReport']['sections'][2]['questions'][10]['answer']
            }

            suspension_modifications = {
                "questionTitle": data['conditionReport']['sections'][2]['questions'][11]['questionTitle'],  
                "selected": data['conditionReport']['sections'][2]['questions'][11]['selected'],
                "answer": data['conditionReport']['sections'][2]['questions'][11]['answer']
            }

            emissions_modifications = {
                "questionTitle": data['conditionReport']['sections'][2]['questions'][12]['questionTitle'],
                "selected": data['conditionReport']['sections'][2]['questions'][12]['selected'],
                "answer": data['conditionReport']['sections'][2]['questions'][12]['answer']
            }
            

            emissions_issue = {
                "questionTitle": 'Emissions Sticker Issue',
                "selected": 'false',
                "answer": ''
            }


            catalytic_converters_missing = {
                "questionTitle": data['conditionReport']['sections'][2]['questions'][13]['questionTitle'],
                "selected": data['conditionReport']['sections'][2]['questions'][13]['selected'],
                "answer": data['conditionReport']['sections'][2]['questions'][13]['answer']
            }

            aftermarket_mechanical = {
                'questionTitle': data['conditionReport']['sections'][2]['questions'][14]['questionTitle'],
                'selected': data['conditionReport']['sections'][2]['questions'][14]['selected'],
                'answer': data['conditionReport']['sections'][2]['questions'][14]['answer']
            }

            engine_accessory_issue = {
                'questionTitle': data['conditionReport']['sections'][2]['questions'][15]['questionTitle'],
                'selected': data['conditionReport']['sections'][2]['questions'][15]['selected'],
                'answer': data['conditionReport']['sections'][2]['questions'][15]['answer']
            }

            fluid_leaks = {
                'questionTitle': data['conditionReport']['sections'][2]['questions'][16]['questionTitle'],
                'selected': data['conditionReport']['sections'][2]['questions'][16]['selected'],
                'answer': data['conditionReport']['sections'][2]['questions'][16]['answer']
            }

            oil_level_issue = {
                "questionTitle": 'Oil Level Issue',
                "selected": 'false',
                "answer": ''
            }

            oil_condition_issue = {
                "questionTitle": 'Oil Condition Issue',
                "selected": 'false',
                "answer": ''
            }

            oil_intermix_dipstick_v2 = {
                'questionTitle': data['conditionReport']['sections'][2]['questions'][17]['questionTitle'],
                'selected': data['conditionReport']['sections'][2]['questions'][17]['selected'],
                'answer': data['conditionReport']['sections'][2]['questions'][17]['answer']
            }

            coolant_level_issue = {
                "questionTitle": 'Coolant Level Issue',
                "selected": 'false',
                "answer": ''
            }

            # section 3 Driveability
            vehicle_inop = {
                "questionTitle": data['conditionReport']['sections'][3]['questions'][0]['questionTitle'],
                "selected": data['conditionReport']['sections'][3]['questions'][0]['selected'],
                "answer": data['conditionReport']['sections'][3]['questions'][0]['answer']
            }

            transmission_issue = {
                "questionTitle": data['conditionReport']['sections'][3]['questions'][1]['questionTitle'],
                "selected": data['conditionReport']['sections'][3]['questions'][1]['selected'],
                "answer": data['conditionReport']['sections'][3]['questions'][1]['answer']
            }

            drivetrain_issue = {
                "questionTitle": data['conditionReport']['sections'][3]['questions'][2]['questionTitle'],
                "selected": data['conditionReport']['sections'][3]['questions'][2]['selected'],
                "answer": data['conditionReport']['sections'][3]['questions'][2]['answer']
            }

            steering_issue = {
                "questionTitle": data['conditionReport']['sections'][3]['questions'][3]['questionTitle'],
                "selected": data['conditionReport']['sections'][3]['questions'][3]['selected'],
                "answer": data['conditionReport']['sections'][3]['questions'][3]['answer']
            }

            break_issue = {
                "questionTitle": data['conditionReport']['sections'][3]['questions'][4]['questionTitle'],
                "selected": data['conditionReport']['sections'][3]['questions'][4]['selected'],
                "answer": data['conditionReport']['sections'][3]['questions'][4]['answer']
            }

            suspension_issue = {
                "questionTitle": data['conditionReport']['sections'][3]['questions'][5]['questionTitle'],
                "selected": data['conditionReport']['sections'][3]['questions'][5]['selected'],
                "answer": data['conditionReport']['sections'][3]['questions'][5]['answer']
            }

            # section - 4 - Warning Lights"

            check_engine_light = {
                "questionTitle": data['conditionReport']['sections'][4]['questions'][0]['questionTitle'],
                "selected": data['conditionReport']['sections'][4]['questions'][0]['selected'],
                "answer": data['conditionReport']['sections'][4]['questions'][0]['answer']
            }

            airbag_light = {
                "questionTitle": data['conditionReport']['sections'][4]['questions'][1]['questionTitle'],
                "selected": data['conditionReport']['sections'][4]['questions'][1]['selected'],
                "answer": data['conditionReport']['sections'][4]['questions'][1]['answer']
            }
            
            brake_light = {
                "questionTitle": data['conditionReport']['sections'][4]['questions'][2]['questionTitle'],
                "selected": data['conditionReport']['sections'][4]['questions'][2]['selected'],
                "answer": data['conditionReport']['sections'][4]['questions'][2]['answer']
            }

            traction_control_light = {
                "questionTitle": data['conditionReport']['sections'][4]['questions'][3]['questionTitle'],
                "selected": data['conditionReport']['sections'][4]['questions'][3]['selected'],
                "answer": data['conditionReport']['sections'][4]['questions'][3]['answer']
            }

            tpms_light = {
                "questionTitle": data['conditionReport']['sections'][4]['questions'][4]['questionTitle'],
                "selected": data['conditionReport']['sections'][4]['questions'][4]['selected'],
                "answer": data['conditionReport']['sections'][4]['questions'][4]['answer']
            }

            battery_light = {
                "questionTitle": data['conditionReport']['sections'][4]['questions'][5]['questionTitle'],
                "selected": data['conditionReport']['sections'][4]['questions'][5]['selected'],
                "answer": data['conditionReport']['sections'][4]['questions'][5]['answer']
            }

            other_warning_light = {
                "questionTitle": data['conditionReport']['sections'][4]['questions'][6]['questionTitle'],
                "selected": data['conditionReport']['sections'][4]['questions'][6]['selected'],
                "answer": data['conditionReport']['sections'][4]['questions'][6]['answer']
            }

            obdii_codes = {
                "questionTitle": data['conditionReport']['sections'][4]['questions'][7]['questionTitle'],
                "selected": data['conditionReport']['sections'][4]['questions'][7]['selected'],
                "answer": data['conditionReport']['sections'][4]['questions'][7]['answer']
            }

            incomplete_readiness_monitors = {
                "questionTitle": data['conditionReport']['sections'][4]['questions'][8]['questionTitle'],
                "selected": data['conditionReport']['sections'][4]['questions'][8]['selected'],
                "answer": data['conditionReport']['sections'][4]['questions'][8]['answer']
            }


            #section - 5 - Interior

            seat_damage = {
                "questionTitle": data['conditionReport']['sections'][5]['questions'][0]['questionTitle'],
                "selected": data['conditionReport']['sections'][5]['questions'][0]['selected'],
                "answer": data['conditionReport']['sections'][5]['questions'][0]['answer']
            }

            carpet_damage = {
                "questionTitle": data['conditionReport']['sections'][5]['questions'][1]['questionTitle'],
                "selected": data['conditionReport']['sections'][5]['questions'][1]['selected'],
                "answer": data['conditionReport']['sections'][5]['questions'][1]['answer']
            }

            dashboard_damage = {
                "questionTitle": data['conditionReport']['sections'][5]['questions'][2]['questionTitle'],
                "selected": data['conditionReport']['sections'][5]['questions'][2]['selected'],
                "answer": data['conditionReport']['sections'][5]['questions'][2]['answer']
            }

            headliner_damage = {
                "questionTitle": data['conditionReport']['sections'][5]['questions'][3]['questionTitle'],
                "selected": data['conditionReport']['sections'][5]['questions'][3]['selected'],
                "answer": data['conditionReport']['sections'][5]['questions'][3]['answer']
            }

            interior_trim_damage = {
                "questionTitle": data['conditionReport']['sections'][5]['questions'][4]['questionTitle'],
                "selected": data['conditionReport']['sections'][5]['questions'][4]['selected'],
                "answer": data['conditionReport']['sections'][5]['questions'][4]['answer']
            }

            interior_order = {
                "questionTitle": data['conditionReport']['sections'][5]['questions'][5]['questionTitle'],
                "selected": data['conditionReport']['sections'][5]['questions'][5]['selected'],
                "answer": data['conditionReport']['sections'][5]['questions'][5]['answer']
            }

            crank_windows = {
                "questionTitle": data['conditionReport']['sections'][5]['questions'][6]['questionTitle'],
                "selected": data['conditionReport']['sections'][5]['questions'][6]['selected'],
                "answer": data['conditionReport']['sections'][5]['questions'][6]['answer']
            }

            no_factory_ac = {
                "questionTitle": data['conditionReport']['sections'][5]['questions'][7]['questionTitle'],
                "selected": data['conditionReport']['sections'][5]['questions'][7]['selected'],
                "answer": data['conditionReport']['sections'][5]['questions'][7]['answer']
            }

            electronics_issue = {
                "questionTitle": data['conditionReport']['sections'][5]['questions'][8]['questionTitle'],
                "selected": data['conditionReport']['sections'][5]['questions'][8]['selected'],
                "answer": data['conditionReport']['sections'][5]['questions'][8]['answer']
            }

            five_digit_odometer = {
                "questionTitle": data['conditionReport']['sections'][5]['questions'][9]['questionTitle'],
                "selected": data['conditionReport']['sections'][5]['questions'][9]['selected'],
                "answer": data['conditionReport']['sections'][5]['questions'][9]['answer']
            }

            sunroof = {
                "questionTitle": data['conditionReport']['sections'][5]['questions'][10]['questionTitle'],
                "selected": data['conditionReport']['sections'][5]['questions'][10]['selected'],
                "answer": data['conditionReport']['sections'][5]['questions'][10]['answer']
            }

            aftermarket_sunroof = {
                "questionTitle": 'Aftermarket Sunroof',
                "selected": '',
                "answer": ''
            }

            backup_camera = {
                "questionTitle": 'Backup camera',
                "selected": '',
                "answer": ''
            }

            charging_cable = {
                "questionTitle": 'Charging Cable',
                "selected": '',
                "answer": ''
            }
            navigation = {
                "questionTitle": data['conditionReport']['sections'][5]['questions'][11]['questionTitle'],
                "selected": data['conditionReport']['sections'][5]['questions'][11]['selected'],
                "answer": data['conditionReport']['sections'][5]['questions'][11]['answer']
            }

            aftermarket_stereo = {
                "questionTitle": data['conditionReport']['sections'][5]['questions'][12]['questionTitle'],
                "selected": data['conditionReport']['sections'][5]['questions'][12]['selected'],
                "answer": data['conditionReport']['sections'][5]['questions'][12]['answer']
            }

            airbag_json_value = {
                "questionTitle": data['conditionReport']['sections'][5]['questions'][13]['questionTitle'],
                "selected": data['conditionReport']['sections'][5]['questions'][13]['selected'],
                "answer": data['conditionReport']['sections'][5]['questions'][13]['answer']
            } 

            hvac_not_working = {
                "questionTitle": data['conditionReport']['sections'][5]['questions'][14]['questionTitle'],
                "selected": data['conditionReport']['sections'][5]['questions'][14]['selected'],
                "answer": data['conditionReport']['sections'][5]['questions'][14]['answer']
            } 

            leather_seats = {
                "questionTitle": data['conditionReport']['sections'][5]['questions'][15]['questionTitle'],
                "selected": data['conditionReport']['sections'][5]['questions'][15]['selected'],
                "answer": data['conditionReport']['sections'][5]['questions'][15]['answer']
            }

            #section - 6 - Wheels & Tires

            aftermarket_wheels = {
                "questionTitle": data['conditionReport']['sections'][6]['questions'][0]['questionTitle'],
                "selected": data['conditionReport']['sections'][6]['questions'][0]['selected'],
                "answer": data['conditionReport']['sections'][6]['questions'][0]['answer']
            }

            damaged_wheels = {
                'questionTitle': data['conditionReport']['sections'][6]['questions'][1]['questionTitle'],
                'selected': data['conditionReport']['sections'][6]['questions'][1]['selected'],
                'answer': data['conditionReport']['sections'][6]['questions'][1]['answer']
            }

            oversized_tires = {
                'questionTitle': data['conditionReport']['sections'][6]['questions'][2]['questionTitle'],
                'selected': data['conditionReport']['sections'][6]['questions'][2]['selected'],
                'answer': data['conditionReport']['sections'][6]['questions'][2]['answer']
            }

            damaged_tires = {
                'questionTitle': data['conditionReport']['sections'][6]['questions'][3]['questionTitle'],
                'selected': data['conditionReport']['sections'][6]['questions'][3]['selected'],
                'answer': data['conditionReport']['sections'][6]['questions'][3]['answer']
            }

            uneven_tread_wear = {
                'questionTitle': data['conditionReport']['sections'][6]['questions'][4]['questionTitle'],
                'selected': data['conditionReport']['sections'][6]['questions'][4]['selected'],
                'answer': data['conditionReport']['sections'][6]['questions'][4]['answer']
            }

            mismatched_tires = {
                'questionTitle': data['conditionReport']['sections'][6]['questions'][5]['questionTitle'],
                'selected': data['conditionReport']['sections'][6]['questions'][5]['selected'],
                'answer': data['conditionReport']['sections'][6]['questions'][5]['answer']
            }

            missing_spare_tire = {
                'questionTitle': data['conditionReport']['sections'][6]['questions'][6]['questionTitle'],
                'selected': data['conditionReport']['sections'][6]['questions'][6]['selected'],
                'answer': data['conditionReport']['sections'][6]['questions'][6]['answer']
            }

            tire_measurements = {
                'questionTitle': data['conditionReport']['sections'][6]['questions'][7]['questionTitle'],
                'selected': data['conditionReport']['sections'][6]['questions'][7]['selected'],
                'answer': data['conditionReport']['sections'][6]['questions'][7]['answer']
            }
            
            # section - 7 - Title & History
            questions = data['conditionReport']['sections'][7]['questions']

            title_absent = {
                'questionTitle': data['conditionReport']['sections'][7]['questions'][0]['questionTitle'],
                'selected': data['conditionReport']['sections'][7]['questions'][0]['selected'],
                'answer': data['conditionReport']['sections'][7]['questions'][0]['answer']
            }
        
            title_branded = {
                'questionTitle': data['conditionReport']['sections'][7]['questions'][1]['questionTitle'],
                'selected': data['conditionReport']['sections'][7]['questions'][1]['selected'],
                'answer': data['conditionReport']['sections'][7]['questions'][1]['answer']
            }
           
            true_mileage_unknown = {
                'questionTitle': data['conditionReport']['sections'][7]['questions'][2]['questionTitle'],
                'selected': data['conditionReport']['sections'][7]['questions'][2]['selected'],
                'answer': data['conditionReport']['sections'][7]['questions'][2]['answer']
            }
        
            flood_damage = {
                'questionTitle': data['conditionReport']['sections'][7]['questions'][3]['questionTitle'],
                'selected': data['conditionReport']['sections'][7]['questions'][3]['selected'],
                'answer': data['conditionReport']['sections'][7]['questions'][3]['answer']
            }
    
            off_lease_vehicle = {
                'questionTitle': data['conditionReport']['sections'][7]['questions'][4]['questionTitle'],
                'selected': data['conditionReport']['sections'][7]['questions'][4]['selected'],
                'answer': data['conditionReport']['sections'][7]['questions'][4]['answer']
            }
            
            repair_order_attached = {
                'questionTitle': data['conditionReport']['sections'][7]['questions'][5]['questionTitle'],
                'selected': data['conditionReport']['sections'][7]['questions'][5]['selected'],
                'answer': data['conditionReport']['sections'][7]['questions'][5]['answer']
            }
            
            repossession = {
                'questionTitle': data['conditionReport']['sections'][7]['questions'][6]['questionTitle'],
                'selected': data['conditionReport']['sections'][7]['questions'][6]['selected'],
                'answer': data['conditionReport']['sections'][7]['questions'][6]['answer']
            }
            
            repossession_papers_wo_title = {
                'questionTitle': data['conditionReport']['sections'][7]['questions'][7]['questionTitle'],
                'selected': data['conditionReport']['sections'][7]['questions'][7]['selected'],
                'answer': data['conditionReport']['sections'][7]['questions'][7]['answer']
            }
            
            mobility = {
                'questionTitle': data['conditionReport']['sections'][7]['questions'][8]['questionTitle'],
                'selected': data['conditionReport']['sections'][7]['questions'][8]['selected'],
                'answer': data['conditionReport']['sections'][7]['questions'][8]['answer']
            }

            if len(questions) > 9:
                transferrable_registration = {
                    "questionTitle": data['conditionReport']['sections'][7]['questions'][9]['questionTitle'],
                    "selected": data['conditionReport']['sections'][7]['questions'][9]['selected'],
                    "answer": data['conditionReport']['sections'][7]['questions'][9]['answer']
                }
            else:
                transferrable_registration = {
                    "questionTitle": 'Transferrable Registration',
                    "selected": 'false',
                    "answer": ''
                }
            
            if len(questions) > 10:
                sold_on_bill_of_sale = {
                    "questionTitle": data['conditionReport']['sections'][7]['questions'][10]['questionTitle'],
                    "selected": data['conditionReport']['sections'][7]['questions'][10]['selected'],
                    "answer": data['conditionReport']['sections'][7]['questions'][10]['answer']
                }
            else:
                sold_on_bill_of_sale = {
                "questionTitle": 'Sold on Bill of Sale',
                "selected": "false",
                "answer": ""
                }
            
            airbag_json_string = json.dumps(airbag_json_value)
            vehicle_json_string = json.dumps(vehicle_inop)
            engine_does_not_crank_json_string = json.dumps(engine_does_not_crank)
            engine_does_not_start_json_string = json.dumps(engine_does_not_start)
            penetrating_rust_json_string = json.dumps(penetrating_rust)
            unbody_damage_json_string = json.dumps(frame_damage)
            engine_noise_json_string = json.dumps(engine_noise)
            engine_hesitation_json_string = json.dumps(engine_hesitation)
            timing_chain_issue_json_string = json.dumps(timing_chain_issue)
            abnormal_exhaust_smoke_json_string = json.dumps(abnormal_exhaust_smoke)
            head_gasket_issue_json_string = json.dumps(head_gasket_issue)
            drivetrain_issue_json_string = json.dumps(drivetrain_issue)
            transmission_issue_json_string = json.dumps(transmission_issue)
            minor_body_type_json_string = json.dumps(minor_body_type)
            moderate_body_type_json_string = json.dumps(moderate_body_type)
            major_body_type_json_string = json.dumps(major_body_type)
            glass_damage_json_string = json.dumps(glass_damage)
            lights_damage_json_string = json.dumps(lights_damage)
            aftermarket_parts_exterior_json_string = json.dumps(aftermarket_parts_exterior)
            poor_quality_repairs_json_string = json.dumps(poor_quality_repairs)
            surface_rust_json_string = json.dumps(surface_rust)
            heavy_rust_json_string = json.dumps(heavy_rust)
            obdii_codes_json_string = json.dumps(obdii_codes)   
            incomplete_readiness_monitors_json_string = json.dumps(incomplete_readiness_monitors)
            seat_damage_json_string = json.dumps(seat_damage)
            dashboard_damage_json_string = json.dumps(dashboard_damage)
            interior_trim_damage_json_string = json.dumps(interior_trim_damage)
            electronics_issue_json_string = json.dumps(electronics_issue)
            break_issue_json_string = json.dumps(break_issue)
            suspension_issue_json_string = json.dumps(suspension_issue)
            steering_issue_json_string = json.dumps(steering_issue)
            aftermarket_wheels_json_string = json.dumps(aftermarket_wheels)
            damaged_wheels_json_string = json.dumps(damaged_wheels)
            damaged_tiles_json_string = json.dumps(damaged_tires)
            tire_measurements_json_string = json.dumps(tire_measurements)
            aftermarket_mechanical_json_string = json.dumps(aftermarket_mechanical)
            engine_accessory_issue_json_string = json.dumps(engine_accessory_issue)
            title_absent_json_string = json.dumps(title_absent)
            title_branded_json_string = json.dumps(title_branded)
            modrate_body_rust_json_string = json.dumps(modrate_body_rust)
            flood_damage_json_string = json.dumps(flood_damage)
            scratches_json_string = json.dumps(scratches)
            hail_damage_json_string = json.dumps(hail_damage)
            mismatched_paint_json_string = json.dumps(mismatched_paint)
            paint_meter_readings_json_string = json.dumps(paint_meter_readings)
            previous_paint_work_json_string = json.dumps(previous_paint_work)
            major_body_rust_json_string = json.dumps(major_body_rust)
            minor_body_rust_json_string = json.dumps(minor_body_rust)
            jump_start_required_json_string = json.dumps(jump_start_required)
            oil_intermix_dipstick_v2_json_string = json.dumps(oil_intermix_dipstick_v2)
            fluid_leaks_json_string = json.dumps(fluid_leaks)
            emissions_modifications_json_string = json.dumps(emissions_modifications)
            catalytic_converters_missing_json_string = json.dumps(catalytic_converters_missing)
            exhaust_modifications_json_string = json.dumps(exhaust_modifications)
            exhaust_noise_json_string = json.dumps(exhaust_noise)
            suspension_modifications_json_string = json.dumps(suspension_modifications)
            engine_does_not_stay_running_json_string = json.dumps(engine_does_not_stay_running)
            check_engine_light_json_string = json.dumps(check_engine_light)
            airbag_light_json_string = json.dumps(airbag_light)
            brake_light_json_string = json.dumps(brake_light)
            traction_control_light_json_string = json.dumps(traction_control_light)
            tpms_light_json_string = json.dumps(tpms_light)
            battery_light_json_string = json.dumps(battery_light)
            other_warning_light_json_string = json.dumps(other_warning_light)
            oversized_tires_json_string = json.dumps(oversized_tires)
            uneven_tread_wear_json_string = json.dumps(uneven_tread_wear)
            mismatched_tires_json_string = json.dumps(mismatched_tires)
            missing_spare_tire_json_string = json.dumps(missing_spare_tire)
            carpet_damage = json.dumps(carpet_damage)
            headliner_damage = json.dumps(headliner_damage)
            interior_order = json.dumps(interior_order)
            crank_windows = json.dumps(crank_windows)
            no_factory_ac = json.dumps(no_factory_ac)
            five_digit_odometer = json.dumps(five_digit_odometer)
            sunroof = json.dumps(sunroof)
            navigation = json.dumps(navigation)
            aftermarket_stereo = json.dumps(aftermarket_stereo)
            hvac_not_working = json.dumps(hvac_not_working)
            leather_seats = json.dumps(leather_seats)
            true_mileage_unknown = json.dumps(true_mileage_unknown)
            off_lease_vehicle = json.dumps(off_lease_vehicle)
            repair_order_attached = json.dumps(repair_order_attached)
            repossession = json.dumps(repossession)
            repossession_papers_wo_title = json.dumps(repossession_papers_wo_title)
            mobility = json.dumps(mobility)
            transferrable_registration = json.dumps(transferrable_registration)
            sold_on_bill_of_sale = json.dumps(sold_on_bill_of_sale)
            aftermarket_sunroof = json.dumps(aftermarket_sunroof)
            backup_camera = json.dumps(backup_camera)
            charging_cable = json.dumps(charging_cable)
            engine_overheats = json.dumps(engine_overheats)
            supercharger_issue = json.dumps(supercharger_issue)
            emissions_issue = json.dumps(emissions_issue)
            oil_level_issue = json.dumps(oil_level_issue)
            oil_condition_issue = json.dumps(oil_condition_issue)
            coolant_level_issue = json.dumps(coolant_level_issue)

            print('Inserting Auction Condition report')
            cursor.execute('INSERT into auction_condition_report (auction_id, air_bag, vehicle_inop, engine_does_not_start, engine_does_not_crank, penetrating_rust,frame_damage,engine_noise,engine_hesitation,timing_chain_issue,abnormal_exhaust_smoke,head_gasket_issue,drivetrain_issue,transmission_issue,minor_body_type,moderate_body_type,major_body_type,glass_damage,lights_damage,aftermarket_parts_exterior,poor_quality_repairs,surface_rust,heavy_rust,obdii_codes,incomplete_readiness_monitors,seat_damage,dashboard_damage,interior_trim_damage,electronics_issue,break_issue,suspension_issue,steering_issue,aftermarket_wheels,damaged_wheels,damaged_tiles,tire_measurements,aftermarket_mechanical,engine_accessory_issue,title_absent,title_branded,modrate_body_rust,flood_damage,scratches, minor_body_rust, major_body_rust, hail_damage, mismatched_paint, paint_meter_readings, previous_paint_work, jump_start_required,oil_intermix_dipstick_v2,fluid_leaks,emissions_modifications,catalytic_converters_missing,exhaust_modifications,exhaust_noise,suspension_modifications,engine_does_not_stay_running,check_engine_light,airbag_light,brake_light,traction_control_light,tpms_light,battery_light,other_warning_light,oversized_tires,uneven_tread_wear,mismatched_tires,missing_spare_tire, carpet_damage, headliner_damage, interior_order, crank_windows, no_factory_ac,five_digit_odometer, sunroof, navigation, aftermarket_stereo, hvac_not_working, leather_seats, true_mileage_unknown,off_lease_vehicle,repair_order_attached, repossession, repossession_papers_wo_title, mobility, transferrable_registration, sold_on_bill_of_sale,aftermarket_sunroof,backup_camera,charging_cable,engine_overheats,supercharger_issue, emissions_issue, oil_level_issue, oil_condition_issue, coolant_level_issue) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (data['id'],airbag_json_string,vehicle_json_string,engine_does_not_start_json_string,engine_does_not_crank_json_string,penetrating_rust_json_string,unbody_damage_json_string,engine_noise_json_string,engine_hesitation_json_string,timing_chain_issue_json_string,abnormal_exhaust_smoke_json_string,head_gasket_issue_json_string,drivetrain_issue_json_string,transmission_issue_json_string,minor_body_type_json_string,moderate_body_type_json_string,major_body_type_json_string,glass_damage_json_string,lights_damage_json_string,aftermarket_parts_exterior_json_string,poor_quality_repairs_json_string,surface_rust_json_string,heavy_rust_json_string,obdii_codes_json_string,incomplete_readiness_monitors_json_string,seat_damage_json_string,dashboard_damage_json_string,interior_trim_damage_json_string,electronics_issue_json_string,break_issue_json_string,suspension_issue_json_string,steering_issue_json_string,aftermarket_wheels_json_string,damaged_wheels_json_string,damaged_tiles_json_string,tire_measurements_json_string,aftermarket_mechanical_json_string,engine_accessory_issue_json_string,title_absent_json_string,title_branded_json_string,modrate_body_rust_json_string,flood_damage_json_string,scratches_json_string, minor_body_rust_json_string, major_body_rust_json_string, hail_damage_json_string, mismatched_paint_json_string, paint_meter_readings_json_string, previous_paint_work_json_string, jump_start_required_json_string,oil_intermix_dipstick_v2_json_string,fluid_leaks_json_string,emissions_modifications_json_string,catalytic_converters_missing_json_string,exhaust_modifications_json_string,exhaust_noise_json_string,suspension_modifications_json_string,engine_does_not_stay_running_json_string,check_engine_light_json_string,airbag_light_json_string,brake_light_json_string,traction_control_light_json_string,tpms_light_json_string,battery_light_json_string,other_warning_light_json_string,oversized_tires_json_string,uneven_tread_wear_json_string,mismatched_tires_json_string,missing_spare_tire_json_string, carpet_damage, headliner_damage, interior_order, crank_windows, no_factory_ac,five_digit_odometer, sunroof, navigation, aftermarket_stereo, hvac_not_working, leather_seats,true_mileage_unknown,off_lease_vehicle,repair_order_attached, repossession, repossession_papers_wo_title, mobility,transferrable_registration,sold_on_bill_of_sale,aftermarket_sunroof,backup_camera,charging_cable,engine_overheats,supercharger_issue, emissions_issue, oil_level_issue, oil_condition_issue, coolant_level_issue))
            
            con.commit()
            return True
        except:
            return ()
        finally:
            con.close()

    def countslights(self, auctions):
        con = ACV.connect(self)
        cursor = con.cursor()
        try:
            cursor.execute('SELECT auction_id from auctions WHERE auction_id = %s AND lights_counts IS NULL',auctions)
            fetchone = cursor.fetchone()            
            if fetchone is not None:
                cursor.execute('SELECT flood_damage, transferrable_registration, sold_on_bill_of_sale, major_body_type, penetrating_rust,	engine_does_not_crank, vehicle_inop, head_gasket_issue, engine_does_not_start, engine_overheats, timing_chain_issue, engine_noise, oil_intermix_dipstick_v2, supercharger_issue, transmission_issue, drivetrain_issue, steering_issue, break_issue, abnormal_exhaust_smoke, engine_hesitation, engine_does_not_stay_running, heavy_rust, modrate_body_rust, moderate_body_type, surface_rust, poor_quality_repairs, hail_damage, catalytic_converters_missing, battery_light, title_branded, title_absent, true_mileage_unknown, frame_damage, repossession, repossession_papers_wo_title, repair_order_attached, mobility, air_bag FROM auction_condition_report WHERE auction_id = %s', (auctions,))
                condition_reports = cursor.fetchall()
                yellow = 0
                orange = 0
                red = 0
                blue = 0
                
                for condition_report in condition_reports:
                    flood_damage_data = json.loads(condition_report[0]) 
                    transferrable_registration_data = json.loads(condition_report[1])
                    sold_on_bill_of_sale_data = json.loads(condition_report[2])
                    major_body_type_data = json.loads(condition_report[3])
                    penetrating_rust_data = json.loads(condition_report[4])
                    engine_does_not_crank_data = json.loads(condition_report[5])
                    vehicle_inop_data = json.loads(condition_report[6])
                    head_gasket_issue_data = json.loads(condition_report[7])
                    engine_does_not_start_data = json.loads(condition_report[8])
                    engine_overheats_data = json.loads(condition_report[9])
                    timing_chain_issue_data = json.loads(condition_report[10])
                    engine_noise_data = json.loads(condition_report[11])
                    oil_intermix_dipstick_v2_data = json.loads(condition_report[12])
                    supercharger_issue_data = json.loads(condition_report[13])
                    transmission_issue_data = json.loads(condition_report[14])
                    drivetrain_issue_data = json.loads(condition_report[15])
                    steering_issue_data = json.loads(condition_report[16])
                    break_issue_data = json.loads(condition_report[17])
                    abnormal_exhaust_smoke_data = json.loads(condition_report[18])
                    engine_hesitation_data = json.loads(condition_report[19])
                    engine_does_not_stay_running_data = json.loads(condition_report[20])
                    heavy_rust_data = json.loads(condition_report[21])
                    modrate_body_rust_data = json.loads(condition_report[22])
                    moderate_body_type_data = json.loads(condition_report[23])
                    surface_rust_data = json.loads(condition_report[24])
                    poor_quality_repairs_data = json.loads(condition_report[25])
                    hail_damage_data = json.loads(condition_report[26])
                    catalytic_converters_missing_data = json.loads(condition_report[27])
                    battery_light_data = json.loads(condition_report[28])
                    title_branded_data = json.loads(condition_report[29])
                    title_absent_data = json.loads(condition_report[30])
                    true_mileage_unknown_data = json.loads(condition_report[31])
                    frame_damage_data = json.loads(condition_report[32])
                    repossession_data = json.loads(condition_report[33])
                    repossession_papers_wo_title_data = json.loads(condition_report[34])
                    repair_order_attached_data = json.loads(condition_report[35])
                    mobility_data = json.loads(condition_report[36])
                    airbag_data = json.loads(condition_report[37])

                    if flood_damage_data['selected'] == True:  
                        orange += 1

                    if transferrable_registration_data['selected'] == True:
                        orange += 1

                    if sold_on_bill_of_sale_data['selected'] == True:
                        red += 1

                    if major_body_type_data['selected'] == True:
                        orange += 1

                    if penetrating_rust_data['selected'] == True:
                        yellow += 1
                    
                    if engine_does_not_crank_data['selected'] == True:
                        orange += 1

                    if vehicle_inop_data['selected'] == True:
                        orange += 1

                    if head_gasket_issue_data['selected'] == True:
                        yellow += 1
                    
                    if engine_does_not_start_data['selected'] == True:
                        orange += 1

                    if engine_overheats_data['selected'] == True:
                        yellow += 1
                    
                    if timing_chain_issue_data['selected'] == True:
                        yellow += 1

                    if engine_noise_data['selected'] == True:
                        yellow += 1

                    if oil_intermix_dipstick_v2_data['selected'] == True:
                        yellow += 1

                    if supercharger_issue_data['selected'] == True:
                        yellow += 1

                    if transmission_issue_data['selected'] == True:
                        yellow += 1

                    if drivetrain_issue_data['selected'] == True:
                        yellow += 1

                    if steering_issue_data['selected'] == True:
                        yellow += 1
                
                    if break_issue_data['selected'] == True:
                        yellow += 1

                    if abnormal_exhaust_smoke_data['selected'] == True:
                        yellow += 1

                    if engine_hesitation_data['selected'] == True:
                        yellow += 1

                    if engine_does_not_stay_running_data['selected'] == True:
                        yellow += 1

                    if heavy_rust_data['selected'] == True:
                        orange += 1
                    
                    if modrate_body_rust_data['selected'] == True:
                        yellow += 1

                    if moderate_body_type_data['selected'] == True:
                        orange += 1

                    if surface_rust_data['selected'] == True:
                        yellow += 1

                    if poor_quality_repairs_data['selected'] == True:
                        yellow += 1

                    if hail_damage_data['selected'] == True:
                        yellow += 1

                    if catalytic_converters_missing_data['selected'] == True:
                        yellow += 1

                    if battery_light_data['selected'] == True:
                        yellow += 1

                    if title_branded_data['selected'] == True:
                        orange += 1

                    if title_absent_data['selected'] == True:
                        blue += 1

                    if true_mileage_unknown_data['selected'] == True:
                        yellow += 1

                    if frame_damage_data['selected'] == True:
                        yellow += 1

                    if repossession_data['selected'] == True:
                        yellow += 1
                    
                    if repossession_papers_wo_title_data['selected'] == True:
                        yellow += 1

                    if repair_order_attached_data['selected'] == True:
                        yellow += 1
                    
                    if mobility_data['selected'] == True:
                        yellow += 1
                    
                    if airbag_data['selected'] == True:
                        orange += 1
                        
                color_count = {
                    "red": red,
                    "blue": blue,
                    "orange": orange,
                    "yellow": yellow,
                }

                lights_count = {color: count for color, count in color_count.items() if count > 0}

                if orange == 0 and yellow == 0 and red == 0 and blue == 0:
                    lights_count = {'green': 0}

                lights_count_json = json.dumps(lights_count)
                cursor.execute('UPDATE auctions SET lights_counts = %s WHERE auction_id = %s', (lights_count_json, auctions))
                con.commit()
                return True
        except Exception as e:
            con.rollback()
            print(f"Error during database operation: {str(e)}")
            traceback.print_exc()
            return False
        
    def checkconditonwithauction(self, auctiondata, conditionreport):
        con = ACV.connect(self)
        cursor = con.cursor()
        try:    

            state = auctiondata[5].split(', ')
            titles = auctiondata[21].split(',')
            mechnical_issue = auctiondata[19].split(',') 
            body_damage = auctiondata[33].split(',')
            
            make_name = auctiondata[2]
            model_name = auctiondata[3]
            max_year = auctiondata[1]
            min_year = auctiondata[1]
            max_mileage = auctiondata[6]
            min_mileage = auctiondata[6]
            final_zip = auctiondata[8]
            state = state[1]
           
            airbagComma = auctiondata[16]
            driveComma = auctiondata[24].split(',')
            mechnicalComma = mechnical_issue
            titleComma = titles
            fireWaterDame = auctiondata[51]
            id_value = conditionreport[0]
           
            query = """
                SELECT * FROM condition_report
                WHERE is_deleted='no' AND (
                    (FIND_IN_SET('{}', make_name) OR FIND_IN_SET('all', make_name)) AND
                    (FIND_IN_SET('{}', model_name) OR FIND_IN_SET('all', model_name)) AND
                    (max_year >= {} AND min_year <= {}) AND
                    (max_mileage >= {} AND min_mileage <= {}) AND
                    (final_zip = '' OR FIND_IN_SET({}, final_zip)) AND
                    ((FIND_IN_SET('{}', state) OR state = '' OR FIND_IN_SET('all', make_name) OR
                    max_year = '' OR min_year = '' OR max_mileage = '' OR min_mileage = '' OR
                    FIND_IN_SET('{}', state) OR state = '') AND
                    ({} OR sdamageImg_s = '') AND
                    (FIND_IN_SET('{}', airbagComma) OR airbagComma = '') AND
                    ({} OR driveComma = '') AND
                    ({} OR getSDamageComma = '') AND 
                    ({} OR titleComma = '' ) AND
                    (FIND_IN_SET('{}', firDamageComma) OR firDamageComma = '') 
                ) AND id = {}) ORDER BY id DESC;
            """.format(make_name, model_name, max_year, min_year, max_mileage, min_mileage,
                    final_zip, state, state,
                    ' AND '.join(["FIND_IN_SET('{}', sdamageImg_s)".format(body) for body in body_damage]),
                    airbagComma, 
                    ' AND '.join(["FIND_IN_SET('{}', driveComma)".format(drive) for drive in driveComma]),
                    ' AND '.join(["FIND_IN_SET('{}', getSDamageComma)".format(mechnical_issue) for mechnical_issue in mechnicalComma]),
                    ' AND '.join(["FIND_IN_SET('{}', titleComma)".format(title) for title in titleComma]),
                    fireWaterDame,
                    id_value)
                        
            cursor.execute(query)

            return cursor.fetchall()
            
        except:
            return ()
        finally:
            con.close()  

    def getauctions(self,):
        con = ACV.connect(self)
        cursor = con.cursor()
        try:    
            current_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')            
            cursor.execute('SELECT * from auctions WHERE action_end_datetime > %s AND status = "active" ORDER BY action_end_datetime ASC', (current_datetime,))
         
            return cursor.fetchall()
        except:
            return ()
        finally:
            con.close()  

    def getauctionsforbid(self,):
        con = ACV.connect(self)
        cursor = con.cursor()
        try:    
            cursor.execute('SELECT * from auctions Where action_start_datetime > %s AND status = "run_list" ORDER BY action_start_datetime DESC', (datetime.datetime.now(),))
            upcomingauctions = cursor.fetchall()

            cursor.execute('SELECT * from auctions Where action_end_datetime > %s AND is_match = %s AND status = "active" ORDER BY action_end_datetime DESC', (datetime.datetime.now(),1))
            activeauctions = cursor.fetchall()
            
            return upcomingauctions + activeauctions

        except:
            return ()
        finally:
            con.close()

    def getconditionReport(self, selected_report_id):
        con = ACV.connect(self)
        cursor = con.cursor()
        try:     
            if selected_report_id == "":
                cursor.execute("SELECT * FROM condition_report where is_deleted='no' AND condition_type IN ('ACV','both') order by id DESC")
            else:
                cursor.execute('SELECT * FROM condition_report WHERE id = %s', (selected_report_id,))
            return cursor.fetchall()
        except:
            return ()
        finally:
            con.close() 

    def deleteAuction(self):
        con = ACV.connect(self)
        cursor = con.cursor()
        try:  
            cursor.execute("SELECT * from auctions Where bid_count = 0 and status = 'active'")
            aucrions = cursor.fetchall()
            for auction in aucrions:
                cursor.execute('DELETE FROM auction_condition_report WHERE auction_id = %s', (auction[4],))
                cursor.execute('DELETE FROM auctions WHERE auction_id = %s', (auction[4],))
            con.commit()
        except:
            return ()
        finally:
            con.close() 

    def searchauction(self, searchval,status):
        con = ACV.connect(self)
        cursor = con.cursor()
        try:
            current_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            if searchval != "":
                if status == "active":
                    cursor.execute('SELECT * FROM auctions WHERE action_end_datetime > %s AND status = "active" AND is_match = 1 AND (vin LIKE %s OR auction_id LIKE %s OR year LIKE %s OR make LIKE %s OR model LIKE %s)', (current_datetime, '%' + searchval + '%', '%' + searchval + '%', '%' + searchval + '%', '%' + searchval + '%', '%' + searchval + '%'))

                elif status == "upcoming":
                    cursor.execute('SELECT * FROM auctions WHERE action_start_datetime > %s AND status = "run_list" AND (vin LIKE %s OR auction_id LIKE %s OR year LIKE %s OR make LIKE %s OR model LIKE %s)', (current_datetime, '%' + searchval + '%', '%' + searchval + '%', '%' + searchval + '%', '%' + searchval + '%', '%' + searchval + '%'))

                elif status == "missed":
                    cursor.execute('SELECT * FROM auctions WHERE action_end_datetime > %s AND is_match = 0 AND (vin LIKE %s OR auction_id LIKE %s OR year LIKE %s OR make LIKE %s OR model LIKE %s)', (current_datetime, '%' + searchval + '%', '%' + searchval + '%', '%' + searchval + '%', '%' + searchval + '%', '%' + searchval + '%'))

                elif status == "won":
                    cursor.execute('SELECT * FROM auctions WHERE win = 1 AND (vin LIKE %s OR auction_id LIKE %s OR year LIKE %s OR make LIKE %s OR model LIKE %s)', ('%' + searchval + '%', '%' + searchval + '%', '%' + searchval + '%', '%' + searchval + '%', '%' + searchval + '%'))

                elif status == "lost":
                    cursor.execute('SELECT * FROM auctions WHERE lost = 1 AND (vin LIKE %s OR auction_id LIKE %s OR year LIKE %s OR make LIKE %s OR model LIKE %s)', ('%' + searchval + '%', '%' + searchval + '%', '%' + searchval + '%', '%' + searchval + '%', '%' + searchval + '%'))
            else:
                return 1

            auctions = cursor.fetchall()
            return auctions
        except:
            return ()
        finally:
            con.close()

    def place_bid(self, id, bid):
        con = ACV.connect(self)
        cursor = con.cursor()
        try:
            cursor.execute('UPDATE auctions SET bid_amount = %s WHERE auction_id = %s', (bid, id))
            con.commit()
        except:
            return ()
        finally:
            con.close()

    def winlostauctions(self):
        con = ACV.connect(self)
        cursor = con.cursor()
        try:
            current_datetime = datetime.datetime.now()
            auction_end_time = current_datetime.strftime("%Y-%m-%d %H:%M:%S ")
            cursor.execute('SELECT * FROM auctions WHERE action_end_datetime < %s AND bid_amount != %s', (auction_end_time, 0))
            expire_auctions = cursor.fetchall()

            won_auction_ids = []
            lost_auction_ids = []

            for auction in expire_auctions:
                if auction[27] == 1 and auction[34] == 1:
                    won_auction_ids.append(auction[4])
                elif auction[27] == 0:
                    lost_auction_ids.append(auction[4])

            if won_auction_ids:
                cursor.execute('UPDATE auctions SET win = %s WHERE auction_id IN %s', (1, tuple(won_auction_ids)))
                con.commit()

            if lost_auction_ids:
                cursor.execute('UPDATE auctions SET lost = %s WHERE auction_id IN %s', (1, tuple(lost_auction_ids)))
                con.commit()

        except:
            return ()
        finally:
            cursor.close()
            con.close()

    def getMisseauction(self,):
        con = ACV.connect(self)
        cursor = con.cursor()
        try:
            cursor.execute('SELECT * FROM auctions WHERE is_match = %s and action_end_datetime > %s and status = "active"', (0,datetime.datetime.now()))
            return  cursor.fetchall()
        except:
            return ()
        finally:
            con.close()
    
    def getwonauction(self,):
        con = ACV.connect(self)
        cursor = con.cursor()
        try:
            cursor.execute('SELECT * FROM auctions WHERE win = %s', (1,))
            return  cursor.fetchall()
        except:
            return ()
        finally:
            con.close()

    def getlostauction(self,):
        con = ACV.connect(self)
        cursor = con.cursor()
        try:
            cursor.execute('SELECT * FROM auctions WHERE lost = %s', (1,))
            return  cursor.fetchall()
        except:
            return ()
        finally:
            con.close()
    
    def getauctioncondition(self, id):
        con = ACV.connect(self)
        cursor = con.cursor()
        try:
            cursor.execute('SELECT * FROM auction_condition_report WHERE auction_id = %s', (id,))
            condition_report = cursor.fetchone()
            cursor.execute('SELECT auction_id, lights, auction_url, distance, location, vin, odometer, transmission, trim, drivetrain, engine, fuel_type, year, make, model, basic_color, action_start_datetime FROM auctions WHERE auction_id = %s', (id,))
            auction = cursor.fetchone()
            return condition_report, auction
        except:
            return ()
        finally:
            con.close()

    def update(self,id,is_high_bidder,nextbidamount):
        con = ACV.connect(self)
        cursor = con.cursor()
        try:
            cursor.execute('UPDATE auctions SET is_high_bidder = %s, next_bid_amount = %s WHERE auction_id = %s', (is_high_bidder,nextbidamount,id))
            con.commit()
        except:
            return ()
        finally:
            con.close()
    
    def updateproxydata(self,id,proxybidamount):
        con = ACV.connect(self)
        cursor = con.cursor()
        try:
            cursor.execute('UPDATE auctions SET proxy_bid_amount = %s WHERE auction_id = %s', (proxybidamount,id))
            con.commit()
        except:
            return ()
        finally:
            con.close()

    def matchauction(self,id,is_match):
        con = ACV.connect(self)
        cursor = con.cursor()
        try:
            if is_match == True:
                cursor.execute('UPDATE auctions SET is_match = %s WHERE auction_id = %s', (1,id))
            else:
                cursor.execute('UPDATE auctions SET is_match = %s WHERE auction_id = %s', (0,id))
            con.commit()
        except:
            return ()
        finally:
            con.close()
    
    def getUpcomingauction(self,):
        con = ACV.connect(self)
        cursor = con.cursor()
        try:
            cursor.execute('SELECT * FROM auctions WHERE status = "run_list" and action_start_datetime > %s',datetime.datetime.now())
            return cursor.fetchall()
        except:
            return ()
        finally:
            con.close()

    def liveAuctions(self,):
        con = ACV.connect(self)
        cursor = con.cursor()
        try:
            cursor.execute('SELECT * FROM auctions')
            return cursor.fetchall()
        except:
            return ()
        finally:
            con.close()

    def liveinsertauctiondata(self, data):
        con = ACV.connect(self)
        cursor = con.cursor()
        try:   

            body_damage = ""
            # major, moderate, minor body damage are false
            if data['conditionReport']['sections'][0]['questions'][2]['selected'] == 0 and data['conditionReport']['sections'][0]['questions'][1]['selected'] == 0 and data['conditionReport']['sections'][0]['questions'][0]['selected'] == 0:
                body_damage = 'No, my vehicle is in good shape!'

            # major body damage is true and moderate body damage is false
            elif data['conditionReport']['sections'][0]['questions'][2]['selected'] == 1 and data['conditionReport']['sections'][0]['questions'][1]['selected'] == 0:
                body_damage = 'FR,RR,SD,TP'
            
            # moderate body damage is true and minor body damage is false
            elif data['conditionReport']['sections'][0]['questions'][1]['selected'] == 1 and data['conditionReport']['sections'][0]['questions'][0]['selected'] == 0:
                body_damage = 'FR'
            
            # major body damage is true and minor body damage is false
            elif data['conditionReport']['sections'][0]['questions'][2]['selected'] == 1 and data['conditionReport']['sections'][0]['questions'][0]['selected'] == 0:
                body_damage = 'FR,RR,SD,TP'
            
            #major body damage is true
            elif data['conditionReport']['sections'][0]['questions'][2]['selected'] == 1:
                body_damage = 'FR,RR,SD,TP'
            
            #moderate body damage is true
            elif data['conditionReport']['sections'][0]['questions'][1]['selected'] == 1:
                body_damage = 'FR'
            
            #minor body damage is true
            elif data['conditionReport']['sections'][0]['questions'][0]['selected'] == 1:
                body_damage = 'No, my vehicle is in good shape!'

            airbag_value = 'N'
            if data['conditionReport']['sections'][5]['questions'][13]['selected'] == 1:
                airbag_value = 'Y'

            start_and_drive = ''
            # if engine_does_not_start is false and engine_does_not_crank is false
            if data['conditionReport']['sections'][2]['questions'][2]['selected'] == 0 and data['conditionReport']['sections'][2]['questions'][1]['selected'] == 0:
                # engine_does_not_stay_running is true or vehicle inoperable is true
                if data['conditionReport']['sections'][2]['questions'][3]['selected'] == 1 or data['conditionReport']['sections'][3]['questions'][0]['selected'] == 1:
                    start_and_drive = 'S'
                
                # engine_does_not_stay_running is true or vehicle inoperable is false
                elif data['conditionReport']['sections'][2]['questions'][3]['selected'] == 1 or data['conditionReport']['sections'][3]['questions'][0]['selected'] == 0:
                    start_and_drive = 'S'

                # engine_does_not_stay_running is false or vehicle inoperable is true
                elif data['conditionReport']['sections'][2]['questions'][3]['selected'] == 0 or data['conditionReport']['sections'][3]['questions'][0]['selected'] == 1:
                    start_and_drive = 'S'
                
                # engine_does_not_stay_running is false or vehicle inoperable is false
                elif data['conditionReport']['sections'][2]['questions'][3]['selected'] == 0 or data['conditionReport']['sections'][3]['questions'][0]['selected'] == 0:
                    if data['conditionReport']['sections'][2]['questions'][3]['selected'] == 0 and data['conditionReport']['sections'][3]['questions'][0]['selected'] == 0:
                        start_and_drive = 'D'

            # if engine_does_not_start is true or engine_does_not_crank is true
            elif data['conditionReport']['sections'][2]['questions'][2]['selected'] == 1 or data['conditionReport']['sections'][2]['questions'][1]['selected'] == 1:
                start_and_drive = 'N'
            
            # if engine_does_not_start is true or engine_does_not_crank is false
            elif data['conditionReport']['sections'][2]['questions'][2]['selected'] == 1 or data['conditionReport']['sections'][2]['questions'][1]['selected'] == 0:
                start_and_drive = 'N'
            
            # if engine_does_not_start is false or engine_does_not_crank is true
            elif data['conditionReport']['sections'][2]['questions'][2]['selected'] == 0 or data['conditionReport']['sections'][2]['questions'][1]['selected'] == 1:
                start_and_drive = 'N'

            trasmission_issue = "No my vehicle is in good shape!"

            if (data['conditionReport']['sections'][3]['questions'][2]['selected'] == 1 or data['conditionReport']['sections'][3]['questions'][1]['selected'] == 1) and (data['conditionReport']['sections'][2]['questions'][4]['selected'] == 1 or data['conditionReport']['sections'][2]['questions'][5]['selected'] == 1 or data['conditionReport']['sections'][2]['questions'][6]['selected'] == 1 or data['conditionReport']['sections'][2]['questions'][9]['selected'] == 1 or data['conditionReport']['sections'][2]['questions'][10]['selected'] == 1) and (data['conditionReport']['sections'][1]['questions'][3]['selected'] == 1 or data['conditionReport']['sections'][1]['questions'][0]['selected'] == 1):
                trasmission_issue = 'Yes major engine issues,Yes major transmission issues,Yes major frame issues'

            elif ((data['conditionReport']['sections'][3]['questions'][2]['selected'] == 1 or data['conditionReport']['sections'][3]['questions'][1]['selected'] == 1) and (data['conditionReport']['sections'][2]['questions'][4]['selected'] == 1 or data['conditionReport']['sections'][2]['questions'][5]['selected'] == 1 or data['conditionReport']['sections'][2]['questions'][6]['selected'] == 1 or data['conditionReport']['sections'][2]['questions'][9]['selected'] == 1 or data['conditionReport']['sections'][2]['questions'][10]['selected'] == 1)):
                trasmission_issue = 'Yes major transmission issues,Yes major engine issues'

            elif ((data['conditionReport']['sections'][2]['questions'][4]['selected'] == 1 or data['conditionReport']['sections'][2]['questions'][5]['selected'] == 1 or data['conditionReport']['sections'][2]['questions'][6]['selected'] == 1 or data['conditionReport']['sections'][2]['questions'][9]['selected'] == 1 or data['conditionReport']['sections'][2]['questions'][10]['selected'] == 1) and (data['conditionReport']['sections'][1]['questions'][3]['selected'] == 1 or data['conditionReport']['sections'][1]['questions'][0]['selected'] == 1)):
                trasmission_issue = 'Yes major engine issues,Yes major frame issues'

            elif ((data['conditionReport']['sections'][3]['questions'][2]['selected'] == 1 or data['conditionReport']['sections'][3]['questions'][1]['selected'] == 1) and (data['conditionReport']['sections'][1]['questions'][3]['questionTitle']['selected'] == 1 or data['conditionReport']['sections'][1]['questions'][0]['selected'] == 1)):
                trasmission_issue = 'Yes major transmission issues,Yes major frame issues'
            
            elif (data['conditionReport']['sections'][3]['questions'][2]['selected'] == 1 or data['conditionReport']['sections'][3]['questions'][1]['selected'] == 1):
                trasmission_issue = 'Yes major transmission issues'

            elif (data['conditionReport']['sections'][2]['questions'][4]['selected'] == 1 or data['conditionReport']['sections'][2]['questions'][5]['selected'] == 1 or data['conditionReport']['sections'][2]['questions'][6]['selected'] == 1 or data['conditionReport']['sections'][2]['questions'][9]['selected'] == 1 or data['conditionReport']['sections'][2]['questions'][10]['selected'] == 1):
                trasmission_issue = 'Yes major engine issues'
            

            elif (data['conditionReport']['sections'][1]['questions'][3]['selected'] == 1 or data['conditionReport']['sections'][1]['questions'][0]['selected'] == 1):
                trasmission_issue = 'Yes major frame issues'


            title_type = ""
            # if sold on bill sale is true
            if data['conditionReport']['sections'][7]['questions'][9]['selected'] == 1:
                title_type = "Unknown"
            else:
                # if branded title is true
                if data['conditionReport']['sections'][7]['questions'][1]['selected'] == 1:
                    title_type = 'Salvage Rebuilt'
                else:
                    # hail damage is true
                    if data['conditionReport']['sections'][0]['questions'][11]['selected'] == 1:
                        title_type = 'Salvage Rebuilt'
                    else:
                        title_type = 'Clean Title'      
            
            fire_water_damage = 'no'
            if data['conditionReport']['sections'][7]['questions'][3]['selected'] == 1:
                fire_water_damage = 'W'

            lights = []
            if data['blueLight'] == 1:
                lights.append('blue')
            
            if data['yellowLight'] == 1:
                lights.append('yellow')
            
            if data['redLight'] == 1:
                lights.append('red')
            
            if data['greenLight'] == 1:
                lights.append('green')
        
            lights_str = ' '.join(lights)
         
            cursor.execute('SELECT auction_id from live_auctions WHERE auction_id = %s',data['id'])
            fetchone = cursor.fetchone()

            if fetchone is None:
                print('insert auction')
                cursor.execute('INSERT INTO live_auctions (year,make,model,auction_id,location,odometer,action_end_datetime,zip_code,bid_amount,bid_count,vin,status,minor_body_type_ans,modrate_body_type_ans,major_body_type_ans,airbag_deployed_ans,engine_start_or_not,engine_start_not_run,transmission_issue_ans,frame_issue_ans,title_absent_ans,title_branded_ans,vehicle_display_name,start_and_drive_ans,next_bid_amount,start_price,is_high_bidder,created_at,body_damage,reserve_met,next_proxy_bid_amount,action_start_datetime,lights,auction_image_url,auction_url, distance,transmission,trim,drivetrain,engine,fuel_type,basic_color,water_or_fire_damage) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', 
                            (data['year'],data['make'],data['model'],data['id'],data['location'],data['odometer'],data['endTime'],data['postalCode'],data['bidAmount'],data['bidCount'],data['vin'],data['status'],
                                # body type damage
                                data['conditionReport']['sections'][0]['questions'][0]['selected'],
                                data['conditionReport']['sections'][0]['questions'][1]['selected'],
                                data['conditionReport']['sections'][0]['questions'][2]['selected'],

                                # airbag issue
                                airbag_value,

                                # engine start 
                                data['conditionReport']['sections'][2]['questions'][2]['selected'],
                                data['conditionReport']['sections'][2]['questions'][3]['selected'],

                                # transmission issue
                                trasmission_issue,

                                # frame issue
                                data['conditionReport']['sections'][1]['questions'][0]['selected'],
                
                                # title issue
                                title_type,
                                data['conditionReport']['sections'][7]['questions'][1]['selected'],

                                data['vehicleDisplayName'],

                                start_and_drive,
                                data['nextBidAmount'],
                                data['startPrice'],
                                data['isHighBidder'],
                                datetime.datetime.now(),
                                body_damage,
                                data['reserveMet'],
                                data['nextProxyAmount'],
                                data['startTime'],
                                lights_str,
                                data['primaryImage']['url'],
                                data['auctionLink'],
                                data['distance'],
                                data['transmission'],
                                data['trim'],
                                data['drivetrain'],
                                data['engine'],
                                data['fuelType'],
                                data['basicColor'],
                                fire_water_damage
                                )),
                
                con.commit()
            else:
                print('update auction')
                cursor.execute('UPDATE live_auctions SET year = %s, make = %s, model = %s, location = %s, odometer= %s, action_end_datetime = %s, zip_code = %s, bid_amount = %s, bid_count = %s, vin = %s, status = %s, minor_body_type_ans = %s, modrate_body_type_ans = %s, major_body_type_ans = %s, airbag_deployed_ans = %s, engine_start_or_not = %s, engine_start_not_run = %s, transmission_issue_ans = %s, frame_issue_ans = %s, title_absent_ans = %s, title_branded_ans = %s, vehicle_display_name = %s, start_and_drive_ans = %s, next_bid_amount = %s, start_price = %s, is_high_bidder = %s, updated_at = %s, body_damage = %s, reserve_met = %s, next_proxy_bid_amount = %s, action_start_datetime = %s, lights = %s, auction_image_url =%s, auction_url = %s, distance = %s, transmission = %s, trim = %s, drivetrain = %s, engine = %s, fuel_type = %s, basic_color = %s, water_or_fire_damage = %s where auction_id = %s',(data['year'],data['make'],data['model'],data['location'],data['odometer'],data['endTime'],data['postalCode'],data['bidAmount'],data['bidCount'],data['vin'],data['status'], 
                    # body type damage
                    data['conditionReport']['sections'][0]['questions'][0]['selected'], 
                    data['conditionReport']['sections'][0]['questions'][1]['selected'], 
                    data['conditionReport']['sections'][0]['questions'][2]['selected'],
                    
                    #airbag issue
                    airbag_value, 
                    
                    #engine start 
                    data['conditionReport']['sections'][2]['questions'][2]['selected'], 
                    data['conditionReport']['sections'][2]['questions'][3]['selected'],

                    #transmission issue
                    trasmission_issue,

                    #frame issue
                    data['conditionReport']['sections'][1]['questions'][0]['selected'],

                    #title issue
                    title_type,
                    data['conditionReport']['sections'][7]['questions'][1]['selected'],

                    data['vehicleDisplayName'],
                    start_and_drive,
                    data['nextBidAmount'],
                    data['startPrice'],
                    data['isHighBidder'],
                    datetime.datetime.now(),
                    body_damage,
                    data['reserveMet'],
                    data['nextProxyAmount'],
                    data['startTime'],
                    lights_str,
                    data['primaryImage']['url'],
                    data['auctionLink'],
                    data['distance'],
                    data['transmission'],
                    data['trim'],
                    data['drivetrain'],
                    data['engine'],
                    data['fuelType'],
                    data['basicColor'],
                    fire_water_damage,
                    data['id']))
                
                con.commit()


        except:
            return ()
        finally:
            con.close()

    def liveauctionconditionreport(self, data):
        con = ACV.connect(self)
        cursor = con.cursor()
        try:
            cursor.execute('SELECT auction_id from live_auction_condition_report WHERE auction_id = %s',data['id'])
            fetchone = cursor.fetchone()
            # section - 0 - Exterior

            minor_body_type = {
                "questionTitle": data['conditionReport']['sections'][0]['questions'][0]['questionTitle'],
                "selected": data['conditionReport']['sections'][0]['questions'][0]['selected'],
                "answer": data['conditionReport']['sections'][0]['questions'][0]['answer']
            }
            
            moderate_body_type = {
                "questionTitle": data['conditionReport']['sections'][0]['questions'][1]['questionTitle'],
                "selected": data['conditionReport']['sections'][0]['questions'][1]['selected'],
                "answer": data['conditionReport']['sections'][0]['questions'][1]['answer']
            }

            major_body_type = {
                "questionTitle": data['conditionReport']['sections'][0]['questions'][2]['questionTitle'],
                "selected": data['conditionReport']['sections'][0]['questions'][2]['selected'],
                "answer": data['conditionReport']['sections'][0]['questions'][2]['answer']
            }
            
            glass_damage = {
                "questionTitle": data['conditionReport']['sections'][0]['questions'][3]['questionTitle'],
                "selected": data['conditionReport']['sections'][0]['questions'][3]['selected'],
                "answer": data['conditionReport']['sections'][0]['questions'][3]['answer']
            }
    
            lights_damage = {
                "questionTitle": data['conditionReport']['sections'][0]['questions'][4]['questionTitle'],
                "selected": data['conditionReport']['sections'][0]['questions'][4]['selected'],
                "answer": data['conditionReport']['sections'][0]['questions'][4]['answer']
            }

            surface_rust = {
                "questionTitle": data['conditionReport']['sections'][0]['questions'][5]['questionTitle'],
                "selected": data['conditionReport']['sections'][0]['questions'][5]['selected'],
                "answer": data['conditionReport']['sections'][0]['questions'][5]['answer']
            } 

            modrate_body_rust = {
                'questionTitle': data['conditionReport']['sections'][0]['questions'][6]['questionTitle'],
                'selected': data['conditionReport']['sections'][0]['questions'][6]['selected'],
                'answer': data['conditionReport']['sections'][0]['questions'][6]['answer']
            }

            heavy_rust = {
                "questionTitle": data['conditionReport']['sections'][0]['questions'][7]['questionTitle'],
                "selected": data['conditionReport']['sections'][0]['questions'][7]['selected'],
                "answer": data['conditionReport']['sections'][0]['questions'][7]['answer']
            }

            penetrating_rust = {
                "questionTitle": data['conditionReport']['sections'][0]['questions'][8]['questionTitle'],
                "selected": data['conditionReport']['sections'][0]['questions'][8]['selected'],
                "answer": data['conditionReport']['sections'][0]['questions'][8]['answer']
            }


            previous_paint_work = {
                "questionTitle": data['conditionReport']['sections'][0]['questions'][9]['questionTitle'],
                "selected": data['conditionReport']['sections'][0]['questions'][9]['selected'],
                "answer": data['conditionReport']['sections'][0]['questions'][9]['answer']
            }  
            
            poor_quality_repairs = {
                "questionTitle": data['conditionReport']['sections'][0]['questions'][10]['questionTitle'],
                "selected": data['conditionReport']['sections'][0]['questions'][10]['selected'],
                "answer": data['conditionReport']['sections'][0]['questions'][10]['answer']
            }

            hail_damage = {
                'questionTitle': data['conditionReport']['sections'][0]['questions'][11]['questionTitle'],
                'selected': data['conditionReport']['sections'][0]['questions'][11]['selected'],
                'answer': data['conditionReport']['sections'][0]['questions'][11]['answer']
            }

            aftermarket_parts_exterior = {
                "questionTitle": data['conditionReport']['sections'][0]['questions'][12]['questionTitle'], 
                "selected": data['conditionReport']['sections'][0]['questions'][12]['selected'],
                "answer": data['conditionReport']['sections'][0]['questions'][12]['answer']
            }

            paint_meter_readings = {
                "questionTitle": data['conditionReport']['sections'][0]['questions'][13]['questionTitle'],
                "selected": data['conditionReport']['sections'][0]['questions'][13]['selected'],
                "answer": data['conditionReport']['sections'][0]['questions'][13]['answer']
            }
            
            # major_body_rust = {
            #     'questionTitle': data['conditionReport']['sections'][0]['questions'][8]['questionTitle'],
            #     'selected': data['conditionReport']['sections'][0]['questions'][8]['selected'],
            #     'answer': data['conditionReport']['sections'][0]['questions'][8]['answer']
            # }

            # mismatched_paint = {
            #     "questionTitle": data['conditionReport']['sections'][0]['questions'][11]['questionTitle'],
            #     "selected": data['conditionReport']['sections'][0]['questions'][11]['selected'],
            #     "answer": data['conditionReport']['sections'][0]['questions'][11]['answer']
            # }

            # section - 1 = Frame & Unibody   

            frame_damage = {
                "questionTitle": data['conditionReport']['sections'][1]['questions'][0]['questionKey'],
                "selected": data['conditionReport']['sections'][1]['questions'][0]['selected'],
                "answer": data['conditionReport']['sections'][1]['questions'][0]['answer']
            }
            
            undercarriage_surface_rust = {
                "questionTitle": data['conditionReport']['sections'][1]['questions'][1]['questionTitle'],
                "selected": data['conditionReport']['sections'][1]['questions'][1]['selected'],
                "answer": data['conditionReport']['sections'][1]['questions'][1]['answer']
            } 

            undercarriage_heavy_rust = {
                "questionTitle": data['conditionReport']['sections'][1]['questions'][2]['questionTitle'],
                "selected": data['conditionReport']['sections'][1]['questions'][2]['selected'],
                "answer": data['conditionReport']['sections'][1]['questions'][2]['answer']
            }

            undercarriage_heavy_rot = {
                 "questionTitle": data['conditionReport']['sections'][1]['questions'][3]['questionTitle'],
                "selected": data['conditionReport']['sections'][1]['questions'][3]['selected'],
                "answer": data['conditionReport']['sections'][1]['questions'][3]['answer']
            }
             
            # section - 2 - Mechanicals

            jump_start_required = {
                "questionTitle": data['conditionReport']['sections'][2]['questions'][0]['questionTitle'],
                "selected": data['conditionReport']['sections'][2]['questions'][0]['selected'],
                "answer": data['conditionReport']['sections'][2]['questions'][0]['answer']
            }

            engine_does_not_crank = {
                "questionTitle": data['conditionReport']['sections'][2]['questions'][1]['questionTitle'],
                "selected": data['conditionReport']['sections'][2]['questions'][1]['selected'],
                "answer": data['conditionReport']['sections'][2]['questions'][1]['answer']
            }

            engine_does_not_start = {
                "questionTitle": data['conditionReport']['sections'][2]['questions'][2]['questionTitle'],
                "selected": data['conditionReport']['sections'][2]['questions'][2]['selected'],
                "answer": data['conditionReport']['sections'][2]['questions'][2]['answer']
            }

            engine_does_not_stay_running = {
                "questionTitle": data['conditionReport']['sections'][2]['questions'][3]['questionTitle'],
                "selected": data['conditionReport']['sections'][2]['questions'][3]['selected'],
                "answer": data['conditionReport']['sections'][2]['questions'][3]['answer']
            }

            engine_noise = {
                "questionTitle": data['conditionReport']['sections'][2]['questions'][4]['questionTitle'],
                "selected": data['conditionReport']['sections'][2]['questions'][4]['selected'],
                "answer": data['conditionReport']['sections'][2]['questions'][4]['answer']
            }

            engine_hesitation = {
                "questionTitle": data['conditionReport']['sections'][2]['questions'][5]['questionTitle'],
                "selected": data['conditionReport']['sections'][2]['questions'][5]['selected'],
                "answer": data['conditionReport']['sections'][2]['questions'][5]['answer']
            }

            engine_overheats = {
                "questionTitle": data['conditionReport']['sections'][2]['questions'][6]['questionTitle'],
                "selected": data['conditionReport']['sections'][2]['questions'][6]['selected'],
                "answer": data['conditionReport']['sections'][2]['questions'][6]['answer']
            }
            
            timing_chain_issue = {
                "questionTitle": data['conditionReport']['sections'][2]['questions'][7]['questionTitle'],
                "selected": data['conditionReport']['sections'][2]['questions'][7]['selected'],
                "answer": data['conditionReport']['sections'][2]['questions'][7]['answer']
            }

            supercharger_issue = {
                "questionTitle": data['conditionReport']['sections'][2]['questions'][8]['questionTitle'],
                "selected": data['conditionReport']['sections'][2]['questions'][8]['selected'],
                "answer": data['conditionReport']['sections'][2]['questions'][8]['answer']
            }
            
            abnormal_exhaust_smoke = {
                "questionTitle": data['conditionReport']['sections'][2]['questions'][9]['questionTitle'],
                "selected": data['conditionReport']['sections'][2]['questions'][9]['selected'],
                "answer": data['conditionReport']['sections'][2]['questions'][9]['answer']
            }

            head_gasket_issue = {
                "questionTitle": data['conditionReport']['sections'][2]['questions'][10]['questionTitle'],
                "selected": data['conditionReport']['sections'][2]['questions'][10]['selected'],
                "answer": data['conditionReport']['sections'][2]['questions'][10]['answer']
            }

            exhaust_noise = {
                "questionTitle": data['conditionReport']['sections'][2]['questions'][11]['questionTitle'],
                "selected": data['conditionReport']['sections'][2]['questions'][11]['selected'],
                "answer": data['conditionReport']['sections'][2]['questions'][11]['answer']
            }

            exhaust_modifications = {
                "questionTitle": data['conditionReport']['sections'][2]['questions'][12]['questionTitle'],
                "selected": data['conditionReport']['sections'][2]['questions'][12]['selected'],
                "answer": data['conditionReport']['sections'][2]['questions'][12]['answer']
            }

            suspension_modifications = {
                "questionTitle": data['conditionReport']['sections'][2]['questions'][13]['questionTitle'],  
                "selected": data['conditionReport']['sections'][2]['questions'][13]['selected'],
                "answer": data['conditionReport']['sections'][2]['questions'][13]['answer']
            }

            emissions_modifications = {
                "questionTitle": data['conditionReport']['sections'][2]['questions'][14]['questionTitle'],
                "selected": data['conditionReport']['sections'][2]['questions'][14]['selected'],
                "answer": data['conditionReport']['sections'][2]['questions'][14]['answer']
            }
            
            emissions_issue = {
                 "questionTitle": data['conditionReport']['sections'][2]['questions'][15]['questionTitle'],
                "selected": data['conditionReport']['sections'][2]['questions'][15]['selected'],
                "answer": data['conditionReport']['sections'][2]['questions'][15]['answer']
            }
            
            catalytic_converters_missing = {
                "questionTitle": data['conditionReport']['sections'][2]['questions'][16]['questionTitle'],
                "selected": data['conditionReport']['sections'][2]['questions'][16]['selected'],
                "answer": data['conditionReport']['sections'][2]['questions'][16]['answer']
            }

            aftermarket_mechanical = {
                'questionTitle': data['conditionReport']['sections'][2]['questions'][17]['questionTitle'],
                'selected': data['conditionReport']['sections'][2]['questions'][17]['selected'],
                'answer': data['conditionReport']['sections'][2]['questions'][17]['answer']
            }

            engine_accessory_issue = {
                'questionTitle': data['conditionReport']['sections'][2]['questions'][18]['questionTitle'],
                'selected': data['conditionReport']['sections'][2]['questions'][18]['selected'],
                'answer': data['conditionReport']['sections'][2]['questions'][18]['answer']
            }

            fluid_leaks = {
                'questionTitle': data['conditionReport']['sections'][2]['questions'][19]['questionTitle'],
                'selected': data['conditionReport']['sections'][2]['questions'][19]['selected'],
                'answer': data['conditionReport']['sections'][2]['questions'][19]['answer']
            }

            oil_level_issue = {
               'questionTitle': data['conditionReport']['sections'][2]['questions'][20]['questionTitle'],
                'selected': data['conditionReport']['sections'][2]['questions'][20]['selected'],
                'answer': data['conditionReport']['sections'][2]['questions'][20]['answer']
            }

            oil_condition_issue = {
                 'questionTitle': data['conditionReport']['sections'][2]['questions'][21]['questionTitle'],
                'selected': data['conditionReport']['sections'][2]['questions'][21]['selected'],
                'answer': data['conditionReport']['sections'][2]['questions'][21]['answer']
            }
            
            oil_intermix_dipstick_v2 = {
                'questionTitle': data['conditionReport']['sections'][2]['questions'][22]['questionTitle'],
                'selected': data['conditionReport']['sections'][2]['questions'][22]['selected'],
                'answer': data['conditionReport']['sections'][2]['questions'][22]['answer']
            }

            coolant_level_issue = {
               'questionTitle': data['conditionReport']['sections'][2]['questions'][23]['questionTitle'],
                'selected': data['conditionReport']['sections'][2]['questions'][23]['selected'],
                'answer': data['conditionReport']['sections'][2]['questions'][23]['answer']
            }
           
            # section 3 Driveability
            vehicle_inop = {
                "questionTitle": data['conditionReport']['sections'][3]['questions'][0]['questionTitle'],
                "selected": data['conditionReport']['sections'][3]['questions'][0]['selected'],
                "answer": data['conditionReport']['sections'][3]['questions'][0]['answer']
            }

            transmission_issue = {
                "questionTitle": data['conditionReport']['sections'][3]['questions'][1]['questionTitle'],
                "selected": data['conditionReport']['sections'][3]['questions'][1]['selected'],
                "answer": data['conditionReport']['sections'][3]['questions'][1]['answer']
            }

            drivetrain_issue = {
                "questionTitle": data['conditionReport']['sections'][3]['questions'][2]['questionTitle'],
                "selected": data['conditionReport']['sections'][3]['questions'][2]['selected'],
                "answer": data['conditionReport']['sections'][3]['questions'][2]['answer']
            }

            steering_issue = {
                "questionTitle": data['conditionReport']['sections'][3]['questions'][3]['questionTitle'],
                "selected": data['conditionReport']['sections'][3]['questions'][3]['selected'],
                "answer": data['conditionReport']['sections'][3]['questions'][3]['answer']
            }

            break_issue = {
                "questionTitle": data['conditionReport']['sections'][3]['questions'][4]['questionTitle'],
                "selected": data['conditionReport']['sections'][3]['questions'][4]['selected'],
                "answer": data['conditionReport']['sections'][3]['questions'][4]['answer']
            }

            suspension_issue = {
                "questionTitle": data['conditionReport']['sections'][3]['questions'][5]['questionTitle'],
                "selected": data['conditionReport']['sections'][3]['questions'][5]['selected'],
                "answer": data['conditionReport']['sections'][3]['questions'][5]['answer']
            }

            # section - 4 - Warning Lights"

            check_engine_light = {
                "questionTitle": data['conditionReport']['sections'][4]['questions'][0]['questionTitle'],
                "selected": data['conditionReport']['sections'][4]['questions'][0]['selected'],
                "answer": data['conditionReport']['sections'][4]['questions'][0]['answer']
            }

            airbag_light = {
                "questionTitle": data['conditionReport']['sections'][4]['questions'][1]['questionTitle'],
                "selected": data['conditionReport']['sections'][4]['questions'][1]['selected'],
                "answer": data['conditionReport']['sections'][4]['questions'][1]['answer']
            }
            
            brake_light = {
                "questionTitle": data['conditionReport']['sections'][4]['questions'][2]['questionTitle'],
                "selected": data['conditionReport']['sections'][4]['questions'][2]['selected'],
                "answer": data['conditionReport']['sections'][4]['questions'][2]['answer']
            }

            traction_control_light = {
                "questionTitle": data['conditionReport']['sections'][4]['questions'][3]['questionTitle'],
                "selected": data['conditionReport']['sections'][4]['questions'][3]['selected'],
                "answer": data['conditionReport']['sections'][4]['questions'][3]['answer']
            }

            tpms_light = {
                "questionTitle": data['conditionReport']['sections'][4]['questions'][4]['questionTitle'],
                "selected": data['conditionReport']['sections'][4]['questions'][4]['selected'],
                "answer": data['conditionReport']['sections'][4]['questions'][4]['answer']
            }

            battery_light = {
                "questionTitle": data['conditionReport']['sections'][4]['questions'][5]['questionTitle'],
                "selected": data['conditionReport']['sections'][4]['questions'][5]['selected'],
                "answer": data['conditionReport']['sections'][4]['questions'][5]['answer']
            }

            other_warning_light = {
                "questionTitle": data['conditionReport']['sections'][4]['questions'][6]['questionTitle'],
                "selected": data['conditionReport']['sections'][4]['questions'][6]['selected'],
                "answer": data['conditionReport']['sections'][4]['questions'][6]['answer']
            }

            obdii_codes = {
                "questionTitle": data['conditionReport']['sections'][4]['questions'][7]['questionTitle'],
                "selected": data['conditionReport']['sections'][4]['questions'][7]['selected'],
                "answer": data['conditionReport']['sections'][4]['questions'][7]['answer']
            }

            incomplete_readiness_monitors = {
                "questionTitle": data['conditionReport']['sections'][4]['questions'][8]['questionTitle'],
                "selected": data['conditionReport']['sections'][4]['questions'][8]['selected'],
                "answer": data['conditionReport']['sections'][4]['questions'][8]['answer']
            }

            #section - 5 - Interior

            seat_damage = {
                "questionTitle": data['conditionReport']['sections'][5]['questions'][0]['questionTitle'],
                "selected": data['conditionReport']['sections'][5]['questions'][0]['selected'],
                "answer": data['conditionReport']['sections'][5]['questions'][0]['answer']
            }

            carpet_damage = {
                "questionTitle": data['conditionReport']['sections'][5]['questions'][1]['questionTitle'],
                "selected": data['conditionReport']['sections'][5]['questions'][1]['selected'],
                "answer": data['conditionReport']['sections'][5]['questions'][1]['answer']
            }

            dashboard_damage = {
                "questionTitle": data['conditionReport']['sections'][5]['questions'][2]['questionTitle'],
                "selected": data['conditionReport']['sections'][5]['questions'][2]['selected'],
                "answer": data['conditionReport']['sections'][5]['questions'][2]['answer']
            }

            headliner_damage = {
                "questionTitle": data['conditionReport']['sections'][5]['questions'][3]['questionTitle'],
                "selected": data['conditionReport']['sections'][5]['questions'][3]['selected'],
                "answer": data['conditionReport']['sections'][5]['questions'][3]['answer']
            }

            interior_trim_damage = {
                "questionTitle": data['conditionReport']['sections'][5]['questions'][4]['questionTitle'],
                "selected": data['conditionReport']['sections'][5]['questions'][4]['selected'],
                "answer": data['conditionReport']['sections'][5]['questions'][4]['answer']
            }

            interior_order = {
                "questionTitle": data['conditionReport']['sections'][5]['questions'][5]['questionTitle'],
                "selected": data['conditionReport']['sections'][5]['questions'][5]['selected'],
                "answer": data['conditionReport']['sections'][5]['questions'][5]['answer']
            }

            crank_windows = {
                "questionTitle": data['conditionReport']['sections'][5]['questions'][6]['questionTitle'],
                "selected": data['conditionReport']['sections'][5]['questions'][6]['selected'],
                "answer": data['conditionReport']['sections'][5]['questions'][6]['answer']
            }

            no_factory_ac = {
                "questionTitle": data['conditionReport']['sections'][5]['questions'][7]['questionTitle'],
                "selected": data['conditionReport']['sections'][5]['questions'][7]['selected'],
                "answer": data['conditionReport']['sections'][5]['questions'][7]['answer']
            }

            electronics_issue = {
                "questionTitle": data['conditionReport']['sections'][5]['questions'][8]['questionTitle'],
                "selected": data['conditionReport']['sections'][5]['questions'][8]['selected'],
                "answer": data['conditionReport']['sections'][5]['questions'][8]['answer']
            }

            five_digit_odometer = {
                "questionTitle": data['conditionReport']['sections'][5]['questions'][9]['questionTitle'],
                "selected": data['conditionReport']['sections'][5]['questions'][9]['selected'],
                "answer": data['conditionReport']['sections'][5]['questions'][9]['answer']
            }

            sunroof = {
                "questionTitle": data['conditionReport']['sections'][5]['questions'][10]['questionTitle'],
                "selected": data['conditionReport']['sections'][5]['questions'][10]['selected'],
                "answer": data['conditionReport']['sections'][5]['questions'][10]['answer']
            }

            aftermarket_sunroof = {
               "questionTitle": data['conditionReport']['sections'][5]['questions'][11]['questionTitle'],
                "selected": data['conditionReport']['sections'][5]['questions'][11]['selected'],
                "answer": data['conditionReport']['sections'][5]['questions'][11]['answer']
            }

            navigation = {
                "questionTitle": data['conditionReport']['sections'][5]['questions'][12]['questionTitle'],
                "selected": data['conditionReport']['sections'][5]['questions'][12]['selected'],
                "answer": data['conditionReport']['sections'][5]['questions'][12]['answer']
            }

            backup_camera = {
                "questionTitle": data['conditionReport']['sections'][5]['questions'][13]['questionTitle'],
                "selected": data['conditionReport']['sections'][5]['questions'][13]['selected'],
                "answer": data['conditionReport']['sections'][5]['questions'][13]['answer']
            }

            charging_cable = {
                 "questionTitle": data['conditionReport']['sections'][5]['questions'][14]['questionTitle'],
                "selected": data['conditionReport']['sections'][5]['questions'][14]['selected'],
                "answer": data['conditionReport']['sections'][5]['questions'][14]['answer']
            }

            aftermarket_stereo = {
                "questionTitle": data['conditionReport']['sections'][5]['questions'][15]['questionTitle'],
                "selected": data['conditionReport']['sections'][5]['questions'][15]['selected'],
                "answer": data['conditionReport']['sections'][5]['questions'][15]['answer']
            }

            airbag_json_value = {
                "questionTitle": data['conditionReport']['sections'][5]['questions'][16]['questionTitle'],
                "selected": data['conditionReport']['sections'][5]['questions'][16]['selected'],
                "answer": data['conditionReport']['sections'][5]['questions'][16]['answer']
            } 

            hvac_not_working = {
                "questionTitle": data['conditionReport']['sections'][5]['questions'][17]['questionTitle'],
                "selected": data['conditionReport']['sections'][5]['questions'][17]['selected'],
                "answer": data['conditionReport']['sections'][5]['questions'][17]['answer']
            } 

            leather_seats = {
                "questionTitle": data['conditionReport']['sections'][5]['questions'][18]['questionTitle'],
                "selected": data['conditionReport']['sections'][5]['questions'][18]['selected'],
                "answer": data['conditionReport']['sections'][5]['questions'][18]['answer']
            }

            #section - 6 - Wheels & Tires

            aftermarket_wheels = {
                "questionTitle": data['conditionReport']['sections'][6]['questions'][0]['questionTitle'],
                "selected": data['conditionReport']['sections'][6]['questions'][0]['selected'],
                "answer": data['conditionReport']['sections'][6]['questions'][0]['answer']
            }

            damaged_wheels = {
                'questionTitle': data['conditionReport']['sections'][6]['questions'][1]['questionTitle'],
                'selected': data['conditionReport']['sections'][6]['questions'][1]['selected'],
                'answer': data['conditionReport']['sections'][6]['questions'][1]['answer']
            }

            oversized_tires = {
                'questionTitle': data['conditionReport']['sections'][6]['questions'][2]['questionTitle'],
                'selected': data['conditionReport']['sections'][6]['questions'][2]['selected'],
                'answer': data['conditionReport']['sections'][6]['questions'][2]['answer']
            }

            damaged_tires = {
                'questionTitle': data['conditionReport']['sections'][6]['questions'][3]['questionTitle'],
                'selected': data['conditionReport']['sections'][6]['questions'][3]['selected'],
                'answer': data['conditionReport']['sections'][6]['questions'][3]['answer']
            }

            uneven_tread_wear = {
                'questionTitle': data['conditionReport']['sections'][6]['questions'][4]['questionTitle'],
                'selected': data['conditionReport']['sections'][6]['questions'][4]['selected'],
                'answer': data['conditionReport']['sections'][6]['questions'][4]['answer']
            }

            mismatched_tires = {
                'questionTitle': data['conditionReport']['sections'][6]['questions'][5]['questionTitle'],
                'selected': data['conditionReport']['sections'][6]['questions'][5]['selected'],
                'answer': data['conditionReport']['sections'][6]['questions'][5]['answer']
            }

            missing_spare_tire = {
                'questionTitle': data['conditionReport']['sections'][6]['questions'][6]['questionTitle'],
                'selected': data['conditionReport']['sections'][6]['questions'][6]['selected'],
                'answer': data['conditionReport']['sections'][6]['questions'][6]['answer']
            }

            tire_measurements = {
                'questionTitle': data['conditionReport']['sections'][6]['questions'][7]['questionTitle'],
                'selected': data['conditionReport']['sections'][6]['questions'][7]['selected'],
                'answer': data['conditionReport']['sections'][6]['questions'][7]['answer']
            }
            
            # section - 7 - Title & History

            title_absent = {
                'questionTitle': data['conditionReport']['sections'][7]['questions'][0]['questionTitle'],
                'selected': data['conditionReport']['sections'][7]['questions'][0]['selected'],
                'answer': data['conditionReport']['sections'][7]['questions'][0]['answer']
            }
        
            title_branded = {
                'questionTitle': data['conditionReport']['sections'][7]['questions'][1]['questionTitle'],
                'selected': data['conditionReport']['sections'][7]['questions'][1]['selected'],
                'answer': data['conditionReport']['sections'][7]['questions'][1]['answer']
            }
           
            true_mileage_unknown = {
                'questionTitle': data['conditionReport']['sections'][7]['questions'][2]['questionTitle'],
                'selected': data['conditionReport']['sections'][7]['questions'][2]['selected'],
                'answer': data['conditionReport']['sections'][7]['questions'][2]['answer']
            }
        
            flood_damage = {
                'questionTitle': data['conditionReport']['sections'][7]['questions'][3]['questionTitle'],
                'selected': data['conditionReport']['sections'][7]['questions'][3]['selected'],
                'answer': data['conditionReport']['sections'][7]['questions'][3]['answer']
            }

            repair_order_attached = {
                'questionTitle': data['conditionReport']['sections'][7]['questions'][4]['questionTitle'],
                'selected': data['conditionReport']['sections'][7]['questions'][4]['selected'],
                'answer': data['conditionReport']['sections'][7]['questions'][4]['answer']
            }
    
            # off_lease_vehicle = {
            #     'questionTitle': data['conditionReport']['sections'][7]['questions'][4]['questionTitle'],
            #     'selected': data['conditionReport']['sections'][7]['questions'][4]['selected'],
            #     'answer': data['conditionReport']['sections'][7]['questions'][4]['answer']
            # }

            repossession = {
                'questionTitle': data['conditionReport']['sections'][7]['questions'][5]['questionTitle'],
                'selected': data['conditionReport']['sections'][7]['questions'][5]['selected'],
                'answer': data['conditionReport']['sections'][7]['questions'][5]['answer']
            }
            
            repossession_papers_wo_title = {
                'questionTitle': data['conditionReport']['sections'][7]['questions'][6]['questionTitle'],
                'selected': data['conditionReport']['sections'][7]['questions'][6]['selected'],
                'answer': data['conditionReport']['sections'][7]['questions'][6]['answer']
            }
            
            mobility = {
                'questionTitle': data['conditionReport']['sections'][7]['questions'][7]['questionTitle'],
                'selected': data['conditionReport']['sections'][7]['questions'][7]['selected'],
                'answer': data['conditionReport']['sections'][7]['questions'][7]['answer']
            }

            transferrable_registration = {
                "questionTitle": data['conditionReport']['sections'][7]['questions'][8]['questionTitle'],
                "selected": data['conditionReport']['sections'][7]['questions'][8]['selected'],
                "answer": data['conditionReport']['sections'][7]['questions'][8]['answer']
            }

            sold_on_bill_of_sale = {
                "questionTitle": data['conditionReport']['sections'][7]['questions'][9]['questionTitle'],
                "selected": data['conditionReport']['sections'][7]['questions'][9]['selected'],
                "answer": data['conditionReport']['sections'][7]['questions'][9]['answer']
            }

            airbag_json_string = json.dumps(airbag_json_value)
            vehicle_json_string = json.dumps(vehicle_inop)
            engine_does_not_crank_json_string = json.dumps(engine_does_not_crank)
            engine_does_not_start_json_string = json.dumps(engine_does_not_start)
            penetrating_rust_json_string = json.dumps(penetrating_rust)
            unbody_damage_json_string = json.dumps(frame_damage)
            engine_noise_json_string = json.dumps(engine_noise)
            engine_hesitation_json_string = json.dumps(engine_hesitation)
            timing_chain_issue_json_string = json.dumps(timing_chain_issue)
            abnormal_exhaust_smoke_json_string = json.dumps(abnormal_exhaust_smoke)
            head_gasket_issue_json_string = json.dumps(head_gasket_issue)
            drivetrain_issue_json_string = json.dumps(drivetrain_issue)
            transmission_issue_json_string = json.dumps(transmission_issue)
            minor_body_type_json_string = json.dumps(minor_body_type)
            moderate_body_type_json_string = json.dumps(moderate_body_type)
            major_body_type_json_string = json.dumps(major_body_type)
            glass_damage_json_string = json.dumps(glass_damage)
            lights_damage_json_string = json.dumps(lights_damage)
            aftermarket_parts_exterior_json_string = json.dumps(aftermarket_parts_exterior)
            poor_quality_repairs_json_string = json.dumps(poor_quality_repairs)
            surface_rust_json_string = json.dumps(surface_rust)
            heavy_rust_json_string = json.dumps(heavy_rust)
            obdii_codes_json_string = json.dumps(obdii_codes)   
            incomplete_readiness_monitors_json_string = json.dumps(incomplete_readiness_monitors)
            seat_damage_json_string = json.dumps(seat_damage)
            dashboard_damage_json_string = json.dumps(dashboard_damage)
            interior_trim_damage_json_string = json.dumps(interior_trim_damage)
            electronics_issue_json_string = json.dumps(electronics_issue)
            break_issue_json_string = json.dumps(break_issue)
            suspension_issue_json_string = json.dumps(suspension_issue)
            steering_issue_json_string = json.dumps(steering_issue)
            aftermarket_wheels_json_string = json.dumps(aftermarket_wheels)
            damaged_wheels_json_string = json.dumps(damaged_wheels)
            damaged_tiles_json_string = json.dumps(damaged_tires)
            tire_measurements_json_string = json.dumps(tire_measurements)
            aftermarket_mechanical_json_string = json.dumps(aftermarket_mechanical)
            engine_accessory_issue_json_string = json.dumps(engine_accessory_issue)
            title_absent_json_string = json.dumps(title_absent)
            title_branded_json_string = json.dumps(title_branded)
            modrate_body_rust_json_string = json.dumps(modrate_body_rust)
            flood_damage_json_string = json.dumps(flood_damage)
            scratches_json_string = json.dumps("")
            hail_damage_json_string = json.dumps(hail_damage)
            mismatched_paint_json_string = json.dumps("")
            paint_meter_readings_json_string = json.dumps(paint_meter_readings)
            previous_paint_work_json_string = json.dumps(previous_paint_work)
            major_body_rust_json_string = json.dumps("")
            minor_body_rust_json_string = json.dumps("")
            jump_start_required_json_string = json.dumps(jump_start_required)
            oil_intermix_dipstick_v2_json_string = json.dumps(oil_intermix_dipstick_v2)
            fluid_leaks_json_string = json.dumps(fluid_leaks)
            emissions_modifications_json_string = json.dumps(emissions_modifications)
            catalytic_converters_missing_json_string = json.dumps(catalytic_converters_missing)
            exhaust_modifications_json_string = json.dumps(exhaust_modifications)
            exhaust_noise_json_string = json.dumps(exhaust_noise)
            suspension_modifications_json_string = json.dumps(suspension_modifications)
            engine_does_not_stay_running_json_string = json.dumps(engine_does_not_stay_running)
            check_engine_light_json_string = json.dumps(check_engine_light)
            airbag_light_json_string = json.dumps(airbag_light)
            brake_light_json_string = json.dumps(brake_light)
            traction_control_light_json_string = json.dumps(traction_control_light)
            tpms_light_json_string = json.dumps(tpms_light)
            battery_light_json_string = json.dumps(battery_light)
            other_warning_light_json_string = json.dumps(other_warning_light)
            oversized_tires_json_string = json.dumps(oversized_tires)
            uneven_tread_wear_json_string = json.dumps(uneven_tread_wear)
            mismatched_tires_json_string = json.dumps(mismatched_tires)
            missing_spare_tire_json_string = json.dumps(missing_spare_tire)
            carpet_damage = json.dumps(carpet_damage)
            headliner_damage = json.dumps(headliner_damage)
            interior_order = json.dumps(interior_order)
            crank_windows = json.dumps(crank_windows)
            no_factory_ac = json.dumps(no_factory_ac)
            five_digit_odometer = json.dumps(five_digit_odometer)
            sunroof = json.dumps(sunroof)
            navigation = json.dumps(navigation)
            aftermarket_stereo = json.dumps(aftermarket_stereo)
            hvac_not_working = json.dumps(hvac_not_working)
            leather_seats = json.dumps(leather_seats)
            true_mileage_unknown = json.dumps(true_mileage_unknown) 
            off_lease_vehicle = json.dumps("")
            repair_order_attached = json.dumps(repair_order_attached)
            repossession = json.dumps(repossession)
            repossession_papers_wo_title = json.dumps(repossession_papers_wo_title)
            mobility = json.dumps(mobility)
            transferrable_registration = json.dumps(transferrable_registration)
            sold_on_bill_of_sale = json.dumps(sold_on_bill_of_sale)
            aftermarket_sunroof = json.dumps(aftermarket_sunroof)
            backup_camera = json.dumps(backup_camera)
            charging_cable = json.dumps(charging_cable)
            engine_overheats = json.dumps(engine_overheats)
            supercharger_issue = json.dumps(supercharger_issue)
            emissions_issue = json.dumps(emissions_issue)
            oil_level_issue = json.dumps(oil_level_issue)
            oil_condition_issue = json.dumps(oil_condition_issue)
            coolant_level_issue = json.dumps(coolant_level_issue)
            undercarriage_surface_rust_string = json.dumps(undercarriage_surface_rust)
            undercarriage_heavy_rust_string = json.dumps(undercarriage_heavy_rust)
            undercarriage_heavy_rot_string = json.dumps(undercarriage_heavy_rot)


            if fetchone is None:
                print('Inserting condition report')
                cursor.execute('INSERT into live_auction_condition_report (auction_id, air_bag, vehicle_inop, engine_does_not_start, engine_does_not_crank, penetrating_rust,frame_damage,engine_noise,engine_hesitation,timing_chain_issue,abnormal_exhaust_smoke,head_gasket_issue,drivetrain_issue,transmission_issue,minor_body_type,moderate_body_type,major_body_type,glass_damage,lights_damage,aftermarket_parts_exterior,poor_quality_repairs,surface_rust,heavy_rust,obdii_codes,incomplete_readiness_monitors,seat_damage,dashboard_damage,interior_trim_damage,electronics_issue,break_issue,suspension_issue,steering_issue,aftermarket_wheels,damaged_wheels,damaged_tiles,tire_measurements,aftermarket_mechanical,engine_accessory_issue,title_absent,title_branded,modrate_body_rust,flood_damage,scratches, minor_body_rust, major_body_rust, hail_damage, mismatched_paint, paint_meter_readings, previous_paint_work, jump_start_required,oil_intermix_dipstick_v2,fluid_leaks,emissions_modifications,catalytic_converters_missing,exhaust_modifications,exhaust_noise,suspension_modifications,engine_does_not_stay_running,check_engine_light,airbag_light,brake_light,traction_control_light,tpms_light,battery_light,other_warning_light,oversized_tires,uneven_tread_wear,mismatched_tires,missing_spare_tire, carpet_damage, headliner_damage, interior_order, crank_windows, no_factory_ac,five_digit_odometer, sunroof, navigation, aftermarket_stereo, hvac_not_working, leather_seats, true_mileage_unknown,off_lease_vehicle,repair_order_attached, repossession, repossession_papers_wo_title, mobility, transferrable_registration, sold_on_bill_of_sale,aftermarket_sunroof,backup_camera,charging_cable,engine_overheats,supercharger_issue, emissions_issue, oil_level_issue, oil_condition_issue, coolant_level_issue,undercarriage_surface_rust, undercarriage_heavy_rust, undercarriage_heavy_rot) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (data['id'],airbag_json_string,vehicle_json_string,engine_does_not_start_json_string,engine_does_not_crank_json_string,penetrating_rust_json_string,unbody_damage_json_string,engine_noise_json_string,engine_hesitation_json_string,timing_chain_issue_json_string,abnormal_exhaust_smoke_json_string,head_gasket_issue_json_string,drivetrain_issue_json_string,transmission_issue_json_string,minor_body_type_json_string,moderate_body_type_json_string,major_body_type_json_string,glass_damage_json_string,lights_damage_json_string,aftermarket_parts_exterior_json_string,poor_quality_repairs_json_string,surface_rust_json_string,heavy_rust_json_string,obdii_codes_json_string,incomplete_readiness_monitors_json_string,seat_damage_json_string,dashboard_damage_json_string,interior_trim_damage_json_string,electronics_issue_json_string,break_issue_json_string,suspension_issue_json_string,steering_issue_json_string,aftermarket_wheels_json_string,damaged_wheels_json_string,damaged_tiles_json_string,tire_measurements_json_string,aftermarket_mechanical_json_string,engine_accessory_issue_json_string,title_absent_json_string,title_branded_json_string,modrate_body_rust_json_string,flood_damage_json_string,scratches_json_string, minor_body_rust_json_string, major_body_rust_json_string, hail_damage_json_string, mismatched_paint_json_string, paint_meter_readings_json_string, previous_paint_work_json_string, jump_start_required_json_string,oil_intermix_dipstick_v2_json_string,fluid_leaks_json_string,emissions_modifications_json_string,catalytic_converters_missing_json_string,exhaust_modifications_json_string,exhaust_noise_json_string,suspension_modifications_json_string,engine_does_not_stay_running_json_string,check_engine_light_json_string,airbag_light_json_string,brake_light_json_string,traction_control_light_json_string,tpms_light_json_string,battery_light_json_string,other_warning_light_json_string,oversized_tires_json_string,uneven_tread_wear_json_string,mismatched_tires_json_string,missing_spare_tire_json_string, carpet_damage, headliner_damage, interior_order, crank_windows, no_factory_ac,five_digit_odometer, sunroof, navigation, aftermarket_stereo, hvac_not_working, leather_seats,true_mileage_unknown,off_lease_vehicle,repair_order_attached, repossession, repossession_papers_wo_title, mobility,transferrable_registration,sold_on_bill_of_sale,aftermarket_sunroof,backup_camera,charging_cable,engine_overheats,supercharger_issue, emissions_issue, oil_level_issue, oil_condition_issue, coolant_level_issue, undercarriage_surface_rust_string, undercarriage_heavy_rust_string, undercarriage_heavy_rot_string))
            else:
                print('Updating condition report')
                cursor.execute('UPDATE live_auction_condition_report SET air_bag = %s, vehicle_inop = %s, engine_does_not_start = %s, engine_does_not_crank = %s, penetrating_rust = %s,frame_damage = %s, engine_noise = %s, engine_hesitation = %s, timing_chain_issue = %s, abnormal_exhaust_smoke = %s, head_gasket_issue = %s,	drivetrain_issue = %s, transmission_issue =%s, minor_body_type = %s, moderate_body_type = %s, major_body_type = %s, glass_damage = %s, lights_damage = %s, aftermarket_parts_exterior = %s, poor_quality_repairs = %s, surface_rust = %s, heavy_rust = %s, obdii_codes = %s, incomplete_readiness_monitors = %s, seat_damage = %s, dashboard_damage = %s, interior_trim_damage = %s, electronics_issue =%s, break_issue =%s, suspension_issue = %s, steering_issue = %s, aftermarket_wheels = %s, damaged_wheels = %s,  damaged_tiles = %s, tire_measurements = %s, aftermarket_mechanical = %s, engine_accessory_issue = %s, title_absent = %s, title_branded = %s, modrate_body_rust = %s, flood_damage = %s, scratches = %s, minor_body_rust = %s, major_body_rust = %s, hail_damage = %s, mismatched_paint = %s, paint_meter_readings = %s, previous_paint_work = %s, jump_start_required = %s, oil_intermix_dipstick_v2 = %s, fluid_leaks = %s, emissions_modifications = %s, catalytic_converters_missing = %s, exhaust_modifications = %s, exhaust_noise = %s, suspension_modifications = %s, engine_does_not_stay_running = %s, check_engine_light = %s, airbag_light = %s, brake_light = %s, traction_control_light = %s, 	tpms_light = %s, battery_light = %s, other_warning_light = %s, oversized_tires = %s, uneven_tread_wear = %s, mismatched_tires = %s, missing_spare_tire = %s, carpet_damage = %s, headliner_damage = %s, interior_order = %s, crank_windows = %s, no_factory_ac = %s, five_digit_odometer = %s, sunroof = %s, navigation = %s, aftermarket_stereo = %s, hvac_not_working = %s,leather_seats = %s, true_mileage_unknown = %s, off_lease_vehicle = %s, repair_order_attached = %s, repossession = %s, repossession_papers_wo_title = %s, mobility = %s, transferrable_registration = %s, sold_on_bill_of_sale = %s, aftermarket_sunroof = %s, backup_camera = %s, charging_cable = %s, engine_overheats = %s, supercharger_issue = %s, emissions_issue = %s, oil_level_issue = %s, oil_condition_issue = %s, coolant_level_issue = %s, undercarriage_surface_rust = %s, undercarriage_heavy_rust = %s, undercarriage_heavy_rot = %s where auction_id = %s', (airbag_json_string,vehicle_json_string,engine_does_not_start_json_string,engine_does_not_crank_json_string,penetrating_rust_json_string,unbody_damage_json_string,engine_noise_json_string,engine_hesitation_json_string,timing_chain_issue_json_string, abnormal_exhaust_smoke_json_string, head_gasket_issue_json_string,drivetrain_issue_json_string,transmission_issue_json_string,minor_body_type_json_string,moderate_body_type_json_string,major_body_type_json_string,glass_damage_json_string,lights_damage_json_string,aftermarket_parts_exterior_json_string,poor_quality_repairs_json_string,surface_rust_json_string,heavy_rust_json_string,obdii_codes_json_string,incomplete_readiness_monitors_json_string,seat_damage_json_string,dashboard_damage_json_string,interior_trim_damage_json_string,electronics_issue_json_string,break_issue_json_string,suspension_issue_json_string,steering_issue_json_string,aftermarket_wheels_json_string,damaged_wheels_json_string,damaged_tiles_json_string,tire_measurements_json_string,aftermarket_mechanical_json_string,engine_accessory_issue_json_string,title_absent_json_string,title_branded_json_string,modrate_body_rust_json_string,flood_damage_json_string,scratches_json_string, minor_body_rust_json_string, major_body_rust_json_string, hail_damage_json_string, mismatched_paint_json_string, paint_meter_readings_json_string, previous_paint_work_json_string,jump_start_required_json_string,oil_intermix_dipstick_v2_json_string,fluid_leaks_json_string,emissions_modifications_json_string,catalytic_converters_missing_json_string,exhaust_modifications_json_string,exhaust_noise_json_string,suspension_modifications_json_string,engine_does_not_stay_running_json_string,check_engine_light_json_string,airbag_light_json_string,brake_light_json_string,traction_control_light_json_string,tpms_light_json_string,battery_light_json_string,other_warning_light_json_string,oversized_tires_json_string,uneven_tread_wear_json_string,mismatched_tires_json_string,missing_spare_tire_json_string, carpet_damage, headliner_damage, interior_order, crank_windows, no_factory_ac,five_digit_odometer, sunroof, navigation, aftermarket_stereo, hvac_not_working, leather_seats, true_mileage_unknown, off_lease_vehicle,repair_order_attached, repossession, repossession_papers_wo_title, mobility, transferrable_registration, sold_on_bill_of_sale, aftermarket_sunroof, backup_camera, charging_cable, engine_overheats, supercharger_issue, emissions_issue, oil_level_issue, oil_condition_issue, coolant_level_issue, undercarriage_surface_rust_string, undercarriage_heavy_rust_string, undercarriage_heavy_rot_string, data['id']))
            con.commit()
            return True
        except:
            return ()
        finally:
            con.close()
    
    def livecountslights(self, auctions):
        con = ACV.connect(self)
        cursor = con.cursor()
        try:
            cursor.execute('SELECT flood_damage, transferrable_registration, sold_on_bill_of_sale, major_body_type, penetrating_rust,	engine_does_not_crank, vehicle_inop, head_gasket_issue, engine_does_not_start, engine_overheats, timing_chain_issue, engine_noise, oil_intermix_dipstick_v2, supercharger_issue, transmission_issue, drivetrain_issue, steering_issue, break_issue, abnormal_exhaust_smoke, engine_hesitation, engine_does_not_stay_running, heavy_rust, modrate_body_rust, moderate_body_type, surface_rust, poor_quality_repairs, hail_damage, catalytic_converters_missing, battery_light, title_branded, title_absent, true_mileage_unknown, frame_damage, repossession, repossession_papers_wo_title, repair_order_attached, mobility, air_bag, undercarriage_heavy_rust, minor_body_type, undercarriage_surface_rust FROM live_auction_condition_report WHERE auction_id = %s', (auctions,))
            condition_reports = cursor.fetchall()
            yellow = 0
            orange = 0
            red = 0
            blue = 0
            
            for condition_report in condition_reports:
                flood_damage_data = json.loads(condition_report[0]) 
                transferrable_registration_data = json.loads(condition_report[1])
                sold_on_bill_of_sale_data = json.loads(condition_report[2])
                major_body_type_data = json.loads(condition_report[3])
                penetrating_rust_data = json.loads(condition_report[4])
                engine_does_not_crank_data = json.loads(condition_report[5])
                vehicle_inop_data = json.loads(condition_report[6])
                head_gasket_issue_data = json.loads(condition_report[7])
                engine_does_not_start_data = json.loads(condition_report[8])
                engine_overheats_data = json.loads(condition_report[9])
                timing_chain_issue_data = json.loads(condition_report[10])
                engine_noise_data = json.loads(condition_report[11])
                oil_intermix_dipstick_v2_data = json.loads(condition_report[12])
                supercharger_issue_data = json.loads(condition_report[13])
                transmission_issue_data = json.loads(condition_report[14])
                drivetrain_issue_data = json.loads(condition_report[15])
                steering_issue_data = json.loads(condition_report[16])
                break_issue_data = json.loads(condition_report[17])
                abnormal_exhaust_smoke_data = json.loads(condition_report[18])
                engine_hesitation_data = json.loads(condition_report[19])
                engine_does_not_stay_running_data = json.loads(condition_report[20])
                heavy_rust_data = json.loads(condition_report[21])
                modrate_body_rust_data = json.loads(condition_report[22])
                moderate_body_type_data = json.loads(condition_report[23])
                surface_rust_data = json.loads(condition_report[24])
                poor_quality_repairs_data = json.loads(condition_report[25])
                hail_damage_data = json.loads(condition_report[26])
                catalytic_converters_missing_data = json.loads(condition_report[27])
                battery_light_data = json.loads(condition_report[28])
                title_branded_data = json.loads(condition_report[29])
                title_absent_data = json.loads(condition_report[30])
                true_mileage_unknown_data = json.loads(condition_report[31])
                frame_damage_data = json.loads(condition_report[32])
                repossession_data = json.loads(condition_report[33])
                repossession_papers_wo_title_data = json.loads(condition_report[34])
                repair_order_attached_data = json.loads(condition_report[35])
                mobility_data = json.loads(condition_report[36])
                airbag_data = json.loads(condition_report[37])
                undercarriage_heavy_rust_data = json.loads(condition_report[38])
                minor_body_type_data = json.loads(condition_report[39])
                undercarriage_surface_rust = json.loads(condition_report[40])

                if sold_on_bill_of_sale_data['selected'] == True:
                    red += 1

                if title_absent_data['selected'] == True:
                    blue += 1

                if flood_damage_data['selected'] == True:  
                    orange += 1

                if transferrable_registration_data['selected'] == True:
                    orange += 1
                
                if engine_does_not_crank_data['selected'] == True:
                    orange += 1
                
                if vehicle_inop_data['selected'] == True:
                    orange += 1

                if major_body_type_data['selected'] == True:
                    orange += 1
                
                if engine_does_not_start_data['selected'] == True:
                    orange += 1

                if undercarriage_heavy_rust_data['selected'] == True:
                    orange += 1

                if moderate_body_type_data['selected'] == True:
                    orange += 1
                
                if heavy_rust_data['selected'] == True:
                    orange += 1
                
                if airbag_data['selected'] == True:
                    orange += 1

                if title_branded_data['selected'] == True:
                    orange += 1

                if penetrating_rust_data['selected'] == True:
                    yellow += 1
                
                if head_gasket_issue_data['selected'] == True:
                    yellow += 1
            
                if engine_overheats_data['selected'] == True:
                    yellow += 1
                
                if timing_chain_issue_data['selected'] == True:
                    yellow += 1

                if engine_noise_data['selected'] == True:
                    yellow += 1

                if oil_intermix_dipstick_v2_data['selected'] == True:
                    yellow += 1

                if supercharger_issue_data['selected'] == True:
                    yellow += 1

                if transmission_issue_data['selected'] == True:
                    yellow += 1

                if drivetrain_issue_data['selected'] == True:
                    yellow += 1

                if steering_issue_data['selected'] == True:
                    yellow += 1
            
                if break_issue_data['selected'] == True:
                    yellow += 1

                if abnormal_exhaust_smoke_data['selected'] == True:
                    yellow += 1

                if engine_hesitation_data['selected'] == True:
                    yellow += 1

                if engine_does_not_stay_running_data['selected'] == True:
                    yellow += 1

                if modrate_body_rust_data['selected'] == True:
                    yellow += 1

                if minor_body_type_data['selected'] == True:
                    yellow += 1

                if surface_rust_data['selected'] == True:
                    yellow += 1
                
                if undercarriage_surface_rust['selected'] == True:
                    yellow += 1

                if poor_quality_repairs_data['selected'] == True:
                    yellow += 1

                if hail_damage_data['selected'] == True:
                    yellow += 1

                if catalytic_converters_missing_data['selected'] == True:
                    yellow += 1

                if battery_light_data['selected'] == True:
                    yellow += 1

                if true_mileage_unknown_data['selected'] == True:
                    yellow += 1

                if frame_damage_data['selected'] == True:
                    yellow += 1

                if repossession_data['selected'] == True:
                    yellow += 1
                
                if repossession_papers_wo_title_data['selected'] == True:
                    yellow += 1

                if repair_order_attached_data['selected'] == True:
                    yellow += 1
                
                if mobility_data['selected'] == True:
                    yellow += 1

            color_count = {
                "red": red,
                "blue": blue,
                "orange": orange,
                "yellow": yellow,
            }

            lights_count = {color: count for color, count in color_count.items() if count > 0}

            if orange == 0 and yellow == 0 and red == 0 and blue == 0:
                lights_count = {'green': 0}

            lights_count_json = json.dumps(lights_count)
            cursor.execute('UPDATE live_auctions SET lights_counts = %s WHERE auction_id = %s', (lights_count_json, auctions))
            con.commit()
            return True
        except Exception as e:
            con.rollback()
            print(f"Error during database operation: {str(e)}")
            traceback.print_exc()
            return False
        
    def getliveauctions(self,):
        con = ACV.connect(self)
        cursor = con.cursor()
        try:        
            cursor.execute('SELECT * from live_auctions WHERE status = "active" ORDER BY action_end_datetime ASC')
         
            return cursor.fetchall()
        except:
            return ()
        finally:
            con.close() 
        
    def getlivewonauction(self,):
        con = ACV.connect(self)
        cursor = con.cursor()
        try:
            cursor.execute('SELECT * FROM live_auctions WHERE win = %s', (1,))
            return  cursor.fetchall()
        except:
            return ()
        finally:
            con.close()

    def getlivelostauction(self,):
        con = ACV.connect(self)
        cursor = con.cursor()
        try:
            cursor.execute('SELECT * FROM live_auctions WHERE lost = %s', (1,))
            return  cursor.fetchall()
        except:
            return ()
        finally:
            con.close()
    
    def getliveauctioncondition(self, id):
        con = ACV.connect(self)
        cursor = con.cursor()
        try:
            cursor.execute('SELECT * FROM live_auction_condition_report WHERE auction_id = %s', (id,))
            condition_report = cursor.fetchone()
            cursor.execute('SELECT auction_id, lights, auction_url, distance, location, vin, odometer, transmission, trim, drivetrain, engine, fuel_type, year, make, model, basic_color, action_start_datetime FROM live_auctions WHERE auction_id = %s', (id,))
            auction = cursor.fetchone()
            return condition_report, auction
        except:
            return ()
        finally:
            con.close()
        
    def getLiveUpcomingauction(self,):
        con = ACV.connect(self)
        cursor = con.cursor()
        try:
            cursor.execute('SELECT * FROM live_auctions WHERE status = "run_list" and action_start_datetime > %s',datetime.datetime.now())
            return cursor.fetchall()
        except:
            return ()
        finally:
            con.close()

    def getNotificationCount(self,):
        con = ACV.connect(self)
        cursor = con.cursor()
        try:
            cursor.execute('SELECT COUNT(id) FROM pubnub')
            result = cursor.fetchone()[0] 
            return result
        except:
            return ()
        finally:
            con.close()
            
    def getNotificationList(self,):
        con = ACV.connect(self)
        cursor = con.cursor()
        try:
            cursor.execute('SELECT * FROM pubnub')
            return cursor.fetchall()
        except:
            return ()
        finally:
            con.close()

    def get_proqoute(self,):
        con = ACV.connect(self)
        cursor = con.cursor()
        #try:    
        current_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute('SELECT * from auctions  ORDER BY action_end_datetime ASC')
        datas = cursor.fetchall()
        try:
            for auction in datas:  
                
                cursor.execute('SELECT * from makes WHERE name = %s ', (auction[2]))
                make_code_data = cursor.fetchone()
                year = auction[1]
                make_code = make_code_data[2]
                make = auction[2]
                model = auction[3]
                key = 'Y'
                zipcode = auction[8]
                mileage = auction[6]
                drive = auction[24].split(',')
                drive1 = auction[24]
                damage = auction[33]
                damage3 = auction[33]
                sdamage = auction[19].split(',')
                title = auction[21]
                airbag1=auction[16]
                fire_damage1=''
                minor_damage = auction[13]
                modrate_damage = auction[14]
                major_damage = auction[15]
                
                drive_api = 'D'
                if 'D' in drive and 'S' in drive:
                    drivable = 'Y'
                    drive_api = 'D'
                elif('D' in drive):
                    drivable = 'Y'
                    drive_api = 'D'
                elif('S' in drive):
                    drivable = 'N'
                    drive_api = 'S'
                else:
                    drivable = 'N'
                    drive_api = 'N'
    
                if(minor_damage == 0 or modrate_damage == 0 or major_damage == 0):
                    damage = 'MN'
                    damage3 = 'MN'
    
                if('No my vehicle is in good shape!' in sdamage):
                    sdamage = ''
                elif(damage =='MN'):
                    if 'Yes major engine issues' in sdamage or 'Yes major transmission issues' in sdamage or 'Yes major frame issues' in sdamage:
                        sdamage = ''
                        damage = 'MC'
                    elif 'Yes minor frame issues' in sdamage:
                        sdamage = ''
                        damage = 'UN'
                    else:
                        sdamage = ''
                        damage = damage
                elif(damage!='MN'):
                    if 'Yes major engine issues' in sdamage or 'Yes major transmission issues' in sdamage or 'Yes major frame issues' in sdamage:
                        sdamage = 'MC'
                        damage = damage
                    elif 'Yes minor frame issues' in sdamage:
                        sdamage = 'UN'
                        damage = damage
                    else:
                        sdamage = ''
                        damage = damage
                else:
                    sdamage = ''
                    damage = damage
                # print(year,'year')
                # print(make_code,'make_code')
                # print(make,'make')
                # print(model,'model')
                # print(key,'key')
                # print(zipcode,'zipcode')
                # print(mileage,'mileage')
                # print(drive_api)
                # print(drivable)
                # print(damage,'damage')
                # print(damage3,'damage3')
                # print(sdamage,'sdamage')
                # print(title,'title')
                # print(airbag1,'airbag1')
                # print(fire_damage1,'fire_damage1')
                # print(minor_damage,'minor_damage')
                # print(modrate_damage,'modrate_damage')
                # print(major_damage,'major_damage')
                # print('nigs1')
                conn = http.client.HTTPSConnection("auth.copart.com")
                payload = ''
                headers = {
                    'Authorization': 'Basic YjJiLXlvdXJjYXJpbnRvY2FzaDo0MTdkMWY2OWZmNjM0MDc4YTI0MTRjMDhkNWNkZGVjOA==',
                    'Cookie': 'copartgauth=185cbe798bb427e3d0276f91261db760; incap_ses_50_844960=OpBmB366tjd+6gze1aKxAE1LiGQAAAAAzK+zaIhr8T48Zo3u9/ucRQ==; visid_incap_844960=TW7QmGE7QnG55BxXNbhyS0xLiGQAAAAAQUIPAAAAAAC14p7orETuJ/gzWe9x+g6p'
                }
                conn.request("POST", "/employee/oauth/token?grant_type=client_credentials", payload, headers)
                res = conn.getresponse()
                data = res.read()
                users = json.loads(data)            
                access_token = 'Bearer '+users['access_token']
                conn = http.client.HTTPSConnection("b2b.copart.com")
                print(damage,'damage')
                print(sdamage,'sdamage')

                #print(title)
                
                if(title=='Unknown,Salvage Rebuilt'):
                    title = 'Salvage Rebuilt'

                if(title=="clean title,Salvage Rebuilt"):
                    title = 'Salvage Rebuilt'
                    
                if(damage=='FR,RR,SD,TP'):
                    damage = 'AO'
                payload = json.dumps({
                    "transactionId": "15397310-0A0A-02AB-07F6-BA0F90581893",
                    "adminInfo": {
                        "sellerCompanyCode": "TWIN",
                        "officeCode": "WCQ7"
                    },
                    "vehicleLocationSite": {
                        "address": {
                            "contact": {
                            "postalCode": zipcode
                            }
                        }
                    },
                    "claimNumber": "",
                    "lossInfo": {
                        "primaryPointOfImpact": damage,
                        "secondaryPointOfImpact" : sdamage,
                        "damageSeverity": "L"
                    },
                    "vehicleInformation": {
                        "year": year,
                        "makeCode": make_code,
                        "makeDescription": make,
                        "model": model,
                        "vehicleType": "V", 
                        "odometerInfo": {    
                            "odometerReading" : mileage, 
                            "odometerBrand": "Actual" 
                        }, 
                        "hasKeys": key
                    },
                    "valuation": {
                        "acv": 5000,
                        "repairCost": 200
                    },
                    "vehicleCondition": {
                        "drivable": drivable,
                        "drivabilityRating": drive_api,
                        "titleCategory": title 
                    }
                })
                
                headers = {
                    'countryCode': 'USA',
                    'Content-Type': 'application/json',
                    'Authorization': access_token,
                    'insco':'YCIC',
                }
                
                #print(payload,'payload')
                
                conn.request("POST", "/v1/proquote", payload, headers)
                res = conn.getresponse()
                data = res.read()
                data = json.loads(data)
                print(data)
                proQuote_data = data['proQuote']
                proQuote = float(proQuote_data)
                proQuoteo = proQuote
                
                
                cursor.execute("SELECT * FROM setting where id = %s ", (1,))
                data_of_setting = cursor.fetchone()
                minPrice = ''
                maxPrice = ''
                perPrice = ''
                
                if(float(proQuote) <= data_of_setting[3]):
                    p1 = data_of_setting[1]
                    proqoute = float((proQuote*p1)/100)
                    minPrice = '0'
                    maxPrice = data_of_setting[3]
                    perPrice = p1
                elif(float(proQuote) >= data_of_setting[5] and float(proQuote) <= data_of_setting[6]):
                    p2 = data_of_setting[4]
                    proqoute = float((proQuote*p2)/100)
                    minPrice = data_of_setting[5]
                    maxPrice = data_of_setting[6]
                    perPrice = p2
                elif(float(proQuote) >= data_of_setting[8] and float(proQuote) <= data_of_setting[9]):
                    p3 = data_of_setting[7]
                    proqoute = float((proQuote*p3)/100)
                    minPrice = data_of_setting[8]
                    maxPrice = data_of_setting[9]
                    perPrice = p3
                elif(float(proQuote) >= data_of_setting[11] and float(proQuote) <= data_of_setting[12]):
                    p3 = data_of_setting[10]
                    proqoute = float((proQuote*p3)/100)
                    minPrice = data_of_setting[11]
                    maxPrice = data_of_setting[12]
                    perPrice = p3
                elif(float(proQuote) >= data_of_setting[14] and float(proQuote) <= data_of_setting[15]):
                    p3 = data_of_setting[13]
                    proqoute = float((proQuote*p3)/100)
                    minPrice = data_of_setting[14]
                    maxPrice = data_of_setting[15]
                    perPrice = p3
                else:
                    p4 = data_of_setting[16]
                    proqoute = float((proQuote*p4)/100)
                    minPrice = data_of_setting[17]
                    maxPrice = 'Above'
                    perPrice = p4
                    
                if mileage=='000':
                    mileage = ''
                    
                mileage = str(mileage)
                zipcode = str(zipcode)
                year = str(year)
                utv = ''
                unable_to_verify_data = ''
                if unable_to_verify_data!='':
                    if mileage =='':
                        query="SELECT * FROM condition_report where is_deleted='no' and FIND_IN_SET('"+make+"', make_name) and FIND_IN_SET('"+model+"', model_name) and min_year <="+year+" and max_year >="+year+" and  unable_to_verify='yes' and FIND_IN_SET('"+zipcode+"', final_zip) and FIND_IN_SET('"+damage3+"', damageComma) and FIND_IN_SET('"+airbag1+"', airbagComma) and FIND_IN_SET('"+drive_api+"', driveComma) and FIND_IN_SET('"+key+"', keyComma) and FIND_IN_SET('"+title+"', titleComma) and FIND_IN_SET('"+fire_damage1+"', firDamageComma) UNION SELECT * FROM condition_report where  (FIND_IN_SET('"+make+"', make_name) AND FIND_IN_SET('"+model+"', model_name) OR (FIND_IN_SET('all', make_name) AND FIND_IN_SET('all', model_name) ))  AND ((min_year <= "+year+" AND max_year >= "+year+") OR  (min_year = '' AND max_year = '')) AND unable_to_verify='yes' AND FIND_IN_SET('"+zipcode+"', final_zip) AND  ((FIND_IN_SET('"+damage3+"', damageComma)  OR  damageComma = '')) AND ((FIND_IN_SET('"+airbag1+"', airbagComma)  OR airbagComma = '')) AND ((FIND_IN_SET('"+drive_api+"', driveComma)    OR driveComma = '')) AND ((FIND_IN_SET('"+key+"', keyComma)   OR keyComma = '')) AND ((FIND_IN_SET('"+title+"', titleComma)  OR titleComma = '')) AND ((FIND_IN_SET('"+fire_damage1+"', firDamageComma)  OR firDamageComma = '')) AND is_deleted='no' order by not_to_exceed desc" 
                        cursor.execute(query)
                        condition1 = cursor.fetchall() 
                        #print(query)
                        #print("in")
                    else:
                        query="SELECT * FROM condition_report where is_deleted='no' and FIND_IN_SET('"+make+"', make_name) and FIND_IN_SET('"+model+"', model_name) and min_year <="+year+" and max_year >="+year+" and  unable_to_verify='yes' and FIND_IN_SET('"+zipcode+"', final_zip)  and FIND_IN_SET('"+damage3+"', damageComma) and FIND_IN_SET('"+airbag1+"', airbagComma) and FIND_IN_SET('"+drive_api+"', driveComma) and FIND_IN_SET('"+key+"', keyComma) and FIND_IN_SET('"+title+"', titleComma) and FIND_IN_SET('"+fire_damage1+"', firDamageComma) UNION SELECT * FROM condition_report where  (FIND_IN_SET('"+make+"', make_name) AND FIND_IN_SET('"+model+"', model_name) OR (FIND_IN_SET('all', make_name) AND FIND_IN_SET('all', model_name)))   AND ((min_year <= "+year+" AND max_year >= "+year+") OR  (min_year = '' AND max_year = '')) AND (unable_to_verify='yes') AND FIND_IN_SET('"+zipcode+"', final_zip) AND  ((FIND_IN_SET('"+damage3+"', damageComma)  OR  damageComma = '')) AND ((FIND_IN_SET('"+airbag1+"', airbagComma)  OR airbagComma = '')) AND ((FIND_IN_SET('"+drive_api+"', driveComma) OR driveComma = '')) AND ((FIND_IN_SET('"+key+"', keyComma) OR keyComma = '')) AND ((FIND_IN_SET('"+title+"', titleComma)  OR titleComma = '')) AND ((FIND_IN_SET('"+fire_damage1+"', firDamageComma)  OR firDamageComma = '')) AND is_deleted='no' order by not_to_exceed desc" 
                        cursor.execute(query)
                        condition1 = cursor.fetchall()
                        #print(query)
                        #print("out")
                else:
                    if mileage =='':
                        query="SELECT * FROM condition_report where is_deleted='no' and FIND_IN_SET('"+make+"', make_name) and FIND_IN_SET('"+model+"', model_name) and min_year <="+year+" and max_year >="+year+" and unable_to_verify='no' and FIND_IN_SET('"+zipcode+"', final_zip) and FIND_IN_SET('"+damage3+"', damageComma) and FIND_IN_SET('"+airbag1+"', airbagComma) and FIND_IN_SET('"+drive_api+"', driveComma) and FIND_IN_SET('"+key+"', keyComma) and FIND_IN_SET('"+title+"', titleComma) and FIND_IN_SET('"+fire_damage1+"', firDamageComma) UNION SELECT * FROM condition_report where  (FIND_IN_SET('"+make+"', make_name) AND FIND_IN_SET('"+model+"', model_name) OR (FIND_IN_SET('all', make_name) AND FIND_IN_SET('all', model_name) ))  AND ((min_year <= "+year+" AND max_year >= "+year+") OR  (min_year = '' AND max_year = ''))  AND FIND_IN_SET('"+zipcode+"', final_zip) AND  ((FIND_IN_SET('"+damage3+"', damageComma)  OR  damageComma = '')) AND ((FIND_IN_SET('"+airbag1+"', airbagComma)  OR airbagComma = '')) AND ((FIND_IN_SET('"+drive_api+"', driveComma)    OR driveComma = '')) AND ((FIND_IN_SET('"+key+"', keyComma)   OR keyComma = '')) AND ((FIND_IN_SET('"+title+"', titleComma)  OR titleComma = '')) AND ((FIND_IN_SET('"+fire_damage1+"', firDamageComma)  OR firDamageComma = '')) AND unable_to_verify='no' AND is_deleted='no' order by not_to_exceed desc" 
                        #print(query)
                        #print("in")
                        cursor.execute(query)
                        condition1 = cursor.fetchall() 
                    else:
                        query="SELECT * FROM condition_report where is_deleted='no' and FIND_IN_SET('"+make+"', make_name) and FIND_IN_SET('"+model+"', model_name) and min_year <="+year+" and max_year >="+year+" and FIND_IN_SET('"+zipcode+"', final_zip) and min_mileage<="+mileage+" and max_mileage >="+mileage+" and FIND_IN_SET('"+damage3+"', damageComma) and FIND_IN_SET('"+airbag1+"', airbagComma) and FIND_IN_SET('"+drive_api+"', driveComma) and FIND_IN_SET('"+key+"', keyComma) and FIND_IN_SET('"+title+"', titleComma) and FIND_IN_SET('"+fire_damage1+"', firDamageComma) UNION SELECT * FROM condition_report where  (FIND_IN_SET('"+make+"', make_name) AND FIND_IN_SET('"+model+"', model_name) OR (FIND_IN_SET('all', make_name) AND FIND_IN_SET('all', model_name)))   AND ((min_year <= "+year+" AND max_year >= "+year+") OR  (min_year = '' AND max_year = '')) AND ((max_mileage >= "+mileage+" AND  min_mileage <= "+mileage+") OR (max_mileage ='' AND min_mileage = '')) AND FIND_IN_SET('"+zipcode+"', final_zip) AND  ((FIND_IN_SET('"+damage3+"', damageComma)  OR  damageComma = '')) AND ((FIND_IN_SET('"+airbag1+"', airbagComma)  OR airbagComma = '')) AND ((FIND_IN_SET('"+drive_api+"', driveComma) OR driveComma = '')) AND ((FIND_IN_SET('"+key+"', keyComma) OR keyComma = '')) AND ((FIND_IN_SET('"+title+"', titleComma)  OR titleComma = '')) AND ((FIND_IN_SET('"+fire_damage1+"', firDamageComma)  OR firDamageComma = '')) AND is_deleted='no' order by not_to_exceed desc" 
                        #print(query)
                        #print("out")
                        cursor.execute(query)
                        condition1 = cursor.fetchall()
                        
                con_amt = ''
                con_type = ''
                con_plus = ''
                con_per = ''
                con_per_amt = ''
                not_to_exceed = ''
                fetch_type1 = 'copart'
                fet_confition_id1 = ''
                condition_title1 = ''
                record_id = '55'
                
                myArray = []
                
                myArray.append({
    	            'con_amt': proqoute,
    	            'con_type': con_type,
    	            'con_plus': con_plus,
    	            'con_per': con_per,
    	            'con_per_amt': con_per_amt,
    	            'not_to_exceed': not_to_exceed,
    	            'record_id': record_id,
    	            'proqoute': proqoute,
    	            'fetch_type1' : fetch_type1,
    	            'fet_confition_id1': fet_confition_id1,
    	            'condition_title1': condition_title1,
    	          })
                        
                for k1 in condition1:
                    fetch_type1 = 'condition report'
                    fet_confition_id1 = k1[0]
                    condition_title1 = k1[1]
                    if(k1[19]=="Fixed Amount"):
                        proqoute = float(k1[24])
                        con_type = 'Fixed Amount'
                        con_amt = k1[24]
                        not_to_exceed = k1[23]
                        record_id = record_id
                    else:
                        con_type = 'Proquote Estimate'
                        if(k1[20]=='minus'):
                            con_plus = '-'
                            if(k1[21]=='percentage'):
                                con_per = '%'
                                per1 = float((proQuote*k1[22])/100)
                                total1 = float(proQuote) - per1
                                if(k1[23]>total1):
                                    proqoute = total1
                                else:
                                    proqoute = float(k1[23])
                                con_per_amt = k1[22]
                            else:
                                con_per = '$'
                                per1 = k1[22]
                                total1 = float(proQuote) - float(per1)
                                if(k1[23]>total1):
                                    proqoute = total1;
                                else:
                                    proqoute = float(k1[23])
                                con_per_amt = per1;
                        else:
                            con_plus = '+'
                            if(k1[21]=='percentage'):
                                con_per = '%'
                                per1 = float((proQuote*k1[22])/100)
                                total1 = float(proQuote) + per1
                                if(k1[23]>total1):
                                    proqoute = total1
                                else:
                                    proqoute = float(k1[23])
                                con_per_amt = k1[22]
                            else:
                                con_per = '$'
                                per1 = k1[22]
                                total1 = float(proQuote) + float(per1);
                                if(k1[23]>total1):
                                    roqoute = total1
                                else:
                                    proqoute = float(k1[23])
                                con_per_amt = per1
                        con_amt = proqoute
                        not_to_exceed = k1[23]
                        record_id = record_id
                    myArray.append({
                        'con_amt': float(con_amt),
                        'con_type': con_type,
                        'con_plus': con_plus,
                        'con_per': con_per,
                        'con_per_amt': con_per_amt,
                        'not_to_exceed': not_to_exceed,
                        'record_id': record_id,
                        'proqoute': proqoute,
                        'fetch_type1' : fetch_type1,
                        'fet_confition_id1': fet_confition_id1,
                        'condition_title1': condition_title1,
                    })
                myArray.sort(key=lambda x: x['con_amt'], reverse=True)
                con_amt = myArray[0]['con_amt']
                con_type = myArray[0]['con_type']
                con_plus = myArray[0]['con_plus']
                con_per = myArray[0]['con_per']
                con_per_amt = myArray[0]['con_per_amt']
                not_to_exceed = myArray[0]['not_to_exceed']
                record_id = myArray[0]['record_id']
                proqoute = myArray[0]['proqoute']
                fetch_type1 = myArray[0]['fetch_type1']
                fet_confition_id1 = myArray[0]['fet_confition_id1']
                condition_title1 = myArray[0]['condition_title1']
                cursor.execute('UPDATE  auctions SET pro_qoute_amount = %s WHERE auction_id = %s', (con_amt, auction[4]))
                con.commit()
                print(con_amt)
                print('end the particular auction here..')
        except:
            return ()
        finally:
            con.close()
