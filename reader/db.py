import sqlite3
import hashlib
import datetime
import time 

def encode_uid(uid):
    encoded = hashlib.md5(str(uid).encode('utf-8'))
    return encoded.hexdigest()


con = sqlite3.connect('./logs.db')
cur = con.cursor()


class Database:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute("""CREATE TABLE IF NOT EXISTS users (
            hui text ,
            f_name text ,   
            l_name text ,
            uid text,
            gender text,
            enrollment text,
            access text,
            term text,
            dates_eaten list)""")
        self.conn.commit()

    def fetch_all(self):
        self.cur.execute("""SELECT * FROM users """)
        rows = self.cur.fetchall()
        # print(rows)
        return rows

    def insert_one(self,f_name, l_name, uid, gender, enrollment, access, term, dates_eaten):
        print("insert invoked ")
        data = f"{f_name} {l_name} {uid} {gender} {enrollment} {access} {term}"
        print(data)
        hui = encode_uid(data)
        print(hui)
        h = hui
        f = f_name
        l = l_name
        g = gender
        u = uid
        e = enrollment
        a = access
        t = term
        d = dates_eaten

        self.cur.execute(f"INSERT INTO users VALUES ('{h}','{f}','{l}','{u}','{g}','{e}','{a}','{t}','{d}')")
        self.conn.commit()

    def update_date(self,hui):

        self.cur.execute("SELECT * FROM users WHERE hui = ? ",(hui,))
        data = self.cur.fetchall()
        print('im here ',data)
        # print(f'Update invoked\n\tUser : {data[0][1]} {data[0][2]}\n')
        self.cur.execute("SELECT dates_eaten FROM users WHERE hui = ? ",(hui,))
        data = self.cur.fetchall()
        if data:
            print('data exissts')

            # The time last scanned is the query return from the hui 
            time_last_scanned = data[0][0]
            timenow = time.time()
            # The difference in time between last scanned and current time 
            time_difference  = timenow - time_last_scanned 
            tdiff_secs = round(time_difference,2)
            tdiff_min = round(time_difference/60,2)
            tdiff_hrs = round(time_difference/360,2)
            tdiff_hrs = round(time_difference/360,2)
            tdiff_dys = round(time_difference/8640,2)

            # print('Time since last scan : ')
            # print('\t',tdiff_secs, 'Seconds')
            # print('\t',tdiff_min,  'Minutes')
            # print('\t',tdiff_hrs , 'Hours')
            # print('\t',tdiff_dys , 'Days\n')

            if tdiff_secs > 10:
                # if the time between scans is above 2 minutes , user is sus 
                # register the scan but also sound the alarm 
                self.cur.execute("UPDATE users SET dates_eaten = ? WHERE hui = ? ", (timenow,hui))
                self.conn.commit()
                print('[ Error ] - Duplicate entry attempt ')
                return "dupe entry"
                # Sound da alarms 

            elif time_difference/360 > 2.1 :
                # valid if the difference in scan times is above 2 hours and a bit more  
                self.cur.execute("UPDATE users SET dates_eaten = ? WHERE hui = ? ", (timenow,hui))
                self.conn.commit()
                pass
            else : 
                self.cur.execute("UPDATE users SET dates_eaten = ? WHERE hui = ? ", (timenow,hui))
                self.conn.commit()
            # if the time between scans is below 2 minutes , the user may just be stupid so allow it 
                pass

            self.cur.execute("SELECT * FROM users WHERE hui = ? ",(hui,))
            data = self.cur.fetchall()
            return data

        else: 
            print('no data found')
            return 'not valid code'
        

    def __del__(self):
        self.conn.close()


db = Database('userdata.db')

# db.insert_one('ribka','solomon','gur/00000/12','female','engeneering','student','2nd year','')
db.fetch_all()

# db.update_date('2052af8392437796097542a9d10dad1b')

# db.fetch_all()