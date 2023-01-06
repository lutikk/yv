import asyncio
import datetime
import re
import time

import vk_api
from tortoise import Tortoise
from vkbottle import API
from vkbottle.bot import Message

from config import main_token
from models import GayDay, DR, ChatSettings


async def init_tortoise():
    await Tortoise.init(
        db_url='sqlite://data/db.sqlite3',
        modules={'models': ['models']}
    )
    await Tortoise.generate_schemas()


def get_user_id_by_domain(user_domain: str):
    """Поиск ID по домену"""
    vk = vk_api.VkApi(token=main_token)

    obj = vk.method('utils.resolveScreenName', {"screen_name": user_domain})

    if isinstance(obj, list):
        return
    if obj['type'] == 'user':
        return obj["object_id"]


def get_user_id(text):
    result = []

    regex = r"(?:vk\.com\/(?P<user>[\w\.]+))|(?:\[id(?P<user_id>[\d]+)\|)"

    for user_domain, user_id in re.findall(regex, text):
        if user_domain:
            result.append(get_user_id_by_domain(user_domain))
        if user_id:
            result.append(int(user_id))

    _result = []
    for r in result:
        if r is not None:
            _result.append(r)
    return _result


async def is_admin(api: API, peer_id: int, user_id: int) -> bool:
    conversation = await api.messages.get_conversation_members(peer_id=peer_id)
    for item in conversation.items:
        if user_id == item.member_id:
            return True if item.is_admin else False


async def get_name(user_id: int, m: Message):
    a = await m.get_user(user_ids=user_id)

    nik3 = f'[id{a.id}|{a.first_name} {a.last_name}]'

    return nik3


def awtor():
    session = vk_api.VkApi(token=main_token)
    vk = session.get_api()
    return vk


async def yv():
    try:
        
        await init_tortoise()
        now = datetime.datetime.now()
        god = now.year
        mes = now.month
        day = now.day
        tim = now.hour
        min = now.minute
        if int(tim) == 12 and int(min) == 00:
            text = ''
            chats = await ChatSettings.all()

            for chat in chats:
                print(chat.peer_id)
                pr = await GayDay.filter(peer_id=chat.peer_id, day=day, mes=mes)
                if len(pr) != 0:

                    text += 'События на сегодня:\n'
                    for p in pr:
                        if p.god == 0 or p.god == int(god):
                            text += f'{p.name}\n'

                happy = await DR.filter(peer_id=chat.peer_id, day=day, mes=mes)
                if len(happy) != 0:
                    text += 'События на сегодня:\n'
                    for p in happy:
                        if p.god == 0:
                            vk = awtor()
                            user = vk.users.get(user_ids=p.user_id)
                            name = f'[id{p.user_id}|{user[0]["first_name"]} {user[0]["last_name"]}]'

                            text += f'{name} исполняется: неизвестно'
                        else:
                            vk = awtor()
                            user = vk.users.get(user_ids=p.user_id)
                            name = f'[id{p.user_id}|{user[0]["first_name"]} {user[0]["last_name"]}]'
                            text += f'{name} исполняется: {int(now.year) - p.god}'
                vk = awtor()
                if not len(text) <= 5:
                    vk.messages.send(peer_id=int(chat.peer_id), message=str(text), random_id=0)

                else:
                    pass
            time.sleep(70)
            await Tortoise.close_connections()
        else:
            await Tortoise.close_connections()
    except Exception as e:
        await Tortoise.close_connections()
        return e


def yv_start():
    while True:
        asyncio.run(yv())
        time.sleep(0.3)
