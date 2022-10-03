from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


TextButtonList = {
    'profile': '👤 Profile',
    'subscribers': '🎟️ Subscriptions',
    'add_product': '➕ Add a product',
    'about': '❔ About the service',
    'feedback': '📮 Feedback',
    'info_users': '🔔 User Information'
}

ButtonList = dict()

for key in TextButtonList.keys():
    ButtonList[key] = KeyboardButton(TextButtonList[key])

user = ReplyKeyboardMarkup(resize_keyboard=True)\
    .add(ButtonList['add_product'])\
    .add(ButtonList['profile'])\
    .insert(ButtonList['subscribers'])\
    .add(ButtonList['about'])\
    .insert(ButtonList['feedback'])

admin = ReplyKeyboardMarkup(resize_keyboard=True)\
    .add(ButtonList['add_product'])\
    .add(ButtonList['profile'])\
    .insert(ButtonList['subscribers'])\
    .add(ButtonList['about'])\
    .insert(ButtonList['feedback'])\
    .add(ButtonList['info_users'])
