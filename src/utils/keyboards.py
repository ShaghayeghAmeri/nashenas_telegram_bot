from telebot import types
import emoji


def create_keyboards(*keys, row_width=2, resize_keyboard=True):
    """
    create a key_board from a list of key
    """
    markup = types.ReplyKeyboardMarkup(
        row_width=row_width, 
        resize_keyboard=resize_keyboard
    )
    keys = map(emoji.emojize, keys)
    buttoms = map(types.KeyboardButton, keys)
    markup.add(*buttoms)

    return markup
