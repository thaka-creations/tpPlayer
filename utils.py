import base64
import hashlib
import json
import os
import platform
import plistlib
import subprocess
import sys
from base64 import b64encode
from datetime import datetime, timedelta
from threading import Thread

import requests
from cryptography.fernet import Fernet
from PyQt5.QtCore import QSettings
from PyQt5.QtGui import QIcon

import settings
from settings import BASE_URL

ss = QSettings("TafaPlayer", "TafaPlayer")


# check if user is authenticated
def is_authenticated():
    authenticated_user = retrieve_headers()
    if isinstance(authenticated_user, dict):
        return True
    return False


# get stored headers
def retrieve_headers():
    try:
        username = ss.value("username")
        password = ss.value("password")
        if username is None or password is None:
            return False
        return {"username": username, "JWTAUTH": password}
    except Exception as e:
        print(e)
        return False


def store_headers(headers, password):
    try:
        ss.setValue("username", headers['username'])
        ss.setValue("password", password)
        ss.setValue("name", b64encode(headers['name'].encode()).decode())
        ss.setValue("phone", b64encode(headers['phone'].encode()).decode())
    except Exception as e:
        print(e)


# delete stored headers
def delete_headers():
    try:
        if ss.value("username"):
            ss.remove("username")
            ss.remove("password")
            ss.remove("name")
            ss.remove("phone")
    except Exception as e:
        print(e)
        if ss.value("username"):
            ss.remove("username")
            ss.remove("password")


# retrieve icon
def get_icon():
    try:
        return QIcon(sys._MEIPASS + '/assets/tafa.ico')
    except AttributeError:
        return QIcon('assets/tafa.ico')


# register user func
def register_user(payload):
    url = f"{BASE_URL}/api/v1/users/register"
    try:
        response = requests.post(url, json=payload, timeout=30)
        if response.status_code == 200:
            return True, response.json()['message']
        else:
            return False, response.json()['message']
    except requests.exceptions.ConnectionError:
        return False, "Could not connect to server. Make sure you are connected to the internet"


# resend otp
def resend_otp(payload):
    url = f"{BASE_URL}/api/v1/users/resend-otp"
    try:
        response = requests.post(url, json=payload, timeout=30)
        if response.status_code == 200:
            return True, response.json()['message']
        else:
            return False, response.json()['message']
    except requests.exceptions.ConnectionError:
        return False, "Could not connect to server. Make sure you are connected to the internet"


# verify otp sent
def verify_otp(payload):
    url = f"{BASE_URL}/api/v1/users/verify-otp"
    try:
        response = requests.post(url, json=payload, timeout=30)
        if response.status_code == 200:
            return True, response.json()['message']
        else:
            return False, response.json()['message']
    except requests.exceptions.ConnectionError:
        return False, "Could not connect to server. Make sure you are connected to the internet"


# get local storage keys, read keys from secure storage
def get_local_keys():
    try:
        keys = ss.value('keys')
        if not isinstance(keys, list):
            return [keys]
        return keys
    except Exception as e:
        print(e)
        return []


# get last connected date
def get_next_connection_date():
    if ss.value('last_date_connected'):
        return ss.value('last_date_connected')
    return None


# set next connection date
def set_next_connection_date():
    next_date = datetime.now() + timedelta(days=30)
    ss.setValue("last_date_connected", next_date.strftime("%Y-%m-%d"))


# compare version with find new version
def check_for_new_version():
    if ss.value('version'):
        version = ss.value('version')
    else:
        version = None

    # latest version
    try:
        latest_version = requests.get(f"{BASE_URL}/api/v1/videos/player-version").json()['version']
        if not version:
            ss.setValue("version", latest_version)
            return True, latest_version
        elif version != latest_version:
            return False, "New version available"
        else:
            return True, latest_version
    except requests.exceptions.ConnectionError:
        return True, None


def get_app_keys():
    try:
        url = f"{BASE_URL}/api/v1/videos/list-app-keys"
        app_id = get_app_id()['id']
        response = requests.get(url, params={'request_id': app_id})
        if not response.status_code == 200:
            return False, "An error occurred"
    except requests.exceptions.ConnectionError:
        return False, "No internet connection"
    except Exception as e:
        print(e)
        return False, "An error occurred"

    return True, response.json()['message']


def sync_keys():
    status, keys = get_app_keys()
    if not status:
        return False, keys

    local_keys = get_local_keys()

    # check if keys are registered on device
    print("local keys", get_local_keys())
    print("app keys", get_app_keys())
    if len(keys) > 0:
        new_keys = [
            key for key in local_keys if key['key'] in keys
        ]
        Thread(target=register_keys, args=(new_keys,), daemon=False).start()


# register keys to app
def register_keys(keys):
    if ss.value('keys'):
        # append to existing keys
        if not isinstance(keys, list):
            existing_keys = ss.value('keys')
            keys = [keys]
            if existing_keys:
                existing_keys.extend(keys)
            else:
                existing_keys = keys
            ss.setValue('keys', existing_keys)
        else:
            ss.setValue('keys', keys)
    else:
        ss.setValue('keys', [keys])


# get machine serial number
def get_mac_serial_number():
    output = subprocess.check_output(['system_profiler', 'SPHardwareDataType'])
    lines = output.decode().split('\n')
    for line in lines:
        if 'Serial Number' in line:
            return line.split()[-1]


def get_windows_serial_number():
    try:
        output = subprocess.run(["wmic", "bios", "get", "serialnumber"], stdout=subprocess.PIPE).stdout.decode("utf-8")
        serial_number = output.split("\n")[1].split(" ")[0]
        return serial_number
    except Exception as e:
        print(e)
        return None


def get_serial_number():
    os_type = platform.system()
    if "darwin" in os_type.lower():
        serial_number = get_mac_serial_number()
    else:
        serial_number = get_windows_serial_number()
    return serial_number


# get mac model name
def get_mac_model_name():
    pl = subprocess.run(["system_profiler", "SPHardwareDataType", "-xml"], capture_output=True).stdout
    plist = plistlib.loads(pl)
    model_name = plist[0]['_items'][0]['machine_model']
    return model_name


def get_windows_model_name():
    output = subprocess.run("wmic csproduct get name", shell=True, capture_output=True, text=True)
    try:
        model_name = output.stdout.strip().split("\n")[2]
    except IndexError:
        model_name = output.stdout.strip().split("\n")[1]
    return model_name


# get machine model name
def get_model_mame():
    os_type = platform.system()
    if 'darwin' in os_type.lower():
        model_name = get_mac_model_name()
    else:
        model_name = get_windows_model_name()
    return model_name


# register app
def register_app():
    url = f"{BASE_URL}/api/v1/videos/app-registered"
    payload = {"serial_number": get_serial_number(), "model_name": get_model_mame()}
    response = requests.post(url, json=payload)

    if not response.status_code == 200:
        return False

    try:
        resp = response.json()['message']
        conf = {'app': resp}
        token = settings.TOKEN_KEY
        key = base64.urlsafe_b64encode(hashlib.sha256(token.encode()).digest()[:32])
        fernet = Fernet(key)
        encrypted_data = fernet.encrypt(json.dumps(conf).encode())
        ss.setValue('config', encrypted_data.decode())
        return True
    except Exception as e:
        print(e)
        return False


# check if app's genuine
def is_app_genuine():
    if not ss.value('config'):
        response = retrieve_headers()
        if isinstance(response, dict):
            delete_headers()
            # register app
            register_app()
        return True
    else:
        # decrypt config
        token = settings.TOKEN_KEY
        key = base64.urlsafe_b64encode(hashlib.sha256(token.encode()).digest()[:32])
        fernet = Fernet(key)
        try:
            encrypted_data = ss.value("config")
            decrypted_data = fernet.decrypt(encrypted_data.encode())
            return json.loads(decrypted_data)
        except Exception as e:
            print(e)
            return False


# get app's id
def get_app_id():
    config = is_app_genuine()
    if isinstance(config, dict):
        return config['app']
    return False


# get alternate registered keys on other devices
def get_registered_keys():
    try:
        url = f"{BASE_URL}/api/v1/videos/list-client-keys"
        headers = retrieve_headers()
        app_id = get_app_id()['id']
        headers.update({'request_id': app_id})
        response = requests.post(url, json=headers)
        if not response.status_code == 200:
            return False, "An error occurred"

        return True, response.json()['message']
    except requests.exceptions.ConnectionError:
        return False, "No internet connection"


def activate_key(key, app_id, headers):
    url = f"{BASE_URL}/api/v1/videos/activate-key"
    headers.update({'key': key, 'app_id': app_id})

    try:
        response = requests.post(url, json=headers)
        if response.status_code == 200:
            return True, response.json()['message']
        elif response.status_code == 403:
            return False, '403'
        else:
            return False, response.json()['message']
    except requests.exceptions.ConnectionError:
        return False, "Kindly check your internet connection"
