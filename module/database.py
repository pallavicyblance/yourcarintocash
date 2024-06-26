import pymysql


class Database:

    def connect(self):

        return pymysql.connect(host="localhost", user="root", password="root", database="carintocash_api", charset='utf8mb4')

    def connect_index(self):
        con = pymysql.connect(host="localhost", user="root", password="root", database="carintocash_api",
                              autocommit=True, charset='utf8mb4')
        return con.cursor(pymysql.cursors.DictCursor)

    def read(self, id):
        con = Database.connect(self)
        cursor = con.cursor()

        try:
            if id == None:
                cursor.execute("SELECT * FROM phone_book order by name asc")
            else:
                cursor.execute(
                    "SELECT * FROM phone_book where id = %s order by name asc", (id,))

            return cursor.fetchall()
        except:
            return ()
        finally:
            con.close()

    def insert(self, data):
        con = Database.connect(self)
        cursor = con.cursor()

        try:
            cursor.execute("INSERT INTO phone_book(name,phone,address) VALUES(%s, %s, %s)",
                           (data['name'], data['phone'], data['address'],))
            con.commit()

            return True
        except:
            con.rollback()

            return False
        finally:
            con.close()

    def update(self, id, data):
        con = Database.connect(self)
        cursor = con.cursor()

        try:
            cursor.execute("UPDATE phone_book set name = %s, phone = %s, address = %s where id = %s",
                           (data['name'], data['phone'], data['address'], id,))
            con.commit()

            return True
        except:
            con.rollback()

            return False
        finally:
            con.close()

    def delete(self, id):
        con = Database.connect(self)
        cursor = con.cursor()

        try:
            cursor.execute("DELETE FROM phone_book where id = %s", (id,))
            con.commit()

            return True
        except:
            con.rollback()

            return False
        finally:
            con.close()
