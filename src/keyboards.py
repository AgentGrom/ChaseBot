from telegram import (
    ReplyKeyboardMarkup, 
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton
) 

from app.models import RoleNames

from main_vars import (
    CHECKWORKS,
    MAKEORDER,
    CHATS,
    ORDERS,
    POSTWORK,
    CHANGE_PHOTOS,
    CHANGE_DESCRIPTION,
    CHANGE_NAME,
    SEND_WORK_FORM,
    EXIT,
    SEND_WORK_FORM_DESIGN,
    SEND_WORK_FORM_DRESS,
    WORK_EXIT,
    REVERT,
    WORK_MENU,
    ADD_PHOTO,
    BUTTON_NAMES
)

ChangePhotosKeyboard = ReplyKeyboardMarkup(
    [
        [
            KeyboardButton('Сохранить'),
            KeyboardButton('Отмена')
        ]
    ], resize_keyboard=True, one_time_keyboard=True
)

ChangePhotosStartKeyboard = ReplyKeyboardMarkup(
    [
        [
            KeyboardButton('Отмена')
        ],
    ], resize_keyboard=True, one_time_keyboard=True
)

ChangeNameKeyboard = ReplyKeyboardMarkup(
    [
        [
            KeyboardButton('Отмена')
        ],
    ], resize_keyboard=True, one_time_keyboard=True
)

PostWorkKeyboard = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('Изменить фото', callback_data=CHANGE_PHOTOS)
        ],
        [
            InlineKeyboardButton('Изменить название', callback_data=CHANGE_NAME)
        ],
        [
            InlineKeyboardButton('Изменить описание', callback_data=CHANGE_DESCRIPTION)
        ],
        [
            InlineKeyboardButton('Опубликовать', callback_data=SEND_WORK_FORM),
            InlineKeyboardButton('Отменить', callback_data=WORK_EXIT)
        ],
    ]
)

PostWorkAdminKeyboard = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('Изменить фото', callback_data=CHANGE_PHOTOS)
        ],
        [
            InlineKeyboardButton('Изменить название', callback_data=CHANGE_NAME)
        ],
        [
            InlineKeyboardButton('Изменить описание', callback_data=CHANGE_DESCRIPTION)
        ],
        [
            InlineKeyboardButton('Опубликовать в Дизайны', callback_data=SEND_WORK_FORM_DESIGN)
        ],
        [
            InlineKeyboardButton('Опубликовать в Работы', callback_data=SEND_WORK_FORM_DRESS)
        ],
        [
            InlineKeyboardButton('Отменить', callback_data=WORK_EXIT)
        ]
    ]
)

PostWorkKeyboardExit = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('Вернуться', callback_data=WORK_MENU),
            InlineKeyboardButton('Удалить', callback_data=EXIT)
        ],
    ]
)

CheckWorksKeyboard = ReplyKeyboardMarkup(
    [
        [
            KeyboardButton('✅Принять'),
            KeyboardButton('❌Отказать')
        ],
        [
            KeyboardButton('↩️Выйти')
        ],
    ], resize_keyboard=True, one_time_keyboard=True
)

RoleKeyboard = {
    RoleNames.basic: ReplyKeyboardMarkup([
        [
            KeyboardButton(BUTTON_NAMES[MAKEORDER])
        ],
        # [
        #     KeyboardButton(BUTTON_NAMES[CHATS]),
        #     KeyboardButton(BUTTON_NAMES[ORDERS])
        # ],
    ], resize_keyboard=True, one_time_keyboard=True ),

    RoleNames.designer: ReplyKeyboardMarkup([
        [
            KeyboardButton(BUTTON_NAMES[POSTWORK])
        ],
        [
            KeyboardButton(BUTTON_NAMES[MAKEORDER])
        ]
        # [
        #     KeyboardButton(BUTTON_NAMES[CHATS]),
        #     KeyboardButton(BUTTON_NAMES[ORDERS])
        # ],
    ], resize_keyboard=True, one_time_keyboard=True ),

    RoleNames.dressmaker: ReplyKeyboardMarkup([
        [
            KeyboardButton(BUTTON_NAMES[POSTWORK])
        ],
        [
            KeyboardButton(BUTTON_NAMES[MAKEORDER])
        ]
        # [
        #     KeyboardButton(BUTTON_NAMES[CHATS]),
        #     KeyboardButton(BUTTON_NAMES[ORDERS])
        # ],
    ], resize_keyboard=True, one_time_keyboard=True ),

    RoleNames.administrator: ReplyKeyboardMarkup([
        [
            KeyboardButton(BUTTON_NAMES[POSTWORK])
        ],
        [
            KeyboardButton(BUTTON_NAMES[CHECKWORKS])
        ],
        # [
        #     KeyboardButton(BUTTON_NAMES[CHATS]),
        #     KeyboardButton(BUTTON_NAMES[ORDERS])
        # ],
    ], resize_keyboard=True, one_time_keyboard=True )
}