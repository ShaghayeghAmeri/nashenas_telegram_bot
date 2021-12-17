import emoji
from loguru import logger
from telebot import types

from src.bot import bot
from src.constant import keyboards
from src.filters import IsAdmin
from src.utils.io import write_json


class Bot:
    """"
    Telegram templete bot
    """
    def __init__(self, telebot):
        self.bot = telebot

        # add custom filters
        self.bot.add_custom_filter(IsAdmin())

        # register handelers
        self.handelers() 

        # run bot
        logger.info('Bot is running...')
        self.bot.infinity_polling()
        
    def handelers(self):
        @self.bot.message_handler(is_admin=True)
        def admin_of_group(message):
    	    self.send_message(message.chat.id, '<strong>You are admin of this group!</strong>')

        @self.bot.message_handler(func=lambda m: True)
        def echo(message):
            # write_json(message.json, 'message.json')
            self.send_message(
            message.chat.id, message.text, 
            reply_markup=keyboards.main
            )	
    
    def send_message(self, chat_id, text, reply_markup=None, emojize=True):
        """
        send message to telegram bot
        """
        if emojize:
            text = emoji.emojize(text)
        self.bot.send_message(chat_id, text, reply_markup=reply_markup)

			
if __name__=='__main__':
    logger.info('bot starts...')
    bot = Bot(telebot=bot)
    bot.run()

 