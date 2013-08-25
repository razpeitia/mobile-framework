from urllib import urlencode
import hashlib
import json

import requests
from settings import API_URL, API_KEY, CLIENT_NAME, CLIENT_VERSION, \
                     PLATFORM_NAME, PLATFORM_VERSION, UNIQUE_ID, CONTENT


class Api(object):
    GET = 0
    POST = 1

    def __init__(self, api_key=API_KEY, client_name=CLIENT_NAME, 
        client_version=CLIENT_VERSION, plataform_name=PLATFORM_NAME,
        platform_version=PLATFORM_VERSION, unique_id=UNIQUE_ID, content=CONTENT):
        self.api_key = api_key
        self.client_name = client_name
        self.client_version = client_version
        self.plataform_name = plataform_name
        self.platform_version = platform_version
        self.unique_id = unique_id
        self.content = content

        params = {
            'api_m' : 'api_init',
            'clientname' : self.client_name,
            'clientversion' : self.client_version,
            'platformname' : self.plataform_name,
            'platformversion' : self.platform_version,
            'uniqueid' : self.unique_id,
            'content' : self.content,
        }
        response = requests.get(API_URL, params=params)
        response = json.loads(response.text)

        self.api_access_token = response['apiaccesstoken']
        self.api_client_id = response['apiclientid']
        self.secret = response['secret']
        self.api_version = response['apiversion']

    def get_signature_for(self, params):
        sorted_query_string = urlencode(sorted(params.items()), doseq=True)
        signature = sorted_query_string + self.api_access_token + self.api_client_id + self.secret + API_KEY
        return hashlib.md5(signature).hexdigest()

    def caller(self, function_name, function_params={}, method=GET, data={}):
        params = {
            'api_m': function_name,
        }
        params.update(function_params)
        
        params['api_sig'] = self.get_signature_for(params)
        
        params.update({
            'api_c': self.api_client_id,
            "api_s": self.api_access_token,
            "api_v": self.api_version,
        })

        if method == self.POST:
            response = requests.post(API_URL, params=params, data=data)
        else:
            response = requests.get(API_URL, params=params)
        return response.text

    def forum_list(self):
        # Shame on you raz, this code is terrible and you should feel bad
        """
        structure = {}
        response = self.caller('forum')
        response = json.loads(response)

        # Init birthday stuff
        response_birthdays = response['response'].get('birthdays', None)
        structure['birthdays'] = birthdays = []

        # Init forum list
        response_forums = response['response'].get('forumbits', None)
        structure['forums'] = forums = []

        # Parse the birthdays
        if isinstance(response_birthdays, list):
            for birthday in response_birthdays:
                birthday = birthday['birthday']
                birthday = {
                    "user_id": birthday.get('userid', None),
                    "username": birthday.get('username', None),
                    "age": birthday.get('age', None),
                }
                birthdays.append(birthday)
        elif isinstance(response_birthdays, dict):
            raise NotImplemented('Implement this lazy ass')

        # Parse the forums
        if isinstance(response_forums, list):
            for forum in response_forums:
                forum_list_response = forum['childforumbits']
                forum_list = []
                
                forum = forum['forum']
                forum = {
                    'forum_id': forum.get('forumid', None),
                    'title': forum.get('title', None),
                    'description': forum.get('description', None),
                    'forum_list': forum_list,
                }
                forums.append(forum)

                for forum in forum_list_response:
                    forum_info = forum['forum']
                    forum_info = {
                        "forum_id": forum_info.get('forumid', None),
                        "thread_count": forum_info.get('threadcount', None),
                        "reply_count": forum_info.get('replycount', None),
                        "title": forum_info.get('title', None),
                        "description": forum_info.get('description', None),
                        "status_icon": forum_info.get('statusicon', None),
                        "browsers": forum_info.get('browsers', None),
                    }
                    forum_list.append(forum_info)
        return structure
        """
        return self.caller('forum')
        
        

    def forum_display(self, forum_id):
        params = {"forumid" : forum_id}
        return self.caller('forumdisplay', params)

    def thread_display(self, thread_id):
        params = {'threadid': thread_id}
        return self.caller('showthread', params=params)

    def login(self, username, password):
        params = {
            'vb_login_username': username, 
            'vb_login_md5password' : hashlib.md5(password).hexdigest(),
        }
        return self.caller('login_login', params, method=Api.POST, data=params)

    def logout(self):
        return self.caller('login_logout')

    def buddy_list(self):
        return self.caller('misc_buddylist')

