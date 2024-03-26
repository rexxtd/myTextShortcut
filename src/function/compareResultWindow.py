import customtkinter as ctk


class ComparisonTopWindow(ctk.CTkToplevel):
     def __init__(self, diff, highlightColor, highlightOption):
        super().__init__()
        self.geometry("600x350")
        self.minsize(600, 350)
        self.title("Comparison Results")
        self.focus_force()

        defaultTextFont = ctk.CTkFont(family="Calibri", size=16, weight='bold')

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure((0, 1), weight=1)

        self.result_box1 = ctk.CTkTextbox(self, wrap=ctk.WORD, state='normal', font=defaultTextFont)
        self.result_box1.configure(autoseparators=True, undo=True, maxundo=-1)
        self.result_box1.grid(row=0, column=0, padx=20, pady=(20, 20), sticky="nsew")
        self.result_box2 = ctk.CTkTextbox(self, wrap=ctk.WORD, state='normal', font=defaultTextFont)
        self.result_box2.configure(autoseparators=True, undo=True, maxundo=-1)
        self.result_box2.grid(row=0, column=1, padx=20, pady=(20, 20), sticky="nsew")

        
        for flag, word in diff:
            if flag == 0:
                self.result_box1.insert("end", word)
                self.result_box2.insert("end", word)
            elif flag == 1:
                self.result_box2.insert("end", word, "diff")
            elif flag == -1:
                self.result_box1.insert("end", word, "diff")
        if (highlightOption=='highlight text'):
            self.result_box1.tag_config('diff', foreground=highlightColor)
            self.result_box2.tag_config('diff', foreground=highlightColor)
        elif (highlightOption=='highlight line'):
            self.result_box1.tag_config('diff', background=highlightColor)
            self.result_box2.tag_config('diff', background=highlightColor)
        