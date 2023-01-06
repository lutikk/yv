import asyncio
import time
import datetime
import os
from utils import yv


def yv_start():
    while True:
        now = datetime.datetime.now()
        tim = now.hour
        min = now.minute
        if int(tim) == 12 and int(min) == 00:
            asyncio.run(yv())
            time.sleep(120)
        else:
            time.sleep(1)
            os.system('service yv2 restart')
