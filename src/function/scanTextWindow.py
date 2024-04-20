import customtkinter as ctk
from PIL import Image, ImageTk
import winocr
import asyncio
import numpy as np
import cv2
from tkinter import messagebox
from googletrans import Translator


class ScanResultWindow(ctk.CTkToplevel):
    def __init__(self, image, scanText_language):
        super().__init__()
        self.image = image.copy()
        self.geometry("800x600")
        self.minsize(800, 600)
        self.title("Scan Text Results")
        self.focus_force()
        # what am i even doing idk probably needs to change this
        self.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24,
                               25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50), weight=1)
        self.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9), weight=1)

        # Create main frames
        self.left_frame = ctk.CTkFrame(self)
        self.left_frame.grid(row=0, rowspan=50, column=0,
                             columnspan=6, padx=(20, 0), pady=20, sticky="nsew")
        self.right_top_frame = ctk.CTkFrame(self)
        self.right_top_frame.grid(
            row=1, rowspan=24, column=6, columnspan=4, padx=20, pady=(10, 20), sticky="nsew")
        self.right_bottom_frame = ctk.CTkFrame(self)
        self.right_bottom_frame.grid(
            row=27, rowspan=49, column=6, columnspan=4, padx=20, pady=(10, 20), sticky="nsew")

        # Create canvas to display the image
        self.canvas = ctk.CTkCanvas(self.left_frame, bg="black")
        self.canvas.pack(fill="both", expand=True)

        defaultTextBoxFont = ctk.CTkFont(family="Calibri", size=17)
        defaultTextButtonFont = ctk.CTkFont(
            family="Calibri", size=14, weight='bold')

        # Create a text label
        self.translate_label = ctk.CTkLabel(
            self, text="Translate To:", font=defaultTextButtonFont)
        self.translate_label.grid(
            row=25, rowspan=1, column=7, columnspan=1, sticky="nsew")

        # Create a text widget to display recognized text
        self.recognize_text_widget = ctk.CTkTextbox(
            self.right_top_frame, wrap=ctk.WORD)
        self.recognize_text_widget.configure(
            autoseparators=True, undo=True, maxundo=-1, font=defaultTextBoxFont)
        self.recognize_text_widget.pack(fill="both", expand=True)

        # Create a text widget to translate the text
        self.translate_text_widget = ctk.CTkTextbox(
            self.right_bottom_frame, wrap=ctk.WORD)
        self.translate_text_widget.configure(
            autoseparators=True, undo=True, maxundo=-1, font=defaultTextBoxFont)
        self.translate_text_widget.pack(fill="both", expand=True)

        # Create buttons to change language option for detecting
        change_lang_var_detected = ctk.StringVar()
        change_lang_value_detected = ["English (Global)", "English (US)", "Korean", "Japanese", "Chinese (Simplified)",
                                      "Chinese (Traditional)", "Russian", "German", "Spanish", "Portuguese", "French"]
        change_lang_detected_switch = ctk.CTkOptionMenu(
            self, variable=change_lang_var_detected, values=change_lang_value_detected, font=defaultTextButtonFont)
        change_lang_detected_switch.grid(row=0, rowspan=1, column=7, columnspan=2, padx=(
            10, 10), pady=(20, 0), sticky="nsew")
        change_lang_detected_switch.set(scanText_language)

        # Create buttons to change language option for translating
        change_lang_var_translate = ctk.StringVar()
        change_lang_value_translate = ["English (Global)", "English (US)", "Korean", "Japanese", "Chinese (Simplified)",
                                       "Chinese (Traditional)", "Russian", "German", "Spanish", "Portuguese", "French"]
        change_lang_translate_switch = ctk.CTkOptionMenu(
            self, variable=change_lang_var_translate, values=change_lang_value_translate, font=defaultTextButtonFont)
        change_lang_translate_switch.grid(row=26, rowspan=1, column=7, columnspan=2, padx=(
            10, 10), pady=(20, 0), sticky="nsew")
        change_lang_translate_switch.set(scanText_language)

        # Create buttons to get text
        get_text_btn = ctk.CTkButton(self, font=defaultTextButtonFont, text="Get Text",
                                     command=lambda: self.insert_text(image, change_lang_detected_switch.get()))
        get_text_btn.grid(row=0, rowspan=1, column=9, columnspan=2,
                          padx=(0, 20), pady=(20, 0), sticky="nsew")

        # Create buttons to translate text
        translate_text_btn = ctk.CTkButton(self, font=defaultTextButtonFont, text="Translate", command=lambda: self.translate_text(
            self.recognize_text_widget.get("0.0", "end"), change_lang_translate_switch.get()))
        translate_text_btn.grid(row=26, rowspan=1, column=9, columnspan=2, padx=(
            0, 20), pady=(20, 0), sticky="nsew")

        self.insert_text(image, scanText_language)

        # Bind the canvas size change event to update the image
        self.canvas.bind("<Configure>", self.on_canvas_resize)

    def on_canvas_resize(self, event):
        # Triggered when the canvas size changes
        self.display_image()

    def display_image(self):
        if self.image:
            self.canvas.delete("all")
            canvas_width, canvas_height = self.canvas.winfo_width(), self.canvas.winfo_height()
            img_width, img_height = self.image.size

            # Calculate the scaling factors for width and height based on the canvas size
            width_scale = canvas_width / img_width
            height_scale = canvas_height / img_height

            # Choose the minimum scaling factor to fit the entire image within the canvas
            scale_factor = min(width_scale, height_scale)

            # Resize the image while maintaining the aspect ratio
            new_width = int(img_width * scale_factor)
            new_height = int(img_height * scale_factor)
            resized_image = self.image.resize(
                (new_width, new_height), Image.LANCZOS)
            self.photo = ImageTk.PhotoImage(resized_image)

            # Calculate the center coordinates for the image on the canvas
            canvas_x = (canvas_width) // 2
            canvas_y = (canvas_height) // 2

            # Display the resized image on the canvas
            self.canvas.create_image(canvas_x, canvas_y, image=self.photo)

    # adding more processing if required

    def image_processing(self, img):
        # convert to cv2 image for image processing
        img_cv2 = np.array(img)
        # RGB, Contrast, Brightness
        gray = cv2.cvtColor(img_cv2, cv2.COLOR_BGR2GRAY)
        return gray

    def translate_text(self, input, translate_language):
        translator = Translator()
        OCR_lang_dict = {
            "English (Global)": "en",
            "English (US)": "en",
            "Korean": "ko",
            "Japanese": "ja",
            "Chinese (Simplified)": "zh-CN",
            "Chinese (Traditional)": "zh-TW",
            "Russian": "ru",
            "German": "de",
            "Spanish": "es",
            "Portuguese": "pt",
            "French": "fr",
        }

        # Translate text
        translate_result = translator.translate(
            str(input), dest=OCR_lang_dict[translate_language])

        if (translate_result != None):
            self.translate_text_widget.delete(1.0, ctk.END)
            self.translate_text_widget.insert(
                ctk.END, f"{translate_result.text}\n")

    def insert_text(self, image, scanText_language):
        if self.image:
            OCR_lang_dict = {
                "English (Global)": "en",
                "English (US)": "en",
                "Korean": "ko",
                "Japanese": "ja",
                "Chinese (Simplified)": "zh-CN",
                "Chinese (Traditional)": "zh-TW",
                "Russian": "ru",
                "German": "de",
                "Spanish": "es",
                "Portuguese": "pt",
                "French": "fr",
            }

            # Process the image using the image_processing function
            processed_img = self.image_processing(image)
            final_img = Image.fromarray(processed_img)
            results = asyncio.run(recognize_text(
                final_img, OCR_lang_dict[scanText_language]))
            if (results != None):
                self.recognize_text_widget.delete(1.0, ctk.END)
                for text in results:
                    self.recognize_text_widget.insert(ctk.END, f"{text}\n")


async def recognize_text(img, lang):
    try:
        result = (await winocr.recognize_pil(img, lang))
        # get only needed information - https://pypi.org/project/winocr/
        results = []
        for line in result.lines:
            results.append(line.text)
        return results
    except Exception as e:
        messagebox.showerror(
            title="Error!", message="Language is not installed.\nPlease install it in the Setting menu first.")
        return None
