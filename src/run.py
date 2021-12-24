import emoji
import pymongo
from loguru import logger
from telebot import types

from src.bot import bot
from src.constant import keyboards, keys, states
from src.filters import IsAdmin
from src.utils.io import write_json


class Bot:
    """"
    Telegram templete bot
    """
    def __init__(self, telebot):

        """
        Initialize bot, database, handlers, and filters.
        """
        self.bot = telebot
        client = pymongo.MongoClient("localhost", 27017)
        self.db = client.nashenas_telegram_bot

        # add custom filters
        self.bot.add_custom_filter(IsAdmin())

        # register handelers
        self.handelers() 

        # run bot
        logger.info('Bot is running...')
        self.bot.infinity_polling()
        
    def handelers(self):
        
        @self.bot.message_handler(commands=['start'])
        def send_welcome(message):
            self.bot.reply_to(message, 
            f"Hey, <strong>{message.chat.first_name}</strong>",
            reply_markup=keyboards.main
            )
           
            self.db.users.update_one(
                {'chat.id': message.chat.id}, 
                {'$set': message.json}, 
                upsert=True
            )
            self.update_state(message.chat.id, states.main)

        @self.bot.message_handler(regexp=emoji.emojize(keys.random_conect))
        def random_connect(message):
            self.send_message(
                message.chat.id,
                'Connecting you to a stranger...', reply_markup=keyboards.exit
            )
            self.update_state(message.chat.id, states.random_connect)
            
            other_user = self.db.users.find_one(
                {
                    'state': states.random_connect,
                    'chat.id': {'$ne': message.chat.id}
                }
            )

            if not other_user:
                return
            # update other_user state
            self.update_state(other_user["chat"]["id"], states.connected)
            self.send_message(
                other_user["chat"]["id"], 
                f'Connecting to {message.chat.id}'
            )

            # update current user states
            self.update_state(message.chat.id, states.connected)
            self.send_message(
                message.chat.id, 
                f'Connected to {other_user["chat"]["id"]}...'
            )

            # store connected users
            self.db.users.update_one(
                {'chat_id': message.chat.id},
                {'$set': {'conected_to': other_user["chat"]["id"]}}
            )
            self.db.users.update_one(
                {'chat_id': other_user["chat"]["id"]},
                {'$set': {'conected_to': message.chat.id}}
            )

        @self.bot.message_handler(regexp=emoji.emojize(keys.exit))
        def exit(message):
            """
            Exit from chat or connecting state.
            """
            self.send_message(
                message.chat.id,
                keys.exit,
                reply_markup=keyboards.main
            )
            self.update_state(message.chat.id, states.main)

            # get connected to user
            connected_to = self.db.users.find_one(
                {'chat.id': message.chat.id}
            )
            if not connected_to:
                return

            # update connected to user state and terminate the connection
            other_chat_id = connected_to['connected_to']
            self.update_state(other_chat_id, states.main)
            self.send_message(
                other_chat_id,
                keys.exit,
                reply_markup=keyboards.main
            )

            # remove connected users
            self.db.users.update_one(
                {'chat.id': message.chat.id},
                {'$set': {'connected_to': None}}
            )
            self.db.users.update_one(
                {'chat.id': other_chat_id},
                {'$set': {'connected_to': None}}
            )
    
        @self.bot.message_handler(is_admin=True)
        def admin_of_group(message):
            self.send_message(message.chat.id, 
            '<strong>You are admin of this group!</strong>'
        )    
  
        @self.bot.message_handler(func=lambda m: True)
        def echo(message):
            user = self.db.users.find_one(
                {'chat.id': message.chat.id}
            )

            if (
                ((not user) or user['state'] != states.connected) or (user['connected_to'] is None)
            ):
                return

            self.send_message(
                user['connected_to'],
                message.text,
            )   
    
    def send_message(self, chat_id, text, reply_markup=None, emojize=True):
        """
        send message to telegram bot
        """
        if emojize:
            text = emoji.emojize(text)
        self.bot.send_message(chat_id, text, reply_markup=reply_markup)

    def update_state(self, chat_id, state):
        """
        Update user state.
        """
        self.db.users.update_one(
            {'chat.id': chat_id},
            {'$set': {'state': state}}
        )


if __name__=='__main__':
    logger.info('bot starts...')
    bot = Bot(telebot=bot)
    bot.run()
