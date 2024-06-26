import pymysql
import http.client
import json
import random

class Offer:  

    def connect(self):
        return pymysql.connect(host="localhost", user="root", password="root", database="carintocash_api", charset='utf8mb4')
    def getoffer(self,fdata):
            con = Offer.connect(self)
            cursor = con.cursor()
            
            try:
                cursor.execute("SELECT * FROM accepted_aps where id = %s", (fdata['id']))
                fetchall = cursor.fetchall()
                
                #return fetchall
                year = fetchall[0][1]
                make_code = fetchall[0][6]
                make = fetchall[0][4]
                model = fetchall[0][5]
                key = fetchall[0][11]
                zipcode = fetchall[0][8]
                damage = fetchall[0][9]
                zipcode = fetchall[0][8]
                title = fetchall[0][10]
                drive = fetchall[0][12]
                revised_price = fetchall[0][40]
                locationname = fetchall[0][17]
                address1 = fetchall[0][18]
                address2 = fetchall[0][19]
                state = fetchall[0][21]
    
                fname = fetchall[0][22]
                lname = fetchall[0][22]
                phone = fetchall[0][24]
                alternatephone = fetchall[0][25]
                ownerfname = fetchall[0][26]
                ownerlname = fetchall[0][26]
                payeefname = fetchall[0][28]
                payeelname = fetchall[0][28]
                city = fetchall[0][20]
                vin = random.randint(1001,9999999999999999999)
    
                drivable ='N'
                if(drive == 'D'):
                    drivable ='Y'
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
                #return access_token
                conn = http.client.HTTPSConnection("b2b.copart.com")
                payload = json.dumps({
    
                  "transactionID": vin,
                  "sellerTransactionID" : vin,
    
                  "currencyCode" : "USD",
                  "companyCode" : "TWIN",
                  "sellerCode" : "IWC1",
                  "assignmentDetails" : {
                    "claimNumber" : "A $"+ revised_price+' '+drive,
                    "primaryDamage" : damage,
                    "pickupRequired" : "Y"
                  },
                  "vehicleDetails" : {
    
                    "vin" : vin,
    
                    "modelYear" : year,
                    "make" : make_code,
                    "modelName" : model,
                    "actualCashValue" : 5000,
                    "repairCost" : 200,
                    "vehicleType" : "V",
                    "mileage" : '',
                    "hasKeys" : key,
                    "drivableInd" : drivable
                  },
    
                  "vehicleLocation" : {
                      "type" : 'V',
                      "name" : fname+' '+lname,
                      "address" : {
                          "addressLine1" : address1,
                          "addressLine2" : address2,
                          "city" : city,
                          "state" : state,
                          "zipcode": zipcode,
                          "country" : "USA"
                      },
                      "telephone" : {
                          "countryCode" : "+1",
                          "number" : phone,
                      },
                      "alternateTelephone" : {
                          "countryCode" : "+1",
                          "number" : alternatephone,
                          
                      }
                  },
                #   "ownerDetails" : {
                #      "name" : {
                #       "firstName" : ownerfname,
                #       "lastName" : ownerfname
                #      }
                #   },
                  "claimantDetails" : {
                      "name" : {
                          "firstName" : fname,
                          "lastName" : lname
                      }
                  },
                  "adjusterDetails" : [
                    {
                      "role": "Assignment",
                      "adjuster": {
                          "employee": {
                              "name": {
                                  "companyName": "TWIN CITIES AUCTION",
                                  #"salutation" : "Mr",
                                  "firstName": "SALES TEAM",
                                  "lastName": "21"
                              },
                              "telephone": {
                                  "type": "Mobile",
                                  "countrycode": "+1",
                                  "number": "972-3915325",
                              },
                              "email": "sales.team21@copart.com"
                          },
                          "supervisor": {
                              "name": {
                                  "companyName": "TWIN CITIES AUCTION",
                                  #"salutation" : "Mr",
                                  "firstName": "SALES TEAM",
                                  "lastName": "21"
                              },
                              "telephone": {
                                  "type": "Mobile",
                                  "countrycode": "+1",
                                  "number": "972-3915325",
                              },
                              "email": "sales.team21@copart.com"
                          }
                      }
                    },
                    {
                      "role": "Auction",
                      "adjuster": {
                          "employee": {
                              "name": {
                                  "companyName": "TWIN CITIES AUCTION",
                                  #"salutation" : "Mr",
                                  "firstName": "SALES TEAM",
                                  "lastName": "21"
                              },
                              "telephone": {
                                  "type": "Mobile",
                                  "countrycode": "+1",
                                  "number": "972-3915325",
                              },
                              "email": "sales.team21@copart.com"
                          },
                          "supervisor": {
                              "name": {
                                  "companyName": "TWIN CITIES AUCTION",
                                  #"salutation" : "Mr",
                                  "firstName": "SALES TEAM",
                                  "lastName": "21"
                              },
                              "telephone": {
                                  "type": "Mobile",
                                  "countrycode": "+1",
                                  "number": "972-3915325",
                              },
                              "email": "sales.team21@copart.com"
                          }
                      }
                    },
                  ],
                  "insuredDetails": {
                     "name": {
                      "companyName" : "TWIN CITIES AUCTION",
                      "firstName" : payeefname,
                      "lastName" : payeefname,
                     }
                  },
                  "alternatePayee" : {
                      "name" : {
                          "firstName" : payeefname,
                          "lastName" : payeelname
                      }
                  }
                })
                
                headers = {
                  'countryCode': 'USA',
                  'Content-Type': 'application/json',
                  'Authorization': access_token,
                  'insco':'YCIC',
                }
                conn.request("POST", "/usaps/v2/assignment", payload, headers)
                res = conn.getresponse()
                data = res.read()
                
                
                cursor.execute("UPDATE accepted_aps set dispatched = %s where id = %s",('yes', fetchall[0][0],))
                con.commit()
                
                return json.loads(data)
            except:
                con.rollback()
                return False
            finally:
                con.close() 
