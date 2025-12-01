from app.controllers.datarecord import DataRecord
from app.controllers.messagerecord import MessageRecord
from bottle import template, redirect, request


class Application():

    def __init__(self):

        self.pages = {
            'pagina': self.pagina,
            'portal': self.portal,
            'message_portal': self.message_portal,
            'messages': self.list_messages,
            'buscar_perfil': self.buscar_perfil
        }

        self.__model= DataRecord()
        self.__messages = MessageRecord()
        self.__current_loginusername= None


    def render(self,page,parameter=None):
        content = self.pages.get(page, self.helper)
        if not parameter:
            return content()
        else:
            return content(parameter)

    def get_session_id(self):
        return request.get_cookie('session_id')

    def helper(self):
        return template('app/views/html/helper')

    def portal(self):
        return template('app/views/html/portal')
    
    def message_portal(self):
        return template('app/views/html/message_portal')
    
    def buscar_perfil(self):
        return template('app/views/html/buscar_perfil')

    def pagina(self,username=None):
        user_messages = self.__messages.find_by_user(username)
        return template('app/views/html/pagina', author=username, user_messages=user_messages)

    def is_authenticated(self, username):
        session_id = self.get_session_id()
        current_username = self.__model.getUserName(session_id)
        return username == current_username

    def authenticate_user(self, username, password):
        session_id = self.__model.checkUser(username, password)
        if session_id:
            self.logout_user()
            self.__current_username= self.__model.getUserName(session_id)
            return session_id, username
        return None

    def is_logged(self):
        session_id = self.get_session_id()
        user = self.__model.getCurrentUser(session_id)
        return user is not None

    def logout_user(self):
        self.__current_username= None
        session_id = self.get_session_id()
        if session_id:
            self.__model.logout(session_id)

    def save_message(self, text):
        session_id = self.get_session_id()
        user = self.__model.getCurrentUser(session_id)
        if not user:
            return redirect('/portal')
        author = user.username
        self.__messages.add_message(author, text)

    def list_messages(self):
        messages = self.__messages.get_all_messages()
        session_id = self.get_session_id()
        current_user = self.__model.getCurrentUser(session_id)
        return template('app/views/html/messages', messages=messages, current_user=current_user)
    
    def delete_message(self, msg_id):
        msg = self.__messages.get_by_id(msg_id)
        if not msg:
            return False  
        session_id = self.get_session_id()
        user = self.__model.getCurrentUser(session_id)
        if not user:
            return False  
    # compara usuário logado com o autor da mensagem
        if getattr(user, "username", None) != getattr(msg, "autor", None):
            return False  
        return self.__messages.delete_message(msg_id)

    def get_message(self, msg_id):
        return self.__messages.get_by_id(msg_id)

    def update_message(self, msg_id, new_text):
        self.__messages.update_message(msg_id, new_text)
