from telegram.ext import (
    CommandHandler, 
    ConversationHandler, 
    MessageHandler, 
    filters,
    CallbackQueryHandler,
)

from main_vars import (
    REG_FALSE,
    REG_TRUE,
    EXIT
)

from main_funcs import start, stop, set_registered_status
from menu_handles import menu_handle
from registration_handles import registration_handle

check_register_handle = [
        CommandHandler("start", start),
        registration_handle,

    ]

check_register_handle1 = ConversationHandler(
    entry_points=[
        CommandHandler("start", start),
        MessageHandler(filters.TEXT & ~filters.COMMAND, start)
        ],
    states={
        REG_FALSE: [registration_handle],
        REG_TRUE: menu_handle,
    },
    fallbacks=[
        CommandHandler('stop', stop),
        CallbackQueryHandler(stop, pattern=f'^{EXIT}$')],
    allow_reentry=True
)

set_registered_status_handle = MessageHandler(filters.TEXT, set_registered_status)