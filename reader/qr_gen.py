"""
Badge creation tool 
Takes data and prints a badge 
"""
from datetime import datetime
import qrcode
from tkinter import *
from tkinter import ttk
from PIL import Image 
import os 
import time
from db import Database
db = Database('./../reader/userdata.db')
db_data = db.fetch_all()
print("[ log ] - Imports successful.")

badge_dir = './badges'
now = datetime.now()
current_time = now.strftime("%H_%M_%S")

def generate_qr(data,main_color,bg_color,qr_ver,padd,box_sixe):
    qr = qrcode.QRCode(
        version=qr_ver,
        error_correction = qrcode.constants.ERROR_CORRECT_Q,
        box_size=box_sixe,
        border=padd,
    )
    qr.add_data(data)
    qr.make(fit=True)
    return qr.make_image(fill_color=main_color, back_color=bg_color)

root = Tk()
root.geometry('1400x800')
root.title('Generate qr badge.')

def gen_code():

    fname_entry_data = fname_entry.get()
    lname_entry_data = lname_entry.get()
    gender_entry_data = gender_entry.get()
    uid_entry_data = uid_entry.get()
    enrollment_entry_data = enrollment_entry.get()
    term_entry_data = term_entry.get()
    access_entry_data = access_entry.get()

    data = db.insert_one(fname_entry_data,lname_entry_data,uid_entry_data,gender_entry_data,enrollment_entry_data,access_entry_data,term_entry_data,time.time())
    fill_color  = '#000000'
    background = '#ffffff'
    qr_code = generate_qr(data,fill_color,background,2,1,20)
    qr_code.save(os.path.join(badge_dir , f'{current_time}-{fname_entry_data}-qrcode.png'))
    print("Generated qrcode")
    return None

def gen_a4px():
    canvas = Image.new('RGBA', (2480,3508), color = (255,255,255,255))
    canvas.save('canvas.png')

gen_a4px()

def clear_input():
    fname_entry.delete(0, END)
    lname_entry.delete(0, END)
    gender_entry.delete(0, END)
    uid_entry.delete(0, END)
    enrollment_entry.delete(0, END)
    term_entry.delete(0, END)
    access_entry.delete(0, END)
    return None

udata_frame     = LabelFrame(root, text="User data",padx =5 ,pady=5)
udata_frame     .grid(row=0,column=0,columnspan=4,padx =10 ,pady=10,sticky="NESW")

log_frame       = LabelFrame(root, text="Log box ",padx =5 ,pady=5)
log_frame       .grid(row=1,column=0,columnspan=4,padx =10 ,pady=10,sticky="NESW")

button_frame    = LabelFrame(root, text="Commands",padx =5 ,pady=5)
button_frame    .grid(row=12,column=0,columnspan=4,padx =10 ,pady=10,sticky="NESW")

db_frame        = LabelFrame(root, text="Database",padx =5 ,pady=5)
db_frame        .grid(row=0,column=4,columnspan=4,rowspan=20 ,padx =10 ,pady=10,sticky="NESW")

# Labels
fname_label         = Label(udata_frame,text='First name :')
lname_label         = Label(udata_frame,text='Last name :')
gender_label        = Label(udata_frame,text='Gender :')
uid_label           = Label(udata_frame,text='UID :')
enrollment_label    = Label(udata_frame,text='Enrollment :')
term_label          = Label(udata_frame,text='Term :')
access_label        = Label(udata_frame,text='Access :')

fname_label     .grid(row=0, column=0,padx=(15,10),pady=10)
lname_label     .grid(row=1, column=0,padx=(15,10),pady=10)
gender_label    .grid(row=2, column=0,padx=(15,10),pady=10)
uid_label       .grid(row=3, column=0,padx=(15,10),pady=10)
enrollment_label.grid(row=4, column=0,padx=(15,10),pady=10)
term_label      .grid(row=5, column=0,padx=(15,10),pady=10)
access_label    .grid(row=6, column=0,padx=(15,10),pady=10)



# Entries

fname_entry         = Entry(udata_frame, width = 20)
lname_entry         = Entry(udata_frame, width = 20)
gender_entry        = Entry(udata_frame, width = 20)
uid_entry           = Entry(udata_frame, width = 20)
enrollment_entry    = Entry(udata_frame, width = 20)
term_entry          = Entry(udata_frame, width = 20)
access_entry        = Entry(udata_frame, width = 20)

fname_entry     .grid(row=0, column=1,padx=10,pady=10)
lname_entry     .grid(row=1, column=1,padx=10,pady=10)
gender_entry    .grid(row=2, column=1,padx=10,pady=10)
uid_entry       .grid(row=3, column=1,padx=10,pady=10)
enrollment_entry.grid(row=4, column=1,padx=10,pady=10)
term_entry      .grid(row=5, column=1,padx=10,pady=10)
access_entry    .grid(row=6, column=1,padx=10,pady=10)

# Command buttons
# -------------------------------------------------------
add_button      = Button(button_frame,text='Add Student  ', command = gen_code)
remove_button   = Button(button_frame,text='Remove student', command = root.quit)
clear_button    = Button(button_frame,text='Clear inputs ', command = clear_input)
exit_button     = Button(button_frame,text='Exit program',fg="#ff1122", command = root.quit)
# -------------------------------------------------------
add_button      .grid(row=10,column=0,padx = 10 , pady = (10,10) ,sticky="NESW" ) 
remove_button   .grid(row=10,column=1,padx = 10 , pady = (10,10) ,sticky="NESW")
clear_button    .grid(row=11,column=0,padx = 10 , pady = (10,10) ,sticky="NESW")
exit_button     .grid(row=11,column=1,padx = 10 , pady = (10,10) ,sticky="NESW")

# log_view
log_view = Listbox(log_frame ,height=10, width=40,font=('raleway'),fg='#000',bg="#fff")
log_view.grid(row = 0, column = 0,columnspan=4,rowspan=1,sticky="NESW")
# -------------------------------------------------------
# db_view
# -------------------------------------------------------
db_view = ttk.Treeview(db_frame,height=30)
db_view['columns'] = ("fname","lname","uid","gender","enrollment","term","access")
# -------------------------------------------------------
db_view.column('#0'         ,width=30 ,anchor=CENTER)
db_view.column('fname'      ,width=120,anchor=CENTER)
db_view.column('lname'      ,width=120,anchor=CENTER)
db_view.column('uid'        ,width=120,anchor=CENTER)
db_view.column('gender'     ,width=120,anchor=CENTER)
db_view.column('enrollment' ,width=120,anchor=CENTER)
db_view.column('term'       ,width=120,anchor=CENTER)
db_view.column('access'     ,width=120,anchor=CENTER)
# -------------------------------------------------------
db_view.heading('#0'            ,text='#0')
db_view.heading('fname'         ,text='First Name')
db_view.heading('lname'         ,text='Last Name')
db_view.heading('uid'           ,text='UID')
db_view.heading('gender'        ,text='Gender')
db_view.heading('enrollment'    ,text='Enrollment')
db_view.heading('term'          ,text='Term')
db_view.heading('access'        ,text='Access')
# -------------------------------------------------------
# print(db_data)
i=0
for entry in db_data:
    print(entry)
    display = entry[1:8]
    db_view.insert(parent='',index='end',iid=i,text='',values=(display))
    i += 1
# -------------------------------------------------------
db_view.grid(row=0, column=5, rowspan=100, padx=10, pady=10)

def main():
    root.mainloop()

if __name__ == "__main__":
    main()

