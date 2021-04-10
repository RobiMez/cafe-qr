import sqlite3
import hashlib
import datetime
import time 

def encode_uid(uid):
    encoded = hashlib.md5(str(uid).encode('utf-8'))
    return encoded.hexdigest()

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
            term text,
            access text,
            dates_eaten text,
            printed text)""")
        self.conn.commit()

    def fetch_all(self):
        self.cur.execute("""SELECT * FROM users """)
        rows = self.cur.fetchall()
        # print(rows)
        return rows

    def insert_one(self,f_name, l_name, uid, gender, enrollment, access, term, dates_eaten,printed):
        print("[ insert ] - Adding a new user.")
        # perfofrm sanitization 
        error = ""
        if f_name == '':
            print("No first name detected ")
            error = "f_name_none"
            return error
        elif l_name == '':
            print("No last name detected ")
            error = "l_name_none"
            return error
        elif uid == '':
            print("No University id detected ")
            error = "uid_none"
            return error
        elif gender == None or gender == 'None':
            print("No gender detected ")
            error = "gender_none"
            return error
        elif enrollment == '':
            print("No Enrollment detected ")
            error = "enrollment_none"
            return error
        elif access == '':
            print("No Access level detected ")
            error = "access_none"
            return error
        elif term == '':
            print("No Term detected ")
            error = "term_none"
            return error
        
        data = f"{f_name} {l_name} {uid} {gender} {enrollment} {term} {access}"
        print(data)
        hui = encode_uid(data)
        self.cur.execute("SELECT * FROM users WHERE hui = ? ",(hui,))
        data_fetched = self.cur.fetchall()
        print(data_fetched)
        if data_fetched != []:
            print("this user already exists")
            error = 'user_exists'
            return error

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
        p = printed
        print('Executing sql')
        self.cur.execute(f"INSERT INTO users VALUES ('{h}','{f}','{l}','{u}','{g}','{e}','{t}','{a}','{d}',{p})")
        self.conn.commit()
        return hui

    def update_date(self,hui):

        self.cur.execute("SELECT * FROM users WHERE hui = ? ",(hui,))
        data = self.cur.fetchall()
        print('Data : ',data)
        # print(f'Update invoked\n\tUser : {data[0][1]} {data[0][2]}\n')
        self.cur.execute("SELECT dates_eaten FROM users WHERE hui = ? ",(hui,))
        data = self.cur.fetchall()
        if data:
            print('data Exists')

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

            if tdiff_secs > 13:
                
                # if the time between scans is above 2 minutes , user is sus 
                # register the scan but also sound the alarm 
                self.cur.execute("UPDATE users SET dates_eaten = ? WHERE hui = ? ", (timenow,hui))
                self.conn.commit()
                print('[ Error ] - Duplicate entry attempt ')
                self.cur.execute("SELECT * FROM users WHERE hui = ? ",(hui,))
                data = self.cur.fetchall()
                return ("dupe entry",data)
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
        
    def remove_one(self,hui):
        self.cur.execute("DELETE FROM users WHERE hui = ? ",(hui,))
        self.conn.commit()
        data = self.cur.fetchall()
        return data
        pass
    
    def update_print_state(self,hui, print_state):
        self.cur.execute("UPDATE users SET printed = ? WHERE hui = ? ",(print_state,hui,))
        self.conn.commit()
        data = self.cur.fetchall()
        return data
        pass
    
    
    def __del__(self):
        self.conn.close()


        
        
db = Database('userdata.db')

db.fetch_all()
