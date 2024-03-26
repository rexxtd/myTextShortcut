import subprocess
from threading import Thread
import time
import customtkinter as ctk
from PIL import Image, ImageTk
import winocr
import asyncio
import numpy as np
import cv2
from tkinter import messagebox
import os.path

has_Windows_OCR = True

class Startup_Screen(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()
        self.title("myShortcut")
        self.loadingTitle = ctk.CTkLabel(self, text="Please wait while the app is loading!", width = 400, font=("",15))
        self.loadingTitle.grid(row=1, column=1, sticky="nsew", pady = 25)
        self.progressBar = ctk.CTkProgressBar(self, height=5, width=350, indeterminate_speed=1.5)
        self.progressBar.grid(row=2, column=1, sticky="nsew", padx = 25)
        self.progressBar.start()
        self.progressBar.configure(mode="indeterminate")

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x_cordinate = int((screen_width/2) - (400/2))
        y_cordinate = int((screen_height/2) - (125/2))

        self.geometry("400x125+{}+{}".format(x_cordinate, y_cordinate))

        Thread(target=self.checkingDependencies).start()
    
    def updateLabel(self, text):
        self.loadingTitle.configure(text=text)

    def checkingDependencies(self):
        global has_Windows_OCR

        time.sleep(1.5)

        self.updateLabel("Checking dependencies...")

        if(os.path.isfile("logo.ico") & os.path.isfile("properties.ini")):
            pass
        else:
            messagebox.showerror("Critical error! Program terminated. ", "Some required files for the program to work are missing!\nPlease re-download the program and try again.\n\nIf the problem still persists, please contact the developers.")
            os._exit(1)
    
        self.withdraw()
        self.quit()