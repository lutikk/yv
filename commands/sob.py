from vkbottle.bot import BotLabeler, Message

from models import GayDay, DR, ChatSettings
from utils import is_admin, get_user_id

bl = BotLabeler()
bl.vbml_ignore_case = True


@bl.message(text=[
    'создать событие <day:int>.<mes:int>\n<name>',
    'создать событие <day:int>.<mes:int>\n <name>',
    'создать событие <day:int>.<mes:int> \n<name>',
    'создать событие <day:int>.<mes:int>.<god:int>\n<name>',
    'создать событие <day:int>.<mes:int>.<god:int> \n<name>',
    'создать событие <day:int>.<mes:int>.<god:int>\n <name>',
])
async def greeting(message: Message, day: int, mes: int, god: int = 0, name: str = "", **kwargs):
    if not await is_admin(message.ctx_api, message.peer_id, message.from_id):
        return
    await GayDay.create(day=day, mes=mes, god=god, name=name, sozd_id=message.from_id, peer_id=message.peer_id)
    return f'Создал событие: "{name}"'


@bl.message(text=[
    'удалить событие <name>'

])
async def greeting(message: Message, name: str):
    if not await is_admin(message.ctx_api, message.peer_id, message.from_id):
        return
    await GayDay.filter(peer_id=message.peer_id, name=name).delete()
    return f'Удалил событие {name}'


@bl.message(text=[
    '+др <day:int>.<mes:int>',
    '+др <day:int>.<mes:int>.<god:int>'
])
async def greeting(message: Message, day: int, mes: int, god: int = 0):
    chat = await ChatSettings.get(peer_id=message.peer_id)
    if chat.user:
        await DR.get_or_create(user_id=message.from_id, peer_id=message.peer_id)
        ss = await DR.get(user_id=message.from_id, peer_id=message.peer_id)
        ss.day = day
        ss.mes = mes
        ss.god = god
        await ss.save()
        return "Создал день рождение"
    else:
        return 'Обратитесь к администрации чата чтоб создать день рождения'


@bl.message(text=[
    'создать др <day:int>.<mes:int> <url>',
    'создать др <day:int>.<mes:int>.<god:int> <url>'
])
async def greeting(message: Message, day: int, mes: int, god: int = 0, url: str = ''):
    if not await is_admin(message.ctx_api, message.peer_id, message.from_id):
        return
    user_id = get_user_id(message.text)[0]
    await DR.get_or_create(user_id=user_id, peer_id=message.peer_id)
    ss = await DR.get(user_id=user_id, peer_id=message.peer_id)
    ss.day = day
    ss.mes = mes
    ss.god = god
    await ss.save()
    return "Создал др"



@bl.message(text=[
    'удалить др <url>'
])
async def greeting(message: Message, url: str = ''):
    if not await is_admin(message.ctx_api, message.peer_id, message.from_id):
        return
    await DR.filter(user_id=get_user_id(message.text)[0], peer_id=message.peer_id).delete()
    return "Удалил др"