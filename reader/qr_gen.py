"""
CAFE-QR Administration interface 
"""
from datetime import datetime
import qrcode
from tkinter import *
from tkinter import ttk
from PIL import Image 
import os 
import time
from db import Database

print("[ Prerun check ] - Imports Successful.")

badge_dir = './badges'
now = datetime.now()
current_time = now.strftime("%H_%M_%S")
current_time_details = now.strftime("%H:%M:%S - %D ")
print(f"[ Time START] - {current_time_details}")
class generator():
    def __init__(self):
        self.db = Database('./../reader/userdata.db')
        self.db_data = self.db.fetch_all()
        
        app_width = 1520
        app_height = 750
        root = Tk()
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width /2) - (app_width/2)
        y = (screen_height /2 )- (app_height/2)
        
        print("screen width ",screen_width)
        print("screen height ",screen_height)
        print("app width ",app_width)
        print("app height ",app_height)
        print("x",x)
        print("y ",y)


        

        
        
        root.geometry(f'{app_width}x{app_height}+{int(x/2)}+{int(y/2)}')
        root.title('Generate qr badge.')
        
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

        self.fname_entry         = Entry(udata_frame, width = 20)
        self.lname_entry         = Entry(udata_frame, width = 20)
        self.sex = StringVar()
        self.sex.set(None)
        self.gender_male         = Radiobutton(udata_frame,text="Male",variable=self.sex,value="Male")
        self.gender_female       = Radiobutton(udata_frame,text="Female",variable=self.sex,value="Female")
        
        self.uid_entry           = Entry(udata_frame, width = 20)
        self.enrollment_entry    = Entry(udata_frame, width = 20)
        # term dropdown 
        self.selected_dropdown = StringVar()
        self.selected_dropdown.set("None")
        
        self.term_dropdown = OptionMenu(udata_frame,self.selected_dropdown,"None","1st year","2nd year")
        
        self.term_entry          = Entry(udata_frame, width = 20)
        self.access_entry        = Entry(udata_frame, width = 20)

        self.fname_entry     .grid(row=0, column=1,columnspan=2,padx=10,pady=10)
        self.lname_entry     .grid(row=1, column=1,columnspan=2,padx=10,pady=10)
        
        self.gender_male     .grid(row=2, column=1,padx=10,pady=10)
        self.gender_female   .grid(row=2, column=2,padx=10,pady=10)
        
        self.uid_entry       .grid(row=3, column=1,columnspan=2,padx=10,pady=10)
        self.enrollment_entry.grid(row=4, column=1,columnspan=2,padx=10,pady=10)
        # self.term_entry      .grid(row=5, column=1,columnspan=2,padx=10,pady=10)
        self.term_dropdown   .grid(row=5, column=1,columnspan=2,padx=10,pady=10,sticky=NSEW)
        self.access_entry    .grid(row=6, column=1,columnspan=2,padx=10,pady=10)

        # Command buttons
        # -------------------------------------------------------
        add_button      = Button(button_frame,text='Add Student ', command = self.gen_code)
        remove_button   = Button(button_frame,text='Remove Selected', command = self.remove_selected)
        refresh_button  = Button(button_frame,text='Refresh views', command = self.render_db_view)
        # update_button   = Button(button_frame,text='Update student', command = self.update_data)
        clear_button    = Button(button_frame,text='Clear inputs ', command = self.clear_input)
        exit_button     = Button(button_frame,text='Exit program',fg="#ff1122", command = root.quit)
        # -------------------------------------------------------
        add_button      .grid(row=10,column=0,padx = 10 , pady = (10,10) ,sticky="NESW" ) 
        remove_button   .grid(row=10,column=1,padx = 10 , pady = (10,10) ,sticky="NESW")
        # update_button   .grid(row=10,column=2,padx = 10 , pady = (10,10) ,sticky="NESW")
        clear_button    .grid(row=11,column=0,padx = 10 , pady = (10,10) ,sticky="NESW")
        exit_button     .grid(row=11,column=1,padx = 10 , pady = (10,10) ,sticky="NESW")
        refresh_button  .grid(row=11,column=2,padx = 10 , pady = (10,10) ,sticky="NESW")

        # log_view
        self.log_view = Listbox(log_frame ,height=10, width=40,font=('raleway'),fg='#000',bg="#fff")
        self.log_view.grid(row = 0, column = 0,columnspan=4,rowspan=1,sticky="NESW")
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
        def select_record(e):
            self.select_data()
        self.db_view.grid(row=0, column=5, rowspan=100, padx=10, pady=10)
        self.db_view.bind("<Double-1>",select_record)
        def ping():
            print('pong')
        # self.db_view.bind("<Double-1>",ping)
        

        root.mainloop()
        pass

    def clear_input(self):
        self.fname_entry.delete(0, END)
        self.lname_entry.delete(0, END)
        self.sex.set(None)
        self.uid_entry.delete(0, END)
        self.enrollment_entry.delete(0, END)
        self.selected_dropdown.set('None')
        self.access_entry.delete(0, END)
        return None

    def remove_selected(self):
        selected = self.db_view.selection()
        for selection in selected:
            values = self.db_view.item(selection,'values')
            self.db.remove_one(values[0])
            self.db_view.delete(selection)
            self.render_db_view()
    # def update_data(self):
    #     selected = self.db_view.selection()
    #     data = ''
    #     for selection in selected:
    #         values = self.db_view.item(selection,'values')
    #         self.db.update_one(values[0],data)
    #         self.db_view.delete(selection)

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

    def generate_qr(self,data,main_color,bg_color,qr_ver,padd,box_sixe):
        
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
        self.db_view.tag_configure('oddrows',background='white')
        self.db_view.tag_configure('evenrows',background='#f1f1f1')
        global count
        count = 0
        for entry in self.db_data:
            display = entry[0:8]
            if count%2 == 0:
                self.db_view.insert(parent='',index='end',iid=count,text='',values=(display),tags=('evenrows',))
            elif count%2 == 1:
                self.db_view.insert(parent='',index='end',iid=count,text='',values=(display),tags=('oddrows',))
            count += 1

        pass

    def gen_code(self):

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
                chunk_mid = type(int(uid_chunk[1]))
            except ValueError as e :
                self.log_view.insert(END,'Error : uid format incorrect: middle')
                self.log_view.insert(END,'Must be of the form : GUR/00000/12 ')
                return None
            try:
                chunk_mid = type(int(uid_chunk[2]))
            except ValueError as e :
                self.log_view.insert(END,'Error : uid format incorrect: last')
                self.log_view.insert(END,'Must be of the form : GUR/00000/12 ')
                return None
            
            if uid_chunk[0].upper() != 'GUR':
                self.log_view.insert(END,'Error : uid format incorrect: first ')
                self.log_view.insert(END,'Must be of the form : GUR/00000/12 ')
                return None
            else:
                uid_entry_data = f"{uid_chunk[0].upper()}/{uid_chunk[1]}/{uid_chunk[2]}"
            

        self.data = self.db.insert_one(fname_entry_data,lname_entry_data,uid_entry_data,gender_entry_data,enrollment_entry_data,access_entry_data,term_entry_data,time.time())
        fill_color  = '#000000'
        background = '#ffffff'
        if self.data.split('_')[-1] == 'exists':
            # it there is already a user
            print("[ Error ] - User exists ")
            self.log_view.insert(END,'Error : User already esists  ')
            self.render_db_view()
        elif self.data.split('_')[-1] == 'none':
            # if there is a none error
            print("[ Error ] - None value ")
            self.log_view.insert(END,'Error : No values inserted ')
            self.render_db_view()
        else:
            # qr_code = self.generate_qr(self.data,fill_color,background,2,1,20)
            # qr_code.save(os.path.join(badge_dir , f'{current_time}-{fname_entry_data}-qrcode.png'))
            print("[ QR ] QRcode Generated.")
            self.render_db_view()
        return None

if __name__ == "__main__":
    gen = generator()

now = datetime.now()
current_time_details = now.strftime("%H:%M:%S - %D ")
print(f"[ Time EXIT ] - {current_time_details}")