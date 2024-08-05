from telegram.ext import ConversationHandler
from enum import Enum

PROCENT_CONST = 0.00
SUMM_CONST = 500
BANK_CARD_CONST = '2202 2068 9877 1063'
BANK_NAME_CONST = 'Сбербанк'
CARD_OWNER_CONST = 'Екатерина З.'

REG_TRUE, REG_FALSE = range(2)

CANCEL = ConversationHandler.END
EXIT, START_REG = range(2, 4)

NAME, EMAIL, AGE, GENDER = range(4, 8)

REVERT, SKIP = range(8, 10)

MAN, WOMAN = range(10, 12)

MAKEORDER, CHATS, ORDERS, POSTWORK = range(12, 16)

WORK_MENU, CHANGE_PHOTOS, CHANGE_NAME, CHANGE_DESCRIPTION = range(16, 20) 
SEND_WORK_FORM = 20
WORK_EXIT = 21
ADD_PHOTO = 22
CHECKWORKS = 23
CHECK_MENU = 24
SEND_WORK_FORM_DESIGN = 25
SEND_WORK_FORM_DRESS = 26
CHAT_WITH_MENU = 27
ANSWER_TO = 28
CANCEL_ORDER = 29
PAY_ORDER = 30
PAY_ACCEPT = 31
PAY_CANCEL = 32
CONFIRM_PAY = 33
CONFIRM_ORDER = 34
CONFIRM_ORDER_FINALY = 35

GROUP_ID = -1002121660317
TOPICS = {
    26: 'новости',
    None: 'общение',
    23: 'дизайны',
    31: 'отзывы',
    135: 'работы'
}

BUTTON_NAMES = {
    MAKEORDER: '🛍 Сделать заказ 🛍',
    CHATS: '💬 Чаты 💬',
    ORDERS: '🛒 Заказы 🛒',
    POSTWORK: '💻 Выложить работу 💻',
    CHECKWORKS: '✅ Работы на модерации ✅'
}