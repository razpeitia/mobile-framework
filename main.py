from pprint import pprint
from vapi import Api

def main():
    api = Api()
    
    forum_list = api.forum_list()
    # forum_display = api.forum_display("130")
    pprint(forum_list)
    # thread_display = api.thread_display()

    # api.login('my_username', 'my_password')
    # api.buddy_list()
    # api.logout()
    
    

if __name__ == '__main__':
    main()
