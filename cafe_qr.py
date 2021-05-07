# library imports : 
import os 
import time
import qrcode
import sqlite3
import hashlib
import cv2
from datetime import datetime
from tkinter import Tk,Frame,LabelFrame,Entry,StringVar,Radiobutton,NSEW,Label,Listbox,CENTER,NO,END,OptionMenu,Button,Scrollbar
from tkinter import ttk
from PIL import Image, ImageDraw, ImageFont
from playsound import playsound
from db import Database
print("[ Prerun check ] - Imports Successful.")
# window root definition 

root = Tk()
app_width = 1520
app_height = 740
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width /2) - (app_width/2)
y = (screen_height /2 )- (app_height/2)
# window size and positioning 
root.geometry(f'{app_width}x{app_height}+{int(x/2)}+{int(y/2)}')
root.title('Cafe QR Administration & Printing ')
# notebook definition 
notebook = ttk.Notebook(root)
notebook.grid(row=0,column=0,padx=1,sticky=NSEW)

admin = Frame(notebook,width=app_width,height=app_height)
printer = Frame(notebook,width=app_width,height=app_height)
eimporter = Frame(notebook,width=app_width,height=app_height)

notebook.add(admin, text='  Administration  ')
notebook.add(printer,text="  Printing  ")
notebook.add(eimporter,text="  Export/Import  ")

# Generator class
class generator():
    """QR Code Generator 
    Methods : 
        gen_a4px
        generate_qr
        generate_single_code
        draw_grids
        draw_major_coords
        paste_badge_background
        write_data
        show_a4
        save_a4
    """
    def __init__(self):
        # load in custom fonts
        self.rubik = ImageFont.truetype(
            "./fonts/Rubik/static/Rubik-Regular.ttf", 36)
        self.rubik_med = ImageFont.truetype(
            "./fonts/Rubik/static/Rubik-Medium.ttf", 36)
        self.qsand = ImageFont.truetype(
            "./fonts/Quicksand/static/Quicksand-Medium.ttf", 60)

    def gen_a4px(self):
        """
        Inputs : 
            self
        Outputs : 
            canvas : PIL image draw object ( canvas but drawable )
            a4 : white a4 size canvas for printing 
            base : transparent mask for alpha compositing 
        """
        # A4 standard size in pixels 2480,3508
        # halved : 1240,1754

        base = Image.new('RGBA', (2480, 3508), color=(255, 255, 255, 0))
        a4 = Image.new('RGBA', (2480, 3508), color=(255, 255, 255, 255))
        canvas = ImageDraw.Draw(a4)
        return canvas, a4,base

    def generate_qr(self,data,main_color,bg_color,qr_ver,padd,box_sixe):
        """
        Inputs :
            self
            data: data to encode as a qr code 
            main_color : color of the readable qr code surface 
            bg_color : background color of the qr code 
            qr_ver : version of the qr code ( how much data it should store ) 
            padd : padding from the surrounding pixels 
            box_size : size of the qr code boxes 
        Outputs :
            PIL image object , ready for pasting 
        """
        qr = qrcode.QRCode(
            version=qr_ver,
            error_correction = qrcode.constants.ERROR_CORRECT_Q,
            box_size=box_sixe,
            border=padd,
        )
        
        qr.add_data(data)
        qr.make(fit=True)
        return qr.make_image(fill_color=main_color, back_color=bg_color)

    def generate_single_code(self,hui):
        """
        Inputs : 
            self
            hui: data to store into the qr code 
        Outputs : 
            qr_code : PIL image 
        """
        fill_color  = '#000000'
        background = '#ffffff'
        qr_code = self.generate_qr(hui,fill_color,background,2,1,20)
        return qr_code

    def draw_grids(self, canvas):
        """
        Inputs : 
            self
            canvas : pil canvas to draw on 
        Outputs : 
            None ( Draws grids on the canvas at 100px divisions .)
        """
        # print('[ Grid ] - drawing grid with 200 pixel subdivisions ')
        # print('[ Grid ] - Canvas param - ', canvas)
        for x in range(0, 3608, 100):
            canvas.line([(0, x), (2480, x)], fill=(
                0, 0, 0, 255), width=1, joint="curve")
        for y in range(0, 3608, 100):
            canvas.line([(y, 0), (y, 3508)], fill=(
                0, 0, 0, 255), width=1, joint="curve")

    def draw_major_coords(self, canvas):
        """
        Inputs : 
            self
            canvas : pil canvas to draw on 
        Outputs : 
            None ( Draws grids on the canvas through the middle and at center points of the badge area .)
        """
        # print('[ Grid ] - drawing grid on major axes and badge location  ')
        # print('[ Grid ] - Canvas param - ', canvas)
        # verticals
        canvas.line([(620, 0), (620, 3508)], fill=(
            0, 0, 0, 255), width=3, joint="curve")
        canvas.line([(1860, 0), (1860, 3508)], fill=(
            0, 0, 0, 255), width=3, joint="curve")
        canvas.line([(1240, 0), (1240, 3508)], fill=(
            0, 0, 0, 255), width=3, joint="curve")
        # horizontals
        canvas.line([(0, 877), (2480, 877)], fill=(
            0, 0, 0, 255), width=3, joint="curve")
        canvas.line([(0, 1754), (2480, 1754)], fill=(
            0, 0, 0, 255), width=3, joint="curve")
        canvas.line([(0, 2631), (2480, 2631)], fill=(
            0, 0, 0, 255), width=3, joint="curve")

    def paste_badge_background(self, canvas, coord):
        """
        Input : 
            self : 
            canvas : canvas to paste on 
            coord : coordinates to paste at 
        Output : 
            None ( Pastes badge background onto the coordinates provided )
        """
        # print('[ Paste bg ] - Pasting badge background  -')
        # print('[ Paste bg ] - Canvas param -', canvas)
        # print('[ Paste bg ] - Coord param -', coord)
        
        for point in coord:
            print("[ Paste bg ] - Pasting badge background on : ", point[0])
            canvas.paste(Image.open('./badge_bg.png'),point[0])

    def write_data(self, canvas, coord, data):
        """
        Input : 
            self : 
            canvas : canvas to write on 
            coord : coordinates to write on  
            data : user data to write on 
        Output : 
            None ( Writes user data on the coordinates provided )
        """
        # print('[ Write ]  - Write User data    -')
        # print('[ Write ]  - Canvas param -', canvas)
        # print('[ Write ]  - Coord param -', coord)
        # print('[ Write ]  - Data param -', data)
        
        i = 0 
        for point in coord:
            print("[ Write ]  - Writing on : ", point)
            # Centered name 
            canvas.text((coord[i][0][0]+437,coord[i][0][1]+734),f"{data[i][0]} {data[i][1]}", font=self.qsand, fill=(0,0,0,255),anchor='ms')
            # left aligned details 
            canvas.text((coord[i][0][0]+60,coord[i][0][1]+794),f"UID : {data[i][2]}", font=self.rubik_med, fill=(0,0,0,255),anchor='lt')
            canvas.text((coord[i][0][0]+60,coord[i][0][1]+864),f"Gender : {data[i][3]}", font=self.rubik, fill=(0,0,0,255),anchor='lt')
            canvas.text((coord[i][0][0]+60,coord[i][0][1]+934),f"Enrollment : {data[i][4]}", font=self.rubik, fill=(0,0,0,255),anchor='lt')
            canvas.text((coord[i][0][0]+60,coord[i][0][1]+1004),f"Term : {data[i][5]}", font=self.rubik, fill=(0,0,0,255),anchor='lt')
            canvas.text((coord[i][0][0]+60,coord[i][0][1]+1074),f"Access : {data[i][6]}", font=self.rubik, fill=(0,0,0,255),anchor='lt')

            i = i + 1

    def show_a4(self, a4,base):
        """
        Inputs : self
            a4 : white canvas 
            base : alpha composite transparent canvas 
        Outputs : 
            None ( Displays the image generated ( a4 ) to the screen with the default photo viewer )
        """
        out = Image.alpha_composite(base, a4)
        print('[ Preview ] Previewing image ')
        out.show()

    def save_a4(self, a4,base,name):
        """
        Inputs : self
            a4 : white canvas 
            base : alpha composite transparent canvas 
            name : The filename of the image to be saved 
        Outputs : 
            None ( saves the image into the out_dir with the filename of name .)
        """
        out = Image.alpha_composite(base, a4)
        out_dir = "./badges"
        print(f'[ Save ] - Saving image as {out_dir}/{name}.png')
        out.save(f'{out_dir}/{name}.png')
# Administration class 
class administration():
    """
    Administration class methods:
        clear_input
        remove_selected
        update_user
        select_data
        render_db_view
        add_user
    """
    def __init__(self):
        # define which database to use for the admin page 
        self.db = Database('../userdata.db')
        self.db_data = self.db.fetch_all()
        # ---------------------------------------------------------------------
        root = admin
        # ---------------------------------------------------------------------
        # Frames ==============================================================
        # ---------------------------------------------------------------------
        udata_frame     = LabelFrame(root, text="User data",padx =5 ,pady=5)
        udata_frame     .grid(row=0,column=0,columnspan=4,padx =10 ,pady=10,sticky="NESW")

        log_frame       = LabelFrame(root, text="Log box ",padx =5 ,pady=5)
        log_frame       .grid(row=1,column=0,columnspan=4,padx =10 ,pady=10,sticky="NESW")

        button_frame    = LabelFrame(root, text="Commands",padx =5 ,pady=5)
        button_frame    .grid(row=12,column=0,columnspan=4,padx =10 ,pady=10,sticky="NESW")

        db_frame        = LabelFrame(root, text="Database",padx =5 ,pady=5)
        db_frame        .grid(row=0,column=4,columnspan=4,rowspan=20 ,padx =10 ,pady=10,sticky="NESW")
        # -------------------------------------------------------------
        # User data ===================================================
        # -------------------------------------------------------------
        # Labels ------------------------------------------------------
        fname_label         = Label(udata_frame,text='First name :')
        lname_label         = Label(udata_frame,text='Last name :')
        gender_label        = Label(udata_frame,text='Gender :')
        uid_label           = Label(udata_frame,text='UID :')
        enrollment_label    = Label(udata_frame,text='Enrollment :')
        term_label          = Label(udata_frame,text='Term :')
        access_label        = Label(udata_frame,text='Access :')
        # -------------------------------------------------------
        fname_label     .grid(row=0, column=0,padx=(15,10),pady=10)
        lname_label     .grid(row=1, column=0,padx=(15,10),pady=10)
        gender_label    .grid(row=2, column=0,padx=(15,10),pady=10)
        uid_label       .grid(row=3, column=0,padx=(15,10),pady=10)
        enrollment_label.grid(row=4, column=0,padx=(15,10),pady=10)
        term_label      .grid(row=5, column=0,padx=(15,10),pady=10)
        access_label    .grid(row=6, column=0,padx=(15,10),pady=10)
        # Entries -----------------------------------------------------
        self.fname_entry         = Entry(udata_frame, width = 20)
        self.lname_entry         = Entry(udata_frame, width = 20)
        self.sex = StringVar()
        self.sex.set(None)
        self.gender_male         = Radiobutton(udata_frame,text="Male",variable=self.sex,value="Male")
        self.gender_female       = Radiobutton(udata_frame,text="Female",variable=self.sex,value="Female")
        self.uid_entry           = Entry(udata_frame, width = 20)
        self.enrollment_entry    = Entry(udata_frame, width = 20)
        self.selected_dropdown = StringVar()
        self.selected_dropdown.set("None")
        self.term_dropdown = OptionMenu(udata_frame,self.selected_dropdown,"None","1st year","2nd year")
        self.term_entry          = Entry(udata_frame, width = 20)
        self.access_entry        = Entry(udata_frame, width = 20)
        # -------------------------------------------------------
        self.fname_entry     .grid(row=0, column=1,columnspan=2,padx=10,pady=10)
        self.lname_entry     .grid(row=1, column=1,columnspan=2,padx=10,pady=10)
        self.gender_male     .grid(row=2, column=1,padx=10,pady=10)
        self.gender_female   .grid(row=2, column=2,padx=10,pady=10)
        self.uid_entry       .grid(row=3, column=1,columnspan=2,padx=10,pady=10)
        self.enrollment_entry.grid(row=4, column=1,columnspan=2,padx=10,pady=10)
        self.term_dropdown   .grid(row=5, column=1,columnspan=2,padx=10,pady=10,sticky=NSEW)
        self.access_entry    .grid(row=6, column=1,columnspan=2,padx=10,pady=10)
        # -------------------------------------------------------
        # Command buttons =======================================
        # -------------------------------------------------------
        add_button      = Button(button_frame,text='Add Student ', command = self.add_user)
        remove_button   = Button(button_frame,text='Remove Selected', command = self.remove_selected)
        refresh_button  = Button(button_frame,text='Refresh views', command = self.render_db_view)
        update_button   = Button(button_frame,text='Update student', command = self.update_user)
        clear_button    = Button(button_frame,text='Clear inputs ', command = self.clear_input)
        exit_button     = Button(button_frame,text='Exit program',fg="#ff1122", command = root.quit)
        # -------------------------------------------------------
        add_button      .grid(row=10,column=0,padx = 10 , pady = (10,10) ,sticky="NESW" ) 
        remove_button   .grid(row=10,column=1,padx = 10 , pady = (10,10) ,sticky="NESW")
        update_button   .grid(row=10,column=2,padx = 10 , pady = (10,10) ,sticky="NESW")
        clear_button    .grid(row=11,column=0,padx = 10 , pady = (10,10) ,sticky="NESW")
        exit_button     .grid(row=11,column=1,padx = 10 , pady = (10,10) ,sticky="NESW")
        refresh_button  .grid(row=11,column=2,padx = 10 , pady = (10,10) ,sticky="NESW")
        # log_view =============================================
        self.log_view = Listbox(log_frame ,height=10, width=55,fg='#000',bg="#fff")
        self.log_view.grid(row = 0, column = 0,columnspan=4,rowspan=1,sticky="NESW")
        # db_view scrollbar -------------------------------------
        self.db_view_scrollbar  = Scrollbar(db_frame)
        self.db_view_scrollbar.grid(row=0,column=6,rowspan=100,sticky=NSEW)
        # db_view_styles ----------------------------------------
        self.db_view_styles = ttk.Style()
        self.db_view_styles.theme_use('clam')
        self.db_view_styles.configure(
            "Treeview",
            background='#fdfdfd',
            rowheight=20,
        )
        self.db_view_styles.map('Treeview',
                background = [('selected','steelblue')])
        # -------------------------------------------------------
        # db_view ===============================================
        # -------------------------------------------------------
        self.db_view = ttk.Treeview(db_frame,height=30,yscrollcommand=self.db_view_scrollbar.set)
        self.db_view['columns'] = ("hui","fname","lname","uid","gender","enrollment","term","access")
        self.db_view_scrollbar.config(command= self.db_view.yview)
        # -------------------------------------------------------
        self.db_view.column('#0'         ,width=0 ,anchor=CENTER,stretch=NO)
        self.db_view.column('hui'        ,width=220,anchor=CENTER)
        self.db_view.column('fname'      ,width=120,anchor=CENTER)
        self.db_view.column('lname'      ,width=120,anchor=CENTER)
        self.db_view.column('uid'        ,width=120,anchor=CENTER)
        self.db_view.column('gender'     ,width=120,anchor=CENTER)
        self.db_view.column('enrollment' ,width=120,anchor=CENTER)
        self.db_view.column('term'       ,width=120,anchor=CENTER)
        self.db_view.column('access'     ,width=120,anchor=CENTER)
        # -------------------------------------------------------
        self.db_view.heading('#0'            ,text='')
        self.db_view.heading('hui'           ,text='Hashed Unique Identifier')
        self.db_view.heading('fname'         ,text='First Name')
        self.db_view.heading('lname'         ,text='Last Name')
        self.db_view.heading('uid'           ,text='UID')
        self.db_view.heading('gender'        ,text='Gender')
        self.db_view.heading('enrollment'    ,text='Enrollment')
        self.db_view.heading('term'          ,text='Term')
        self.db_view.heading('access'        ,text='Access')
        # -------------------------------------------------------
        self.render_db_view()
        # -------------------------------------------------------
        def select_record(e):
            self.select_data()
        self.db_view.grid(row=0, column=5, rowspan=100, padx=10, pady=10)
        self.db_view.bind("<Double-1>",select_record)
        # -------------------------------------------------------

    def clear_input(self):
        """
        Clears the input fields.
        """
        self.fname_entry.delete(0, END)
        self.lname_entry.delete(0, END)
        self.sex.set(None)
        self.uid_entry.delete(0, END)
        self.enrollment_entry.delete(0, END)
        self.selected_dropdown.set('None')
        self.access_entry.delete(0, END)
        return None

    def remove_selected(self):
        """
        Removes a user from the database and the view.
        """
        selected = self.db_view.selection()
        for selection in selected:
            values = self.db_view.item(selection,'values')
            self.db.remove_one(values[0])
            self.db_view.delete(selection)
            self.render_db_view()

    def update_user(self):
        selected = self.db_view.selection()
        print(f"[ Update button ] - Selected :{selected}")
        if len(selected) == 1:
            for selection in selected:
                values = self.db_view.item(selection,'values')
                print(f"[ Update button ] - values {values}")
                fname_entry_data = self.fname_entry.get().capitalize()
                lname_entry_data = self.lname_entry.get().capitalize()
                gender_entry_data = self.sex.get()
                uid_entry_data = self.uid_entry.get()
                enrollment_entry_data = self.enrollment_entry.get()
                term_entry_data = self.selected_dropdown.get()
                access_entry_data = self.access_entry.get()
                retun = self.db.update_one(values[0],fname_entry_data,lname_entry_data,uid_entry_data,gender_entry_data,enrollment_entry_data,access_entry_data,term_entry_data)
                print("return value of query : ",retun)
                self.render_db_view()

    def select_data(self):
        selected = self.db_view.selection()
        print(selected)
        for selection in selected:
            values = self.db_view.item(selection,'values')
            print('values : ',values)
        self.clear_input()
        self.fname_entry.insert(0,values[1])
        self.lname_entry.insert(0,values[2])
        self.sex.set(values[4])
        self.uid_entry.insert(0,values[3] )
        self.enrollment_entry.insert(0,values[5])
        self.selected_dropdown.set(values[6])
        self.access_entry.insert(0,values[7])
        return None

    def render_db_view(self):
        print("[ render ] - db view ")
        # fetch data from db 
        self.db_data = self.db.fetch_all()
        # remove previous data 
        self.db_view.delete(*self.db_view.get_children())
        # render data
        self.db_view.tag_configure('oddrows',background='white')
        self.db_view.tag_configure('evenrows',background='#f4f4f4')
        global count
        count = 0
        for entry in self.db_data:
            display = entry[0:8]
            if count%2 == 0:
                self.db_view.insert(parent='',index='end',iid=count,text='',values=(display),tags=('evenrows',))
            elif count%2 == 1:
                self.db_view.insert(parent='',index='end',iid=count,text='',values=(display),tags=('oddrows',))
            count += 1

    def add_user(self):

        fname_entry_data = self.fname_entry.get().capitalize()
        lname_entry_data = self.lname_entry.get().capitalize()
        gender_entry_data = self.sex.get()
        uid_entry_data = self.uid_entry.get()
        enrollment_entry_data = self.enrollment_entry.get()
        term_entry_data = self.selected_dropdown.get()
        access_entry_data = self.access_entry.get()
        #---------------------------------------------------
        # prequery sanitization
        #---------------------------------------------------
        print("[ prequery sanitization ]")
        print('First Name',fname_entry_data)
        print('Last Name',lname_entry_data)
        print('UID',uid_entry_data)
        print('Enrollment',enrollment_entry_data)
        print('Term',term_entry_data)
        print('Access',access_entry_data)
        
        uid_chunk = uid_entry_data.split('/')
        print(uid_chunk)
        if len(uid_chunk)!= 3:
            self.log_view.insert(END,'Error : uid format incorrect')
            self.log_view.insert(END,'Must be of the form : GUR/00000/12 ')
            return None
        elif term_entry_data == "None":
            self.log_view.insert(END,'Error : Select a term')
            return None
        else:
            try:
                type(int(uid_chunk[1]))
            except ValueError :
                self.log_view.insert(END,'Error : uid format incorrect: middle')
                self.log_view.insert(END,'Must be of the form : GUR/00000/12 ')
                return None
            try:
                type(int(uid_chunk[2]))
            except ValueError :
                self.log_view.insert(END,'Error : uid format incorrect: last')
                self.log_view.insert(END,'Must be of the form : GUR/00000/12 ')
                return None
            
            if uid_chunk[0].upper() != 'GUR':
                self.log_view.insert(END,'Error : uid format incorrect: first ')
                self.log_view.insert(END,'Must be of the form : GUR/00000/12 ')
                return None
            else:
                uid_entry_data = f"{uid_chunk[0].upper()}/{uid_chunk[1]}/{uid_chunk[2]}"


        self.data = self.db.insert_one(fname_entry_data,lname_entry_data,uid_entry_data,gender_entry_data,enrollment_entry_data,access_entry_data,term_entry_data,time.time(),'False')
        if self.data.split('_')[-1] == 'exists':
            # it there is already a user
            print("[ Error ] - User exists ")
            self.log_view.insert(END,'Error : User already esists  ')
        elif self.data.split('_')[-1] == 'none':
            # if there is a none error
            print("[ Error ] - None value ")
            self.log_view.insert(END,'Error : No values inserted ')

        self.render_db_view()
        return None
# Printing class
class print_interface():
    def __init__(self):
        self.db = Database('../userdata.db')
        self.db_data = self.db.fetch_all()
        
        root = printer
        
        self.log_frame       = LabelFrame(root, text="Log box ",padx =5 ,pady=5)
        self.log_frame       .grid(row=1,column=0,columnspan=4,padx =10 ,pady=10,sticky="NESW")

        self.button_frame    = LabelFrame(root, text="Commands",padx =5 ,pady=5)
        self.button_frame    .grid(row=12,column=0,columnspan=4,padx =10 ,pady=10,sticky="NESW")

        db_frame        = LabelFrame(root, text="Database",padx =5 ,pady=5)
        db_frame        .grid(row=0,column=4,columnspan=4,rowspan=20 ,padx =10 ,pady=10,sticky="NESW")

        # Command buttons
        # -------------------------------------------------------

        unprint_button = Button(self.button_frame,text='Unprint', command = self.unset_printed)
        print_button = Button(self.button_frame,text='Print', command = self.set_printed)
        
        refresh_button  = Button(self.button_frame,text='Refresh views', command = self.render_db_view)
        exit_button     = Button(self.button_frame,text='Exit program',fg="#ff1122", command = root.quit)
        # -------------------------------------------------------
        self.print_4_button = Button(self.button_frame,text='Print 4', command = self.print_4,state='disabled')
        self.print_4_button  .grid(row=10,column=2,padx = 10 , pady = (10,10) ,sticky="NESW")

        unprint_button  .grid(row=10,column=1,padx = 10 , pady = (10,10) ,sticky="NESW")
        print_button    .grid(row=10,column=0,padx = 10 , pady = (10,10) ,sticky="NESW")
        
        exit_button     .grid(row=11,column=0,padx = 10 , pady = (10,10) ,sticky="NESW")
        refresh_button  .grid(row=11,column=1,padx = 10 , pady = (10,10) ,sticky="NESW")

        # log_view
        self.log_view = Listbox(self.log_frame ,height=10, width=50,fg='#000',bg="#fff")
        self.log_view.grid(row = 0, column = 0,sticky="NESW")
        # -------------------------------------------------------
        # db_view scrollbar 
        self.db_view_scrollbar  = Scrollbar(db_frame)
        self.db_view_scrollbar.grid(row=0,column=6,rowspan=100,sticky=NSEW)
        # db_view_styles 
        self.db_view_styles = ttk.Style()
        self.db_view_styles.theme_use('clam')
        self.db_view_styles.configure(
            "Treeview",
            background='#fdfdfd',
            rowheight=20,

        )
        self.db_view_styles.map('Treeview',
                background = [('selected','steelblue')])
        # db_view
        # -------------------------------------------------------
        self.db_view = ttk.Treeview(db_frame,height=30,yscrollcommand=self.db_view_scrollbar.set)
        self.db_view['columns'] = ("hui","fname","lname","uid","gender","enrollment","term","access")
        self.db_view_scrollbar.config(command= self.db_view.yview)
        # -------------------------------------------------------
        self.db_view.column('#0'         ,width=0 ,anchor=CENTER,stretch=NO)
        self.db_view.column('hui'        ,width=220,anchor=CENTER)
        self.db_view.column('fname'      ,width=120,anchor=CENTER)
        self.db_view.column('lname'      ,width=120,anchor=CENTER)
        self.db_view.column('uid'        ,width=120,anchor=CENTER)
        self.db_view.column('gender'     ,width=120,anchor=CENTER)
        self.db_view.column('enrollment' ,width=120,anchor=CENTER)
        self.db_view.column('term'       ,width=120,anchor=CENTER)
        self.db_view.column('access'     ,width=120,anchor=CENTER)
        # -------------------------------------------------------
        self.db_view.heading('#0'            ,text='')
        self.db_view.heading('hui'           ,text='Hashed Unique Identifier')
        self.db_view.heading('fname'         ,text='First Name')
        self.db_view.heading('lname'         ,text='Last Name')
        self.db_view.heading('uid'           ,text='UID')
        self.db_view.heading('gender'        ,text='Gender')
        self.db_view.heading('enrollment'    ,text='Enrollment')
        self.db_view.heading('term'          ,text='Term')
        self.db_view.heading('access'        ,text='Access')
        # -------------------------------------------------------
        self.render_db_view()
        # -------------------------------------------------------
        self.db_view.grid(row=0, column=5, rowspan=100, padx=10, pady=10)
        # self.db_view.bind("<Double-1>",select_record)
        self.db_view.bind("<ButtonRelease-1>",self.select_4_printing)

        pass

    def set_printed(self):
        print("owo")
        selected = self.db_view.selection()
        data = '1'
        for selection in selected:
            values = self.db_view.item(selection,'values')
            self.db.update_print_state(values[0],data)
        self.render_db_view()
        pass
    
    def unset_printed(self):
        print("owo")
        selected = self.db_view.selection()
        data = '0'
        for selection in selected:
            values = self.db_view.item(selection,'values')
            self.db.update_print_state(values[0],data)
        self.render_db_view()
        pass


    def select_data(self):
        selected = self.db_view.selection()
        print(selected)
        self.log_view.delete(0,END)
        for selection in selected:
            values = self.db_view.item(selection,'values')
            print('values : ',values)
            for value in values:
                self.log_view.insert(END,value)

        return None

    def select_4_printing(self,e):
        selected = self.db_view.selection()
        print(selected)
        to_print = []
        
        for selection in selected:
            values = self.db_view.item(selection,'values')
            print('hui : ',values)
            data = self.db.fetch_one(values[0])
            print('data',data)
            if data[0][-1] == '1':
                print('1 printed?')
            elif data[0][-1] == '0':
                print('0 not printed?')
                to_print.append(data[0][0])

        # only enable the print 4 button if there are 4 elements selected 
        if len(to_print) == 4 :
            print("we at 4 now ")
            self.print_4_button.config(state='normal')
        else:
            self.print_4_button.config(state='disabled')

        self.log_view.delete(0,END)
        for item in to_print:
            self.log_view.insert(END,item)

        pass

    def print_4(self):
        selected = self.db_view.selection()
        print("4 selected ", selected)
        to_print = []
        
        for selection in selected:
            values = self.db_view.item(selection,'values')
            dbreturn = self.db.fetch_one(values[0])
            print("4 values ", values)
            print("4 dbreturn ", dbreturn)
            entry = (dbreturn[0][1],dbreturn[0][2],dbreturn[0][3],dbreturn[0][4],dbreturn[0][5],dbreturn[0][6],dbreturn[0][7])
            to_print.append(entry)
        print("toprint",to_print)
        
        self.gen = generator()
        a4_canvas = self.gen.gen_a4px()
        canvas = a4_canvas[0]
        a4 = a4_canvas[1]
        base = a4_canvas[2]
        badge_coords = [[(183, 257), (1057, 1497)], 
                        [(1423, 257), (2297, 1497)], 
                        [(183, 2011), (1057, 3251)], 
                        [(1423, 2011), (2297, 3251)]]
        # draw sequence : 
        self.gen.draw_major_coords(canvas)
        self.gen.draw_grids(canvas)
        self.gen.paste_badge_background(a4,badge_coords)
        self.gen.write_data(canvas, badge_coords, to_print)

        self.paste_qr(a4,badge_coords)
        namestr = ''
        for item in to_print:
            splitd = item[2].split('/')
            namestr = namestr + '_'+ splitd[1]
        self.gen.save_a4(a4,base,f'{namestr}')
        self.set_printed()

        pass
    
    def paste_qr(self,canvas,coords):
        """
        Inputs : 
            canvas
            coords
        Outputs :
            
        
        """
        print("coords: ",coords)
        print("canvas: ",canvas)
        # for the 4 thingies 
        # generate code 
        # paste into a4 canvas 
        j = 0
        
        selected = self.db_view.selection()
        for selection in selected:
            values = self.db_view.item(selection,'values')
            dbreturn = self.db.fetch_one(values[0])


            print('pasting qr code ')
            print('pasting photo')
            code = self.gen.generate_single_code(dbreturn[0][0])
            code = code.resize((530,530))
            canvas.paste(code,(coords[j][0][0]+172,coords[j][0][1]+90))
            
            
            j = j + 1


            # code.save(f"{j}.png")
            print("code",code)
            
            print("saved qr image ")
        pass
    
    def generate_qr(self,data,main_color,bg_color,qr_ver,padd,box_sixe):
        """
        Inputs :
            data (contents of the code )
            main_color ( color of the qr code foreground )
            bg_color ( color of the qr code background)
            qr_ver ( qr code version )
            padd ( padding between the readable code and the surrounding pixels  )
            box_size ( box size )
        Outputs : 
            Pillow image object 
        """
        qr = qrcode.QRCode(
            version=qr_ver,
            error_correction = qrcode.constants.ERROR_CORRECT_Q,
            box_size=box_sixe,
            border=padd,
        )
        qr.add_data(data)
        qr.make(fit=True)
        return qr.make_image(fill_color=main_color, back_color=bg_color)

    def render_db_view(self):
        print("[ render ] - db view ")
        # fetch data from db 
        self.db_data = self.db.fetch_all()
        # remove previous data 
        self.db_view.delete(*self.db_view.get_children())
        # render data
        self.db_view.tag_configure('printed',background='#77cc99')
        self.db_view.tag_configure('not_printed',background='pink')
        global count
        count = 0
        for entry in self.db_data:
            display = entry[0:8]
            print(entry)
            if entry[-1] == '0':
                self.db_view.insert(parent='',index='end',iid=count,text='',values=(display),tags=('not_printed',))
            elif entry[-1] == '1':
                self.db_view.insert(parent='',index='end',iid=count,text='',values=(display),tags=('printed',))
            count += 1
        pass

class eimport():
    def __init__(self):
        self.db = Database('../userdata.db')
        self.db_data = self.db.fetch_all()
        root = eimporter 
        
        self.button_frame    = LabelFrame(root, text="Commands",padx =5 ,pady=5)
        self.button_frame    .grid(row=0,column=0,padx =10 ,pady=10,sticky="NESW")

        export_button = Button(self.button_frame,text='Export as CSV', command = self.export_csv)
        # import_button = Button(self.button_frame,text='Import from CSV ', command = root.quit ,state="disabled")
        
        exit_button     = Button(self.button_frame,text='Exit program',fg="#ff1122", command = root.quit)
        
        export_button.grid(row=0,column = 0,padx = 10 , pady = (10,10) ,sticky="NESW" )
        # import_button.grid(row=0,column = 1,padx = 10 , pady = (10,10) ,sticky="NESW")
        exit_button.grid(row=0 ,column = 2,padx = 10 , pady = (10,10) ,sticky="NESW" )
        
    def export_csv(self):
        print('Export triggered ')
        self.db = Database('../userdata.db')
        self.db_data = self.db.fetch_all()
        
        export_dir = './exports/'
        current_time = time.strftime('%A-%B-%d_%m_%Y-%H_%M_%S')
        

        print(current_time,'\n')
        # print(filename,'\n')
        export_file = open(f'{export_dir}{current_time}Export.csv','w')
        export_file.write('HUI,First_name,Last_name,UID,Sex,Stream,Term,Access,Time_eaten,Print_status\n')
        for record in self.db_data : 
            print(record,'\n')
            subrec = ''
            for item in record : 
                subrec = subrec + item + ','
            subrec = subrec+ "\n"
            print(subrec)
            export_file.write(subrec)
        export_file.close()
        

admin_ui = administration()
print_ui = print_interface()
eimport_ui = eimport()

def refresh_notebook(e):
    admin_ui.render_db_view()
    print_ui.render_db_view()

notebook.bind('<<NotebookTabChanged>>',refresh_notebook)

root.mainloop()