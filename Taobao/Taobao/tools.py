import re
import random
import time

import os
import re
import xlwt
import sqlite3
import requests
from win32.win32crypt import CryptUnprotectData


def data_cleaning(data):
    if ' ' in data:
        data = re.sub(' ', '', data)
    if "'" in data:
        data = re.sub("'", '', data)
    if r'\n' in data:
        data = re.sub(r'\\n', '', data)
    return data


def getcookiefromchrome():
    host = '.taobao.com'
    cookies_str = ''
    cookiepath = os.environ['LOCALAPPDATA'] + r"\Google\Chrome\User Data\Default\Cookies"
    sql = "select host_key,name,encrypted_value from cookies where host_key='%s'" % host
    with sqlite3.connect(cookiepath) as conn:
        cu = conn.cursor()
        cookies = {name: CryptUnprotectData(encrypted_value)[1].decode() for host_key, name, encrypted_value in
                   cu.execute(sql).fetchall()}
        # for key,values in cookies.items():
        # cookies_str = cookies_str + str(key)+"="+str(values)+';'
        return cookies
