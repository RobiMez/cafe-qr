# import the necessary packages
from __future__ import print_function
from PIL import Image
from PIL import ImageTk
import tkinter as tki
import threading
import datetime
import imutils
import cv2
import os
from pyzbar import pyzbar
import time
from db import Database
from playsound import playsound

class qr_read:
    def __init__(self, vs):
        # store the video stream object and output path, then initialize
        # the most recently read frame, thread for reading frames, and
        # the thread stop event
        self.vs = vs

        self.frame = None
        self.thread = None
        self.stopEvent = None
        # initialize the root window and image panel
        self.root = tki.Tk()
        self.panel = None
        
        self.root.geometry('1500x600')
        self.barcodes = None

        # qr_text = tki.StringVar()
        # qr_label = tki.Label(self.root , textvariable=qr_text)
        # qr_label.grid(row = 0,column=1)
        # qr_text.set("looking for code")
        # self.qr_label = qr_label
        # self.qr_text = qr_text

        qr_details = tki.Listbox(self.root ,height=18, width=55,font=('raleway'),fg='green',bg="#eee")

        qr_details.grid(row=0,column=1,pady=20,padx=20)

        self.qr_details = qr_details
        self.code_visible = None


        # w = tki.Label( self.root,text='...',font=('helvetica',24),fg='green',width=10,height=10)
        # w.pack(side="right",padx=(20,20),pady=20)

        # start a thread that constantly pools the video sensor for
        # the most recently read frame
        self.stopEvent = threading.Event()
        self.thread = threading.Thread(target=self.videoLoop, args=())
        # self.b_thread = threading.Thread(target=self.beep_thread, args=())
        self.thread.start()
        # self.b_thread.start()
        # set a callback to handle when the window is closed
        self.root.wm_title("QR_read")
        self.root.wm_protocol("WM_DELETE_WINDOW", self.onClose)


    def videoLoop(self):
        try:
            # keep looping over frames until we are instructed to stop

            last_code = None
            while not self.stopEvent.is_set():

                # Grab the frame from the video stream and resize
                # print('code visible ',self.code_visible)
                self.frame = self.vs.read()
                self.frame = imutils.resize(self.frame, width=700)

                # Try decoding every frame 
                barcodes = pyzbar.decode(self.frame)
                # The last scanned code to avoid dupes 

                if barcodes:
                    # Scope : barcode has been detected 

                    # Loop through all decoded barcodes from the frame
                    # and display a bounding box on the video stream 
                    self.code_visible = True

                    for code in barcodes:

                        (x, y, w, h) = code.rect
                        barcodeData = code.data.decode("utf-8")
                        barcodeType = code.type
                        cv2.rectangle(self.frame, (x, y),(x + w, y + h), (10, 255, 10), 3)
                        text = "{} ({})".format(barcodeData, barcodeType)
                        cv2.putText(self.frame, text, (x, y - 10),cv2.FONT_HERSHEY_DUPLEX, 0.5, (135, 72, 32), 1)
                        if last_code is None :
                            print('\n First scan since execution ')
                            last_code = barcodeData
                            self.qr_details.delete(0,tki.END)
                            self.qr_details.insert(tki.END,barcodeData)
                            playsound('./waves/555061__magnuswaker__repeatable-beep.wav')

                        if barcodeData != last_code :
                            last_code = barcodeData
                            print(" \t New Code Detected ")
                            print(' Setting the last scanned value to the current code ')
                            self.qr_details.delete(0,tki.END)
                            self.qr_details.insert(tki.END,barcodeData)
                            playsound('./waves/555061__magnuswaker__repeatable-beep.wav')
                            db = Database('userdata.db')
                            print(db.update_date(barcodeData))

                        # self.qr_details.insert(tki.END,barcodeData)
                        # print(text)
                        # playsound('./waves/555061__magnuswaker__repeatable-beep.wav')
                else:
                    # Scope : there is no code on the screen
                    self.code_visible = False
                    pass 

                image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(image)
                image = ImageTk.PhotoImage(image)

                # initialize panel if none
                if self.panel is None:
                    self.panel = tki.Label(image=image)
                    self.panel.image = image
                    self.panel.grid(row=0,column=0, padx=(20, 20), pady=20)
                # otherwise, update the panel
                else:
                    self.panel.configure(image=image)
                    self.panel.image = image

        except RuntimeError as e:
            print(f"[INFO] RuntimeError caught :{e}")



    def onClose(self):
        # set the stop event, cleanup the camera, and allow the rest of
        # the quit process to continue
        print("[INFO] closing...")
        self.stopEvent.set()
        self.vs.stop()
        self.root.quit()
