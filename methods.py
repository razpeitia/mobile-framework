from urllib import urlencode
from hashlib import md5
from json import loads

import requests

API_URL = 'http://www.forosdelweb.com/api.php'
API_KEY = "AQUI EL API KEY"

CLIENT_NAME = "python-client"
CLIENT_VERSION = "0.1"
PLATFORM_NAME = "python"
PLATFORM_VERSION =  "2.5"
UNIQUE_ID = "1023456789"
CONTENT = ''

def get_tokens(api_init):
    return api_init["apiaccesstoken"], api_init["apiclientid"], api_init["secret"]

def create_signature(apikey, api_init , call):
    apiaccesstoken, apiclientid, secret = get_tokens(api_init) 
    sorted_query_string = urlencode(sorted(call.items()), doseq=True)
    sign = sorted_query_string + apiaccesstoken + apiclientid + secret + API_KEY
    return md5(sign).hexdigest()

def add_params(params, api_init):
    params["api_c"] = api_init["apiclientid"]
    params["api_s"] = api_init["apiaccesstoken"]
    params["api_v"] = api_init["apiversion"]
    
def add_signature(params, api_init):
    signature = create_signature(API_KEY, api_init, params)
    params["api_sig"] = signature
    
def caller(api_init, params, signature=False, method="get", post_data={}):
    if signature:
        add_signature(params, api_init)
    if api_init:
        add_params(params, api_init)
    if method == "post":
        response = requests.post(API_URL, params=params, data=post_data)
        response_str = response.text
    else:
        response = requests.get(API_URL, params=params)
        response_str = response.text
    return loads(response_str)
    

def api_init():
    params = {
        'api_m' : 'api_init',
        'clientname' : CLIENT_NAME,
        'clientversion' : CLIENT_VERSION,
        'platformname' : PLATFORM_NAME,
        'platformversion' : PLATFORM_VERSION,
        'uniqueid' : UNIQUE_ID,
        'content' : CONTENT,
    }
    return caller(None, params)

def forum_display(api_init, forumid):
    params = {'api_m': 'forumdisplay', "forumid" : forumid}
    return caller(api_init, params, signature=True) 

def login_login(api_init, vb_login_username, vb_login_md5password):
    params = {'api_m': 'login_login', 
              'vb_login_username': vb_login_username, 
              'vb_login_md5password' : vb_login_md5password}
    return caller(api_init, params, signature=True, method="post", post_data=params)

def login_logout(api_init):
    params = {'api_m': 'login_logout'}
    return caller(api_init, params, signature=True)

def misc_buddylist(api_init, session):
    params = {'api_m': 'misc_buddylist'}
    return caller(api_init, params, signature=True)
