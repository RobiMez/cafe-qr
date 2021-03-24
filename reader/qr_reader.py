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
# import pymongo

# client = MongoClient('localhost', 27017)
# db = client.qr
# collection = db.users 

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



        # start a thread that constantly pools the video sensor for
        # the most recently read frame
        self.stopEvent = threading.Event()
        self.thread = threading.Thread(target=self.videoLoop, args=())
        self.thread.start()
        # set a callback to handle when the window is closed
        self.root.wm_title("QR_read")
        self.root.wm_protocol("WM_DELETE_WINDOW", self.onClose)

    def videoLoop(self):

        try:
            # keep looping over frames until we are instructed to stop
            while not self.stopEvent.is_set():
                # grab the frame from the video stream and resize
                self.frame = self.vs.read()
                self.frame = imutils.resize(self.frame, width=600)
                # OpenCV represents images in BGR order; however PIL
                # represents images in RGB order, so we need to swap
                # the channels, then convert to PIL and ImageTk format later

                # Decode the qr codes
                barcodes = pyzbar.decode(self.frame)
                # Loop through all decoded barcodes from the frame
                for code in barcodes:

                    (x, y, w, h) = code.rect
                    barcodeData = code.data.decode("utf-8")
                    barcodeType = code.type
                    cv2.rectangle(self.frame, (x, y),
                                  (x + w, y + h), (10, 255, 10), 3)
                    # print(f'cum {barcodeData}{barcodeType}')
                    text = "{} ({})".format(barcodeData, barcodeType)
                    cv2.putText(self.frame, text, (x, y - 10),
                                cv2.FONT_HERSHEY_DUPLEX, 0.5, (135, 72, 32), 1)

                if barcodes:
                    w = tki.Text( self.root,font=('helvetica',24),fg='green',width=10,height=10)
                    w.pack(side="right",padx=(20,20),pady=20)
                
                image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(image)
                image = ImageTk.PhotoImage(image)

                # initialize panel if none
                if self.panel is None:
                    self.panel = tki.Label(image=image)
                    self.panel.image = image
                    self.panel.pack(side="left", padx=(20, 400), pady=20)

                # otherwise, update the panel
                else:
                    self.panel.configure(image=image)
                    self.panel.image = image

        except RuntimeError as e:
            print("[INFO] RuntimeError caught ")

    def onClose(self):
        # set the stop event, cleanup the camera, and allow the rest of
        # the quit process to continue
        print("[INFO] closing...")
        self.stopEvent.set()
        self.vs.stop()
        self.root.quit()
