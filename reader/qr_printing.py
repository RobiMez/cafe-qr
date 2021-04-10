"""
CAFE-QR Printing interface 
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
class print_interface():
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
        root.title('Print interface .')
        
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

        unprint_button  .grid(row=10,column=1,padx = 10 , pady = (10,10) ,sticky="NESW")
        print_button    .grid(row=10,column=0,padx = 10 , pady = (10,10) ,sticky="NESW")

        
        exit_button     .grid(row=11,column=0,padx = 10 , pady = (10,10) ,sticky="NESW")
        refresh_button  .grid(row=11,column=1,padx = 10 , pady = (10,10) ,sticky="NESW")

        # log_view
        self.log_view = Listbox(self.log_frame ,height=10, width=40,fg='#000',bg="#fff")
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
        # self.db_view.bind("<Double-1>",select_record)
        self.db_view.bind("<ButtonRelease-1>",self.select_4_printing)

        root.mainloop()
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

    def clear_input(self):
        self.fname_entry.delete(0, END)
        self.lname_entry.delete(0, END)
        self.sex.set(None)
        self.uid_entry.delete(0, END)
        self.enrollment_entry.delete(0, END)
        self.selected_dropdown.set('None')
        self.access_entry.delete(0, END)
        return None

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

        if len(selected) ==4 :
            print("we at 4 now ")
            print_4_button = Button(self.button_frame,text='Print 4', command = self.print_4)
            print_4_button  .grid(row=10,column=2,padx = 10 , pady = (10,10) ,sticky="NESW")
        else :
            print_4_button.delete()
        self.log_view.delete(0,END)
        self.log_view.insert(END,len(selected))

        pass

    def print_4(self):
        pass

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


if __name__ == "__main__":
    gen = print_interface()

now = datetime.now()
current_time_details = now.strftime("%H:%M:%S - %D ")
print(f"[ Time EXIT ] - {current_time_details}")