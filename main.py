from vkbottle import Bot

from commands import labelers
from config import main_token
from middlewares import NoBotMiddleware, ChatNewsAdd
from utils import init_tortoise

bot = Bot(main_token)

bot.labeler.vbml_ignore_case = True
for custom_labeler in labelers:
    bot.labeler.load(custom_labeler)

bot.labeler.message_view.register_middleware(NoBotMiddleware)
bot.labeler.message_view.register_middleware(ChatNewsAdd)

session_manager = True
ignore_error = True
ask_each_event = True

if __name__ == "__main__":
    bot.loop_wrapper.on_startup += [init_tortoise()]
    bot.run_forever()
