"""
Badge creation tool 
Takes data and prints a badge 
"""
from datetime import datetime
import qrcode
from tkinter import *
from PIL import Image 
import os 
import time
from db import Database
db = Database('./../reader/userdata.db')
db.fetch_all()
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
root.geometry('1000x800')
root.title('Generate qr badge.')

def gen_code():

    fname_entry_data = fname_entry.get()
    lname_entry_data = lname_entry.get()
    gender_entry_data = gender_entry.get()
    uid_entry_data = uid_entry.get()
    enrollment_entry_data = enrollment_entry.get()
    term_entry_data = term_entry.get()
    access_entry_data = access_entry.get()

    if fname_entry_data == '':
        fname_label_warning     .grid(row=0, column=3,padx=(40,10),pady=(40,10))
    elif lname_entry_data == '':
        lname_label_warning     .grid(row=1, column=3,padx=(40,10),pady=10)
    elif gender_entry_data == '':
        gender_label_warning    .grid(row=2, column=3,padx=(40,10),pady=10)
    elif uid_entry_data == '':
        uid_label_warning       .grid(row=3, column=3,padx=(40,10),pady=10)
    elif enrollment_entry_data == '':
        enrollment_label_warning.grid(row=4, column=3,padx=(40,10),pady=10)
    elif term_entry_data == '':
        term_label_warning      .grid(row=5, column=3,padx=(40,10),pady=10)
    elif access_entry_data == '':
        access_label_warning    .grid(row=6, column=3,padx=(40,10),pady=10)
    else:
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

# Labels
fname_label         = Label(root,text='First name :')
lname_label         = Label(root,text='Last name :')
gender_label        = Label(root,text='Gender :')
uid_label           = Label(root,text='UID :')
enrollment_label    = Label(root,text='Enrollment :')
term_label          = Label(root,text='Term :')
access_label        = Label(root,text='Access :')

fname_label     .grid(row=0, column=0,padx=(40,10),pady=(40,10))
lname_label     .grid(row=1, column=0,padx=(40,10),pady=10)
gender_label    .grid(row=2, column=0,padx=(40,10),pady=10)
uid_label       .grid(row=3, column=0,padx=(40,10),pady=10)
enrollment_label.grid(row=4, column=0,padx=(40,10),pady=10)
term_label      .grid(row=5, column=0,padx=(40,10),pady=10)
access_label    .grid(row=6, column=0,padx=(40,10),pady=10)

# Label warnings 
fname_label_warning         = Label(root,text='First name is required')
lname_label_warning         = Label(root,text='Last name is required')
gender_label_warning        = Label(root,text='Gender is required')
uid_label_warning           = Label(root,text='UID is required')
enrollment_label_warning    = Label(root,text='Enrollment is required ')
term_label_warning          = Label(root,text='Term is required ')
access_label_warning        = Label(root,text='Access is required ')

# Entries

fname_entry         = Entry(root, width = 20)
lname_entry         = Entry(root, width = 20)
gender_entry        = Entry(root, width = 20)
uid_entry           = Entry(root, width = 20)
enrollment_entry    = Entry(root, width = 20)
term_entry          = Entry(root, width = 20)
access_entry        = Entry(root, width = 20)

fname_entry     .grid(row=0, column=1,padx=10,pady=(40,10))
lname_entry     .grid(row=1, column=1,padx=10,pady=10)
gender_entry    .grid(row=2, column=1,padx=10,pady=10)
uid_entry       .grid(row=3, column=1,padx=10,pady=10)
enrollment_entry.grid(row=4, column=1,padx=10,pady=10)
term_entry      .grid(row=5, column=1,padx=10,pady=10)
access_entry    .grid(row=6, column=1,padx=10,pady=10)

Button(root,text='Add Student & QRCode ', command = gen_code)   .grid(row=10,column=1,padx = 10 , pady = (50,10) )
Button(root,text='Clear input ', command = clear_input)         .grid(row=12,column=1,padx = 10 , pady = (10,10)  )
Button(root,text='Exit program', command = root.quit)           .grid(row=13,column=1,padx = 10 ,pady = (10,10) )

def main():
    root.mainloop()

if __name__ == "__main__":
    main()














# ID-1
# The ID-1 format specifies a size of 85.60 by 53.98 millimetres (3 3⁄8 in × 2 1⁄8 in) and rounded corners with a radius of 2.88–3.48 mm (about ​1⁄8 in). It is commonly used for payment cards (ATM cards, credit cards, debit cards, etc.). Today it is also used for driving licences and personal identity cards in many countries, automated fare collection system cards for public transport, in retail loyalty cards, and even crew member certificates (particularly for aircrew[5]). 

# common ppi setting is 300 ppi 

# 1 inch is 300 pixels 

# 3.375 * 2.15 inches
# 1,012.5 px * 645

# 7.25625 inches sq 

# so our canvas will need to be 

#  3.370 inches wide and 2.125 inches high.