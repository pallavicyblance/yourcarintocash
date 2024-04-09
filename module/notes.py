import pymysql
import smtplib
import datetime

import requests
from Misc.functions import *

import requests

class Notes:



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
        return pymysql.connect(host="localhost", user="root", password="", database="carintocash", charset='utf8mb4')

    def noteadd(self , data):
        con =  Notes.connect(self)
        cursor = con.cursor()
        try:
            # print(data)
            note = data['notes'].replace("\n", "<br />")
            cursor.execute("INSERT INTO notes(`inquiry_id`,`user_id`, `notes` ,`file`, `created_date`) VALUES (%s,%s,%s,%s,%s)",(data['inquiry_id'], data['user_id'],note, data['file'],gettimeincst(),))
            con.commit()
            return True
        except:
            con.rollback()
            return False
        finally:
            con.close()

    def get_notes(self, id):
        con =  Notes.connect(self)
        cursor = con.cursor()
        try:
            # print(id)
            cursor.execute("SELECT notes.*, admin.first_name FROM notes INNER JOIN admin ON admin.id = notes.user_id WHERE notes.inquiry_id = %s ORDER BY created_date DESC",(id,))

            return cursor.fetchall()
        except:
            con.rollback()
            return False
        finally:
            con.close()

    def delete_notes(self,id):
        con =  Notes.connect(self)
        cursor = con.cursor()
        try:
            # print(id)
            cursor.execute("DELETE FROM `notes` WHERE id = %s",(id,))
            con.commit()
            return True
        except:
            con.rollback()
            return False
        finally:
            con.close()

    def update_status(self , data):
        con =  Notes.connect(self)
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