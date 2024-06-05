from flask import Flask, flash 
import pymysql
from module.acceptedaps import Acceptedaps
from module.acv import ACV
# from Misc.dbconnect import *
import http.client
import json
acceptedaps = Acceptedaps()
acv = ACV()

class Proqoute:
    def connect(self):
        # return connect()
        return pymysql.connect(host="localhost", user="root", password="", database="carcash", charset='utf8mb4') 

    def generateproqoute():
        proqoute_instance = Proqoute() 
        con = proqoute_instance.connect()
        cursor = con.cursor()
        try:
            auctionsfetched = acv.getauctions()
            for auction in auctionsfetched:  
                if auction[38] is None:
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
                    fire_damage1= auction[51]
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
                    
                    if(title=='Unknown,Salvage Rebuilt'):
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
                    
                    
                    conn.request("POST", "/v1/proquote", payload, headers)
                    res = conn.getresponse()
                    data = res.read()
                    data = json.loads(data)
                    print('data',data)
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
                else:
                    print(auction[4],'auction proqoute already generated')
        except:
            return ()