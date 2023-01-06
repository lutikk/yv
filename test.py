import datetime

from utils import awtor

now = datetime.datetime.now()

print("Текущая дата и время с использованием метода str:")
print(now)

print("Текущая дата и время с использованием атрибутов:")
print("Текущий год: %d" % now.year)
print("Текущий месяц: %d" % now.month)
print("Текущий день: %d" % now.day)
print("Текущий час: %d" % now.hour)
print("Текущая минута: %d" % now.minute)
print("Текущая секунда: %d" % now.second)
print("Текущая микросекунда: %d" % now.microsecond)
print("Текущая дата и время с использованием strftime:")
print(now.strftime("%d-%m-%Y %H:%M"))

print("Текущая дата и время с использованием isoformat:")
print(now.isoformat())

vk = awtor()

user = vk.users.get(user_ids=1)
name = f'{user[0]["first_name"]} {user[0]["last_name"]}'
print(name)
