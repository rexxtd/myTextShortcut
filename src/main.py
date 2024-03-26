#import packages
import os
import sys
from threading import Thread
from tkinter import messagebox
import webbrowser
import customtkinter as ctk
from PIL import Image, ImageTk
import difflib
import re
import configparser
from ctypes import windll
import diff_match_patch as dmp_module
import winocr
import asyncio
import cv2
import numpy as np
import win32gui, win32con, win32api, win32process
import psutil
import subprocess


# import other modules
import function.processText as pT
import function.compareResultWindow as cRW
import function.scanText as sT
import function.checkDependencies as chkD
import function.bgChangeOccupancy as bgCO
import function.ocrLangCheck as oLC

version = "1.0.0" # I don't know how to make a checking version without deploying to a local server, so this is the replacement T_T
appName = "MyShortcut (General)"
conf_url = "https://confluence.nexon.com/display/NWVNQA/%5BDunpaM%5D+MyShortcut+tool"
backgroundImage_inputPath = 'background.png' #easter1
backgroundOccupancy = 0.7 #easter1
#load config folder and config file path
current_dir = os.path.abspath(os.path.dirname(__file__))
configSetting_path = 'setting.ini'
configProperties_path = 'properties.ini'

# save settings to .ini file
def settingSaver(new_theme, new_appTransparency, new_highlightColor, new_highlightOption, new_scanText_method, new_scanText_language):
    setting_save = configparser.ConfigParser()
    setting_save.add_section('General')
    setting_save.add_section('Text Compare')
    setting_save.add_section('Scan Text')

    setting_save.set('General', 'theme', new_theme)
    setting_save.set('General', 'appTransparency', str(new_appTransparency))
    setting_save.set('Text Compare', 'highlightColor', new_highlightColor)
    setting_save.set('Text Compare', 'highlightOption', new_highlightOption)
    setting_save.set('Scan Text', 'scanMethod', new_scanText_method)
    setting_save.set('Scan Text', 'language', new_scanText_language)

    with open(configSetting_path, 'w') as configfile:
        setting_save.write(configfile)

def set_scanText_method(value):
    setting_save = configparser.ConfigParser()
    setting_save.read(configSetting_path)
    setting_save.set('Scan Text', 'scanMethod', value)

    with open(configSetting_path, 'w') as configfile:
        setting_save.write(configfile)

# save app properties to .ini file
def propertiesSaver(new_width, new_height):
    properties_save = configparser.ConfigParser()
    properties_save.add_section('App Properties')

    properties_save.set('App Properties', 'width', str(new_width))
    properties_save.set('App Properties', 'height', str(new_height))

    with open(configProperties_path, 'w') as configfile:
        properties_save.write(configfile)


# generate config files with default setting
def generateDefaultSettingConfig():
    default_theme = 'Dark'
    default_appTransparency = '1'
    default_highlightColor = '#33818a'
    default_highlightOption = 'Highlight Text'
    default_scanMethod = 'WinOCR'
    default_language = 'Korean'
    settingSaver(default_theme, default_appTransparency, default_highlightColor, default_highlightOption, default_scanMethod, default_language)

def generateDefaultPropertiesConfig():
    default_width = '957'
    default_height = '500'
    propertiesSaver(default_width, default_height)

def checkConfigExist():
    setting = configparser.ConfigParser()
    properties = configparser.ConfigParser()

    while True:
        try:
            with open(configSetting_path):
                setting.read(configSetting_path)
                break
        except:
            # if there are no config files, create new files with default setting
            messagebox.showwarning(title="Warning!", message="No config settings found!\nPlease try to restart the application or contact administrator.")
            generateDefaultSettingConfig()
            sys.exit(0)

    try:
        with open(configProperties_path):
            properties.read(configProperties_path)
    except:
        # if there are no config files, create new files with default setting
        messagebox.showwarning(title="Warning!", message="No config properties file found!\nPlease try to restart the application or contact administrator.")
        generateDefaultPropertiesConfig()
        sys.exit(0)

    return (setting, properties)


# reading data from config files
def configLoader():
    setting, properties = checkConfigExist()   
    # Define variables for configuration values
    # setting variables
    try:
        config_setting_value = {
            'theme': setting.get('General', 'theme'),
            'appTransparency': setting.get('General', 'appTransparency'),
            'highlightColor': setting.get('Text Compare', 'highlightColor'),
            'highlightOption': setting.get('Text Compare', 'highlightOption'),
            'scanText_method': setting.get('Scan Text', 'scanMethod'),
            'scanText_language': setting.get('Scan Text', 'language'),
        }
        # properties value
        config_properties_value = {
            'width': properties.get('App Properties', 'width'),
            'height': properties.get('App Properties', 'height'),
        }
    except Exception as e:
        messagebox.showerror(title="Error", message="The following error occurs when trying to run the program:\n" + str(e) + ".\nPlease try to contact to administrator.")
    return config_setting_value, config_properties_value


setting_values, properties_values = configLoader()
### Passing config values through configLoader module
# setting config
theme = setting_values['theme']
appTransparency = setting_values['appTransparency']
highlightColor = setting_values['highlightColor']
highlightOption = setting_values['highlightOption']
scanText_method = setting_values['scanText_method']
scanText_language = setting_values['scanText_language']

# properties config
app_width = int(properties_values['width'])
app_height = int(properties_values['height'])

def set_transparent_color(theme_name):
    if (theme_name == "Dark"):
        hex_color = "#000000"
        RGBA_color = win32api.RGB(0, 0, 0)
    elif (theme_name == "Light"):
        hex_color = "#ffffff"
        RGBA_color = win32api.RGB(255, 255, 255)
    return (hex_color, RGBA_color)

transparent_fg_color, transparent_RGBA_color = set_transparent_color(theme)


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode(theme)
        loadingScreen = chkD.Startup_Screen()
        loadingScreen.mainloop()

        self.title(appName + " v" + version)
        try:
            app_geometry = str(app_width) + "x" + str(app_height)
            self.geometry(app_geometry)
        except Exception as e:
            messagebox.showwarning(title="Warning!", message="Error getting application's size: " + str(e) + "!!!\nUsing default size instead.")
            self.geometry("957x500")
        self.minsize(957, 500)
        logoPath = 'logo.ico'
        self.iconbitmap(logoPath)
        self.attributes('-alpha', appTransparency)
        self.result_window = None

        def on_closing():
            if messagebox.askokcancel("Quit", "Do you want to quit?"):
                propertiesSaver(self.winfo_width(), self.winfo_height())
                self.destroy()

        self.protocol("WM_DELETE_WINDOW", on_closing)

        # create multiple font styles
        sideBarButtonFont = ctk.CTkFont(family="Century Gothic", size=17, weight='bold')
        header_1Font = ctk.CTkFont(family="Century Gothic", size=16, weight='bold')
        defaultTextButtonFont = ctk.CTkFont(family="Calibri", size=14, weight='bold')
        defaultTextBoxFont = ctk.CTkFont(family="Calibri", size=17)

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # load images with light and dark mode image
        image_path = os.path.join(current_dir,"icon")
        self.logo_image = ctk.CTkImage(Image.open(os.path.join(image_path, "logo.png")), size=(60, 60))
        self.textCompare_image = ctk.CTkImage(light_image=Image.open(os.path.join(image_path, "text_dark.png")),
                                                        dark_image=Image.open(os.path.join(image_path, "text_light.png")), size=(26, 26))                               
        self.scanText_image = ctk.CTkImage(light_image=Image.open(os.path.join(image_path, "ocr_dark.png")),
                                                     dark_image=Image.open(os.path.join(image_path, "ocr_light.png")), size=(26, 26))
        self.setting_image = ctk.CTkImage(light_image=Image.open(os.path.join(image_path, "setting_dark.png")),
                                                    dark_image=Image.open(os.path.join(image_path, "setting_light.png")), size=(26, 26))
        self.help_image = ctk.CTkImage(light_image=Image.open(os.path.join(image_path, "help_dark.png")),
                                                    dark_image=Image.open(os.path.join(image_path, "help_light.png")), size=(26, 26))
        
        # Load the background image with transparency (e.g., a PNG image with alpha channel)
        try:
            background_image_process = bgCO.change_occupancy(backgroundImage_inputPath, backgroundOccupancy)
            background_image = ImageTk.PhotoImage(background_image_process)
        except Exception as e:
            #print(e)
            print("BG_ERROR: No background found! Use None instead.")
            background_image = None


        def create_transparent_fg(widget):
            hwnd = widget.winfo_id()
            colorkey = transparent_RGBA_color
            wnd_exstyle = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
            new_exstyle = wnd_exstyle | win32con.WS_EX_LAYERED
            win32gui.SetWindowLong(hwnd,win32con.GWL_EXSTYLE,new_exstyle)
            win32gui.SetLayeredWindowAttributes(hwnd,colorkey,255,win32con.LWA_COLORKEY)


        # create navigation frame
        self.navigation_frame = ctk.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        # change this number depending on the total button added to navigation bar
        self.navigation_frame.grid_rowconfigure(8, weight=1)

        self.navigation_frame_label = ctk.CTkLabel(self.navigation_frame, text="MyShortcut", image=self.logo_image, compound="left", font=ctk.CTkFont(family="Century Gothic", size=20, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.textCompare_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Text Compare", font=sideBarButtonFont,
                                                          fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                          image=self.textCompare_image, anchor="w", command=self.textCompare_button_event)
        self.textCompare_button.grid(row=1, column=0, sticky="ew")

        self.scanText_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Scan Text", font=sideBarButtonFont,
                                                          fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                          image=self.scanText_image, anchor="w", command=lambda: scanTextFunc(scanText_method, scanText_language))
        self.scanText_button.grid(row=2, column=0, sticky="ew")

        self.setting_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Setting", font=sideBarButtonFont,
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.setting_image, anchor="w", command=self.setting_button_event)
        self.setting_button.grid(row=3, column=0, sticky="ew")

        def help_button_event():
            messagebox.showinfo(title="Information", message="Creator: RexTD@nexonnetworks.com\nMore information can be found on the Confluence website.")
            webbrowser.open(conf_url)

        self.help_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Help", font=sideBarButtonFont,
                                                    fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                    image=self.help_image, anchor="w", command=help_button_event)
        self.help_button.grid(row=6, column=0, sticky="ew")


        # create text compare frame
        self.textCompare_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.textCompare_frame.grid_rowconfigure(0, weight=1)
        self.textCompare_frame.grid_columnconfigure((0, 1), weight=1)
        # Create a Label widget to display the background image
        textCompare_frame_background_label = ctk.CTkLabel(self.textCompare_frame, text="", image=background_image)
        textCompare_frame_background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # textbox
        self.textCompare_frame_textbox1 = ctk.CTkTextbox(self.textCompare_frame)
        self.textCompare_frame_textbox1.configure(autoseparators=True, undo=True, maxundo=-1, font=defaultTextBoxFont)
        self.textCompare_frame_textbox1.grid(row=0, column=0, padx=20, pady=(20, 0), sticky="nsew")
        self.textCompare_frame_textbox2 = ctk.CTkTextbox(self.textCompare_frame)
        self.textCompare_frame_textbox2.configure(autoseparators=True, undo=True, maxundo=-1, font=defaultTextBoxFont)
        self.textCompare_frame_textbox2.grid(row=0, column=1, padx=20, pady=(20, 0), sticky="nsew")

        # Other Widgets
        self.textCompare_frame_button = ctk.CTkButton(self.textCompare_frame, text="Compare Text", font=defaultTextButtonFont, command=lambda: get_textCompare())
        self.textCompare_frame_button.grid(row=1, column=1, padx=20, pady=20, sticky="ew")

        self.optionText_comboBox_var = ctk.StringVar(value="Select Text Options")

        def combobox_callback(choice):
            if (choice == "Remove <xyz> tags"):
                processText(1)
            elif (choice == "Remove 'xyz>' tag only"):
                processText(2)
            elif (choice == "Remove extra spaces"):
                processText(3)
            elif (choice == "Change to uppercase"):
                processText(4)
            elif (choice == "Change to Lowercase"):
                processText(5)


        self.optionText_comboBox = ctk.CTkComboBox(master=self.textCompare_frame, font=defaultTextButtonFont, state="readonly",
                                                             values=["Remove <xyz> tags", "Remove 'xyz>' tag only", "Remove extra spaces", "Change to uppercase", "Change to Lowercase"],
                                                             command=combobox_callback, variable=self.optionText_comboBox_var)
        self.optionText_comboBox.grid(row=1, column=0, padx=20, pady=20, sticky="ew")

        # process text
        def processText(option):
            # get text from both text box
            text1 = self.textCompare_frame_textbox1.get("1.0", 'end-1c')
            text2 = self.textCompare_frame_textbox2.get("1.0", 'end-1c')
            # delete old text to replace
            self.textCompare_frame_textbox1.delete("0.0", "end")
            self.textCompare_frame_textbox2.delete("0.0", "end")

            # check process option
            # 1: Remove <xyz> tags
            # 2: Remove 'xyz>' tag only
            # 3: remove extra spaces/lines break
            # 4: Change text to upper case
            # 5: Change text to lower case
            if (option == 1):
                # insert text into each text box
                for sentences in pT.processText_removeTag(text1):
                    self.textCompare_frame_textbox1.insert("end", sentences + '\n')
                for sentences in pT.processText_removeTag(text2):
                    self.textCompare_frame_textbox2.insert("end", sentences + '\n')
            elif (option == 2):
                for sentences in pT.processText_removeFirstTag(text1):
                    self.textCompare_frame_textbox1.insert("end", sentences + '\n')
                for sentences in pT.processText_removeFirstTag(text2):
                    self.textCompare_frame_textbox2.insert("end", sentences + '\n')
            elif (option == 3):
                output = pT.processText_removeSpace(text1)
                self.textCompare_frame_textbox1.insert("end", output)
                output = pT.processText_removeSpace(text2)
                self.textCompare_frame_textbox2.insert("end", output)
            elif (option == 4):
                output = text1.upper()
                self.textCompare_frame_textbox1.insert("end", output)
                output = text2.upper()
                self.textCompare_frame_textbox2.insert("end", output)
            elif (option == 5):
                output = text1.lower()
                self.textCompare_frame_textbox1.insert("end", output)
                output = text2.lower()
                self.textCompare_frame_textbox2.insert("end", output)

        def get_textCompare():
            text1 = self.textCompare_frame_textbox1.get("1.0", 'end-1c')
            text2 = self.textCompare_frame_textbox2.get("1.0", 'end-1c')
            # split text into each line 
            lines1 = text1.splitlines()
            lines2 = text2.splitlines()

            # Remove empty spaces at the beginning and end of each line
            lines1 = [line.strip() for line in lines1]
            lines2 = [line.strip() for line in lines2]

            cleaned_text1 = '\n'.join(lines1).strip()
            cleaned_text2 = '\n'.join(lines2).strip()

            # check if the whole text are different, if no then no need to compare lines
            diff_all = list(difflib.unified_diff(cleaned_text1, cleaned_text2))
            if (len(diff_all) == 0):
                messagebox.showinfo(title="Comparison Result", message="Both texts are identical!")
            else:
                if (highlightOption.lower() == 'highlight text' or highlightOption.lower() == 'highlight line'):
                    dmp = dmp_module.diff_match_patch()
                    diff = dmp.diff_main(text1, text2)
                    dmp.diff_cleanupSemantic(diff)
                    self.result_window = cRW.ComparisonTopWindow(diff, highlightColor, highlightOption.lower())
                else:
                    messagebox.showerror(title="Error", message="Highlight Option setting is not corrected.\nPlease check your settings!")

        ### SCAN TEXT
        # minimize app when selecting Scan Text option
        def scanTextFunc(scanText_method, scanText_language):
            if (scanText_method=="WinOCR"):
                self.iconify()
                sT.scanTextFunc(scanText_method, scanText_language)
                self.deiconify()
            else:
                sT.scanTextFunc(scanText_method, scanText_language)

        ### CREATE SETTING FRAME
        self.setting_frame = ctk.CTkScrollableFrame(self, corner_radius=0, fg_color="transparent")
        self.setting_frame.grid_rowconfigure(0, weight=0)
        self.setting_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        # Create a Label widget to display the background image
        setting_frame_background_label = ctk.CTkLabel(self.setting_frame, text="", image=background_image)
        setting_frame_background_label.place(x=0, y=0, relwidth=1, relheight=1)

        ### General settings
        self.setting_header_1_label = ctk.CTkLabel(self.setting_frame, text="General", font=header_1Font, fg_color=transparent_fg_color)
        self.setting_header_1_label.grid(row=0, column=0, padx=0, pady=(30,0), sticky="ew")
        create_transparent_fg(self.setting_header_1_label) 

        # Theme settings        
        self.theme_setting_label = ctk.CTkLabel(self.setting_frame, text="Theme", font=defaultTextButtonFont, fg_color=transparent_fg_color)
        self.theme_setting_label.grid(row=1, column=0, columnspan=2, padx=(50,0), pady=10, sticky="ew")
        create_transparent_fg(self.theme_setting_label)

        theme_values = ["Light", "Dark"]
        self.theme_setting_menu = ctk.CTkOptionMenu(self.setting_frame, values=theme_values, font=defaultTextButtonFont, command=self.theme_setting_event)
        self.theme_setting_menu.grid(row=1, column=2, padx=0, pady=10, sticky="ew")
        self.theme_setting_menu.set(theme)

        # Transparency settings        
        self.transparency_setting_label = ctk.CTkLabel(self.setting_frame, text="Application Transparency", font=defaultTextButtonFont, fg_color=transparent_fg_color)
        self.transparency_setting_label.grid(row=2, column=0, columnspan=2, padx=(50,0), pady=10, sticky="ew")
        create_transparent_fg(self.transparency_setting_label)

        def slider_event(value):
            self.attributes('-alpha', self.transparency_setting_slider.get())
            self.slide_label.configure(text=self.transparency_setting_slider.get())

        self.transparency_setting_slider = ctk.CTkSlider(self.setting_frame, from_=0.3, to=1.0, bg_color= transparent_fg_color, fg_color=transparent_fg_color, command=slider_event)
        self.transparency_setting_slider.grid(row=2, column=2, padx=(50,0), pady=10, sticky="ew")
        create_transparent_fg(self.transparency_setting_slider)
        
        try:
            self.transparency_setting_slider.set(float(appTransparency))
        except Exception as e:
            messagebox.showerror(title="Error", message="Error occurs: " + str(e) + ".\nSome setting value is not correct.\nMaybe try to delete the setting file or contact administrator.")

        self.slide_label = ctk.CTkLabel(self.setting_frame, text=appTransparency, font=defaultTextButtonFont, fg_color=transparent_fg_color)
        self.slide_label.grid(row=2, column=3, padx=(10,0), pady=10, sticky="w")
        create_transparent_fg(self.slide_label)

        ### Text Compare settings
        self.setting_header_2_label = ctk.CTkLabel(self.setting_frame, text="Text Compare", font=header_1Font, fg_color=transparent_fg_color)
        self.setting_header_2_label.grid(row=3, column=0, padx=(0,0), pady=5, sticky="ew")
        create_transparent_fg(self.setting_header_2_label)

        # Highlight color settings
        self.highlight_color_label = ctk.CTkLabel(self.setting_frame, text="Highlight color (HEX)", font=defaultTextButtonFont, fg_color=transparent_fg_color)
        self.highlight_color_label.grid(row=4, column=0, columnspan = 2, padx=(50,0), pady=10, sticky="ew")
        create_transparent_fg(self.highlight_color_label)

        def highlight_color_validate_input(input):
            # Check if the input is empty or has more than 7 characters
            if len(input) > 7:
                return False
            return True

        self.highlight_color_entry = ctk.CTkEntry(self.setting_frame, placeholder_text=highlightColor, validate="key", validatecommand=(self.register(highlight_color_validate_input), '%P'), font=defaultTextButtonFont, corner_radius=5)
        self.highlight_color_entry.grid(row=4, column=2, padx=0, pady=10, sticky="ew")
        
        # Highlight option settings
        self.highlight_option_lable = ctk.CTkLabel(self.setting_frame, text="Highlight Option", font=defaultTextButtonFont, fg_color=transparent_fg_color)
        self.highlight_option_lable.grid(row=5, column=0, columnspan = 2, padx=(50,0), pady=10, sticky="ew")
        create_transparent_fg(self.highlight_option_lable)

        # Create StringVars to store the selected values of the OptionMenus
        highlight_option_var = ctk.StringVar()
        highlight_option_settings_value = ["Highlight Text", "Highlight Line"]
        self.highlight_option_settings_switch = ctk.CTkOptionMenu(self.setting_frame, variable = highlight_option_var, values=highlight_option_settings_value, font=defaultTextButtonFont)
        self.highlight_option_settings_switch.grid(row=5, column=2, sticky="nsew", padx=0, pady=10)
        self.highlight_option_settings_switch.set(highlightOption)
        
        ### Scan Text settings
        self.setting_header_3_label = ctk.CTkLabel(self.setting_frame, text="Scan Text", font=header_1Font, fg_color=transparent_fg_color)
        self.setting_header_3_label.grid(row=6, column=0, padx=(0,0), pady=5, sticky="ew")
        create_transparent_fg(self.setting_header_3_label)
        
        # OCR method settings
        def update_second_optionmenu_state(*args):
            if OCR_method_var.get() == "LINE":
                self.OCR_language_setting_switch.configure(state=ctk.DISABLED)
            else:
                self.OCR_language_setting_switch.configure(state=ctk.NORMAL)

        # Create StringVars to store the selected values of the OptionMenus
        OCR_method_var = ctk.StringVar()
        OCR_language_var = ctk.StringVar()

        self.OCR_method_setting_label = ctk.CTkLabel(self.setting_frame, text="Scan method", font=defaultTextButtonFont, fg_color=transparent_fg_color)
        self.OCR_method_setting_label.grid(row=7, column=0, columnspan = 2, padx=(50,0), pady=10, sticky="ew")
        create_transparent_fg(self.OCR_method_setting_label)
        
        OCR_method_setting_values = ["WinOCR"]
        self.OCR_method_setting_switch = ctk.CTkOptionMenu(self.setting_frame, variable = OCR_method_var, values=OCR_method_setting_values, font=defaultTextButtonFont)
        self.OCR_method_setting_switch.grid(row=7, column=2, sticky="nsew", padx=0, pady=10)
        self.OCR_method_setting_switch.set(scanText_method)
        
        # OCR language settings
        self.OCR_language_setting_label = ctk.CTkLabel(self.setting_frame, text="Default language", font=defaultTextButtonFont, fg_color=transparent_fg_color)
        self.OCR_language_setting_label.grid(row=8, column=0, columnspan = 2, padx=(50,0), pady=10, sticky="ew")
        create_transparent_fg(self.OCR_language_setting_label)
        
        OCR_language_setting_switch_values = ["English (Global)", "English (US)","Korean", "Japanese", "Chinese (Simplified)", "Chinese (Traditional)", "Russian", "German", "Spanish", "Portuguese", "French"]
        self.OCR_language_setting_switch = ctk.CTkOptionMenu(self.setting_frame, variable= OCR_language_var, values=OCR_language_setting_switch_values, font=defaultTextButtonFont)
        self.OCR_language_setting_switch.grid(row=8, column=2, sticky="nsew", padx=0, pady=10)
        self.OCR_language_setting_switch.set(scanText_language)

        # Bind an event to the first OptionMenu to update the second one's state
        OCR_method_var.trace_add("write", update_second_optionmenu_state)
        # call the function to set the initial state of the second OptionMenu
        update_second_optionmenu_state()

        # Empty label above save setting for good spacing
        self.empty_label = ctk.CTkLabel(self.setting_frame, text="", font=defaultTextButtonFont, fg_color=transparent_fg_color)
        self.empty_label.grid(row=17, column=1, padx=(0,30), pady=10, sticky="nse") 
        create_transparent_fg(self.empty_label)

        # Save setting button
        self.save_setting_btn = ctk.CTkButton(self.setting_frame, text="Save", font=defaultTextButtonFont, command=lambda: saveSetting())
        self.save_setting_btn.grid(row=18, column=3, padx=(0,30), pady=10, sticky="nse") 

        # save new settings to config file
        def saveSetting():
            # Get input from entry box
            get_new_highlightColor = self.highlight_color_entry.get()
            # Check if the new value is empty, assign to old value instead
            new_highlightColor = highlightColor if get_new_highlightColor in [None, ""] else get_new_highlightColor
            new_highlightOption = self.highlight_option_settings_switch.get()
            new_theme = self.theme_setting_menu.get()
            new_appTransparency = self.transparency_setting_slider.get()
            new_scanText_method = self.OCR_method_setting_switch.get()
            new_scanText_language = self.OCR_language_setting_switch.get()

            # Check if new value is correct for their condition
            # 1. Check HEX format of highlight color
            hex_color_pattern = r'^#([0-9A-Fa-f]{3}){1,2}$'
            if re.match(hex_color_pattern, new_highlightColor):
                try:
                    settingSaver(new_theme, new_appTransparency, new_highlightColor, new_highlightOption, new_scanText_method, new_scanText_language)
                    propertiesSaver(self.winfo_width(), self.winfo_height())
                    messagebox.showinfo(title="Restart required", message="Saved successfully.\nThe app will now restart.")
                    #Restarts the current program.
                    python = sys.executable
                    os.execl(python, python, * sys.argv)
                except Exception as e:
                    messagebox.showerror(title="Error", message="Unknown error occurs!\n" + str(e))
            else:
                messagebox.showerror(title="Error", message="The highlight color is incorrect. Please make sure it is in the correct HEX format.")

        ### Add OCR Language settings
        self.add_ocr_lang_setting_header_1_label = ctk.CTkLabel(self.setting_frame, text="Add OCR Language", font=header_1Font, fg_color=transparent_fg_color)
        self.add_ocr_lang_setting_header_1_label.grid(row=9, column=0, padx=(10,0), pady=5, sticky="ew")
        create_transparent_fg(self.add_ocr_lang_setting_header_1_label)

        self.availableOCRLang_label = ctk.CTkLabel(self.setting_frame, text="Available Language", font=defaultTextButtonFont, fg_color=transparent_fg_color)
        self.availableOCRLang_label.grid(row=10, column=0, columnspan=2, padx=(50,0), pady=10, sticky="ew")
        create_transparent_fg(self.availableOCRLang_label)

        self.addOCRLanguage_header_2_label = ctk.CTkLabel(self.setting_frame, text="OCR Language", font=defaultTextButtonFont, fg_color=transparent_fg_color)
        self.addOCRLanguage_header_2_label.grid(row=11, column=0, columnspan=2, padx=(50,0), pady=10, sticky="ew")
        create_transparent_fg(self.addOCRLanguage_header_2_label)

        ### Button
        self.check_OCR_lang_btn = ctk.CTkButton(self.setting_frame, text="Check language", font=defaultTextButtonFont, command=lambda: check_available_OCR_language())
        self.check_OCR_lang_btn.grid(row=10, column=2, sticky="nsew", padx=0, pady=10)

        self.add_OCR_lang_btn = ctk.CTkButton(self.setting_frame, text="Add", font=defaultTextButtonFont, command=lambda: add_OCR_language())
        self.add_OCR_lang_btn.grid(row=11, column=3, sticky="nsew", padx=60, pady=10)

        ### OptionMenu
        OCR_lang_values = ["English (Global)", "English (US)","Korean", "Japanese", "Chinese (Simplified)", "Chinese (Traditional)", "Russian", "German", "Spanish", "Portuguese", "French"]
        OCR_lang_dict = {
            "English (Global)" : "en-GB",
            "English (US)": "en-US",
            "Korean": "ko-KR", 
            "Japanese": "ja-JP", 
            "Chinese (Simplified)": "zh-CN", 
            "Chinese (Traditional)": "zh-TW", 
            "Russian": "ru-RU",
            "German": "de-DE",
            "Spanish": "es-ES",
            "Portuguese":"pt-PT",
            "French":"fr-FR",
        }
        self.OCR_lang_optionmenu = ctk.CTkOptionMenu(self.setting_frame, values=OCR_lang_values, font=defaultTextButtonFont)
        self.OCR_lang_optionmenu.grid(row=11, column=2, sticky="nsew", padx=0, pady=10)

        def check_available_OCR_language():
            output = ""
            for language in OCR_lang_values:
                if language in OCR_lang_dict:
                    result, powershell_result = oLC.is_ocr_language_installed(OCR_lang_dict[language])
                    if (result):
                        output = output + f"{language}: Installed.\n"
                    else:
                        output = output + f"{language}: Not installed.\n"
            messagebox.showinfo(title="Available Language", message=output)

        def add_OCR_language():
            OCR_lang_select_value = self.OCR_lang_optionmenu.get()
            if (OCR_lang_select_value == ""):
                messagebox.showerror(title="Add OCR Language", message="You have not selected any language.")
            elif OCR_lang_select_value in OCR_lang_values:
                result, powershell_result = oLC.ocr_lang_installer(OCR_lang_dict[OCR_lang_select_value])
                if (result):
                    message = f"{OCR_lang_select_value} is installed successfully."
                    messagebox.showinfo(title="Add OCR Language", message=message)
                else:
                    message = f"Failed to install {OCR_lang_select_value} OCR language.\nPlease try again or contact administrator."
                    messagebox.showerror(title="Add OCR Language", message=message)
                    messagebox.showerror(title="Add OCR Language", message=powershell_result)
            else:
                messagebox.showerror(title="Add OCR Language", message="The selected language is not available yet.")

        # select default frame
        self.select_frame_by_name("textCompare")


    def select_frame_by_name(self, name):
        # set button color for selected button
        self.textCompare_button.configure(fg_color=("gray75", "gray25") if name == "textCompare" else "transparent")
        self.setting_button.configure(fg_color=("gray75", "gray25") if name == "setting" else "transparent")
        self.help_button.configure(fg_color=("gray75", "gray25") if name == "help" else "transparent")

        # show selected frame
        if name == "textCompare":
            self.textCompare_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.textCompare_frame.grid_forget()
        if name == "setting":
            self.setting_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.setting_frame.grid_forget()


    def textCompare_button_event(self):
        self.select_frame_by_name("textCompare")

    def setting_button_event(self):
        self.select_frame_by_name("setting")     

    def theme_setting_event(self, new_appearance_mode):
        ctk.set_appearance_mode(new_appearance_mode)


if __name__ == "__main__":
    app = App()
    app.mainloop()
