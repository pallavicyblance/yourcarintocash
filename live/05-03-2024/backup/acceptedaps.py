import numpy as np
import pymysql
import smtplib
import datetime
import json

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
        return pymysql.connect(host="localhost", user="carintocash1", password="zkY$$}_vtXO=", database="carintocash1", charset='utf8mb4')
        #return pymysql.connect(host="localhost", user="root", password="", database="carintocash", charset='utf8mb4')
    def read(self, id,param,param1):
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
        try:
            if id == None:
                if param:
                    if status=='monthly':
                        cursor.execute("SELECT * FROM accepted_aps where MONTH(`created_at`) = MONTH(now()) and YEAR(`created_at`) = YEAR(now()) ORDER BY id DESC  ")
                    elif status=='weekly':
                        cursor.execute("SELECT * FROM accepted_aps where week(`created_at`) = week(now()) ORDER BY id DESC  ")
                    elif status=='today':
                        cursor.execute("SELECT * FROM accepted_aps WHERE DATE_FORMAT(`created_at`, '%Y-%m-%d') = CURDATE()  ")
                    elif status=='userfrom':
                        cursor.execute("SELECT * FROM accepted_aps WHERE `ref_id` !=''  ")
                    else:
                        if param1:
                            cursor.execute("SELECT * FROM accepted_aps where status='"+status+"' ORDER BY dispatched ASC  ")
                        else:
                            cursor.execute("SELECT * FROM accepted_aps where status='"+status+"' ORDER BY id DESC  ")
                else:
                    cursor.execute("SELECT * FROM accepted_aps ORDER BY id DESC  ")
            else:
                cursor.execute(
                    "SELECT * FROM accepted_aps where id = %s ", (id,))
            return cursor.fetchall()
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

                cursor.execute("INSERT INTO accepted_aps(year, makeid, modelid, make, model, make_code, vin, ipaddr, hostname,created_at,user_city,user_state,user_country,ref_id) VALUES(%s, %s, %s, %s, %s, %s, %s, %s,  %s,  %s, %s,%s,%s,%s)", (data['year'], data['make_id'], data['model_id'], data['make'], data['model'],  data['make_code'], data['vin'],  data['ipaddr'], data['hostname'],datetime.datetime.now(),data['user_city'],data['user_state'],data['user_country'],aaa,))
                con.commit()
                inquiry_id = int(cursor.lastrowid)
                #offer_id  = "YCIC" + str(inquiry_id)
                offer_id  = "YC" + str(inquiry_id).zfill(4)
                cursor1.execute("UPDATE accepted_aps set offer_id =%s where id = %s", (offer_id,inquiry_id,))
                con1.commit()
                return inquiry_id
            else:
                id = data['record_id']
                mileage1 = data['mileage'] + ',000'
                
                if mileage1==',000':
                    mileage1 = ''
                if data['currenttab']=='17':
                    if data['sharing_genrate_id'] !='' :
                        cursor.execute("UPDATE accepted_aps set status = %s,  ownerfname = %s,  payeefname = %s  where id = %s",('accept', data['ownerfname'],  data['payeefname'], id,))
                        con.commit()
                    else:
                        cursor.execute("UPDATE accepted_aps set status = %s, year = %s, makeid = %s, modelid = %s , make = %s , model = %s, zip = %s, damage = %s, title = %s, car_key = %s, drive = %s, mileage = %s, airbag = %s, fire_damage = %s , type = %s , locationname = %s , address1 = %s, address2 = %s, city = %s , state = %s, fname = %s,  phone = %s, alternatephone = %s, ownerfname = %s,  payeefname = %s ,  sdamage = %s where id = %s",('accept',data['year'], data['make_id'], data['model_id'], data['make'], data['model'], data['v_zip'], data['damage'], data['title'], data['key'], data['drive'], mileage1, data['airbag'], data['fire_damage'], data['type'], data['locationname'], data['address1'], data['address2'], data['city'], data['state'], data['fname'],  data['phone'], data['alternatephone'], data['ownerfname'],  data['payeefname'],data['sdamage'], id,))
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
                    cursor.execute("UPDATE accepted_aps set   original_price = %s,revised_price = %s,year = %s, makeid = %s, modelid = %s , make = %s , model = %s, zip = %s, damage = %s, title = %s, car_key = %s, drive = %s, mileage = %s, airbag = %s, fire_damage = %s , type = %s , locationname = %s , address1 = %s, address2 = %s, city = %s , state = %s, fname = %s,  phone = %s, alternatephone = %s, ownerfname = %s,  payeefname = %s ,  sdamage = %s where id = %s",(data['original_price'],data['revised_price'],data['year'], data['make_id'], data['model_id'], data['make'], data['model'], data['v_zip'], data['damage'], data['title'], data['key'], data['drive'], mileage1, data['airbag'], data['fire_damage'], data['type'], data['locationname'], data['address1'], data['address2'], data['city'], data['state'], data['fname'],  data['phone'], data['alternatephone'], data['ownerfname'], data['payeefname'],data['sdamage'], id,))
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

    def getdeclineoffer(self):
        con = Acceptedaps.connect(self)
        cursor = con.cursor()
        try:
            cursor.execute("SELECT * FROM `accepted_aps` WHERE status = %s" ,('Decline'))
            return cursor.fetchall()
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
            print('insert')
            cursor.execute("INSERT INTO condition_report(title, estimate, not_to_exceed_type_action, not_to_exceed_type, not_to_exceed_per, not_to_exceed, fixed_amt_txt, make_model, min_year, max_year, min_mileage, max_mileage, zip, damage, damageimg, make_name, model_name, make1, model1, sdamageImg_s, range_zip, damageComma, airbagComma, driveComma, getSDamageComma, keyComma, titleComma, firDamageComma, unable_to_verify, state, country, final_zip, sessionid ) VALUES( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s , %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s )",(data['filter_title'],estimate,data['not_to_exceed_type_action'], data['not_to_exceed_type'], data['not_to_exceed_per'], data['not_to_exceed'] , data['fixed_amt_txt'], abc, data['year_min'],data['year_max'],data['mileage_min'],data['mileage_max'],data['zip'],getDamage1,abc1,make_name1,model_name1,make_id_s,model_id_s,sdamageImg_s,rangearray,damageComma,airbagComma,driveComma,getSDamageComma,keyComma,titleComma,firDamageComma,unable_to_verify_data, stateComma,usa_data, allZip, sessionid ))
            con.commit()
            condition_id = cursor.lastrowid
            #print(condition_id)
        else:
            print("update")
            #cursor.execute("UPDATE condition_report set title = %s, estimate = %s, not_to_exceed_type_action = %s, not_to_exceed_type = %s , not_to_exceed_per = %s , not_to_exceed = %s, fixed_amt_txt = %s , make_model = %s, min_mileage = %s, max_mileage=%s,  zip=%s , damage=%s , damageimg=%s , make_name=%s , model_name=%s ,  make1=%s , model1=%s,sdamageImg_s=%s ,min_year=%s ,max_year=%s,distance_amt=%s,range_zip=%s,final_zip=%s,damageComma=%s,airbagComma=%s,driveComma=%s,getSDamageComma=%s,keyComma=%s,titleComma=%s,firDamageComma=%s,unable_to_verify=%s,distance_amt1=%s,range_zip1=%s,distance_amt2=%s,range_zip2=%s,final_zip1=%s,final_zip2=%s,final_zip3=%s,final_zip5=%s,state=%s,country=%s    where id = %s",(data['filter_title'], estimate,data['not_to_exceed_type_action'], data['not_to_exceed_type'],data['not_to_exceed_per'], data['not_to_exceed'] , data['fixed_amt_txt'],adcostrray,data['mileage_min'],data['mileage_max'],data['zip'],getDamage1,abc1,make_name1,model_name1,make_id_s,model_id_s,sdamageImg_s,data['year_min'],data['year_max'],data['distance_amt'],data['range_zip'],allZip,damageComma,airbagComma,driveComma,getSDamageComma,keyComma,titleComma,firDamageComma,unable_to_verify_data,data['distance_amt1'],data['range_zip1'],data['distance_amt2'],data['range_zip2'],allZip1,allZip2,allZip3,allZip5,stateComma,usa_data,data['condition_report_id']))
            #cursor.execute("UPDATE condition_report set title = %s, estimate = %s, not_to_exceed_type_action = %s, not_to_exceed_type = %s , not_to_exceed_per = %s , not_to_exceed = %s, fixed_amt_txt = %s , make_model = %s, min_mileage = %s, max_mileage=%s,  zip=%s , damage=%s , damageimg=%s , make_name=%s , model_name=%s ,  make1=%s , model1=%s,sdamageImg_s=%s ,min_year=%s ,max_year=%s,distance_amt=%s,range_zip=%s,final_zip=%s,damageComma=%s,airbagComma=%s,driveComma=%s,getSDamageComma=%s,keyComma=%s,titleComma=%s,firDamageComma=%s,unable_to_verify=%s,distance_amt1=%s,range_zip1=%s,distance_amt2=%s,range_zip2=%s,final_zip1=%s,final_zip2=%s,final_zip3=%s,final_zip5=%s,state=%s,country=%s    where id = %s",(data['filter_title'], estimate,data['not_to_exceed_type_action'], data['not_to_exceed_type'],data['not_to_exceed_per'], data['not_to_exceed'] , data['fixed_amt_txt'],adcostrray,data['mileage_min'],data['mileage_max'],data['zip'],getDamage1,abc1,make_name1,model_name1,make_id_s,model_id_s,sdamageImg_s,data['year_min'],data['year_max'],data['distance_amt'],data['range_zip'],allZip,damageComma,airbagComma,driveComma,getSDamageComma,keyComma,titleComma,firDamageComma,unable_to_verify_data,data['distance_amt1'],data['range_zip1'],data['distance_amt2'],data['range_zip2'],allZip1,allZip2,allZip3,allZip5,stateComma,usa_data,data['condition_report_id']))
            #con.commit()
            #condition_id = data['condition_report_id']
            cursor.execute("UPDATE condition_report set title = %s, estimate = %s, not_to_exceed_type_action = %s, not_to_exceed_type = %s, not_to_exceed_per = %s, not_to_exceed = %s, fixed_amt_txt = %s , make_model = %s, min_year = %s, max_year = %s, min_mileage = %s, max_mileage = %s, zip = %s, damage = %s, damageimg = %s, make_name = %s, model_name=%s, make1=%s, model1 = %s, sdamageImg_s = %s, range_zip = %s, damageComma = %s, airbagComma = %s, driveComma = %s, getSDamageComma = %s, keyComma = %s, titleComma = %s, firDamageComma = %s, unable_to_verify = %s , state  = %s, country = %s, final_zip = %s where id = %s", (data['filter_title'],estimate,data['not_to_exceed_type_action'], data['not_to_exceed_type'], data['not_to_exceed_per'], data['not_to_exceed'] , data['fixed_amt_txt'], abc, data['year_min'],data['year_max'],data['mileage_min'],data['mileage_max'],data['zip'],getDamage1,abc1,make_name1,model_name1,make_id_s,model_id_s,sdamageImg_s,rangearray,damageComma,airbagComma,driveComma,getSDamageComma,keyComma,titleComma,firDamageComma,unable_to_verify_data, stateComma, usa_data, allZip, data['condition_report_id']))
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
        #print(data)
        #print("delete from condition_report where id = %s", (data['id'],))
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
            cursor.execute("SELECT * FROM `zipcode` WHERE zipcode = '"+v_zip+"'")
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
            
    def updateimg(self , ids,filename):
        con =  Acceptedaps.connect(self)
        cursor = con.cursor()
        try:
            cursor.execute("UPDATE `accepted_aps` SET `chat_imag`= %s WHERE id = %s",(filename,ids))
            con.commit()
            return True
        except:
            con.rollback()
            return False
        finally:
            con.close()
    #new code value added end here country

