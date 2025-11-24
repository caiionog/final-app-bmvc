from datetime import datetime
import uuid

class UserMessage:
    def __init__(self, autor, texto, id=None, timestamp=None):
        self.id = id or str(uuid.uuid4())   
        self.autor = autor
        self.texto = texto
        self.timestamp = timestamp or datetime.now().strftime("%d/%m/%Y %H:%M")