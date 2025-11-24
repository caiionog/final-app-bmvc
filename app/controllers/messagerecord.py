# app/controllers/messagerecord.py
import json
import uuid
import os
from datetime import datetime
from app.models.user_message import UserMessage

class MessageRecord:
    """Banco de dados JSON para o recurso Mensagens"""

    def __init__(self):
        self.__path = "app/controllers/db/user_messages.json"
        self.__messages = []
        self._ensure_file()
        self.read()

    def _ensure_file(self):
        folder = os.path.dirname(self.__path)
        if folder and not os.path.exists(folder):
            os.makedirs(folder, exist_ok=True)
        if not os.path.exists(self.__path):
            with open(self.__path, "w", encoding="utf-8") as f:
                json.dump([], f, indent=4)

    def read(self):
        try:
            with open(self.__path, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if not content:
                    self.__messages = []
                    return
                data = json.loads(content)
                # cria instâncias UserMessage (aceita dict ou já instância)
                self.__messages = []
                for item in data:
                    if isinstance(item, dict):
                        # converte chaves antigas (texto/text) se necessário
                        self.__messages.append(UserMessage(
                            autor=item.get("autor") or item.get("author"),
                            texto=item.get("texto") or item.get("text"),
                            id=item.get("id"),
                            timestamp=item.get("timestamp")
                        ))
                    else:
                        # caso já sejam objetos (raro)
                        self.__messages.append(item)
        except (FileNotFoundError, json.JSONDecodeError):
            self.__messages = []

    def save(self):
        """Salva lista completa no JSON"""
        with open(self.__path, "w", encoding="utf-8") as f:
            # converte objetos UserMessage para dicts
            data = []
            for m in self.__messages:
                # suporto tanto atributos 'texto' quanto 'text'
                data.append({
                    "id": getattr(m, "id", None),
                    "autor": getattr(m, "autor", None),
                    "texto": getattr(m, "texto", None),
                    "timestamp": getattr(m, "timestamp", None)
                })
            json.dump(data, f, indent=4, ensure_ascii=False)

    # CREATE
    def add_message(self, author, content):
        new_msg = UserMessage(author, content)
        self.__messages.append(new_msg)
        self.save()
        return new_msg

    # READ
    def get_all_messages(self):
        return self.__messages

    def find_by_user(self, author):
        return [msg for msg in self.__messages if msg.autor == author]

    def get_by_id(self, msg_id):
        for m in self.__messages:
            if m.id == msg_id:
                return m
        return None

    # UPDATE
    def update_message(self, msg_id, new_text):
        for m in self.__messages:
            if m.id == msg_id:
                m.texto = new_text
                m.timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                self.save()
                return True
        return False

    # DELETE
    def delete_message(self, msg_id):
        orig_len = len(self.__messages)
        self.__messages = [m for m in self.__messages if m.id != msg_id]
        if len(self.__messages) != orig_len:
            self.save()
            return True
        return False
