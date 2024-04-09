import pymysql
import http.client
import json

import requests

class Qoute:   
    def connect(self):
        return pymysql.connect(host="localhost", user="carintocash1", password="zkY$$}_vtXO=", database="carintocash1", charset='utf8mb4')
        #return pymysql.connect(host="localhost", user="root", password="", database="carintocash", charset='utf8mb4')

    def frontend1(self, fdata,unable_to_verify_data):
        con = Qoute.connect(self)
        cursor = con.cursor()
        try:
            year = fdata['year']
            print(year)
            fid = fdata['record_id']
            make_code = fdata['make_code']
            make = fdata['make']
            model = fdata['model']
            key = fdata['key']
            zipcode = fdata['v_zip']
            damage3 = fdata['damage']
            sdamage = fdata['sdamage']
            zipcode = fdata['v_zip']
            title = fdata['title']
            drive1 = fdata['drive']
            mileage1 = fdata['mileage']+',000'
            mileage=mileage1.replace(",","")
            drivable ='N'
            airbag1 = fdata['airbag']
            fire_damage1 = fdata['fire_damage']
            damageimg = fdata.getlist('damageimg[]')
            
            if mileage=='000':
                    mileage = ''
              
            # if(mileage==''):
            #     query="SELECT * FROM condition_report where FIND_IN_SET('"+make+"', make_name) and FIND_IN_SET('"+model+"', model_name) and min_year <="+year+" and max_year >="+year+" and FIND_IN_SET('"+zipcode+"', zip) and damage='"+damage3+"' and airbag='"+airbag1+"' and drive='"+drive1+"' and key1='"+key+"' and title_type='"+title+"' and fire_damage='"+fire_damage1+"' UNION SELECT * FROM condition_report where FIND_IN_SET('"+make+"', make_name) UNION SELECT * FROM condition_report where FIND_IN_SET('"+model+"', model_name) UNION SELECT * FROM condition_report where min_year <="+year+" and max_year >="+year+" UNION SELECT * FROM condition_report where FIND_IN_SET('"+zipcode+"', zip) UNION SELECT * FROM condition_report where  damage='"+damage3+"' UNION SELECT * FROM condition_report where  airbag='"+airbag1+"' UNION SELECT * FROM condition_report where  drive='"+drive1+"' UNION SELECT * FROM condition_report where  key1='"+key+"' UNION SELECT * FROM condition_report where  title_type='"+title+"' UNION SELECT * FROM condition_report where  fire_damage='"+fire_damage1+"' UNION SELECT * FROM condition_report order by make_name desc LIMIT 1" 
            #     print(query)
            #     cursor.execute(query)
            #     return cursor.fetchone() 
            # else:
            #     query="SELECT * FROM condition_report where FIND_IN_SET('"+make+"', make_name) and FIND_IN_SET('"+model+"', model_name) and min_year <="+year+" and max_year >="+year+" and FIND_IN_SET('"+zipcode+"', zip) and min_mileage<="+mileage+" and max_mileage >="+mileage+" and damage='"+damage3+"' and airbag='"+airbag1+"' and drive='"+drive1+"' and key1='"+key+"' and title_type='"+title+"' and fire_damage='"+fire_damage1+"' UNION SELECT * FROM condition_report where FIND_IN_SET('"+make+"', make_name) UNION SELECT * FROM condition_report where FIND_IN_SET('"+model+"', model_name) UNION SELECT * FROM condition_report where min_year <="+year+" and max_year >="+year+" UNION SELECT * FROM condition_report where FIND_IN_SET('"+zipcode+"', zip) UNION SELECT * FROM condition_report where min_mileage<="+mileage+" and max_mileage >="+mileage+" UNION SELECT * FROM condition_report where  damage='"+damage3+"' UNION SELECT * FROM condition_report where  airbag='"+airbag1+"' UNION     SELECT * FROM condition_report where  drive='"+drive1+"' UNION SELECT * FROM condition_report where  key1='"+key+"' UNION SELECT * FROM condition_report where  title_type='"+title+"' UNION SELECT * FROM condition_report where  fire_damage='"+fire_damage1+"' UNION SELECT * FROM condition_report order by make_name desc LIMIT 1"  
            #     print(query)
            #     cursor.execute(query)
            #     return cursor.fetchone() 
            # if mileage=='':
            #     query="SELECT * FROM condition_report where FIND_IN_SET('"+make+"', make_name) and FIND_IN_SET('"+model+"', model_name) and min_year <="+year+" and max_year >="+year+" and FIND_IN_SET('"+zipcode+"', final_zip) and damage='"+damage3+"' and airbag='"+airbag1+"' and drive='"+drive1+"' and key1='"+key+"' and title_type='"+title+"' and fire_damage='"+fire_damage1+"' UNION SELECT * FROM condition_report where  ((FIND_IN_SET('"+make+"', make_name) AND FIND_IN_SET('"+model+"', model_name)) OR (FIND_IN_SET('all', make_name) AND FIND_IN_SET('all', model_name) ) ) AND ((min_year <= "+year+" AND max_year >= "+year+") OR  (min_year = '' AND max_year = ''))  AND ((FIND_IN_SET('"+zipcode+"', final_zip) OR final_zip ='')) AND  (damage = '"+damage3+"' OR  damage = '') AND (airbag = '"+airbag1+"' OR airbag = '') AND (drive = '"+drive1+"' OR drive = '') AND (key1 = '"+key+"' OR key1 = '') AND (title_type = '"+title+"' OR title_type = '') AND (fire_damage = '"+fire_damage1+"' OR fire_damage = '') order by make_name desc LIMIT 1" 
            #     print(query+'g1')
            #     cursor.execute(query)
            #     return cursor.fetchone() 
            # else:
            #     query="SELECT * FROM condition_report where FIND_IN_SET('"+make+"', make_name) and FIND_IN_SET('"+model+"', model_name) and min_year <="+year+" and max_year >="+year+" and FIND_IN_SET('"+zipcode+"', final_zip) and min_mileage<="+mileage+" and max_mileage >="+mileage+" and damage='"+damage3+"' and airbag='"+airbag1+"' and drive='"+drive1+"' and key1='"+key+"' and title_type='"+title+"' and fire_damage='"+fire_damage1+"' UNION SELECT * FROM condition_report where  ((FIND_IN_SET('"+make+"', make_name) AND FIND_IN_SET('"+model+"', model_name)) OR (FIND_IN_SET('all', make_name) AND FIND_IN_SET('all', model_name) ) ) AND ((min_year <= "+year+" AND max_year >= "+year+") OR  (min_year = '' AND max_year = ''))  AND ( (max_mileage >= "+mileage+" AND min_mileage <= "+mileage+") OR (max_mileage ='' AND min_mileage = '') ) AND ((FIND_IN_SET('"+zipcode+"', final_zip) OR final_zip ='')) AND  (damage = '"+damage3+"' OR  damage = '') AND (airbag = '"+airbag1+"' OR airbag = '') AND (drive = '"+drive1+"' OR drive = '') AND (key1 = '"+key+"' OR key1 = '') AND (title_type = '"+title+"' OR title_type = '') AND (fire_damage = '"+fire_damage1+"' OR fire_damage = '') order by make_name desc LIMIT 1"
            #     print(query+'g1')
            #     cursor.execute(query)
            #     return cursor.fetchone()

            utv = ''
            # if unable_to_verify_data!='':
            #     if mileage =='':
            #         query="SELECT * FROM condition_report where FIND_IN_SET('"+make+"', make_name) and FIND_IN_SET('"+model+"', model_name) and min_year <="+year+" and max_year >="+year+" and  unable_to_verify='yes' and FIND_IN_SET('"+damage3+"', damageComma) and FIND_IN_SET('"+airbag1+"', airbagComma) and FIND_IN_SET('"+drive1+"', driveComma) and FIND_IN_SET('"+key+"', keyComma) and FIND_IN_SET('"+title+"', titleComma) and FIND_IN_SET('"+fire_damage1+"', firDamageComma) UNION SELECT * FROM condition_report where  (FIND_IN_SET('"+make+"', make_name) AND FIND_IN_SET('"+model+"', model_name) OR (FIND_IN_SET('all', make_name) AND FIND_IN_SET('all', model_name) ))  AND ((min_year <= "+year+" AND max_year >= "+year+") OR  (min_year = '' AND max_year = '')) AND (unable_to_verify='yes') AND ((FIND_IN_SET('"+zipcode+"', final_zip) OR final_zip ='')) AND  ((FIND_IN_SET('"+damage3+"', damageComma)  OR  damageComma = '')) AND ((FIND_IN_SET('"+airbag1+"', airbagComma)  OR airbagComma = '')) AND ((FIND_IN_SET('"+drive1+"', driveComma)    OR driveComma = '')) AND ((FIND_IN_SET('"+key+"', keyComma)   OR keyComma = '')) AND ((FIND_IN_SET('"+title+"', titleComma)  OR titleComma = '')) AND ((FIND_IN_SET('"+fire_damage1+"', firDamageComma)  OR firDamageComma = '')) order by make_name desc LIMIT 1 " 
            #         print(query)
            #         print("in")
            #         cursor.execute(query)
            #         return cursor.fetchone() 
            #     else:
            #         query="SELECT * FROM condition_report where FIND_IN_SET('"+make+"', make_name) and FIND_IN_SET('"+model+"', model_name) and min_year <="+year+" and max_year >="+year+" and  unable_to_verify='yes' and FIND_IN_SET('"+damage3+"', damageComma) and FIND_IN_SET('"+airbag1+"', airbagComma) and FIND_IN_SET('"+drive1+"', driveComma) and FIND_IN_SET('"+key+"', keyComma) and FIND_IN_SET('"+title+"', titleComma) and FIND_IN_SET('"+fire_damage1+"', firDamageComma) UNION SELECT * FROM condition_report where  (FIND_IN_SET('"+make+"', make_name) AND FIND_IN_SET('"+model+"', model_name) OR (FIND_IN_SET('all', make_name) AND FIND_IN_SET('all', model_name)))   AND ((min_year <= "+year+" AND max_year >= "+year+") OR  (min_year = '' AND max_year = '')) AND (unable_to_verify='yes') AND ((FIND_IN_SET('"+zipcode+"', final_zip) OR final_zip ='')) AND  ((FIND_IN_SET('"+damage3+"', damageComma)  OR  damageComma = '')) AND ((FIND_IN_SET('"+airbag1+"', airbagComma)  OR airbagComma = '')) AND ((FIND_IN_SET('"+drive1+"', driveComma) OR driveComma = '')) AND ((FIND_IN_SET('"+key+"', keyComma) OR keyComma = '')) AND ((FIND_IN_SET('"+title+"', titleComma)  OR titleComma = '')) AND ((FIND_IN_SET('"+fire_damage1+"', firDamageComma)  OR firDamageComma = '')) order by make_name desc LIMIT 1 " 
            #         print(query)
            #         print("out")
            #         cursor.execute(query)
            #         return cursor.fetchone()
            # else:
            #     if mileage =='':
            #         query="SELECT * FROM condition_report where FIND_IN_SET('"+make+"', make_name) and FIND_IN_SET('"+model+"', model_name) and min_year <="+year+" and max_year >="+year+" and unable_to_verify='no' and FIND_IN_SET('"+zipcode+"', final_zip) and FIND_IN_SET('"+damage3+"', damageComma) and FIND_IN_SET('"+airbag1+"', airbagComma) and FIND_IN_SET('"+drive1+"', driveComma) and FIND_IN_SET('"+key+"', keyComma) and FIND_IN_SET('"+title+"', titleComma) and FIND_IN_SET('"+fire_damage1+"', firDamageComma) UNION SELECT * FROM condition_report where  (FIND_IN_SET('"+make+"', make_name) AND FIND_IN_SET('"+model+"', model_name) OR (FIND_IN_SET('all', make_name) AND FIND_IN_SET('all', model_name) ))  AND ((min_year <= "+year+" AND max_year >= "+year+") OR  (min_year = '' AND max_year = ''))  AND ((FIND_IN_SET('"+zipcode+"', final_zip) OR final_zip ='')) AND  ((FIND_IN_SET('"+damage3+"', damageComma)  OR  damageComma = '')) AND ((FIND_IN_SET('"+airbag1+"', airbagComma)  OR airbagComma = '')) AND ((FIND_IN_SET('"+drive1+"', driveComma)    OR driveComma = '')) AND ((FIND_IN_SET('"+key+"', keyComma)   OR keyComma = '')) AND ((FIND_IN_SET('"+title+"', titleComma)  OR titleComma = '')) AND ((FIND_IN_SET('"+fire_damage1+"', firDamageComma)  OR firDamageComma = '')) AND unable_to_verify='no' order by make_name desc LIMIT 1 " 
            #         print(query)
            #         print("in")
            #         cursor.execute(query)
            #         return cursor.fetchone() 
            #     else:
            #         query="SELECT * FROM condition_report where FIND_IN_SET('"+make+"', make_name) and FIND_IN_SET('"+model+"', model_name) and min_year <="+year+" and max_year >="+year+" and unable_to_verify='no' and FIND_IN_SET('"+zipcode+"', final_zip) and min_mileage<="+mileage+" and max_mileage >="+mileage+" and FIND_IN_SET('"+damage3+"', damageComma) and FIND_IN_SET('"+airbag1+"', airbagComma) and FIND_IN_SET('"+drive1+"', driveComma) and FIND_IN_SET('"+key+"', keyComma) and FIND_IN_SET('"+title+"', titleComma) and FIND_IN_SET('"+fire_damage1+"', firDamageComma) UNION SELECT * FROM condition_report where  (FIND_IN_SET('"+make+"', make_name) AND FIND_IN_SET('"+model+"', model_name) OR (FIND_IN_SET('all', make_name) AND FIND_IN_SET('all', model_name)))   AND ((min_year <= "+year+" AND max_year >= "+year+") OR  (min_year = '' AND max_year = '')) AND ((max_mileage >= "+mileage+" AND  min_mileage <= "+mileage+") OR (max_mileage ='' AND min_mileage = '')) AND ((FIND_IN_SET('"+zipcode+"', final_zip) OR final_zip ='')) AND  ((FIND_IN_SET('"+damage3+"', damageComma)  OR  damageComma = '')) AND ((FIND_IN_SET('"+airbag1+"', airbagComma)  OR airbagComma = '')) AND ((FIND_IN_SET('"+drive1+"', driveComma) OR driveComma = '')) AND ((FIND_IN_SET('"+key+"', keyComma) OR keyComma = '')) AND ((FIND_IN_SET('"+title+"', titleComma)  OR titleComma = '')) AND ((FIND_IN_SET('"+fire_damage1+"', firDamageComma)  OR firDamageComma = '')) AND unable_to_verify='no' order by make_name desc LIMIT 1 " 
            #         print(query)
            #         print("out")
            #         cursor.execute(query)
            #         return cursor.fetchone()
            # if unable_to_verify_data!='':
            #     if mileage =='':
            #         query="SELECT * FROM condition_report where FIND_IN_SET('"+make+"', make_name) and FIND_IN_SET('"+model+"', model_name) and min_year <="+year+" and max_year >="+year+" and  unable_to_verify='yes' and (FIND_IN_SET('"+zipcode+"', final_zip) or FIND_IN_SET('"+zipcode+"', final_zip1) or FIND_IN_SET('"+zipcode+"', final_zip2)) and FIND_IN_SET('"+damage3+"', damageComma) and FIND_IN_SET('"+airbag1+"', airbagComma) and FIND_IN_SET('"+drive1+"', driveComma) and FIND_IN_SET('"+key+"', keyComma) and FIND_IN_SET('"+title+"', titleComma) and FIND_IN_SET('"+fire_damage1+"', firDamageComma) UNION SELECT * FROM condition_report where  (FIND_IN_SET('"+make+"', make_name) AND FIND_IN_SET('"+model+"', model_name) OR (FIND_IN_SET('all', make_name) AND FIND_IN_SET('all', model_name) ))  AND ((min_year <= "+year+" AND max_year >= "+year+") OR  (min_year = '' AND max_year = '')) AND (unable_to_verify='yes') AND ((FIND_IN_SET('"+zipcode+"', final_zip) OR final_zip ='') or (FIND_IN_SET('"+zipcode+"', final_zip1) OR final_zip1 ='') or (FIND_IN_SET('"+zipcode+"', final_zip2) OR final_zip2 ='')) AND  ((FIND_IN_SET('"+damage3+"', damageComma)  OR  damageComma = '')) AND ((FIND_IN_SET('"+airbag1+"', airbagComma)  OR airbagComma = '')) AND ((FIND_IN_SET('"+drive1+"', driveComma)    OR driveComma = '')) AND ((FIND_IN_SET('"+key+"', keyComma)   OR keyComma = '')) AND ((FIND_IN_SET('"+title+"', titleComma)  OR titleComma = '')) AND ((FIND_IN_SET('"+fire_damage1+"', firDamageComma)  OR firDamageComma = '')) order by not_to_exceed desc" 
            #         print(query)
            #         print("in")
            #         cursor.execute(query)
            #         return cursor.fetchall() 
            #     else:
            #         query="SELECT * FROM condition_report where FIND_IN_SET('"+make+"', make_name) and FIND_IN_SET('"+model+"', model_name) and min_year <="+year+" and max_year >="+year+" and  unable_to_verify='yes' and (FIND_IN_SET('"+zipcode+"', final_zip) or FIND_IN_SET('"+zipcode+"', final_zip1) or FIND_IN_SET('"+zipcode+"', final_zip2)) and FIND_IN_SET('"+damage3+"', damageComma) and FIND_IN_SET('"+airbag1+"', airbagComma) and FIND_IN_SET('"+drive1+"', driveComma) and FIND_IN_SET('"+key+"', keyComma) and FIND_IN_SET('"+title+"', titleComma) and FIND_IN_SET('"+fire_damage1+"', firDamageComma) UNION SELECT * FROM condition_report where  (FIND_IN_SET('"+make+"', make_name) AND FIND_IN_SET('"+model+"', model_name) OR (FIND_IN_SET('all', make_name) AND FIND_IN_SET('all', model_name)))   AND ((min_year <= "+year+" AND max_year >= "+year+") OR  (min_year = '' AND max_year = '')) AND (unable_to_verify='yes') AND ((FIND_IN_SET('"+zipcode+"', final_zip) OR final_zip ='') or (FIND_IN_SET('"+zipcode+"', final_zip1) OR final_zip1 ='') or (FIND_IN_SET('"+zipcode+"', final_zip2) OR final_zip2 ='')) AND  ((FIND_IN_SET('"+damage3+"', damageComma)  OR  damageComma = '')) AND ((FIND_IN_SET('"+airbag1+"', airbagComma)  OR airbagComma = '')) AND ((FIND_IN_SET('"+drive1+"', driveComma) OR driveComma = '')) AND ((FIND_IN_SET('"+key+"', keyComma) OR keyComma = '')) AND ((FIND_IN_SET('"+title+"', titleComma)  OR titleComma = '')) AND ((FIND_IN_SET('"+fire_damage1+"', firDamageComma)  OR firDamageComma = '')) order by not_to_exceed desc" 
            #         print(query)
            #         print("out")
            #         cursor.execute(query)
            #         return cursor.fetchall()
            # else:
            #     if mileage =='':
            #         query="SELECT * FROM condition_report where FIND_IN_SET('"+make+"', make_name) and FIND_IN_SET('"+model+"', model_name) and min_year <="+year+" and max_year >="+year+" and unable_to_verify='no' and (FIND_IN_SET('"+zipcode+"', final_zip) or FIND_IN_SET('"+zipcode+"', final_zip1) or FIND_IN_SET('"+zipcode+"', final_zip2)) and FIND_IN_SET('"+damage3+"', damageComma) and FIND_IN_SET('"+airbag1+"', airbagComma) and FIND_IN_SET('"+drive1+"', driveComma) and FIND_IN_SET('"+key+"', keyComma) and FIND_IN_SET('"+title+"', titleComma) and FIND_IN_SET('"+fire_damage1+"', firDamageComma) UNION SELECT * FROM condition_report where  (FIND_IN_SET('"+make+"', make_name) AND FIND_IN_SET('"+model+"', model_name) OR (FIND_IN_SET('all', make_name) AND FIND_IN_SET('all', model_name) ))  AND ((min_year <= "+year+" AND max_year >= "+year+") OR  (min_year = '' AND max_year = ''))  AND ((FIND_IN_SET('"+zipcode+"', final_zip) OR final_zip ='') or (FIND_IN_SET('"+zipcode+"', final_zip1) OR final_zip1 ='') or (FIND_IN_SET('"+zipcode+"', final_zip2) OR final_zip2 ='')) AND  ((FIND_IN_SET('"+damage3+"', damageComma)  OR  damageComma = '')) AND ((FIND_IN_SET('"+airbag1+"', airbagComma)  OR airbagComma = '')) AND ((FIND_IN_SET('"+drive1+"', driveComma)    OR driveComma = '')) AND ((FIND_IN_SET('"+key+"', keyComma)   OR keyComma = '')) AND ((FIND_IN_SET('"+title+"', titleComma)  OR titleComma = '')) AND ((FIND_IN_SET('"+fire_damage1+"', firDamageComma)  OR firDamageComma = '')) AND unable_to_verify='no' order by not_to_exceed desc" 
            #         print(query)
            #         print("in")
            #         cursor.execute(query)
            #         return cursor.fetchall() 
            #     else:
            #         query="SELECT * FROM condition_report where FIND_IN_SET('"+make+"', make_name) and FIND_IN_SET('"+model+"', model_name) and min_year <="+year+" and max_year >="+year+" and unable_to_verify='no' and (FIND_IN_SET('"+zipcode+"', final_zip) or FIND_IN_SET('"+zipcode+"', final_zip1) or FIND_IN_SET('"+zipcode+"', final_zip2)) and min_mileage<="+mileage+" and max_mileage >="+mileage+" and FIND_IN_SET('"+damage3+"', damageComma) and FIND_IN_SET('"+airbag1+"', airbagComma) and FIND_IN_SET('"+drive1+"', driveComma) and FIND_IN_SET('"+key+"', keyComma) and FIND_IN_SET('"+title+"', titleComma) and FIND_IN_SET('"+fire_damage1+"', firDamageComma) UNION SELECT * FROM condition_report where  (FIND_IN_SET('"+make+"', make_name) AND FIND_IN_SET('"+model+"', model_name) OR (FIND_IN_SET('all', make_name) AND FIND_IN_SET('all', model_name)))   AND ((min_year <= "+year+" AND max_year >= "+year+") OR  (min_year = '' AND max_year = '')) AND ((max_mileage >= "+mileage+" AND  min_mileage <= "+mileage+") OR (max_mileage ='' AND min_mileage = '')) AND ((FIND_IN_SET('"+zipcode+"', final_zip) OR final_zip ='') or (FIND_IN_SET('"+zipcode+"', final_zip1) OR final_zip1 ='') or (FIND_IN_SET('"+zipcode+"', final_zip2) OR final_zip2 ='')) AND  ((FIND_IN_SET('"+damage3+"', damageComma)  OR  damageComma = '')) AND ((FIND_IN_SET('"+airbag1+"', airbagComma)  OR airbagComma = '')) AND ((FIND_IN_SET('"+drive1+"', driveComma) OR driveComma = '')) AND ((FIND_IN_SET('"+key+"', keyComma) OR keyComma = '')) AND ((FIND_IN_SET('"+title+"', titleComma)  OR titleComma = '')) AND ((FIND_IN_SET('"+fire_damage1+"', firDamageComma)  OR firDamageComma = '')) AND unable_to_verify='no' order by not_to_exceed desc " 
            #         print(query)
            #         print("out")
            #         cursor.execute(query)
            #         return cursor.fetchall()
            if unable_to_verify_data!='':
                if mileage =='':
                    #query="SELECT * FROM condition_report where FIND_IN_SET('"+make+"', make_name) and FIND_IN_SET('"+model+"', model_name) and min_year <="+year+" and max_year >="+year+" and  unable_to_verify='yes' and (FIND_IN_SET('"+zipcode+"', final_zip) or FIND_IN_SET('"+zipcode+"', final_zip1) or FIND_IN_SET('"+zipcode+"', final_zip2)) or FIND_IN_SET('"+zipcode+"', final_zip3) or FIND_IN_SET('"+zipcode+"', final_zip5)) and FIND_IN_SET('"+damage3+"', damageComma) and FIND_IN_SET('"+airbag1+"', airbagComma) and FIND_IN_SET('"+drive1+"', driveComma) and FIND_IN_SET('"+key+"', keyComma) and FIND_IN_SET('"+title+"', titleComma) and FIND_IN_SET('"+fire_damage1+"', firDamageComma) UNION SELECT * FROM condition_report where  (FIND_IN_SET('"+make+"', make_name) AND FIND_IN_SET('"+model+"', model_name) OR (FIND_IN_SET('all', make_name) AND FIND_IN_SET('all', model_name) ))  AND ((min_year <= "+year+" AND max_year >= "+year+") OR  (min_year = '' AND max_year = '')) AND (unable_to_verify='yes') AND ((FIND_IN_SET('"+zipcode+"', final_zip)) or (FIND_IN_SET('"+zipcode+"', final_zip1)) or (FIND_IN_SET('"+zipcode+"', final_zip2))) or (FIND_IN_SET('"+zipcode+"', final_zip3)) or (FIND_IN_SET('"+zipcode+"', final_zip5))) AND  ((FIND_IN_SET('"+damage3+"', damageComma)  OR  damageComma = '')) AND ((FIND_IN_SET('"+airbag1+"', airbagComma)  OR airbagComma = '')) AND ((FIND_IN_SET('"+drive1+"', driveComma)    OR driveComma = '')) AND ((FIND_IN_SET('"+key+"', keyComma)   OR keyComma = '')) AND ((FIND_IN_SET('"+title+"', titleComma)  OR titleComma = '')) AND ((FIND_IN_SET('"+fire_damage1+"', firDamageComma)  OR firDamageComma = '')) order by not_to_exceed desc" 
                    query="SELECT * FROM condition_report where is_deleted='no' and FIND_IN_SET('"+make+"', make_name) and FIND_IN_SET('"+model+"', model_name) and min_year <="+year+" and max_year >="+year+" and  unable_to_verify='yes' and FIND_IN_SET('"+zipcode+"', final_zip) and FIND_IN_SET('"+damage3+"', damageComma) and FIND_IN_SET('"+airbag1+"', airbagComma) and FIND_IN_SET('"+drive1+"', driveComma) and FIND_IN_SET('"+key+"', keyComma) and FIND_IN_SET('"+title+"', titleComma) and FIND_IN_SET('"+fire_damage1+"', firDamageComma) UNION SELECT * FROM condition_report where  (FIND_IN_SET('"+make+"', make_name) AND FIND_IN_SET('"+model+"', model_name) OR (FIND_IN_SET('all', make_name) AND FIND_IN_SET('all', model_name) ))  AND ((min_year <= "+year+" AND max_year >= "+year+") OR  (min_year = '' AND max_year = '')) AND unable_to_verify='yes' AND FIND_IN_SET('"+zipcode+"', final_zip) AND  ((FIND_IN_SET('"+damage3+"', damageComma)  OR  damageComma = '')) AND ((FIND_IN_SET('"+airbag1+"', airbagComma)  OR airbagComma = '')) AND ((FIND_IN_SET('"+drive1+"', driveComma)    OR driveComma = '')) AND ((FIND_IN_SET('"+key+"', keyComma)   OR keyComma = '')) AND ((FIND_IN_SET('"+title+"', titleComma)  OR titleComma = '')) AND ((FIND_IN_SET('"+fire_damage1+"', firDamageComma)  OR firDamageComma = '')) AND is_deleted='no' order by not_to_exceed desc" 
                    print(query)
                    print("in")
                    cursor.execute(query)
                    return cursor.fetchall() 
                else:
                    #query="SELECT * FROM condition_report where FIND_IN_SET('"+make+"', make_name) and FIND_IN_SET('"+model+"', model_name) and min_year <="+year+" and max_year >="+year+" and  unable_to_verify='yes' and (FIND_IN_SET('"+zipcode+"', final_zip) or FIND_IN_SET('"+zipcode+"', final_zip1) or FIND_IN_SET('"+zipcode+"', final_zip2)) or FIND_IN_SET('"+zipcode+"', final_zip3) or FIND_IN_SET('"+zipcode+"', final_zip5)) and FIND_IN_SET('"+damage3+"', damageComma) and FIND_IN_SET('"+airbag1+"', airbagComma) and FIND_IN_SET('"+drive1+"', driveComma) and FIND_IN_SET('"+key+"', keyComma) and FIND_IN_SET('"+title+"', titleComma) and FIND_IN_SET('"+fire_damage1+"', firDamageComma) UNION SELECT * FROM condition_report where  (FIND_IN_SET('"+make+"', make_name) AND FIND_IN_SET('"+model+"', model_name) OR (FIND_IN_SET('all', make_name) AND FIND_IN_SET('all', model_name)))   AND ((min_year <= "+year+" AND max_year >= "+year+") OR  (min_year = '' AND max_year = '')) AND (unable_to_verify='yes') AND ((FIND_IN_SET('"+zipcode+"', final_zip)) or (FIND_IN_SET('"+zipcode+"', final_zip1)) or (FIND_IN_SET('"+zipcode+"', final_zip2))) or (FIND_IN_SET('"+zipcode+"', final_zip3)) or (FIND_IN_SET('"+zipcode+"', final_zip5))) AND  ((FIND_IN_SET('"+damage3+"', damageComma)  OR  damageComma = '')) AND ((FIND_IN_SET('"+airbag1+"', airbagComma)  OR airbagComma = '')) AND ((FIND_IN_SET('"+drive1+"', driveComma) OR driveComma = '')) AND ((FIND_IN_SET('"+key+"', keyComma) OR keyComma = '')) AND ((FIND_IN_SET('"+title+"', titleComma)  OR titleComma = '')) AND ((FIND_IN_SET('"+fire_damage1+"', firDamageComma)  OR firDamageComma = '')) order by not_to_exceed desc"
                    query="SELECT * FROM condition_report where is_deleted='no' and FIND_IN_SET('"+make+"', make_name) and FIND_IN_SET('"+model+"', model_name) and min_year <="+year+" and max_year >="+year+" and  unable_to_verify='yes' and FIND_IN_SET('"+zipcode+"', final_zip)  and FIND_IN_SET('"+damage3+"', damageComma) and FIND_IN_SET('"+airbag1+"', airbagComma) and FIND_IN_SET('"+drive1+"', driveComma) and FIND_IN_SET('"+key+"', keyComma) and FIND_IN_SET('"+title+"', titleComma) and FIND_IN_SET('"+fire_damage1+"', firDamageComma) UNION SELECT * FROM condition_report where  (FIND_IN_SET('"+make+"', make_name) AND FIND_IN_SET('"+model+"', model_name) OR (FIND_IN_SET('all', make_name) AND FIND_IN_SET('all', model_name)))   AND ((min_year <= "+year+" AND max_year >= "+year+") OR  (min_year = '' AND max_year = '')) AND (unable_to_verify='yes') AND FIND_IN_SET('"+zipcode+"', final_zip) AND  ((FIND_IN_SET('"+damage3+"', damageComma)  OR  damageComma = '')) AND ((FIND_IN_SET('"+airbag1+"', airbagComma)  OR airbagComma = '')) AND ((FIND_IN_SET('"+drive1+"', driveComma) OR driveComma = '')) AND ((FIND_IN_SET('"+key+"', keyComma) OR keyComma = '')) AND ((FIND_IN_SET('"+title+"', titleComma)  OR titleComma = '')) AND ((FIND_IN_SET('"+fire_damage1+"', firDamageComma)  OR firDamageComma = '')) AND is_deleted='no' order by not_to_exceed desc" 
                    print(query)
                    print("out")
                    cursor.execute(query)
                    return cursor.fetchall()
            else:
                if mileage =='':
                    #query="SELECT * FROM condition_report where FIND_IN_SET('"+make+"', make_name) and FIND_IN_SET('"+model+"', model_name) and min_year <="+year+" and max_year >="+year+" and unable_to_verify='no' and (FIND_IN_SET('"+zipcode+"', final_zip) or FIND_IN_SET('"+zipcode+"', final_zip1) or FIND_IN_SET('"+zipcode+"', final_zip2)) or FIND_IN_SET('"+zipcode+"', final_zip3) or FIND_IN_SET('"+zipcode+"', final_zip5)) and FIND_IN_SET('"+damage3+"', damageComma) and FIND_IN_SET('"+airbag1+"', airbagComma) and FIND_IN_SET('"+drive1+"', driveComma) and FIND_IN_SET('"+key+"', keyComma) and FIND_IN_SET('"+title+"', titleComma) and FIND_IN_SET('"+fire_damage1+"', firDamageComma) UNION SELECT * FROM condition_report where  (FIND_IN_SET('"+make+"', make_name) AND FIND_IN_SET('"+model+"', model_name) OR (FIND_IN_SET('all', make_name) AND FIND_IN_SET('all', model_name) ))  AND ((min_year <= "+year+" AND max_year >= "+year+") OR  (min_year = '' AND max_year = ''))  AND ((FIND_IN_SET('"+zipcode+"', final_zip)) or (FIND_IN_SET('"+zipcode+"', final_zip1)) or (FIND_IN_SET('"+zipcode+"', final_zip2))) or (FIND_IN_SET('"+zipcode+"', final_zip3)) or (FIND_IN_SET('"+zipcode+"', final_zip5))) AND  ((FIND_IN_SET('"+damage3+"', damageComma)  OR  damageComma = '')) AND ((FIND_IN_SET('"+airbag1+"', airbagComma)  OR airbagComma = '')) AND ((FIND_IN_SET('"+drive1+"', driveComma)    OR driveComma = '')) AND ((FIND_IN_SET('"+key+"', keyComma)   OR keyComma = '')) AND ((FIND_IN_SET('"+title+"', titleComma)  OR titleComma = '')) AND ((FIND_IN_SET('"+fire_damage1+"', firDamageComma)  OR firDamageComma = '')) AND unable_to_verify='no' order by not_to_exceed desc" 
                    query="SELECT * FROM condition_report where is_deleted='no' and FIND_IN_SET('"+make+"', make_name) and FIND_IN_SET('"+model+"', model_name) and min_year <="+year+" and max_year >="+year+" and unable_to_verify='no' and FIND_IN_SET('"+zipcode+"', final_zip) and FIND_IN_SET('"+damage3+"', damageComma) and FIND_IN_SET('"+airbag1+"', airbagComma) and FIND_IN_SET('"+drive1+"', driveComma) and FIND_IN_SET('"+key+"', keyComma) and FIND_IN_SET('"+title+"', titleComma) and FIND_IN_SET('"+fire_damage1+"', firDamageComma) UNION SELECT * FROM condition_report where  (FIND_IN_SET('"+make+"', make_name) AND FIND_IN_SET('"+model+"', model_name) OR (FIND_IN_SET('all', make_name) AND FIND_IN_SET('all', model_name) ))  AND ((min_year <= "+year+" AND max_year >= "+year+") OR  (min_year = '' AND max_year = ''))  AND FIND_IN_SET('"+zipcode+"', final_zip) AND  ((FIND_IN_SET('"+damage3+"', damageComma)  OR  damageComma = '')) AND ((FIND_IN_SET('"+airbag1+"', airbagComma)  OR airbagComma = '')) AND ((FIND_IN_SET('"+drive1+"', driveComma)    OR driveComma = '')) AND ((FIND_IN_SET('"+key+"', keyComma)   OR keyComma = '')) AND ((FIND_IN_SET('"+title+"', titleComma)  OR titleComma = '')) AND ((FIND_IN_SET('"+fire_damage1+"', firDamageComma)  OR firDamageComma = '')) AND unable_to_verify='no' AND is_deleted='no' order by not_to_exceed desc" 
                    print(query)
                    print("in")
                    cursor.execute(query)
                    return cursor.fetchall() 
                else:
                    #query="SELECT * FROM condition_report where FIND_IN_SET('"+make+"', make_name) and FIND_IN_SET('"+model+"', model_name) and min_year <="+year+" and max_year >="+year+" and unable_to_verify='no' and (FIND_IN_SET('"+zipcode+"', final_zip) or FIND_IN_SET('"+zipcode+"', final_zip1) or FIND_IN_SET('"+zipcode+"', final_zip2)) or FIND_IN_SET('"+zipcode+"', final_zip3) or FIND_IN_SET('"+zipcode+"', final_zip5)) and min_mileage<="+mileage+" and max_mileage >="+mileage+" and FIND_IN_SET('"+damage3+"', damageComma) and FIND_IN_SET('"+airbag1+"', airbagComma) and FIND_IN_SET('"+drive1+"', driveComma) and FIND_IN_SET('"+key+"', keyComma) and FIND_IN_SET('"+title+"', titleComma) and FIND_IN_SET('"+fire_damage1+"', firDamageComma) UNION SELECT * FROM condition_report where  (FIND_IN_SET('"+make+"', make_name) AND FIND_IN_SET('"+model+"', model_name) OR (FIND_IN_SET('all', make_name) AND FIND_IN_SET('all', model_name)))   AND ((min_year <= "+year+" AND max_year >= "+year+") OR  (min_year = '' AND max_year = '')) AND ((max_mileage >= "+mileage+" AND  min_mileage <= "+mileage+") OR (max_mileage ='' AND min_mileage = '')) AND ((FIND_IN_SET('"+zipcode+"', final_zip)) or (FIND_IN_SET('"+zipcode+"', final_zip1)) or (FIND_IN_SET('"+zipcode+"', final_zip2))) or (FIND_IN_SET('"+zipcode+"', final_zip3)) or (FIND_IN_SET('"+zipcode+"', final_zip5))) AND  ((FIND_IN_SET('"+damage3+"', damageComma)  OR  damageComma = '')) AND ((FIND_IN_SET('"+airbag1+"', airbagComma)  OR airbagComma = '')) AND ((FIND_IN_SET('"+drive1+"', driveComma) OR driveComma = '')) AND ((FIND_IN_SET('"+key+"', keyComma) OR keyComma = '')) AND ((FIND_IN_SET('"+title+"', titleComma)  OR titleComma = '')) AND ((FIND_IN_SET('"+fire_damage1+"', firDamageComma)  OR firDamageComma = '')) AND unable_to_verify='no' order by not_to_exceed desc " 
                    query="SELECT * FROM condition_report where is_deleted='no' and FIND_IN_SET('"+make+"', make_name) and FIND_IN_SET('"+model+"', model_name) and min_year <="+year+" and max_year >="+year+" and FIND_IN_SET('"+zipcode+"', final_zip) and min_mileage<="+mileage+" and max_mileage >="+mileage+" and FIND_IN_SET('"+damage3+"', damageComma) and FIND_IN_SET('"+airbag1+"', airbagComma) and FIND_IN_SET('"+drive1+"', driveComma) and FIND_IN_SET('"+key+"', keyComma) and FIND_IN_SET('"+title+"', titleComma) and FIND_IN_SET('"+fire_damage1+"', firDamageComma) UNION SELECT * FROM condition_report where  (FIND_IN_SET('"+make+"', make_name) AND FIND_IN_SET('"+model+"', model_name) OR (FIND_IN_SET('all', make_name) AND FIND_IN_SET('all', model_name)))   AND ((min_year <= "+year+" AND max_year >= "+year+") OR  (min_year = '' AND max_year = '')) AND ((max_mileage >= "+mileage+" AND  min_mileage <= "+mileage+") OR (max_mileage ='' AND min_mileage = '')) AND FIND_IN_SET('"+zipcode+"', final_zip) AND  ((FIND_IN_SET('"+damage3+"', damageComma)  OR  damageComma = '')) AND ((FIND_IN_SET('"+airbag1+"', airbagComma)  OR airbagComma = '')) AND ((FIND_IN_SET('"+drive1+"', driveComma) OR driveComma = '')) AND ((FIND_IN_SET('"+key+"', keyComma) OR keyComma = '')) AND ((FIND_IN_SET('"+title+"', titleComma)  OR titleComma = '')) AND ((FIND_IN_SET('"+fire_damage1+"', firDamageComma)  OR firDamageComma = '')) AND is_deleted='no' order by not_to_exceed desc" 
                    print(query)
                    print("out")
                    cursor.execute(query)
                    return cursor.fetchall()
        except:
            con.rollback()
            return False
        finally:
            con.close()

    def getqoute(self, fdata):
            con = Qoute.connect(self)
            cursor = con.cursor()
            year = fdata['year']
            year = fdata['year']
            fid = fdata['record_id']
            make_code = fdata['make_code']
            make = fdata['make']
            model = fdata['model']
            key = fdata['key']
            zipcode = fdata['v_zip']
            damage = fdata['damage']
            sdamage = fdata['sdamage']
            zipcode = fdata['v_zip']
            title = fdata['title']
            drive = fdata['drive']
            mileage = fdata['mileage']+',000'
            
            drivable ='N'
            
            if mileage==',000':
                    mileage = ''
                    
            transformed_string=mileage.replace(",","")
            
            damageimg = fdata.getlist('damageimg[]')

            #print(damageimg[0])
            if(damage!='MN'):
              if(len(damageimg)>1):
                damage = 'AO'
              else:
                if(len(damageimg)==0):
                  damage = 'MN'
                else:
                  damage = damageimg[0]
            else:
              damage = 'MN'


            cursor.execute("UPDATE accepted_aps set damage1 = %s where id = %s",(damage, fid,))
            con.commit()
              
            if(drive == 'D'):
                drivable ='Y' 
                
            if(sdamage=='Vehicle is in good shape!'):

              sdamage = ''
            elif(damage=='MN'):
              if(sdamage=='Major engine issues' or sdamage=='Major Transmission issues' or sdamage=="Yes, major engine issues" or sdamage=="Yes, major transmission issues"):
                sdamage = ''
                damage = 'MC'
              elif(sdamage=='Major Frame Issues' or sdamage=='Yes, major frame issues'):
                sdamage = ''
                damage = 'UN'
              else:
                sdamage = ''
                damage = damage
            elif(damage!='MN'):
              if(sdamage=='Major engine issues' or sdamage=='Major Transmission issues' or sdamage=="Yes, major engine issues" or sdamage=="Yes, major transmission issues"):
                sdamage = 'MC'
                damage = damage
              elif(sdamage=='Major Frame Issues' or sdamage=='Yes, major frame issues'):
                sdamage = 'UN'
                damage = damage
              else:
                sdamage = ''
                damage = damage
            else:
                sdamage = ''
                damage = damage
                
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
                    "odometerReading" : transformed_string, 
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
                "drivabilityRating": drive,
                "titleCategory": title 
              }
            })
            #return payload
            headers = {
              'countryCode': 'USA',
              'Content-Type': 'application/json',
              'Authorization': access_token,
              'insco':'YCIC',
            }
            conn.request("POST", "/v1/proquote", payload, headers)
            res = conn.getresponse()
            data = res.read()
            return json.loads(data)
