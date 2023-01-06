from vkbottle import BaseMiddleware
from vkbottle.bot import Message

from models import ChatSettings


class NoBotMiddleware(BaseMiddleware[Message]):
    "нам нужны кожанные мешки уебок"

    async def pre(self):
        return self.event.from_id > 0


class ChatNewsAdd(BaseMiddleware[Message]):
    'Для добавления новых чатов'

    async def pre(self):
        await ChatSettings.get_or_new(peer_id=self.event.peer_id)
        return True
