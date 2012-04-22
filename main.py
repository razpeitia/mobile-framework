import methods

def main():
    #api_init requerido para varias llamadas
    api_init = methods.api_init()
    
    #Despliega informacion del foro 130 aka python
    forum_display = methods.forum_display(api_init, "130")
    print forum_display
    
    #Login del usuario
    #nombre de usuario y el password en md5 hexdigest requerido
    session = methods.login_login(api_init, "username", "md5 password")
    print session
    
    #Obtenemos la lista de amigos
    print methods.misc_buddylist(api_init, session)
    
    #Logout exitoso
    print methods.login_logout(api_init)
    

if __name__ == '__main__':
    main()
