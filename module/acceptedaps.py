from flask import Flask,session
import numpy as np
import pymysql
import smtplib
import logging
import datetime
import traceback
import json
from datetime import date
from Misc.functions import *
import http.client

import requests

class Acceptedaps:

    def getLocationInfo(self,ip):

        response = requests.get(f'https://ipapi.co/{ip}/json/').json()
        location_data = {
            "ip": ip,
            "city": response.get("city"),
            "region": response.get("region"),
            "country": response.get("country_name")
        }
        return location_data

    def connect(self):
        #return pymysql.connect(host="localhost", user="carintocash1", password="zkY$$}_vtXO=", database="carintocash1", charset='utf8mb4')
        return pymysql.connect(host="localhost", user="root", password="", database="carintocash", charset='utf8mb4')
    
    def read(self, id,param,param1,start,length, column, order, searchData, start_date, end_date):
        # Reads data from the 'accepted_aps' table based on the provided parameters.

        # Args:
        #     id (int): The ID of the record to retrieve. If None, retrieves all records.
        #     param (str): The parameter to filter the records. Possible values: 'completed', 'incomplete', 'accepted', 'monthly', 'weekly', 'today', 'userfrom'.
        #     param1 (str): Additional parameter for filtering the records.
        #     start (int): The starting index of the records to retrieve.
        #     length (int): The number of records to retrieve.
        #     column (str): The column to sort the records by. Possible values: 'date', 'offerif', 'orignalprice', 'revisedprice', 'offer'.
        #     order (str): The order in which to sort the records. Possible values: 'ASC' (ascending), 'DESC' (descending).
        #     search: The search term to filter the records.

        # Returns:
        #     list: A list of records retrieved from the 'accepted_aps' table.
        con = Acceptedaps.connect(self)
        cursor = con.cursor()
        if param:
            if param=='completed':
                status = 'complete'
            elif param=='incomplete':
                status = 'incomplete'
            elif param=='accepted':
                status = 'accept'  
            elif param=='monthly':
                status = 'monthly'
            elif param=='weekly': 
                status = 'weekly'
            elif param=='today': 
                status = 'today'
            elif param=='userfrom': 
                status = 'userfrom'
        
        if column == 'date':
            column = 'created_at'
        elif column == 'offerif':
            column = 'offer_id'
        elif column == 'revisedprice':
            column = 'revised_price'
        elif column == 'offer':
            column = 'status_update'
        else:
            column = 'created_at'

        start_date = changeStartDateFormat(start_date)
        end_date = changeEndDateFormat(end_date)

        try:
            if id == None:  
                if param:
                    if status=='monthly':
                        cursor.execute("SELECT id,year,model,make,zip,original_price,status,user_city,user_state,created_at,revised_price,offer_id,dispatched,ref_id,status_update FROM accepted_aps where MONTH(`created_at`) = MONTH(now()) and YEAR(`created_at`) = YEAR(now()) AND created_at BETWEEN %s AND %s AND (offer_id LIKE %s OR year LIKE %s OR make LIKE %s OR model LIKE %s OR revised_price LIKE %s ) ORDER BY {} {}  LIMIT %s OFFSET %s".format(column, order),(start_date, end_date, '%' + searchData + '%', '%' + searchData + '%', '%' + searchData + '%', '%' + searchData + '%', '%' + searchData + '%', int(length), int(start)))
                    elif status=='weekly':
                        cursor.execute("SELECT id,year,model,make,zip,original_price,status,user_city,user_state,created_at,revised_price,offer_id,dispatched,ref_id,status_update FROM accepted_aps where week(`created_at`) = week(now()) AND created_at BETWEEN %s AND %s AND (offer_id LIKE %s OR year LIKE %s OR make LIKE %s OR model LIKE %s OR revised_price LIKE %s ) ORDER BY {} {}  LIMIT %s OFFSET %s".format(column, order),(start_date, end_date, '%' + searchData + '%', '%' + searchData + '%', '%' + searchData + '%', '%' + searchData + '%', '%' + searchData + '%', int(length), int(start)))
                    elif status=='today':
                        cursor.execute("SELECT id,year,model,make,zip,original_price,status,user_city,user_state,created_at,revised_price,offer_id,dispatched,ref_id,status_update FROM accepted_aps WHERE DATE_FORMAT(`created_at`, '%Y-%m-%d') = CURDATE() AND created_at BETWEEN %s AND %s AND (offer_id LIKE %s OR year LIKE %s OR make LIKE %s OR model LIKE %s OR revised_price LIKE %s ) ORDER BY {} {}  LIMIT %s OFFSET %s".format(column, order),(start_date, end_date, '%' + searchData + '%', '%' + searchData + '%', '%' + searchData + '%', '%' + searchData + '%', '%' + searchData + '%', int(length), int(start)))
                    elif status=='userfrom':
                        cursor.execute("SELECT id,year,model,make,zip,original_price,status,user_city,user_state,created_at,revised_price,offer_id,dispatched,ref_id,status_update FROM accepted_aps WHERE `ref_id` !='' AND created_at BETWEEN %s AND %s AND (offer_id LIKE %s OR year LIKE %s OR make LIKE %s OR model LIKE %s OR revised_price LIKE %s ) ORDER BY {} {}  LIMIT %s OFFSET %s".format(column, order),(start_date, end_date, '%' + searchData + '%', '%' + searchData + '%', '%' + searchData + '%', '%' + searchData + '%', '%' + searchData + '%', int(length), int(start)))
                    else:
                        if param1:
                            cursor.execute("SELECT id, year, model, make, zip, original_price, status, user_city, user_state, created_at, revised_price, offer_id, dispatched, ref_id, status_update FROM accepted_aps WHERE status = %s AND created_at BETWEEN %s AND %s AND (offer_id LIKE %s OR year LIKE %s OR make LIKE %s OR model LIKE %s OR revised_price LIKE %s ) ORDER BY {} {}  LIMIT %s OFFSET %s".format(column, order), (status, start_date , end_date , '%' + searchData + '%', '%' + searchData + '%', '%' + searchData + '%', '%' + searchData + '%', '%' + searchData + '%', int(length), int(start)))

                        else:
                            cursor.execute("SELECT id,year,model,make,zip,original_price,status,user_city,user_state,created_at,revised_price,offer_id,dispatched,ref_id,status_update FROM accepted_aps where status='"+status+"' AND created_at BETWEEN %s AND %s AND (offer_id LIKE %s OR year LIKE %s OR make LIKE %s OR model LIKE %s OR revised_price LIKE %s ) ORDER BY {} {}  LIMIT %s OFFSET %s".format(column, order),(start_date, end_date, '%' + searchData + '%', '%' + searchData + '%', '%' + searchData + '%', '%' + searchData + '%', '%' + searchData + '%', int(length), int(start)))
                else:
                    cursor.execute("SELECT id,year,model,make,zip,original_price,status,user_city,user_state,created_at,revised_price,offer_id,dispatched,ref_id,status_update FROM accepted_aps WHERE created_at BETWEEN %s AND %s AND (offer_id LIKE %s OR year LIKE %s OR make LIKE %s OR model LIKE %s OR revised_price LIKE %s ) ORDER BY {} {}  LIMIT %s OFFSET %s".format(column, order),(start_date, end_date, '%' + searchData + '%', '%' + searchData + '%', '%' + searchData + '%', '%' + searchData + '%', '%' + searchData + '%', int(length), int(start)))
            else:
                cursor.execute(
                    "SELECT id,year,model,make,zip,original_price,status,user_city,user_state,created_at,revised_price,offer_id,dispatched,ref_id,status_update FROM accepted_aps where id = %s AND created_at BETWEEN %s AND %s AND (offer_id LIKE %s OR year LIKE %s OR make LIKE %s OR model LIKE %s OR revised_price LIKE %s ) LIMIT %s OFFSET %s", (id,start_date, end_date, '%' + searchData + '%', '%' + searchData + '%', '%' + searchData + '%', '%' + searchData + '%', '%' + searchData + '%', int(length), int(start)))
            return cursor.fetchall()
        except:
            return ()
        finally:
            con.close() 

    def readnew(self, id):
        con = Acceptedaps.connect(self)
        cursor = con.cursor()
        try:
            cursor.execute("SELECT * FROM accepted_aps where id = %s ", (id,))
            return cursor.fetchall()
        except:
            return ()
        finally:
            con.close()
              
    def total_record(self, id,param,param1,start_date, end_date):
        # Returns the total number of records based on the given parameters.
        # Args:
        #     id (int): The ID of the record to retrieve. If None, all records are considered.
        #     param (str): The parameter to filter the records. Possible values are 'completed', 'incomplete', 'accepted',
        #                  'monthly', 'weekly', 'today', and 'userfrom'.
        #     param1 (bool): Additional parameter to determine the sorting order of the records.
        # Returns:
        #     int: The total number of records.
        # Raises:
        #     Exception: If there is an error executing the SQL query.

        con = Acceptedaps.connect(self)
        cursor = con.cursor()
        if param:
            if param=='completed':
                status = 'complete'
            elif param=='incomplete':
                status = 'incomplete'
            elif param=='accepted':
                status = 'accept'  
            elif param=='monthly':
                status = 'monthly'
            elif param=='weekly': 
                status = 'weekly'
            elif param=='today': 
                status = 'today'
            elif param=='userfrom': 
                status = 'userfrom'
        
        start_date = changeStartDateFormat(start_date)
        end_date = changeEndDateFormat(end_date)

        try:
            if id == None:  
                if param:
                    if status=='monthly':
                        cursor.execute("SELECT COUNT(*) FROM accepted_aps where MONTH(`created_at`) = MONTH(now()) and YEAR(`created_at`) = YEAR(now()) AND created_at BETWEEN %s AND %s ORDER BY id DESC ",(start_date, end_date))
                    elif status=='weekly':
                        cursor.execute("SELECT COUNT(*) FROM accepted_aps where week(`created_at`) = week(now()) AND created_at BETWEEN %s AND %s ORDER BY id DESC ",(start_date, end_date))
                    elif status=='today':
                        cursor.execute("SELECT COUNT(*) FROM accepted_aps WHERE DATE_FORMAT(`created_at`, '%Y-%m-%d') = CURDATE() AND created_at BETWEEN %s AND %s ",(start_date, end_date))
                    elif status=='userfrom':
                        cursor.execute("SELECT COUNT(*) FROM accepted_aps WHERE `ref_id` !='' AND created_at BETWEEN %s AND %s ",(start_date, end_date))
                    else:
                        if param1:
                            cursor.execute("SELECT COUNT(*) FROM accepted_aps where status='"+status+"' AND created_at BETWEEN %s AND %s ORDER BY dispatched ASC ",(start_date, end_date))
                        else:
                            cursor.execute("SELECT COUNT(*) FROM accepted_aps where status='"+status+"' AND created_at BETWEEN %s AND %s ORDER BY id DESC ",(start_date, end_date))
                else:
                    cursor.execute("SELECT COUNT(*) FROM accepted_aps AND created_at BETWEEN %s AND %s ORDER BY id DESC",(start_date, end_date))
            else:
                cursor.execute(
                    "SELECT COUNT(*) FROM accepted_aps where id = %s AND created_at BETWEEN %s AND %s", (id,start_date, end_date))
            return cursor.fetchone()[0]
        except:
            return ()
        finally:
            con.close()        
       
    def acceptbidsave(self, data):
        con = Acceptedaps.connect(self)
        cursor = con.cursor()
        try:
            cursor.execute("DELETE FROM auto_inquiry where ipaddr = %s  AND hostname = %s", (data['ipaddr'], data['hostname'],))
            con.commit()
            cursor.execute("INSERT INTO accepted_aps(year, makeid, modelid, make, model, vin, zip, damage, title, car_key, drive, mileage, airbag, fire_damage, type, address1, address2, city, state, fname, phone, alternatephone, ownerfname, payeefname, created_at) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (data['year'], data['make_id'], data['model_id'], data['make'], data['model'], data['vin'], data['v_zip'], data['damage'], data['title'], data['key'], data['drive'], data['mileage'], data['airbag'], data['fire_damage'], data['type'], data['address1'], data['address2'], data['city'], data['state'], data['fname'],  data['phone'], data['alternatephone'], data['ownerfname'], data['payeefname'],datetime.datetime.now(),))
            con.commit()
            return True
        except:
            con.rollback()
            return False
        finally:
            con.close()
    def autoinquiryget(self, IPAddr,hostname):
        con = Acceptedaps.connect(self)
        cursor = con.cursor()
        try:           
            cursor.execute("SELECT * FROM auto_inquiry where ipaddr = %s  AND hostname = %s", (IPAddr,hostname))
            return cursor.fetchall()
        except:
            con.rollback()
            return False
        finally:
            con.close()
    def autoinquirysave(self, data):
        con = Acceptedaps.connect(self)
        con1 = Acceptedaps.connect(self)
        cursor = con.cursor()
        cursor1 = con1.cursor()

        try:            
            if data['record_id'] == '':
                if data['ref_id'] == 'https://yourcarintocash.com/':
                    aaa = ''
                elif data['ref_id'] == 'http://m.facebook.com':    
                    aaa = 'https://l.facebook.com/'	
                else:
                    aaa = data['ref_id']
                print("INSERT INTO accepted_aps(year, makeid, modelid, make, model, make_code, vin, ipaddr, hostname,created_at,user_city,user_state,user_country,ref_id) VALUES(%s, %s, %s, %s, %s, %s, %s, %s,  %s, %s, %s, %s, %s, %s)", (data['year'], data['make_id'], data['model_id'], data['make'], data['model'],  data['make_code'], data['vin'],  data['ipaddr'], data['hostname'],datetime.datetime.now(),data['user_city'],data['user_state'],data['user_country'],aaa,))
                    
                cursor.execute("INSERT INTO accepted_aps(year, makeid, modelid, make, model, make_code, vin, ipaddr, hostname,created_at,user_city,user_state,user_country,ref_id) VALUES(%s, %s, %s, %s, %s, %s, %s, %s,  %s,  %s, %s,%s,%s,%s)", (data['year'], data['make_id'], data['model_id'], data['make'], data['model'],  data['make_code'], data['vin'],  data['ipaddr'], data['hostname'],datetime.datetime.now(),data['user_city'],data['user_state'],data['user_country'],aaa,))
                con.commit()
                print('1111')
                inquiry_id = int(cursor.lastrowid)
                #offer_id  = "YCIC" + str(inquiry_id)
                offer_id  = "YC" + str(inquiry_id).zfill(4)
                cursor1.execute("UPDATE accepted_aps set offer_id =%s where id = %s", (offer_id,inquiry_id,))
                con1.commit()
                return inquiry_id
            else:
                print('else')
                id = data['record_id']
                mileage1 = data['mileage'] + ',000'
                if data['currenttab']=='17':
                    if data['sharing_genrate_id'] !='' :
                        cursor.execute("UPDATE accepted_aps set status = %s,  ownerfname = %s,  payeefname = %s  where id = %s",('accept', data['ownerfname'],  data['payeefname'], id,))
                        con.commit()
                    else:
                        cursor.execute("UPDATE accepted_aps set status = %s, year = %s, makeid = %s, modelid = %s , make = %s , model = %s, zip = %s, damage = %s, title = %s, car_key = %s, drive = %s, mileage = %s, airbag = %s, fire_damage = %s , type = %s , locationname = %s , address1 = %s, address2 = %s, city = %s , state = %s, fname = %s, email = %s ,phone = %s, alternatephone = %s, ownerfname = %s,  payeefname = %s ,  sdamage = %s where id = %s",('accept',data['year'], data['make_id'], data['model_id'], data['make'], data['model'], data['v_zip'], data['damage'], data['title'], data['key'], data['drive'], mileage1, data['airbag'], data['fire_damage'], data['type'], data['locationname'], data['address1'], data['address2'], data['city'], data['state'], data['fname'],  data['email'], data['phone'], data['alternatephone'], data['ownerfname'],  data['payeefname'],data['sdamage'], id,))
                        con.commit()
                    return True 
                elif data['sharing_genrate_id'] !='' :
                    # print("darshan")
                    cursor.execute ("UPDATE `accepted_aps` SET `type`= %s,`locationname`= %s,`address1`= %s,`address2`= %s,`city`= %s,`state`= %s,`fname`= %s,`phone`= %s,`alternatephone`= %s,`ownerfname`= %s WHERE id = %s", (data['type'], data['locationname'], data['address1'], data['address2'], data['city'], data['state'],data['fname'], data['phone'], data['alternatephone'],data['ownerfname'],id,))
                    con.commit()
                    return True 
                elif data['currenttab']=='16': 
                    cursor.execute("UPDATE accepted_aps set status = %s, year = %s, makeid = %s, modelid = %s , make = %s , model = %s, zip = %s, damage = %s, title = %s, car_key = %s, drive = %s, mileage = %s, airbag = %s, fire_damage = %s , type = %s , locationname = %s , address1 = %s, address2 = %s, city = %s , state = %s, fname = %s,  phone = %s, alternatephone = %s, ownerfname = %s,  payeefname = %s ,  sdamage = %s where id = %s",('complete',data['year'], data['make_id'], data['model_id'], data['make'], data['model'], data['v_zip'], data['damage'], data['title'], data['key'], data['drive'], mileage1, data['airbag'], data['fire_damage'], data['type'], data['locationname'], data['address1'], data['address2'], data['city'], data['state'], data['fname'], data['phone'], data['alternatephone'], data['ownerfname'],  data['payeefname'] ,data['sdamage'], id,))
                    con.commit()
                    return True          
                else:
                    cursor.execute("UPDATE accepted_aps set   original_price = %s,revised_price = %s,year = %s, makeid = %s, modelid = %s , make = %s , model = %s, zip = %s, damage = %s, title = %s, car_key = %s, drive = %s, mileage = %s, airbag = %s, fire_damage = %s , type = %s , locationname = %s , address1 = %s, address2 = %s, city = %s , state = %s, fname = %s, email = %s  ,phone = %s, alternatephone = %s, ownerfname = %s,  payeefname = %s ,  sdamage = %s where id = %s",(data['original_price'],data['revised_price'],data['year'], data['make_id'], data['model_id'], data['make'], data['model'], data['v_zip'], data['damage'], data['title'], data['key'], data['drive'], mileage1, data['airbag'], data['fire_damage'], data['type'], data['locationname'], data['address1'], data['address2'], data['city'], data['state'], data['fname'], data['email'] ,data['phone'], data['alternatephone'], data['ownerfname'], data['payeefname'],data['sdamage'], id,))
                    con.commit()
                    return True

                
        except:
            con.rollback()
            return False
        finally:
            con.close()
    def updateautoinquiry(self, data):
        con = Acceptedaps.connect(self)
        cursor = con.cursor()
        try:            
            cursor.execute("SELECT * FROM auto_inquiry where ipaddr = %s  AND hostname = %s", (data['ipaddr'], data['hostname']))
            fetchall = cursor.fetchall()
            id = fetchall[0][0]       
            #cursor.execute("UPDATE auto_inquiry set year = %s, makeid = %s, modelid = %s , make = %s , model = %s, zip = %s , damage = %s, title = %s where id = %s",
                               #(data['year'], data['make_id'], data['model_id'], data['make'], data['model'], data['v_zip'], data['damage'], data['title'],  id,))
            #cursor.execute("UPDATE auto_inquiry set year = %s, makeid = %s, modelid = %s , make = %s , model = %s, zip = %s, damage = %s, title = %s, car_key = %s, drive = %s, mileage = %s, airbag = %s, fire_damage = %s , type = %s , address1 = %s where id = %s",(data['year'], data['make_id'], data['model_id'], data['make'], data['model'], data['v_zip'], data['damage'], data['title'], data['key'], data['drive'], data['mileage'], data['airbag'], data['fire_damage'], data['type'], data['address1'], id,))
            cursor.execute("UPDATE auto_inquiry set year = %s, makeid = %s, modelid = %s , make = %s , model = %s, zip = %s, damage = %s, title = %s, car_key = %s, drive = %s, mileage = %s, airbag = %s, fire_damage = %s , type = %s , locationname = %s , address1 = %s, address2 = %s, city = %s , state = %s, fname = %s,  phone = %s, alternatephone = %s, ownerfname = %s,  payeefname = %s where id = %s",(data['year'], data['make_id'], data['model_id'], data['make'], data['model'], data['v_zip'], data['damage'], data['title'], data['key'], data['drive'], data['mileage'], data['airbag'], data['fire_damage'], data['type'], data['locationname'], data['address1'], data['address2'], data['city'], data['state'], data['fname'], data['phone'], data['alternatephone'], data['ownerfname'], data['payeefname'] , id,))
            con.commit()
            return True              
                
        except:
            con.rollback()            
            return False
        finally:
            con.close()
    
    def deleteinquiry(self, data):
        con = Acceptedaps.connect(self)
        cursor = con.cursor()
        try:
            cursor.execute("DELETE FROM accepted_aps where id = %s", (data['id'],))
            con.commit()
            return True
            return cursor.fetchall()
        except:
            return ()
        finally:
            con.close()
            
    def deleteinquiryall(self, data):
        con = Acceptedaps.connect(self)
        cursor = con.cursor()
        try:
            cursor.execute("DELETE FROM `accepted_aps` WHERE id IN("+data['id']+")")
            con.commit()
            return True
            return cursor.fetchall()
        except:
            return ()
        finally:
            con.close()
            
    def getvinmake(self, data):
        con = Acceptedaps.connect(self)
        cursor = con.cursor()
        try:
            
            query="SELECT * FROM makes where name LIKE '"+data['Make']+"%'"
            cursor.execute(query)           
            return cursor.fetchone() 
        except:
            return ()
        finally:
            con.close() 
    def getvinmodel(self, data):
        con = Acceptedaps.connect(self)
        cursor = con.cursor()
        try:
            
            query="SELECT * FROM models where name LIKE '"+data['Model']+"%'"
            cursor.execute(query)           
            return cursor.fetchone() 
        except:
            return ()
        finally:
            con.close() 
            
        
    def modelYearcheck(self, data):
        con = Acceptedaps.connect(self)
        cursor = con.cursor()
        try:
            cursor.execute("SELECT * FROM years where year = %s ", (data['modelyear'],))
            fetchall = cursor.fetchall()
            if len(fetchall) == 0:
                currentDT = datetime.datetime.now()
                created_at = currentDT.strftime("%Y-%m-%d %H:%M")
                cursor.execute("INSERT INTO years(year) VALUES(%s )",(data['modelyear'], ))
                con.commit()
                return True
            else:
               return fetchall
        except:
            return ()
        finally:
            con.close()

    def makecheck(self, data):
        con = Acceptedaps.connect(self)
        cursor = con.cursor()
        try:
            cursor.execute("SELECT * FROM makes where name = %s ", (data['make'],))
            fetchall = cursor.fetchall()
            if len(fetchall) == 0:
                cursor.execute("INSERT INTO makes(name,shortcode) VALUES(%s, %s )",(data['make'],data['make'], ))
                con.commit()
                make_id = cursor.lastrowid
                cursor.execute("INSERT INTO vehiclespecschema_year(make_id,year) VALUES(%s, %s )",(make_id,data['modelyear'], ))
                con.commit()
                return True
            else:
                makesid = fetchall[0][0]
                #print("SELECT * FROM vehiclespecschema_year where make_id = %s AND year = %s", (makesid, data['modelyear']))
                cursor.execute("SELECT * FROM vehiclespecschema_year where make_id = %s AND year = %s", (makesid, data['modelyear']))
                fetch_all = cursor.fetchall()
                #print(fetch_all)
                #print('fetch_all vipul kodufad')
                if len(fetch_all) == 0:
                    cursor.execute("INSERT INTO vehiclespecschema_year(make_id,year) VALUES(%s, %s )",(makesid,data['modelyear'], ))
                    con.commit()
                return fetch_all
        except:
            return ()
        finally:
            con.close()

    def getmakeID(self, data):
        con = Acceptedaps.connect(self)
        cursor = con.cursor()
        try:
            cursor.execute("SELECT id FROM makes where name = %s ", (data['make'],))
            makes = cursor.fetchone()
            return makes
        except:
            return ()
        finally:
            con.close()

    def make_year_check(self, data,makeID):
        con = Acceptedaps.connect(self)
        cursor = con.cursor()
        try:
            cursor.execute("SELECT * FROM vehiclespecschema_year where make_id = %s AND year = %s", (makeID, data['modelyear']))
            fetchall = cursor.fetchall()
            if len(fetchall) == 0:
                
                cursor.execute("INSERT INTO vehiclespecschema_year(make_id,year) VALUES(%s, %s )",(makeID,data['modelyear'], ))
                con.commit()
                make_id = cursor.lastrowid
                return make_id
            else:
                return fetchall[0][0]
        except:
            return ()
        finally:
            con.close()
    def modelcheck(self, data,yid):
        con = Acceptedaps.connect(self)
        cursor = con.cursor()
        try:
            cursor.execute("SELECT * FROM models where name = %s ", (data['model'],))
            fetchall = cursor.fetchall()
            if len(fetchall) == 0:
                cursor.execute("INSERT INTO models(name) VALUES(%s )",(data['model'], ))
                con.commit()
                model_id = cursor.lastrowid
                cursor.execute("INSERT INTO vehiclespecschema_model(vssy_id,modelId) VALUES(%s, %s )",(yid,model_id,  ))
                con.commit()
                return True
            else:
                modelId = fetchall[0][0]
                #print('fetchall============================>',modelId)
                #print("SELECT * FROM vehiclespecschema_model where vssy_id = %s AND modelId = %s", (yid, modelId))
                cursor.execute("SELECT * FROM vehiclespecschema_model where vssy_id = %s AND modelId = %s", (yid, modelId))
                fetch_all = cursor.fetchall()
                if len(fetch_all) == 0:
                    cursor.execute("INSERT INTO vehiclespecschema_model(vssy_id,modelId) VALUES (%s, %s)",(yid,modelId,))
                    con.commit()
                return fetchall

        except:
            return ()
        finally:
            con.close()
            
    def getnotificationcounter(self):
        con = Acceptedaps.connect(self)
        cursor = con.cursor()
        cursor = con.cursor()
        try:
            #return current_time1;
            cursor.execute("SELECT count(`id`) FROM `accepted_aps` WHERE status = 'accept' and dispatched='no' ")
            return cursor.fetchall()

        except:
            return ()
        finally:
            con.close()

    def getofferid(self, data):
        con = Acceptedaps.connect(self)
        cursor = con.cursor()
        try:
            cursor.execute("SELECT offer_id FROM accepted_aps where id = %s ", (data['id'],))
            return cursor.fetchone() 
        except:
            return ()
        finally:
            con.close()
            
    def d_insert(self ,data):
        con = Acceptedaps.connect(self)
        cursor = con.cursor()
        #print(data)
        try:
            id = data['id']
            img1_str=data['interior_photo']
            img2_str=data['vin_photo']
            img3_str=data['mileage_photo']
            img5_str=data['hidden_file-2']
           

            cursor.execute("Update accepted_aps set d_name = %s, d_email=%s, d_phone=%s, d_Interior_photo=%s, d_vin_photo=%s,d_mileage_photo=%s,status=%s,why_did_decline=%s,d_Interior_photo1=%s, except_price=%s where offer_id = %s", (data['d_name'],data['d_email'],data['d_phone'],img5_str,img2_str,img3_str,'Decline',data['why_did_decline'],img1_str,data['except_price'], id,))
            con.commit()
            return "Thank you for providing the information, We appreciate your feedback."
        except:
            return "error"
        finally:
            con.close()
    
    def decline_data(self, id):
        con = Acceptedaps.connect(self)
        cursor = con.cursor()
        try:
            cursor.execute("SELECT * FROM `accepted_aps` WHERE id = %s",(id,))

            return  cursor.fetchone()
        except:
            return "error"
        finally:
            con.close()
            
    def getdeclineoffer(self, start, length, start_date, end_date, column, order, search):

        # Retrieves a list of declined offers from the 'accepted_aps' table based on the specified parameters.
        # Parameters:
        # - start_date: The start date of the inquiry data.
        # - end_date: The end date of the inquiry data.
        # - start: The starting index of the records to retrieve.
        # - length: The number of records to retrieve.
        # - column: The column to sort the records by.
        # - order: The order in which to sort the records (ASC or DESC).
        # - search: The search term to filter the records.

        # Returns:
        # - A list of declined offers matching the specified parameters.
        # - If an error occurs, returns "error".
        con = Acceptedaps.connect(self)
        cursor = con.cursor()
        try:
            if column == 'date':
                column = 'created_at'
            elif column == 'offerif':
                column = 'offer_id'
            elif column == 'revisedprice':
                column = 'revised_price'
            elif column == 'offer':
                column = 'status_update'
            else:
                column = 'created_at'

            start_date = changeStartDateFormat(start_date)
            end_date = changeEndDateFormat(end_date)
            
            cursor.execute("SELECT id, year, model, make, zip, original_price, status, user_city, user_state, created_at, revised_price, offer_id, dispatched, ref_id, status_update FROM accepted_aps WHERE status = %s AND created_at BETWEEN %s AND %s AND (offer_id LIKE %s OR year LIKE %s OR make LIKE %s OR model LIKE %s OR revised_price LIKE %s ) ORDER BY {} {} LIMIT %s OFFSET %s".format(column, order), ('Decline', start_date, end_date, '%' + search + '%', '%' + search + '%', '%' + search + '%', '%' + search + '%', '%' + search + '%', int(length), int(start)))
            return cursor.fetchall()
        except:
            return "error"
        finally:
            con.close()
        
    # Retrieves the total number of records with a status of 'Decline' from the 'accepted_aps' table.
    def get_total_records_decline(self, start_date, end_date,):

        con = Acceptedaps.connect(self)
        cursor = con.cursor()
        try:
            start_date = changeStartDateFormat(start_date)
            end_date = changeEndDateFormat(end_date)
            cursor.execute("SELECT count(*) FROM `accepted_aps` WHERE status = %s AND created_at BETWEEN %s AND %s", ('Decline',start_date, end_date))
            return cursor.fetchall()[0][0]
        except:
            return "error"
        finally:
            con.close()


    def getmodels1(self, data):
        con = Acceptedaps.connect(self)
        cursor = con.cursor()
        try:
            cursor.execute("SELECT md.name model, md.id modelId FROM makes m LEFT Join vehiclespecschema_year vssy ON m.id = vssy.make_id LEFT JOIN vehiclespecschema_model vssm ON vssm.vssy_id = vssy.id LEFT JOIN models md ON md.id = vssm.modelId   Where m.id = %s group by vssm.modelId ", (data,) )
            a = cursor.fetchall()
            return a
        except:
            return ()
        finally:
            con.close()

    def getmakes1(self,):
        con = Acceptedaps.connect(self)
        cursor = con.cursor()
        try:           
            cursor.execute("SELECT * FROM makes ")
            return cursor.fetchall()           
        except:
            return ()
        finally:
            con.close()

    def get_zipcode_list(self, data):
        con = Acceptedaps.connect(self)
        cursor = con.cursor()
        con1 = Acceptedaps.connect(self)
        cursor1 = con1.cursor()
        con2 = Acceptedaps.connect(self)
        cursor2 = con2.cursor()
        con3 = Acceptedaps.connect(self)
        cursor3 = con3.cursor()
        try:
            q1 = "SELECT * FROM zipcode where zipcode='"+data['range_zip']+"'"
            cursor.execute(q1)
            getRecord = cursor.fetchone()                     
            if getRecord:              
                allZip = ''
                q2 = "SELECT `zipcode`, ( 3959 * ACOS( COS( RADIANS(" + str(getRecord[4]) + ") ) * COS( RADIANS(`latitude`) ) * COS( RADIANS(`longitude`) - RADIANS(" + str(getRecord[5]) + ") ) + SIN( RADIANS(" + str(getRecord[4]) + ") ) * SIN( RADIANS(`latitude`) ) ) ) AS distance FROM zipcode HAVING distance <= " + data['distance_amt'] + " ORDER BY distance"
                cursor1.execute(q2)
                getRecord1 = cursor1.fetchall()
                if len(getRecord1) != 0:
                    arr = np.array(getRecord1)               
                    allZip = (",".join(arr[:, 0]))  
                    cursor2.execute("SELECT * FROM condition_zipcode where sessionid = %s AND numbers = %s ", (data['sessionid'],data['numbers']))
                    fetch_all = cursor2.fetchone()
                    if fetch_all:
                        #new_final_zip = allZip +fetch_all[2]
                        #my_list_new_arr = new_final_zip.split(",")
                        #unique_list = list(set(my_list_new_arr)) 
                        #allZip = (",".join(set(unique_list))) 
                        cursor3.execute("UPDATE `condition_zipcode` set zipcode = %s   where id = %s",(allZip , fetch_all[0]))
                        con3.commit()
                    else:
                        cursor3.execute("INSERT INTO `condition_zipcode` (`sessionid`, `zipcode`, `numbers`) VALUES (%s, %s, %s)",(data['sessionid'], allZip, data['numbers'] ))
                        con3.commit()
                              
                return allZip
                cursor1.close()
        except:
            return ()
        finally:
            con.close()
    
    
    def saveConditionReportAdd(self,data):
        con = Acceptedaps.connect(self)
        cursor = con.cursor() 

        con1 = Acceptedaps.connect(self)
        cursor1 = con1.cursor()

        con2 = Acceptedaps.connect(self)
        cursor2 = con2.cursor()         

        usa = data.get("usa")
        getStateData = data.getlist("state[]")


        con3 = Acceptedaps.connect(self)
        cursor3 = con3.cursor() 

        con4 = Acceptedaps.connect(self)
        cursor4 = con4.cursor()    

        usa_data = '';
        if usa:
            usa_data = 'USA'

        stateComma = '';
        if getStateData:
            for k1 in getStateData:
                stateComma = stateComma+k1+','

        unable_to_verify = data.get("unable_to_verify") 
        unable_to_verify_data = 'no';
        if unable_to_verify:
            unable_to_verify_data = 'yes'

        #print(unable_to_verify_data+'unable_to_verify_data')
        getBodyDamageData = data.getlist("damage[]")
        damageComma = '';
        if getBodyDamageData:
            for k1 in getBodyDamageData:
                damageComma = damageComma+k1+','
        getAirBag = data.getlist('airbag[]')
        
        
        airbagComma = '';
        if getAirBag:
            for k1 in getAirBag:
                airbagComma = airbagComma+k1+','

        getDrive = data.getlist('drive[]')
        driveComma = '';
        if getDrive:
            for k1 in getDrive:
                driveComma = driveComma+k1+','

        getSDamage = data.getlist('sdamage[]')
        getSDamageComma = '';
        if getSDamage:
            for k1 in getSDamage:
                getSDamageComma = getSDamageComma+k1+','

        getKey = data.getlist('key[]') 
        keyComma = '';
        if getKey:
            for k1 in getKey:
                keyComma = keyComma+k1+','

        getTitleType = data.getlist('title[]')
        titleComma = '';
        if getTitleType:
            for k1 in getTitleType:
                titleComma = titleComma+k1+','

        getFireDamage = data.getlist('fire_damage[]')
        firDamageComma = '';
        if getFireDamage:
            for k1 in getFireDamage:
                firDamageComma = firDamageComma+k1+','


        # =================
        getDamage = data.getlist("damage[]")
        getDamageImg = data.getlist("damageimg[]")

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


        getMakeData = data.getlist("make[]")
        make_id_s = '';
        model_id_s = '';
        adcostrray = []
        if getMakeData:
            for k in getMakeData:
                make_id = k
                make_id_s = make_id_s+k+','
                model_id = data.getlist("model["+k+"]")
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

        getestimateData=''
       
        #getStateData=''
        
        if data['Estimate']=='1':
            estimate = 'Proquote Estimate'
        else:
            estimate = 'Fixed Amount'
            
        if data['make_name']=='':
            make_name1 = 'all'
            model_name1 = 'all'
        else:
            make_name1 = data['make_name']
            model_name1 = data['model_name']
        i=0
        range_array = []
        for k in data.getlist('range_zip[]'):
            distance = data.getlist('distance_amt[]')[i]
            #listzip = data.getlist('listzip[]')[i]
            i=i+1
            if k !="" :
                range_array.append({'id' : i, 'distance' : distance, 'range_zip' : k })                
                #new_final_zip = allZip +listzip
                #my_list_new_arr = new_final_zip.split(",")
                #unique_list = list(set(my_list_new_arr)) 
                #allZip = (",".join(set(unique_list)))                

        rangearray = json.dumps(range_array)
        allZip=''
        if usa_data!='':
            countryQuery = "SELECT `zipcode` FROM zipcode order by id"
            cursor2.execute(countryQuery)
            zipalllist = cursor2.fetchall()
            arr = np.array(zipalllist)               
            allZip = (",".join(arr[:, 0])) 
        else:
            allZiplist =''
            allstateZip ='';
            if stateComma!='':
                stringStateData = ''
                for k in getStateData:
                    stringStateData = stringStateData + "'" + k + "',"

                stringStateData = stringStateData.rstrip(',')
                countryQuery1 = "SELECT `zipcode` FROM zipcode where `state` in(" + stringStateData+") order by id"
                cursor2.execute(countryQuery1)
                countryZip3 = cursor2.fetchall()
                if len(countryZip3) != 0:
                    arr = np.array(countryZip3)               
                    allstateZip = (",".join(arr[:, 0]))
                    allZiplist += allstateZip

                #print(allstateZip)  
            allZip1 = allZip2 = allZip3 = ''
            cursor1.execute("SELECT zipcode FROM condition_zipcode where sessionid = %s  LIMIT 0, 15 ", (data['sessionid']))
            zipalllist1 = cursor1.fetchall()
            if len(zipalllist1) != 0:
                arr = np.array(zipalllist1)               
                new_final_zip1 = (",".join(arr[:, 0]))
                my_list_new_arr1 = new_final_zip1.split(",")          
                unique_list1 = list(set(my_list_new_arr1)) 
                allZip1 = (",".join(set(unique_list1))) 
                allZiplist += allZip1+',' 
            cursor1.close() 

            cursor3.execute("SELECT zipcode FROM condition_zipcode where sessionid = %s  LIMIT 15, 15 ", (data['sessionid']))
            zipalllist2 = cursor3.fetchall()
            if len(zipalllist2) != 0:
                arr = np.array(zipalllist2)               
                new_final_zip2 = (",".join(arr[:, 0]))
                my_list_new_arr2 = new_final_zip2.split(",")          
                unique_list2 = list(set(my_list_new_arr2)) 
                allZip2 = (",".join(set(unique_list2))) 
                allZiplist += allZip2+','
            cursor3.close()  

            cursor4.execute("SELECT zipcode FROM condition_zipcode where sessionid = %s  LIMIT 30, 20 ", (data['sessionid']))
            zipalllist3 = cursor4.fetchall()
            if len(zipalllist3) != 0:
                arr = np.array(zipalllist3)               
                new_final_zip3 = (",".join(arr[:, 0]))
                my_list_new_arr3 = new_final_zip3.split(",")          
                unique_list3 = list(set(my_list_new_arr3)) 
                allZip3 = (",".join(set(unique_list3)))
                allZiplist += allZip3+','
            cursor4.close()               
               
            if allZiplist !="" :                 
                my_list_new_arr = allZiplist.split(",")          
                unique_list = list(set(my_list_new_arr)) 
                allZip = (",".join(set(unique_list)))  
         



                #if allstateZip !="":
                    #new_final_zip = new_final_zip+','+allstateZip               
                #my_list_new_arr = new_final_zip.split(",")          
                #unique_list = list(set(my_list_new_arr)) 
                #allZip = (",".join(set(unique_list))) 
        sessionid = data['sessionid']
        if data['condition_report_id']=='':        
            cursor.execute("INSERT INTO condition_report(title, condition_type, estimate, not_to_exceed_type_action, not_to_exceed_type, not_to_exceed_per, not_to_exceed, fixed_amt_txt, make_model, min_year, max_year, min_mileage, max_mileage, zip, damage, damageimg, make_name, model_name, make1, model1, sdamageImg_s, range_zip, damageComma, airbagComma, driveComma, getSDamageComma, keyComma, titleComma, firDamageComma, unable_to_verify, state, country, final_zip, sessionid ) VALUES( %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s , %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s )",(data['filter_title'],data['condition_type'],estimate,data['not_to_exceed_type_action'], data['not_to_exceed_type'], data['not_to_exceed_per'], data['not_to_exceed'] , data['fixed_amt_txt'], abc, data['year_min'],data['year_max'],data['mileage_min'],data['mileage_max'],data['zip'],getDamage1,abc1,make_name1,model_name1,make_id_s,model_id_s,sdamageImg_s,rangearray,damageComma,airbagComma,driveComma,getSDamageComma,keyComma,titleComma,firDamageComma,unable_to_verify_data, stateComma,usa_data, allZip, sessionid ))           
            con.commit()
            condition_id = cursor.lastrowid
            #print(condition_id)
        else:
            #cursor.execute("UPDATE condition_report set title = %s, estimate = %s, not_to_exceed_type_action = %s, not_to_exceed_type = %s , not_to_exceed_per = %s , not_to_exceed = %s, fixed_amt_txt = %s , make_model = %s, min_mileage = %s, max_mileage=%s,  zip=%s , damage=%s , damageimg=%s , make_name=%s , model_name=%s ,  make1=%s , model1=%s,sdamageImg_s=%s ,min_year=%s ,max_year=%s,distance_amt=%s,range_zip=%s,final_zip=%s,damageComma=%s,airbagComma=%s,driveComma=%s,getSDamageComma=%s,keyComma=%s,titleComma=%s,firDamageComma=%s,unable_to_verify=%s,distance_amt1=%s,range_zip1=%s,distance_amt2=%s,range_zip2=%s,final_zip1=%s,final_zip2=%s,final_zip3=%s,final_zip5=%s,state=%s,country=%s    where id = %s",(data['filter_title'], estimate,data['not_to_exceed_type_action'], data['not_to_exceed_type'],data['not_to_exceed_per'], data['not_to_exceed'] , data['fixed_amt_txt'],adcostrray,data['mileage_min'],data['mileage_max'],data['zip'],getDamage1,abc1,make_name1,model_name1,make_id_s,model_id_s,sdamageImg_s,data['year_min'],data['year_max'],data['distance_amt'],data['range_zip'],allZip,damageComma,airbagComma,driveComma,getSDamageComma,keyComma,titleComma,firDamageComma,unable_to_verify_data,data['distance_amt1'],data['range_zip1'],data['distance_amt2'],data['range_zip2'],allZip1,allZip2,allZip3,allZip5,stateComma,usa_data,data['condition_report_id']))
            #cursor.execute("UPDATE condition_report set title = %s, estimate = %s, not_to_exceed_type_action = %s, not_to_exceed_type = %s , not_to_exceed_per = %s , not_to_exceed = %s, fixed_amt_txt = %s , make_model = %s, min_mileage = %s, max_mileage=%s,  zip=%s , damage=%s , damageimg=%s , make_name=%s , model_name=%s ,  make1=%s , model1=%s,sdamageImg_s=%s ,min_year=%s ,max_year=%s,distance_amt=%s,range_zip=%s,final_zip=%s,damageComma=%s,airbagComma=%s,driveComma=%s,getSDamageComma=%s,keyComma=%s,titleComma=%s,firDamageComma=%s,unable_to_verify=%s,distance_amt1=%s,range_zip1=%s,distance_amt2=%s,range_zip2=%s,final_zip1=%s,final_zip2=%s,final_zip3=%s,final_zip5=%s,state=%s,country=%s    where id = %s",(data['filter_title'], estimate,data['not_to_exceed_type_action'], data['not_to_exceed_type'],data['not_to_exceed_per'], data['not_to_exceed'] , data['fixed_amt_txt'],adcostrray,data['mileage_min'],data['mileage_max'],data['zip'],getDamage1,abc1,make_name1,model_name1,make_id_s,model_id_s,sdamageImg_s,data['year_min'],data['year_max'],data['distance_amt'],data['range_zip'],allZip,damageComma,airbagComma,driveComma,getSDamageComma,keyComma,titleComma,firDamageComma,unable_to_verify_data,data['distance_amt1'],data['range_zip1'],data['distance_amt2'],data['range_zip2'],allZip1,allZip2,allZip3,allZip5,stateComma,usa_data,data['condition_report_id']))
            #con.commit()
            #condition_id = data['condition_report_id']
            cursor.execute("UPDATE condition_report set title = %s, condition_type = %s, estimate = %s, not_to_exceed_type_action = %s, not_to_exceed_type = %s, not_to_exceed_per = %s, not_to_exceed = %s, fixed_amt_txt = %s , make_model = %s, min_year = %s, max_year = %s, min_mileage = %s, max_mileage = %s, zip = %s, damage = %s, damageimg = %s, make_name = %s, model_name=%s, make1=%s, model1 = %s, sdamageImg_s = %s, range_zip = %s, damageComma = %s, airbagComma = %s, driveComma = %s, getSDamageComma = %s, keyComma = %s, titleComma = %s, firDamageComma = %s, unable_to_verify = %s , state  = %s, country = %s, final_zip = %s where id = %s", (data['filter_title'],data['condition_type'],estimate,data['not_to_exceed_type_action'], data['not_to_exceed_type'], data['not_to_exceed_per'], data['not_to_exceed'] , data['fixed_amt_txt'], abc, data['year_min'],data['year_max'],data['mileage_min'],data['mileage_max'],data['zip'],getDamage1,abc1,make_name1,model_name1,make_id_s,model_id_s,sdamageImg_s,rangearray,damageComma,airbagComma,driveComma,getSDamageComma,keyComma,titleComma,firDamageComma,unable_to_verify_data, stateComma, usa_data, allZip, data['condition_report_id']))
            con.commit()
            condition_id = data['condition_report_id']
        return condition_id

    

    #new code value added start here country
    def saveConditionReport(self,data,getestimateData,adcostrray, getDamage1,abc1,make_id_s,model_id_s,sdamageImg_s,damageComma,airbagComma,driveComma,getSDamageComma,keyComma,titleComma,firDamageComma,unable_to_verify_data,usa_data,stateComma,getStateData):
        con = Acceptedaps.connect(self)
        cursor = con.cursor()
        
        print(data)
        
        con1 = Acceptedaps.connect(self)
        cursor1 = con1.cursor()

        con2 = Acceptedaps.connect(self)
        cursor2 = con2.cursor()
        
        con3 = Acceptedaps.connect(self)
        cursor3 = con3.cursor()

        con5 = Acceptedaps.connect(self)
        cursor5 = con5.cursor()

        con6 = Acceptedaps.connect(self)
        cursor6 = con6.cursor()

        con7 = Acceptedaps.connect(self)
        cursor7 = con7.cursor()
        
        #new code value added start here country
        con8 = Acceptedaps.connect(self)
        cursor8 = con8.cursor()

        con9 = Acceptedaps.connect(self)
        cursor9 = con9.cursor()

        allZip = ',';
        allZip1 = '';
        allZip2 = '';
        allZip3 = '';
        allZip5 = '';

        if usa_data!='':
            countryQuery = "SELECT `zipcode` FROM zipcode order by id"
            cursor8.execute(countryQuery)
            countryZip = cursor8.fetchall() 
            cnt = 1
            for k in countryZip:
                cnt = cnt + 1
                if cnt < 10000:
                    allZip = allZip +k[0] + ','
                elif cnt > 10000 and cnt < 20000:
                    allZip1 = allZip1 +k[0] + ','
                elif cnt >= 20000 and cnt < 30000:
                    allZip2 = allZip2 +k[0] + ','
                elif cnt >= 30000 and cnt < 40000:
                    allZip3 = allZip3 +k[0] + ','
                elif cnt >= 40000:
                    allZip5 = allZip5 +k[0] + ','
            cursor8.close()

        if stateComma!='':
            stringStateData = ''

            if usa_data=='':
                for k in getStateData:
                    stringStateData = stringStateData + "'" + k + "',"

                stringStateData = stringStateData.rstrip(',')
                countryQuery1 = "SELECT `zipcode` FROM zipcode where `state` in(" + stringStateData+") order by id"
                cursor9.execute(countryQuery1)
                countryZip3 = cursor9.fetchall() 
                cnt1 = 1
                
                for k in countryZip3:
                    cnt1 = cnt1 + 1
                    if cnt1 < 10000:
                        allZip = allZip +k[0] + ','
                    elif cnt1 > 10000 and cnt1 < 20000:
                        allZip1 = allZip1 +k[0] + ','
                    elif cnt1 >= 20000 and cnt1 < 30000:
                        allZip2 = allZip2 +k[0] + ','
                    elif cnt1 >= 30000 and cnt1 < 40000:
                        allZip3 = allZip3 +k[0] + ','
                    elif cnt1 >= 40000:
                        allZip5 = allZip5 +k[0] + ','
                cursor9.close()
        #new code value added end here country
        
        if data['Estimate']=='1':
            estimate = 'Proquote Estimate'
        else:
            estimate = 'Fixed Amount'
            
        if data['make_name']=='':
            make_name1 = 'all'
            model_name1 = 'all'
        else:
            make_name1 = data['make_name']
            model_name1 = data['model_name']
            
        q1 = "SELECT * FROM zipcode where zipcode='"+data['range_zip']+"'"
        cursor1.execute(q1)
        getRecord = cursor1.fetchone() 
        
        if getRecord:
            q2 = "SELECT `zipcode`, ( 3959 * ACOS( COS( RADIANS(" + str(getRecord[4]) + ") ) * COS( RADIANS(`latitude`) ) * COS( RADIANS(`longitude`) - RADIANS(" + str(getRecord[5]) + ") ) + SIN( RADIANS(" + str(getRecord[4]) + ") ) * SIN( RADIANS(`latitude`) ) ) ) AS distance FROM zipcode HAVING distance <= " + str(data['distance_amt']) + " ORDER BY distance"
            cursor2.execute(q2)
            getRecord1 = cursor2.fetchall() 
            for k in getRecord1:
                allZip = allZip +k[0] + ','
            cursor2.close()
            
        if data['range_zip1'] !='' : 
            q11 = "SELECT * FROM zipcode where zipcode='"+data['range_zip1']+"'"
            cursor3.execute(q11)
            getRecorddata1 = cursor3.fetchone() 
            
            if getRecorddata1:
                q22 = "SELECT `zipcode`, ( 3959 * ACOS( COS( RADIANS(" + str(getRecorddata1[4]) + ") ) * COS( RADIANS(`latitude`) ) * COS( RADIANS(`longitude`) - RADIANS(" + str(getRecorddata1[5]) + ") ) + SIN( RADIANS(" + str(getRecorddata1[4]) + ") ) * SIN( RADIANS(`latitude`) ) ) ) AS distance FROM zipcode HAVING distance <= " + str(data['distance_amt1']) + " ORDER BY distance"
                cursor5.execute(q22)
                getRecordsub1 = cursor5.fetchall()
                # Process the results
                for k in getRecordsub1:
                    allZip1 = allZip1 +k[0] + ','
                cursor5.close()

        if data['range_zip2'] !='' : 
            q111 = "SELECT * FROM zipcode where zipcode='"+data['range_zip2']+"'"
            cursor6.execute(q111)
            getRecorddata2 = cursor6.fetchone() 
            
            if getRecorddata2:
                q222 = "SELECT `zipcode`, ( 3959 * ACOS( COS( RADIANS(" + str(getRecorddata2[4]) + ") ) * COS( RADIANS(`latitude`) ) * COS( RADIANS(`longitude`) - RADIANS(" + str(getRecorddata2[5]) + ") ) + SIN( RADIANS(" + str(getRecorddata2[4]) + ") ) * SIN( RADIANS(`latitude`) ) ) ) AS distance FROM zipcode HAVING distance <= " + str(data['distance_amt2']) + " ORDER BY distance"
                cursor7.execute(q222)
                getRecordsub2 = cursor7.fetchall() 
                # Process the results
                for k in getRecordsub2:
                    allZip2 = allZip2 +k[0] + ','
                cursor7.close()
        
        if data['condition_report_id']=='':
            cursor.execute("INSERT INTO condition_report(title,estimate,not_to_exceed_type_action,not_to_exceed_type,not_to_exceed_per,not_to_exceed,fixed_amt_txt,make_model, min_year,max_year,min_mileage,max_mileage,zip,damage,damageimg,make_name,model_name,make1,model1,sdamageImg_s,distance_amt,range_zip,final_zip,damageComma,airbagComma,driveComma,getSDamageComma,keyComma,titleComma,firDamageComma,unable_to_verify,distance_amt1,range_zip1,distance_amt2,range_zip2,final_zip1,final_zip2,final_zip3,final_zip5,state,country) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s ,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s )",(data['filter_title'], estimate,data['not_to_exceed_type_action'], data['not_to_exceed_type'],data['not_to_exceed_per'], data['not_to_exceed'] , data['fixed_amt_txt'],adcostrray,data['year_min'],data['year_max'],data['mileage_min'],data['mileage_max'],data['zip'],getDamage1,abc1,make_name1,model_name1,make_id_s,model_id_s,sdamageImg_s,data['distance_amt'],data['range_zip'],allZip,damageComma,airbagComma,driveComma,getSDamageComma,keyComma,titleComma,firDamageComma,unable_to_verify_data,data['distance_amt1'],data['range_zip1'],data['distance_amt2'],data['range_zip2'],allZip1,allZip2,allZip3,allZip5,stateComma,usa_data))
            con.commit()
            condition_id = cursor.lastrowid
        else:
            cursor.execute("UPDATE condition_report set title = %s, estimate = %s, not_to_exceed_type_action = %s, not_to_exceed_type = %s , not_to_exceed_per = %s , not_to_exceed = %s, fixed_amt_txt = %s , make_model = %s, min_mileage = %s, max_mileage=%s,  zip=%s , damage=%s , damageimg=%s , make_name=%s , model_name=%s ,  make1=%s , model1=%s,sdamageImg_s=%s ,min_year=%s ,max_year=%s,distance_amt=%s,range_zip=%s,final_zip=%s,damageComma=%s,airbagComma=%s,driveComma=%s,getSDamageComma=%s,keyComma=%s,titleComma=%s,firDamageComma=%s,unable_to_verify=%s,distance_amt1=%s,range_zip1=%s,distance_amt2=%s,range_zip2=%s,final_zip1=%s,final_zip2=%s,final_zip3=%s,final_zip5=%s,state=%s,country=%s    where id = %s",(data['filter_title'], estimate,data['not_to_exceed_type_action'], data['not_to_exceed_type'],data['not_to_exceed_per'], data['not_to_exceed'] , data['fixed_amt_txt'],adcostrray,data['mileage_min'],data['mileage_max'],data['zip'],getDamage1,abc1,make_name1,model_name1,make_id_s,model_id_s,sdamageImg_s,data['year_min'],data['year_max'],data['distance_amt'],data['range_zip'],allZip,damageComma,airbagComma,driveComma,getSDamageComma,keyComma,titleComma,firDamageComma,unable_to_verify_data,data['distance_amt1'],data['range_zip1'],data['distance_amt2'],data['range_zip2'],allZip1,allZip2,allZip3,allZip5,stateComma,usa_data,data['condition_report_id']))
            con.commit()
            condition_id = data['condition_report_id']
        return condition_id


    def getConditionalFilter(self,):
        con = Acceptedaps.connect(self)
        cursor = con.cursor()
        # try:           
        #     cursor.execute("SELECT `id`, `title`, `make1`, `model1`, `make_model`, `min_year`, `max_year`, `min_distance`, `max_distance`, `min_mileage`, `max_mileage`, `damage`, `damageimg`, `airbag`, `drive`, `sdamage`, `key1`, `title_type`, `fire_damage`, `estimate`, `not_to_exceed_type_action`, `not_to_exceed_type`, `not_to_exceed_per`, `not_to_exceed`, `fixed_amt_txt`, `zip`, `make_name`, `model_name`, `not_to_exceed1`, `sdamageImg_s`, `distance_amt`, `range_zip`, `damageComma`, `airbagComma`, `driveComma`, `getSDamageComma`, `keyComma`, `titleComma`, `firDamageComma`, `unable_to_verify`, `distance_amt1`, `range_zip1`, `distance_amt2`, `range_zip2`, `final_zip1`, `final_zip2` from condition_report")
        #     return cursor.fetchall()           
        # except:
        #     return ()
        # finally:
        #     con.close()
        
        # Define the columns you want to retrieve
        columns = ["id", "title", "make1", "model1", "make_model", "min_year", "max_year", "min_distance",
                   "max_distance", "min_mileage", "max_mileage", "damage", "damageimg", "airbag", "drive",
                   "sdamage", "key1", "title_type", "fire_damage", "estimate", "not_to_exceed_type_action",
                   "not_to_exceed_type", "not_to_exceed_per", "not_to_exceed", "fixed_amt_txt", "zip",
                   "make_name", "model_name", "not_to_exceed1", "sdamageImg_s", "distance_amt", "range_zip",
                   "damageComma", "airbagComma", "driveComma", "getSDamageComma", "keyComma", "titleComma",
                   "firDamageComma", "unable_to_verify", "distance_amt1", "range_zip1", "distance_amt2",
                   "range_zip2", "final_zip1", "final_zip2"]

        # Use a parameterized query to fetch data
        query = "SELECT {} FROM condition_report where is_deleted='no'  order by id desc".format(", ".join(columns))
        cursor.execute(query)

        # Fetch all rows
        return cursor.fetchall()
    #11-1-2024 start
    def getConditionalFilterDeleted(self,):
        con = Acceptedaps.connect(self)
        cursor = con.cursor()
        
        columns = ["id", "title", "make1", "model1", "make_model", "min_year", "max_year", "min_distance",
                   "max_distance", "min_mileage", "max_mileage", "damage", "damageimg", "airbag", "drive",
                   "sdamage", "key1", "title_type", "fire_damage", "estimate", "not_to_exceed_type_action",
                   "not_to_exceed_type", "not_to_exceed_per", "not_to_exceed", "fixed_amt_txt", "zip",
                   "make_name", "model_name", "not_to_exceed1", "sdamageImg_s", "distance_amt", "range_zip",
                   "damageComma", "airbagComma", "driveComma", "getSDamageComma", "keyComma", "titleComma",
                   "firDamageComma", "unable_to_verify", "distance_amt1", "range_zip1", "distance_amt2",
                   "range_zip2", "final_zip1", "final_zip2"]

        # Use a parameterized query to fetch data
        query = "SELECT {} FROM condition_report where is_deleted='yes'  order by id desc".format(", ".join(columns))
        cursor.execute(query)

        # Fetch all rows
        return cursor.fetchall()
    #11-1-2024 end

    def get_conditional_list(self,):
        con = Acceptedaps.connect(self)
        cursor = con.cursor()
        columns = ["id", "title", "make1", "model1", "make_model", "min_year", "max_year", "min_distance",
                   "max_distance", "min_mileage", "max_mileage", "damage", "damageimg", "airbag", "drive",
                   "sdamage", "key1", "title_type", "fire_damage", "estimate", "not_to_exceed_type_action",
                   "not_to_exceed_type", "not_to_exceed_per", "not_to_exceed", "fixed_amt_txt", "zip",
                   "make_name", "model_name", "not_to_exceed1", "sdamageImg_s", "distance_amt", "range_zip",
                   "damageComma", "airbagComma", "driveComma", "getSDamageComma", "keyComma", "titleComma",
                   "firDamageComma", "unable_to_verify", "distance_amt1", "range_zip1", "distance_amt2",
                   "range_zip2", "final_zip1", "final_zip2","country","state"]

        # Use a parameterized query to fetch data
        query = "SELECT {} FROM condition_report where is_deleted='no'  order by id desc".format(", ".join(columns))
        cursor.execute(query)

        # Fetch all rows
        return cursor.fetchall()

    #11-1-2024 start
    def get_conditional_list_deleted(self,):
        con = Acceptedaps.connect(self)
        cursor = con.cursor()
        columns = ["id", "title", "make1", "model1", "make_model", "min_year", "max_year", "min_distance",
                   "max_distance", "min_mileage", "max_mileage", "damage", "damageimg", "airbag", "drive",
                   "sdamage", "key1", "title_type", "fire_damage", "estimate", "not_to_exceed_type_action",
                   "not_to_exceed_type", "not_to_exceed_per", "not_to_exceed", "fixed_amt_txt", "zip",
                   "make_name", "model_name", "not_to_exceed1", "sdamageImg_s", "distance_amt", "range_zip",
                   "damageComma", "airbagComma", "driveComma", "getSDamageComma", "keyComma", "titleComma",
                   "firDamageComma", "unable_to_verify", "distance_amt1", "range_zip1", "distance_amt2",
                   "range_zip2", "final_zip1", "final_zip2","country","state"]

        # Use a parameterized query to fetch data
        query = "SELECT {} FROM condition_report where is_deleted='yes' order by id desc".format(", ".join(columns))
        cursor.execute(query)

        # Fetch all rows
        return cursor.fetchall()
    #11-1-2024 end


    def getConditionalData(self, data):
        con = Acceptedaps.connect(self)
        cursor = con.cursor()
        try:
            cursor.execute("SELECT * FROM condition_report where id = %s ", (data,))
            makes = cursor.fetchone()
            return makes
        except:
            return ()
        finally:
            con.close()

    #11-1-2024 start
    def deletecondition(self, data):
        con = Acceptedaps.connect(self)
        cursor = con.cursor()
        try:
            cursor.execute("update condition_report set is_deleted='yes' where id = %s", (data['id'],))
            con.commit()
            return True
            return cursor.fetchall()
        except:
            return ()
        finally:
            con.close()

    def deleteconditionhard(self, data):
        con = Acceptedaps.connect(self)
        cursor = con.cursor()
        print(data)
        print("delete from condition_report where id = %s", (data['id'],))
        try:
            cursor.execute("delete from condition_report where id = %s", (data['id'],))
            con.commit()
            return True
            return cursor.fetchall()
        except:
            return ()
        finally:
            con.close()

    def restorecondition(self, data):
        con = Acceptedaps.connect(self)
        cursor = con.cursor()
        try:
            cursor.execute("update condition_report set is_deleted='no' where id = %s", (data['id'],))
            con.commit()
            return True
        except:
            return ()
        finally:
            con.close()
    #11-1-2024 end

    def getconditional(self, id):
        con = Acceptedaps.connect(self)
        cursor = con.cursor()
        
        try:
            cursor.execute("SELECT * FROM condition_report where id = %s ", (id,))
            return cursor.fetchall()
        except:
            return ()
        finally:
            con.close() 
            
    def get_price(self , id):
        con = Acceptedaps.connect(self)
        cursor = con.cursor()
        try:
            cursor.execute("SELECT * FROM `accepted_aps` WHERE offer_id = %s " , (id,))
            return cursor.fetchall()
        except:
            con.rollback()
            return False
        finally:
            con.close()

    def getzipcode(self , data):
        con = Acceptedaps.connect(self)
        cursor = con.cursor()
        try:
            v_zip = data['v_zip']
            cursor.execute("SELECT * FROM `get_location` WHERE DELIVERY_ZIPCODE = '"+v_zip+"'")
            return cursor.fetchone()
        except:
            con.rollback()
            return False
        finally:
            con.close()

    def insert_zip_code(self , data):
        con = Acceptedaps.connect(self)
        cursor = con.cursor()
        try:
            cursor.execute("UPDATE `accepted_aps` SET `zip` = %s , `user_city`= %s,`user_state`= %s,`user_country`= %s WHERE id = %s",(data['v_zip'],data['user_city'],data['user_state'],data['user_country'],data['record_id']))
            con.commit()
            return True
        except:
            con.rollback()
            return False
        finally:
            con.close()
    
    def insert_sharing(self ,sharing_id):
        con = Acceptedaps.connect(self)
        cursor = con.cursor()
        con1 = Acceptedaps.connect(self)
        cursor1 = con1.cursor()
        con2 = Acceptedaps.connect(self)
        cursor2 = con2.cursor()

        try:
            cursor.execute("SELECT * FROM `accepted_aps` WHERE offer_id = %s",(sharing_id))
            a = cursor.fetchall()
            print(a)
            if a != '':
                cursor1.execute("INSERT INTO `accepted_aps` (`year`, `makeid`, `modelid`, `make`, `model`, `make_code`, `vin`, `zip`, `damage`, `title`, `car_key`, `drive`, `mileage`, `airbag`, `fire_damage` , `user_city`, `user_state`, `user_country`,`ipaddr`,`hostname`,`created_at`,`original_price`,`revised_price`, `sdamage`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(a[0][1], a[0][2], a[0][3], a[0][4], a[0][5], a[0][6], a[0][7], a[0][8], a[0][9], a[0][10], a[0][11], a[0][12], a[0][13], a[0][14], a[0][15], a[0][35], a[0][36], a[0][37] ,a[0][31],a[0][32],datetime.datetime.now(),a[0][39],a[0][40],a[0][41]))
                con1.commit()
                inquiry_id = int(cursor1.lastrowid)
                offer_id  = "YC" + str(inquiry_id).zfill(4)
                cursor2.execute("UPDATE accepted_aps set offer_id =%s where id = %s", (offer_id,inquiry_id,))
                con2.commit()
                print(inquiry_id)
                return inquiry_id

        except:
            con.rollback()
            return False
        finally:
            con.close()

    def update_status(self , data):
        con =  Acceptedaps.connect(self)
        cursor = con.cursor()
        try:
            # a = data['']
            # print(data['data'])
            cursor.execute("UPDATE `accepted_aps` SET `status_update`= %s WHERE id = %s",(data['data'],data['id']))
            con.commit()
            return True
        except:
            con.rollback()
            return False
        finally:
            con.close()
            
    def fetchPriceFrom(self , record_id,matchType,condition_id,condition_title):
        con =  Acceptedaps.connect(self)
        cursor = con.cursor()
        try:
            if matchType=='condition report' :
                cursor.execute("UPDATE `accepted_aps` SET `fetch_type`= %s,`fet_confition_id`= %s,`condition_title`= %s WHERE id = %s",(matchType,condition_id,condition_title,record_id))
            else:
                cursor.execute("UPDATE `accepted_aps` SET `fetch_type`= %s WHERE id = %s",(matchType,record_id))
            con.commit()
            return True
        except:
            con.rollback()
            return False
        finally:
            con.close()
            
    def updateofferid(self , data):
        con =  Acceptedaps.connect(self)
        cursor = con.cursor()
        try:
            
            cursor.execute("UPDATE `accepted_aps` SET `minPrice`= %s,`maxPrice`= %s,`perPrice`= %s WHERE id = %s",(data['minPrice'],data['maxPrice'],data['perPrice'],data['id']))
            con.commit()
            return True
        except:
            con.rollback()
            return False
        finally:
            con.close()
            
    def updateofferidcondition(self , data):
        con =  Acceptedaps.connect(self)
        cursor = con.cursor()
        try:
            
            cursor.execute("UPDATE `accepted_aps` SET `con_amt`= %s,`con_type`= %s,`con_plus`= %s,`con_per`= %s,`con_per_amt`= %s WHERE id = %s",(data['con_amt'],data['con_type'],data['con_plus'],data['con_per'],data['con_per_amt'],data['id']))
            con.commit()
            return True
        except:
            con.rollback()
            return False
        finally:
            con.close()
            
    #new code value added start here country
    def getState(self,):
        con = Acceptedaps.connect(self)
        cursor = con.cursor()
        try:           
            cursor.execute("SELECT * FROM states")
            return cursor.fetchall()
        except:
            con.rollback()
            return False
        finally:
            con.close()
            
    def getAllState(self,ids):
        con = Acceptedaps.connect(self)
        cursor = con.cursor()

        my_list = ids.split(",")
        my_lists = tuple(my_list)
        newString = ''
        for k in my_lists:
            newString = newString + "'" + k + "',"

        length= len (newString)
        newString=newString[ :length-1]
        try: 
            print("SELECT Name FROM states where Code IN ("+newString+") ")          
            cursor.execute("SELECT Name FROM states where Code IN ("+newString+") ")
            return cursor.fetchall()
        except:
            con.rollback()
            return False
        finally:
            con.close()
    #new code value added end here country
            
    #code added by pallavi

    def insertauctiondata(self, data, nextproxybidamount):
        con = Acceptedaps.connect(self)
        cursor = con.cursor()
        try:     

            body_damage = ""
            if data['conditionReport']['sections'][0]['questions'][2]['selected'] == 1:
                body_damage = 'FR,RR,SD,TP'

            elif data['conditionReport']['sections'][0]['questions'][1]['selected'] == 1:
                body_damage = 'FR,RR'
            
            elif data['conditionReport']['sections'][0]['questions'][0]['selected'] == 1:
                body_damage = 'SD'

            airbag_value = 'N'
            if data['conditionReport']['sections'][5]['questions'][13]['selected'] == 1:
                airbag_value = 'Y'

            if(data['conditionReport']['sections'][3]['questions'][0]['selected'] == 0 and data['conditionReport']['sections'][2]['questions'][2]['selected'] == 0):
                start_and_drive = "D,S"
            elif(data['conditionReport']['sections'][3]['questions'][0]['selected'] == 0):
                start_and_drive = "D"
            else:
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
            if data['conditionReport']['sections'][7]['questions'][0]['selected'] == 1 and (data['conditionReport']['sections'][7]['questions'][1]['selected'] == 1 or data['conditionReport']['sections'][0]['questions'][9]['selected'] == 1):
                title_type = 'clean title,Salvage Rebuilt'

            elif data['conditionReport']['sections'][7]['questions'][0]['selected'] == 0 and (data['conditionReport']['sections'][7]['questions'][1]['selected'] == 1 or data['conditionReport']['sections'][0]['questions'][9]['selected'] == 1):
                title_type = 'Unknown,Salvage Rebuilt'

            elif data['conditionReport']['sections'][7]['questions'][1]['selected'] == 1 or data['conditionReport']['sections'][0]['questions'][9]['selected'] == 1:
                title_type = 'Salvage Rebuilt'

            elif data['conditionReport']['sections'][7]['questions'][0]['selected'] == 1:
                title_type = 'clean title'

            elif data['conditionReport']['sections'][7]['questions'][0]['selected'] == 0:
                title_type = 'Unknown'

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
                
                cursor.execute('INSERT INTO auctions (year,make,model,auction_id,location,odometer,action_end_datetime,zip_code,bid_amount,bid_count,vin,status,minor_body_type_ans,modrate_body_type_ans,major_body_type_ans,airbag_deployed_ans,engine_start_or_not,engine_start_not_run,transmission_issue_ans,frame_issue_ans,title_absent_ans,title_branded_ans,vehicle_display_name,start_and_drive_ans,next_bid_amount,start_price,is_high_bidder,created_at,body_damage,reserve_met,next_proxy_bid_amount,action_start_datetime,lights,auction_image_url,auction_url, distance,transmission,trim,drivetrain,engine,fuel_type,basic_color) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', 
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
                                nextproxybidamount,
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
                                data['basicColor']
                                )),
                
                con.commit()
            else:
                cursor.execute('UPDATE auctions SET year = %s, make = %s, model = %s, location = %s, odometer= %s, action_end_datetime = %s, zip_code = %s, bid_amount = %s, bid_count = %s, vin = %s, status = %s, minor_body_type_ans = %s, modrate_body_type_ans = %s, major_body_type_ans = %s, airbag_deployed_ans = %s, engine_start_or_not = %s, engine_start_not_run = %s, transmission_issue_ans = %s, frame_issue_ans = %s, title_absent_ans = %s, title_branded_ans = %s, vehicle_display_name = %s, start_and_drive_ans = %s, next_bid_amount = %s, start_price = %s, is_high_bidder = %s, updated_at = %s, body_damage = %s, reserve_met = %s, next_proxy_bid_amount = %s, action_start_datetime = %s, lights = %s, auction_image_url =%s, auction_url = %s, distance = %s, transmission = %s, trim = %s, drivetrain = %s, engine = %s, fuel_type = %s, basic_color = %s where auction_id = %s',(data['year'],data['make'],data['model'],data['location'],data['odometer'],data['endTime'],data['postalCode'],data['bidAmount'],data['bidCount'],data['vin'],data['status'], 
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
                    nextproxybidamount,
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
                    data['id']))
                
                con.commit()


        except:
            return ()
        finally:
            con.close()

    def auctionconditionreport(self, data):
        con = Acceptedaps.connect(self)
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

            if fetchone is None:
                print('Inserting')
                cursor.execute('INSERT into auction_condition_report (auction_id, air_bag, vehicle_inop, engine_does_not_start, engine_does_not_crank, penetrating_rust,frame_damage,engine_noise,engine_hesitation,timing_chain_issue,abnormal_exhaust_smoke,head_gasket_issue,drivetrain_issue,transmission_issue,minor_body_type,moderate_body_type,major_body_type,glass_damage,lights_damage,aftermarket_parts_exterior,poor_quality_repairs,surface_rust,heavy_rust,obdii_codes,incomplete_readiness_monitors,seat_damage,dashboard_damage,interior_trim_damage,electronics_issue,break_issue,suspension_issue,steering_issue,aftermarket_wheels,damaged_wheels,damaged_tiles,tire_measurements,aftermarket_mechanical,engine_accessory_issue,title_absent,title_branded,modrate_body_rust,flood_damage,scratches, minor_body_rust, major_body_rust, hail_damage, mismatched_paint, paint_meter_readings, previous_paint_work, jump_start_required,oil_intermix_dipstick_v2,fluid_leaks,emissions_modifications,catalytic_converters_missing,exhaust_modifications,exhaust_noise,suspension_modifications,engine_does_not_stay_running,check_engine_light,airbag_light,brake_light,traction_control_light,tpms_light,battery_light,other_warning_light,oversized_tires,uneven_tread_wear,mismatched_tires,missing_spare_tire, carpet_damage, headliner_damage, interior_order, crank_windows, no_factory_ac,five_digit_odometer, sunroof, navigation, aftermarket_stereo, hvac_not_working, leather_seats, true_mileage_unknown,off_lease_vehicle,repair_order_attached, repossession, repossession_papers_wo_title, mobility, transferrable_registration, sold_on_bill_of_sale,aftermarket_sunroof,backup_camera,charging_cable,engine_overheats,supercharger_issue, emissions_issue, oil_level_issue, oil_condition_issue, coolant_level_issue) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (data['id'],airbag_json_string,vehicle_json_string,engine_does_not_start_json_string,engine_does_not_crank_json_string,penetrating_rust_json_string,unbody_damage_json_string,engine_noise_json_string,engine_hesitation_json_string,timing_chain_issue_json_string,abnormal_exhaust_smoke_json_string,head_gasket_issue_json_string,drivetrain_issue_json_string,transmission_issue_json_string,minor_body_type_json_string,moderate_body_type_json_string,major_body_type_json_string,glass_damage_json_string,lights_damage_json_string,aftermarket_parts_exterior_json_string,poor_quality_repairs_json_string,surface_rust_json_string,heavy_rust_json_string,obdii_codes_json_string,incomplete_readiness_monitors_json_string,seat_damage_json_string,dashboard_damage_json_string,interior_trim_damage_json_string,electronics_issue_json_string,break_issue_json_string,suspension_issue_json_string,steering_issue_json_string,aftermarket_wheels_json_string,damaged_wheels_json_string,damaged_tiles_json_string,tire_measurements_json_string,aftermarket_mechanical_json_string,engine_accessory_issue_json_string,title_absent_json_string,title_branded_json_string,modrate_body_rust_json_string,flood_damage_json_string,scratches_json_string, minor_body_rust_json_string, major_body_rust_json_string, hail_damage_json_string, mismatched_paint_json_string, paint_meter_readings_json_string, previous_paint_work_json_string, jump_start_required_json_string,oil_intermix_dipstick_v2_json_string,fluid_leaks_json_string,emissions_modifications_json_string,catalytic_converters_missing_json_string,exhaust_modifications_json_string,exhaust_noise_json_string,suspension_modifications_json_string,engine_does_not_stay_running_json_string,check_engine_light_json_string,airbag_light_json_string,brake_light_json_string,traction_control_light_json_string,tpms_light_json_string,battery_light_json_string,other_warning_light_json_string,oversized_tires_json_string,uneven_tread_wear_json_string,mismatched_tires_json_string,missing_spare_tire_json_string, carpet_damage, headliner_damage, interior_order, crank_windows, no_factory_ac,five_digit_odometer, sunroof, navigation, aftermarket_stereo, hvac_not_working, leather_seats,true_mileage_unknown,off_lease_vehicle,repair_order_attached, repossession, repossession_papers_wo_title, mobility,transferrable_registration,sold_on_bill_of_sale,aftermarket_sunroof,backup_camera,charging_cable,engine_overheats,supercharger_issue, emissions_issue, oil_level_issue, oil_condition_issue, coolant_level_issue))
            else:
                print('Updating')
                cursor.execute('UPDATE auction_condition_report SET air_bag = %s, vehicle_inop = %s, engine_does_not_start = %s, engine_does_not_crank = %s, penetrating_rust = %s,frame_damage = %s, engine_noise = %s, engine_hesitation = %s, timing_chain_issue = %s, abnormal_exhaust_smoke = %s, head_gasket_issue = %s,	drivetrain_issue = %s, transmission_issue =%s, minor_body_type = %s, moderate_body_type = %s, major_body_type = %s, glass_damage = %s, lights_damage = %s, aftermarket_parts_exterior = %s, poor_quality_repairs = %s, surface_rust = %s, heavy_rust = %s, obdii_codes = %s, incomplete_readiness_monitors = %s, seat_damage = %s, dashboard_damage = %s, interior_trim_damage = %s, electronics_issue =%s, break_issue =%s, suspension_issue = %s, steering_issue = %s, aftermarket_wheels = %s, damaged_wheels = %s,  damaged_tiles = %s, tire_measurements = %s, aftermarket_mechanical = %s, engine_accessory_issue = %s, title_absent = %s, title_branded = %s, modrate_body_rust = %s, flood_damage = %s, scratches = %s, minor_body_rust = %s, major_body_rust = %s, hail_damage = %s, mismatched_paint = %s, paint_meter_readings = %s, previous_paint_work = %s, jump_start_required = %s, oil_intermix_dipstick_v2 = %s, fluid_leaks = %s, emissions_modifications = %s, catalytic_converters_missing = %s, exhaust_modifications = %s, exhaust_noise = %s, suspension_modifications = %s, engine_does_not_stay_running = %s, check_engine_light = %s, airbag_light = %s, brake_light = %s, traction_control_light = %s, 	tpms_light = %s, battery_light = %s, other_warning_light = %s, oversized_tires = %s, uneven_tread_wear = %s, mismatched_tires = %s, missing_spare_tire = %s, carpet_damage = %s, headliner_damage = %s, interior_order = %s, crank_windows = %s, no_factory_ac = %s, five_digit_odometer = %s, sunroof = %s, navigation = %s, aftermarket_stereo = %s, hvac_not_working = %s,leather_seats = %s, true_mileage_unknown = %s, off_lease_vehicle = %s, repair_order_attached = %s, repossession = %s, repossession_papers_wo_title = %s, mobility = %s, transferrable_registration = %s, sold_on_bill_of_sale = %s, aftermarket_sunroof = %s, backup_camera = %s, charging_cable = %s, engine_overheats = %s, supercharger_issue = %s, emissions_issue = %s, oil_level_issue = %s, oil_condition_issue = %s, coolant_level_issue = %s where auction_id = %s', (airbag_json_string,vehicle_json_string,engine_does_not_start_json_string,engine_does_not_crank_json_string,penetrating_rust_json_string,unbody_damage_json_string,engine_noise_json_string,engine_hesitation_json_string,timing_chain_issue_json_string, abnormal_exhaust_smoke_json_string, head_gasket_issue_json_string,drivetrain_issue_json_string,transmission_issue_json_string,minor_body_type_json_string,moderate_body_type_json_string,major_body_type_json_string,glass_damage_json_string,lights_damage_json_string,aftermarket_parts_exterior_json_string,poor_quality_repairs_json_string,surface_rust_json_string,heavy_rust_json_string,obdii_codes_json_string,incomplete_readiness_monitors_json_string,seat_damage_json_string,dashboard_damage_json_string,interior_trim_damage_json_string,electronics_issue_json_string,break_issue_json_string,suspension_issue_json_string,steering_issue_json_string,aftermarket_wheels_json_string,damaged_wheels_json_string,damaged_tiles_json_string,tire_measurements_json_string,aftermarket_mechanical_json_string,engine_accessory_issue_json_string,title_absent_json_string,title_branded_json_string,modrate_body_rust_json_string,flood_damage_json_string,scratches_json_string, minor_body_rust_json_string, major_body_rust_json_string, hail_damage_json_string, mismatched_paint_json_string, paint_meter_readings_json_string, previous_paint_work_json_string,jump_start_required_json_string,oil_intermix_dipstick_v2_json_string,fluid_leaks_json_string,emissions_modifications_json_string,catalytic_converters_missing_json_string,exhaust_modifications_json_string,exhaust_noise_json_string,suspension_modifications_json_string,engine_does_not_stay_running_json_string,check_engine_light_json_string,airbag_light_json_string,brake_light_json_string,traction_control_light_json_string,tpms_light_json_string,battery_light_json_string,other_warning_light_json_string,oversized_tires_json_string,uneven_tread_wear_json_string,mismatched_tires_json_string,missing_spare_tire_json_string, carpet_damage, headliner_damage, interior_order, crank_windows, no_factory_ac,five_digit_odometer, sunroof, navigation, aftermarket_stereo, hvac_not_working, leather_seats, true_mileage_unknown, off_lease_vehicle,repair_order_attached, repossession, repossession_papers_wo_title, mobility, transferrable_registration, sold_on_bill_of_sale, aftermarket_sunroof, backup_camera, charging_cable, engine_overheats, supercharger_issue, emissions_issue, oil_level_issue, oil_condition_issue, coolant_level_issue, data['id']))
            con.commit()
            return True
        except:
            return ()
        finally:
            con.close()

    def countslights(self, auctions):
        con = Acceptedaps.connect(self)
        cursor = con.cursor()
        try:
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


            # if orange > 0 and yellow > 0 and red > 0 and blue > 0:
            #     lights_count = {'orange': orange, 'yellow': yellow, 'red': red, 'blue': blue}   

            # if orange > 0 and yellow > 0 and red > 0:
            #     lights_count = {'orange': orange, 'yellow': yellow, 'red': red}
            
            # if orange > 0 and yellow > 0 and blue > 0:
            #     lights_count = {'orange': orange, 'yellow': yellow, 'blue': blue}

            # if yellow > 0 and red > 0 and blue > 0:
            #     lights_count = {'yellow': yellow, 'red': red, 'blue': blue}
            
            # if orange > 0 and red > 0 and blue > 0:
            #     lights_count = {'orange': orange, 'red': red, 'blue': blue}
            
            # if yellow > 0 and red > 0:
            #     lights_count = {'yellow': yellow, 'red': red}
            
            # if orange > 0 and yellow > 0:
            #     lights_count = {'orange': orange, 'yellow': yellow}
            #     print('lights_count11', lights_count)
            
            # if orange > 0 and red > 0:
            #     print('ggg')
            #     lights_count = {'orange': orange, 'red': red}

            # if orange > 0 and blue > 0:
            #     print('ggg')
            #     lights_count = {'orange': orange, 'blue': blue}
            
            # if yellow > 0 and blue > 0:
            #     lights_count = {'yellow': yellow, 'blue': blue}
            
            # if red > 0 and blue > 0:
            #     lights
            # _count = {'red': red, 'blue': blue}
            
            # color_count = {
            #     "orange": orange,
            #     "yellow": yellow,
            #     "red": red,
            #     "blue": blue
            # }

            # filtered_color_count = {color: count for color, count in color_count.items() if count > 0}

            # json_data = json.dumps(filtered_color_count)
            # print('newwwww',json_data)
            
            # if orange > 0:
            #     print("orange")
            #     lights_count = {'orange': orange}
            
            # if yellow > 0:
            #     print('yellow')
            #     lights_count = {'yellow': yellow}
            
            # if red > 0:
            #     lights_count = {'red': red}
            
            # if blue > 0:
            #     lights_count = {'blue': blue}

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
        con = Acceptedaps.connect(self)
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
                    ({} OR titleComma = '' )
                ) AND id = {}) ORDER BY id DESC;
            """.format(make_name, model_name, max_year, min_year, max_mileage, min_mileage,
                    final_zip, state, state,
                    ' AND '.join(["FIND_IN_SET('{}', sdamageImg_s)".format(body) for body in body_damage]),
                    airbagComma, 
                    ' AND '.join(["FIND_IN_SET('{}', driveComma)".format(drive) for drive in driveComma]),
                    ' AND '.join(["FIND_IN_SET('{}', getSDamageComma)".format(mechnical_issue) for mechnical_issue in mechnicalComma]),
                    ' AND '.join(["FIND_IN_SET('{}', titleComma)".format(title) for title in titleComma]),
                    
                    id_value)
                        
            cursor.execute(query)

            return cursor.fetchall()
            #run sql

            # query = """
            #     SELECT * FROM condition_report
            #     WHERE is_deleted='no' AND (
            #         (FIND_IN_SET('{}', make_name) OR FIND_IN_SET('all', make_name)) AND
            #         (FIND_IN_SET('{}', model_name) OR FIND_IN_SET('all', model_name)) AND
            #         (max_year >= {} AND min_year <= {}) AND
            #         (max_mileage >= {} AND min_mileage <= {}) AND
            #         (final_zip = '' OR FIND_IN_SET({}, final_zip)) AND
            #         ((FIND_IN_SET('{}', state) OR state = '' OR FIND_IN_SET('all', make_name) OR
            #         max_year = '' OR min_year = '' OR max_mileage = '' OR min_mileage = '' OR
            #         FIND_IN_SET('{}', state) OR state = '') AND
            #         (FIND_IN_SET('{}', airbagComma) OR airbagComma = '') AND
            #         (FIND_IN_SET('{}', driveComma) OR driveComma = '') AND
            #         ({} OR getSDamageComma = '') AND 
            #         ({} OR titleComma = '' )
            #     ) AND id = {}) ORDER BY id DESC;
            # """.format(make_name, model_name, max_year, min_year, max_mileage, min_mileage,
            #         final_zip, state, state, airbagComma, driveComma, 
            #         ' AND '.join(["FIND_IN_SET('{}', getSDamageComma)".format(mechnical_issue) for mechnical_issue in mechnicalComma]),
            #         ' AND '.join(["FIND_IN_SET('{}', titleComma)".format(title) for title in titleComma]),
            #         id_value)
                        
            # cursor.execute(query)
            

            #end sql 
            
        except:
            return ()
        finally:
            con.close()  

    def getauctions(self,):
        con = Acceptedaps.connect(self)
        cursor = con.cursor()
        try:    
            current_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            # user_id = session['acv_user_id'] 
            
            # print('''
            #     SELECT 
            #         auctions.*, 
            #         MAX(bids.bid_amount) AS auction_highest_bid_amount
            #     FROM 
            #         auctions 
            #     JOIN 
            #         bids ON bids.auction_id = auctions.auction_id 
            #     WHERE 
            #         auctions.action_end_datetime > %s 
            #         AND auctions.status = "active" 
            #         AND bids.user_id = %s 
            #     GROUP BY 
            #         auctions.auction_id
            #     ORDER BY 
            #         auctions.action_end_datetime ASC
            # ''', (current_datetime, user_id))
            # cursor.execute('''
            #     SELECT 
            #         auctions.*, 
            #         MAX(bids.bid_amount) AS auction_highest_bid_amount
            #     FROM 
            #         auctions 
            #     JOIN 
            #         bids ON bids.auction_id = auctions.auction_id 
            #     WHERE 
            #         auctions.action_end_datetime > %s 
            #         AND auctions.status = "active" 
            #         AND bids.user_id = %s 
            #     GROUP BY 
            #         auctions.auction_id
            #     ORDER BY 
            #         auctions.action_end_datetime ASC
            # ''', (current_datetime, user_id))

            
            cursor.execute('SELECT * from auctions WHERE action_end_datetime > %s AND status = "active" ORDER BY action_end_datetime ASC', (current_datetime,))
         
            return cursor.fetchall()
        except:
            return ()
        finally:
            con.close()  

    def getauctionsbid(self,):
        con = Acceptedaps.connect(self)
        cursor = con.cursor()
        try:    
            cursor.execute('SELECT * from auctions Where action_end_datetime > %s AND is_match = %s AND status = "active" ORDER BY action_end_datetime DESC', (datetime.datetime.now(),1))
            return cursor.fetchall()
        except:
            return ()
        finally:
            con.close() 

    def getauctionsforbid(self,):
        con = Acceptedaps.connect(self)
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
        con = Acceptedaps.connect(self)
        cursor = con.cursor()
        try:     
            if selected_report_id == "":
                cursor.execute("SELECT * FROM condition_report where is_deleted='no' AND condition_type = 'ACV' order by id desc")
            else:
                cursor.execute('SELECT * FROM condition_report WHERE id = %s', (selected_report_id,))
            return cursor.fetchall()
        except:
            return ()
        finally:
            con.close() 

    def deleteAuction(self):
        con = Acceptedaps.connect(self)
        cursor = con.cursor()
        try:  
            cursor.execute("SELECT * from auctions Where bid_count = 0 and status = 'active'")
            aucrions = cursor.fetchall()
            for auction in aucrions:
                cursor.execute('DELETE FROM auction_condition_report WHERE auction_id = %s', (auction[4],))
                cursor.execute('DELETE FROM auctions WHERE auction_id = %s', (auction[4],))
                logging.info(auction[4],"Auction Deleted")
            con.commit()
        except:
            return ()
        finally:
            con.close() 

    def searchauction(self, searchval,status):
        con = Acceptedaps.connect(self)
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
        con = Acceptedaps.connect(self)
        cursor = con.cursor()
        try:
            cursor.execute('UPDATE auctions SET bid_amount = %s WHERE auction_id = %s', (bid, id))
            con.commit()
        except:
            return ()
        finally:
            con.close()

    def addbid(self, id, bid, user_id):
        con = Acceptedaps.connect(self)
        cursor = con.cursor()

        try:
            cursor.execute('SELECT * from bids where auction_id = %s and user_id = %s', (id, user_id))
            auction_bid = cursor.fetchone()

            if auction_bid is not None:
                cursor.execute('UPDATE bids SET bid_amount = %s, bid_datetime = %s WHERE auction_id = %s and user_id = %s', (bid, datetime.datetime.now(), id, user_id))
            else:
                cursor.execute('INSERT INTO bids (auction_id, bid_amount, bid_datetime, user_id) VALUES (%s, %s, %s, %s)', (id, bid, datetime.datetime.now(),user_id))
            con.commit()
        except:
            return ()
        finally:
            con.close()

    def winlostauctions(self):
        con = Acceptedaps.connect(self)
        cursor = con.cursor()
        try:
            current_datetime = datetime.datetime.now()
            auction_end_time = current_datetime.strftime("%Y-%m-%d %H:%M:%S ")
            cursor.execute('SELECT * FROM auctions WHERE action_end_datetime < %s AND bid_amount != %s', (auction_end_time, 0))
            expire_auctions = cursor.fetchall()

            won_auction_ids = []
            lost_auction_ids = []

            for auction in expire_auctions:
                if auction[27] == 1 and auction[36] == 1:
                    won_auction_ids.append(auction[4])
                elif auction[27] == 0:
                    lost_auction_ids.append(auction[4])

            if won_auction_ids:
                cursor.execute('UPDATE auctions SET win = %s WHERE auction_id IN %s', (1, tuple(won_auction_ids)))
                # logging.info(won_auction_ids,"Auction Won")
                con.commit()

            if lost_auction_ids:
                cursor.execute('UPDATE auctions SET lost = %s WHERE auction_id IN %s', (1, tuple(lost_auction_ids)))
                # logging.info(lost_auction_ids,"Auction Lost")
                con.commit()

        except:
            return ()
        finally:
            cursor.close()
            con.close()

    def getMisseauction(self,):
        con = Acceptedaps.connect(self)
        cursor = con.cursor()
        try:
            cursor.execute('SELECT * FROM auctions WHERE is_match = %s and action_end_datetime > %s and status = "active"', (0,datetime.datetime.now()))
            return  cursor.fetchall()
        except:
            return ()
        finally:
            con.close()
    
    def getwonauction(self,):
        con = Acceptedaps.connect(self)
        cursor = con.cursor()
        try:
            cursor.execute('SELECT * FROM auctions WHERE win = %s', (1,))
            return  cursor.fetchall()
        except:
            return ()
        finally:
            con.close()

    def getlostauction(self,):
        con = Acceptedaps.connect(self)
        cursor = con.cursor()
        try:
            cursor.execute('SELECT * FROM auctions WHERE lost = %s', (1,))
            return  cursor.fetchall()
        except:
            return ()
        finally:
            con.close()
    
    def getauctioncondition(self, id):
        con = Acceptedaps.connect(self)
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
        con = Acceptedaps.connect(self)
        cursor = con.cursor()
        try:
            cursor.execute('UPDATE auctions SET is_high_bidder = %s, next_bid_amount = %s WHERE auction_id = %s', (is_high_bidder,nextbidamount,id))
            con.commit()
        except:
            return ()
        finally:
            con.close()
    
    def updateproxydata(self,id,proxybidamount):
        con = Acceptedaps.connect(self)
        cursor = con.cursor()
        try:
            cursor.execute('UPDATE auctions SET proxy_bid_amount = %s WHERE auction_id = %s', (proxybidamount,id))
            con.commit()
        except:
            return ()
        finally:
            con.close()

    def matchauction(self,id,is_match):
        con = Acceptedaps.connect(self)
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
        con = Acceptedaps.connect(self)
        cursor = con.cursor()
        try:
            cursor.execute('SELECT * FROM auctions WHERE status = "run_list" and action_start_datetime > %s',datetime.datetime.now())
            return cursor.fetchall()
        except:
            return ()
        finally:
            con.close()

    # code ended by pallavi


               

        



