'''
Created on 01 October 2017
@author: Yahya Almardeny

This helper file to show a window for getting the required information
from the user in order to connect to the server

'''

from tkinter import *
import os
	
############################# Device Setup #################################
# Input: file
# Remarks: Ask for the device name in the very first run in addition to the
# techinical info for connceting to the Server
###########################################################################
def get_information(file):
    if not os.path.isfile(file):
        global id, ip, port
        id = ip = port = ''
        while(id.strip()=='' or ip.strip()=='' or port.strip()==''): # accept no empty input!
            root = Tk()
            root.title("Device Setup")
            width, height = 300,120
            screenW, screenH = root.winfo_screenwidth(), root.winfo_screenheight()
            posX , posY = screenW/2 - width/2 , screenH/2 - height/2
            root.geometry("%dx%d+%d+%d" % (width, height, posX, posY)) # center the window
            Label(root, text="Device Name", pady=10, padx = 10).grid(row=0)
            entryId = Entry(root)
            entryId.grid(row=0, column=1)
            Label(root, text="Server IP", pady=2, padx = 10).grid(row=1)
            entryServerIp = Entry(root)
            entryServerIp.grid(row=1, column=1)
            Label(root, text="Server Port", pady=2, padx = 10).grid(row=2)
            entryServerPort = Entry(root)
            entryServerPort.grid(row=2, column=1)
            def __close(*args):
                global id, ip, port
                id = entryId.get()
                ip = entryServerIp.get()
                port = entryServerPort.get()
                root.destroy()
            Button(root, text="OK", command=__close).grid(row=3, column=1, pady=10)
            root.bind('<Return>', __close)
            root.mainloop()
        device_infoFile = open(file, 'w+')
        device_infoFile.write(id+","+ip+","+port)
        device_infoFile.close()
			
			
########################## Notification Window ############################
# Input: mssg
# Remarks: Notify User with error
###########################################################################		
def notify_erro(mssg):
    root = Tk()
    root.title("Error!")
    width, height = 300,85
    screenW, screenH = root.winfo_screenwidth(), root.winfo_screenheight()
    posX , posY = screenW/2 - width/2 , screenH/2 - height/2
    root.geometry("%dx%d+%d+%d" % (width, height, posX, posY))
    Label(root, text=mssg, pady=10, padx = 10).pack()
    def __abort():
        root.destroy()
        Button(root, text="OK", command=__abort).pack()
