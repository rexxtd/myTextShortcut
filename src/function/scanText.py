import time
from tkinter import messagebox
import psutil
import pyautogui
from PIL import ImageGrab
import function.scanTextWindow as stW

# OCR Function
def scanTextFunc(scanText_method, scanText_language):
    if (scanText_method=="WinOCR"):
        if (monitor_screen_clipping_host()):
            # captureCheck = False
            # Take a screenshot of the defined area
            image = ImageGrab.grabclipboard()
            if (image == None):
                message = "You need to capture the image before scanning text."
                messagebox.showerror(title="Error", message=message)
            else:               
                lang_check = True
                lang_list = ["English (Global)", "English (US)","Korean", "Japanese", "Chinese (Simplified)", "Chinese (Traditional)", "Russian", "German", "Spanish", "Portuguese", "French"]
                if (scanText_language in lang_list):
                    lang_check = True
                else:
                    message = "Unknown language package. Please check your settings."
                    messagebox.showerror(title="Error", message=message)
                    lang_check = False
                if (lang_check):
                    stW.ScanResultWindow(image, scanText_language)

    else:
        message = "Unknown scan method. Please check your settings."
        messagebox.showerror(title="Error", message=message)

def monitor_screen_clipping_host():
    # Run snipping tool using shortcut
    pyautogui.hotkey("win", "shift", "s")
    time.sleep(0.1)
    # check if snipping tool is working before listen event starts
    checker = False
    for process in psutil.process_iter(attrs=['pid', 'name']):
        if process.info['name'] == 'ScreenClippingHost.exe':
            checker = True
    if checker == False:
        messagebox.showerror(title="Error", message="Cannot launch Snipper Tool. Make sure Snip & Sketch is installed on your device, and shortcuts are available.")
    else:
        while (checker == True):
            found = False
            for process in psutil.process_iter(attrs=['pid', 'name']):
                if process.info['name'] == 'ScreenClippingHost.exe':
                    found = True
                    break
            if (found != True):
                break 
            time.sleep(0.2)  # Adjust the sleep duration as needed
        return True
    