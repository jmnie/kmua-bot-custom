from telegram import Chat

from ..dao.chat import get_chat_by_id, delete_chat
from ..dao import db
from ..dao.quote import delete_quote
from ..models.models import ChatData


def delete_chat_data_and_quotes(chat: Chat | ChatData):
    # 删除与该群组相关的所有数据
    db_chat = get_chat_by_id(chat.id)
    if db_chat is None:
        return
    for quote in db_chat.quotes:
        delete_quote(quote)
    delete_chat(db_chat)
    db.commit()
