"""
Badge creation tool 
Takes data and prints a badge 
"""
from datetime import datetime
import qrcode
from tkinter import *
from PIL import Image 
import os 
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
root.geometry('400x400')
root.title('Generate qr badge.')

def gen_code():
    data = e.get()
    fill_color  = '#000000'
    background = '#ffffff'
    qr_code = generate_qr(data,fill_color,background,2,1,20)
    qr_code.save(os.path.join(badge_dir , f'{current_time}-qrcode.png'))
    print("Generated qrcode")
    return None

def gen_a4px():
    canvas = Image.new('RGBA', (2480,3508), color = (255,255,255,255))
    canvas.save('canvas.png')

gen_a4px()

def clear_input():
    e.delete(0, END)
    return None

e = Entry(root, width = 20)
e.pack(padx = 30 , pady = 30 )

Button(root,text='Generate QR code ', command = gen_code).pack(padx = 30 , pady = 30 )
Button(root,text='Clear input ', command = clear_input).pack(padx = 30 , pady = 30 )



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