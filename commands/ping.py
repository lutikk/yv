import datetime
import time

from vkbottle.bot import BotLabeler, Message

from models import GayDay, DR, ChatSettings
from utils import is_admin, get_name

bl = BotLabeler()
bl.vbml_ignore_case = True


@bl.message(text='пинг')
async def greeting(message: Message):
    delta = round(time.time() - message.date, 2)

    # А ты думал тут все чесно будет? Не, я так не работаю...
    if delta < 0:
        delta = "666"
    await message.answer(f"Понг\nУшел бухать за {delta} секунд")


@bl.message(text=[
    'праздники',
    'события',
    'что сегодня'
])
async def greeting(message: Message):
    text = 'События на сегодня:\n'
    now = datetime.datetime.now()
    ss = await GayDay.filter(peer_id=message.peer_id, day=now.day, mes=now.month)
    if len(ss) == 0:
        text += "На сегодня событий нет\n"
    else:
        for s in ss:
            if s.god == 0 or s.god == now.year:
                text += f'{s.name}\n'
            else:
                pass
    sq = await DR.filter(peer_id=message.peer_id, day=now.day, mes=now.month)
    text += "Дни рождения:\n"
    if len(sq) == 0:
        text += "На сегодня днюх не обнаружено"
    else:
        for sss in sq:
            if sss.god == 0:
                name = await get_name(sss.user_id, message)
                text += f'{name} исполняется: неизвестно'
            else:
                name = await get_name(sss.user_id, message)
                text += f'{name} исполняется: {int(now.year) - sss.god}'

    return text


@bl.message(text='др +юзеры')
async def greeting(message: Message):
    if not await is_admin(message.ctx_api, message.peer_id, message.from_id):
        return
    chat_db = await ChatSettings.get(peer_id=message.peer_id)
    chat_db.user = True
    await chat_db.save()
    return "Теперь пользователи беседы могут сами заполнять свои дни рождения"


@bl.message(text='др -юзеры')
async def greeting(message: Message):
    if not await is_admin(message.ctx_api, message.peer_id, message.from_id):
        return
    chat_db = await ChatSettings.get(peer_id=message.peer_id)
    chat_db.user = False
    await chat_db.save()
    return "Теперь пользователи беседы не могут сами заполнять свои дни рождения"
