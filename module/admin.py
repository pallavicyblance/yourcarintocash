import pymysql
class Admin:
    def connect(self):
       return pymysql.connect(host="localhost", user="root", password="", database="carcash", charset='utf8mb4')
    def read(self, id):
        con = Admin.connect(self)
        cursor = con.cursor()
        try:
            if id == None:
                cursor.execute("SELECT * FROM admin order by name asc")
            else:
                cursor.execute(
                    "SELECT * FROM admin where id = %s ", (id,))
            return cursor.fetchall()
        except:
            return ()
        finally:
            con.close()
    def adminlogin(self, data):
        con = Admin.connect(self)
        cursor = con.cursor()
        
        try: 
            # return "SELECT * FROM admin where username = %s AND password = %s ", (data['username'],data['password'],)
            cursor.execute("SELECT * FROM admin where email = %s AND password = %s ", (data['username'],data['password'],))
            return cursor.fetchall()          
          
        except:                       
            return False
        finally:
            con.close() 

    def update(self, id, data,email_noti_data):
        con = Admin.connect(self)
        cursor = con.cursor()

        try:
            cursor.execute("UPDATE admin set first_name = %s, last_name = %s, phone = %s , address = %s , email = %s , email_noti = %s where id = %s",
                           (data['first_name'], data['last_name'], data['phone'], data['address'], data['email'],email_noti_data, id,))
            con.commit()
            return True
        except:
            con.rollback()
            return False
        finally:
            con.close()

    def delete(self, id):
        con = Admin.connect(self)
        cursor = con.cursor()

        try:
            cursor.execute("DELETE FROM admin where id = %s", (id,))
            con.commit()

            return True
        except:
            con.rollback()

            return False
        finally:
            con.close()
    
    def listing(self):
        con = Admin.connect(self)
        cursor = con.cursor()

        try:

            cursor.execute("SELECT * FROM admin order by id desc")
                # cursor.execute("SELECT * FROM `admin`")
            return cursor.fetchall()
        except:
            con.rollback()
            return "erroor"
        finally:
            con.close()
            
    
    def remove(self , id):
        con = Admin.connect(self)
        cursor = con.cursor()
        try:
            cursor.execute("DELETE FROM admin WHERE id = %s" ,(id,))
            con.commit()
            return "Admin has been Deleted successfully."
        except:
            con.rollback()
            return False
        finally:
            con.close()
    # darshan changes 31-08-2023 1 closw
    def editdata(self,id):
        con = Admin.connect(self)
        cursor = con.cursor()
        try:
            cursor.execute("SELECT * FROM `admin` WHERE id = %s",(id,))
            return cursor.fetchone()
        except:
            con.rollback()
            return False
        finally:
            con.close()
    # darshan 1 changes 21/08/2023 close
    # darshan changes 22/08/2023

    # unique_validatation
    def valid(self,data):
        con = Admin.connect(self)
        cursor = con.cursor()
        try:
            if data['id']:
                return 0
            else:
                cursor.execute("SELECT username,email FROM admin WHERE email =%s OR username =%s",(data['email'],data['username']))
                # con.commit()
                return cursor.fetchall()
        except:
            return "not fatching"
        finally:
            con.close()
    # darshan changes 22/08/2023 close
    def role(self,id):
        con = Admin.connect(self)
        cursor = con.cursor()
        try:
            cursor.execute("SELECT role FROM admin WHERE id = %s",(id,))
            return cursor.fetchall()
        except:
            return False
        finally:
            con.close()
            
    def updatepass(self,data):
        con = Admin.connect(self)
        cursor = con.cursor()
        try:
            cursor.execute("UPDATE admin set password = %s where id = %s",(data['confirm_password'],data['id']))
            con.commit()
            return "Password has been changed successfully."
        except:
            return "error"
        finally:
            con.close()
            
    def insert(self, data,email_noti_data):
        con = Admin.connect(self)
        con1 = Admin.connect(self)
        cursor = con.cursor()
        cursor1 = con1.cursor()
        try:
            if data['id']:
                # return data
                cursor.execute("UPDATE admin set first_name = %s, last_name = %s, phone = %s , address = %s , email = %s , role=%s , email_noti=%s where id = %s",(data['first_name'], data['last_name'], data['phone'],data['address'],data['email'],data['role'],email_noti_data, data['id'],))
                con.commit()
                if data['role'] == "Staff":
                    return "Staff has been Updated successfully."
                else:
                    return "Admin has been Updated successfully."
            else:
                cursor.execute("SELECT username FROM admin WHERE username =%s",(data['username']))
                cursor1.execute("SELECT email FROM admin WHERE email =%s",(data['email']))
                # return len(cursor.fetchall())
                fetch = len(cursor.fetchall())
                fetch1=len(cursor1.fetchall())
                # return fetch
                if fetch != 0:
                    return 0
                elif fetch1 != 0:
                    return 1
                # else:
                #     return "inserted suuccesss"
                else:
                    cursor.execute("INSERT INTO admin(first_name,last_name,phone,address,username,email,password,role,email_noti) VALUES(%s, %s, %s,%s, %s, %s,%s,%s,%s)",(data['first_name'], data['last_name'], data['phone'],data['address'],data['username'],data['email'],data['password'],data['role'],email_noti_data))
                    con.commit()
                    if data['role'] == "Staff":
                        return "Staff has been Created successfully."
                    else:
                        return "Admin has been Created successfully."
        except:
            con.rollback()
            return False
        finally:
            con.close()

    # code added by pallavi    
    def storeToken(self, jwtToken, id, pubnum_auth_key, pubnum_expiration, pubnum_subscribe_key):
        con = Admin.connect(self)
        cursor = con.cursor()
        try:

            cursor.execute("SELECT * FROM acv_jwt_token where user_id = %s", (id,))
            fetchone = cursor.fetchone()

            if fetchone is not None:
                cursor.execute("UPDATE acv_jwt_token set jwt_token = %s, pubnum_auth_key = %s, pubnum_expiration = %s, pubnum_subscribe_key = %s where user_id = %s", (jwtToken,pubnum_auth_key, pubnum_expiration, pubnum_subscribe_key,id))
            else:
                cursor.execute("INSERT INTO acv_jwt_token (jwt_token,user_id,pubnum_auth_key,pubnum_expiration,pubnum_subscribe_key) VALUES (%s, %s, %s, %s, %s)", (jwtToken,id,pubnum_auth_key, pubnum_expiration, pubnum_subscribe_key))
            con.commit()
            return "Token has been stored successfully."
        except:
            return "error"
        finally:
            con.close()

    def getjwttoken(self,id):
        con = Admin.connect(self)
        cursor = con.cursor()
        try:
            cursor.execute("SELECT jwt_token,user_id,pubnum_auth_key,pubnum_subscribe_key FROM acv_jwt_token where user_id = %s",(id))
            return cursor.fetchone()
        except:
            return "error"
        finally:
            con.close()

    # code ended by pallavi
    
    
