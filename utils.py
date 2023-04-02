import sys
from base64 import b64encode

import requests
from PyQt6.QtCore import QSettings
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMessageBox

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
