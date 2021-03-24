import sqlite3
import hashlib

def encode_uid(uid):
    encoded = hashlib.md5(str(uid).encode('utf-8'))
    return encoded.hexdigest()

con = sqlite3.connect('./logs.db')
cur = con.cursor()


def add_user(f_name, l_name, uid, gender, enrollment, access, term):
    print(encode_uid(uid))
    cur.execute(
        f"""INSERT INTO users VALUES ('{f_name}','{l_name}','{encode_uid(uid)}','{gender}','{enrollment}','{access}','{term}')""")


add_user('dawit','solomon','gur/00000/12','male','engeneering','student','2ndyear')

print(con)
print(cur)


# users  = cur.execute("""CREATE TABLE users(
#     f_name text ,
#     l_name text ,
#     uid text,
#     gender text,
#     enrollment text,
#     access text,
#     term text

# ) """)


# cur.execute("""INSERT INTO users VALUES ('admin','doe','gur/00000/12')""")

cur.execute("""SELECT * FROM users""")

print(cur.fetchall())
print(cur.fetchone())

con.commit()
con.close()
