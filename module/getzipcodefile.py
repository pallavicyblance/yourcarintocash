import pymysql
import smtplib
import datetime

import requests

class Getzipcodefile:

    def connect(self):
        return pymysql.connect(host="localhost", user="root", password="", database="carcash", charset='utf8mb4')
        #return pymysql.connect(host="localhost", user="root", password="", database="carintocash", charset='utf8mb4')
    
    def getNewZipFunc(self,zipData):
        con = Getzipcodefile.connect(self)
        cursor = con.cursor()

        con1 = Getzipcodefile.connect(self)
        cursor5 = con1.cursor()
        allZip1 = ''
        if zipData !='' : 
            q11 = "SELECT * FROM zipcode where zipcode='"+zipData+"'"
            cursor.execute(q11)
            getRecorddata1 = cursor.fetchone() 
            
            if getRecorddata1:
                q22 = "SELECT `zipcode`, ( 3959 * ACOS( COS( RADIANS(" + str(getRecorddata1[4]) + ") ) * COS( RADIANS(`latitude`) ) * COS( RADIANS(`longitude`) - RADIANS(" + str(getRecorddata1[5]) + ") ) + SIN( RADIANS(" + str(getRecorddata1[4]) + ") ) * SIN( RADIANS(`latitude`) ) ) ) AS distance FROM zipcode HAVING distance <= " + str(data['distance_amt1']) + " ORDER BY distance"
                cursor5.execute(q22)
                getRecordsub1 = cursor5.fetchall()
                # Process the results
                for k in getRecordsub1:
                    allZip1 = allZip1 +k[0] + ','
                cursor5.close()
        return allZip1

