from telegram.ext import (
    CommandHandler, 
    ConversationHandler, 
    MessageHandler, 
    filters,
    CallbackQueryHandler
)

from registration_funcs import (
    registration_age_revert,
    registration_age_skip,
    registration_age_text,
    registration_email_revert,
    registration_email_text,
    registration_gender_man,
    registration_gender_revert,
    registration_gender_skip,
    registration_gender_woman,
    registration_name_skip,
    registration_name_text,
    registration_start_skip,
    registration_start_text,
    stop_under_button,
    stop_under_command,
    
)

from main_vars import (
    CANCEL, 
    EXIT, 
    START_REG,
    NAME,
    EMAIL, 
    AGE, 
    GENDER,
    REVERT, 
    SKIP,
    MAN, 
    WOMAN,
    )

registration_handle = ConversationHandler(
    entry_points=[
        MessageHandler(
            filters.Regex("^Начать$") , registration_start_text
        ),
        CallbackQueryHandler(registration_start_skip, pattern=f"^{str(START_REG)}$")
                ],
    states={
        NAME: [
            MessageHandler(
                filters.TEXT & ~(filters.COMMAND), registration_name_text
            ),
            CallbackQueryHandler(registration_name_skip, pattern=f"^{SKIP}$"),
        ],
        EMAIL: [
            MessageHandler(
                filters.TEXT & ~(filters.COMMAND), registration_email_text
            ),
            CallbackQueryHandler(registration_email_revert, pattern=f"^{REVERT}$")
        ],
        AGE: [
            MessageHandler(
                filters.TEXT & ~(filters.COMMAND), registration_age_text
            ),
            CallbackQueryHandler(registration_age_skip, pattern=f"^{SKIP}$"),
            CallbackQueryHandler(registration_age_revert, pattern=f"^{REVERT}$")
        ],
        GENDER: [
            CallbackQueryHandler(registration_gender_man, pattern=f"^{MAN}$"),
            CallbackQueryHandler(registration_gender_woman, pattern=f"^{WOMAN}$"),
            CallbackQueryHandler(registration_gender_skip, pattern=f"^{SKIP}$"),
            CallbackQueryHandler(registration_gender_revert, pattern=f"^{REVERT}$"),
        ],
    },
    fallbacks=[
        CommandHandler('stop', stop_under_command),
        CallbackQueryHandler(stop_under_button, pattern=f'^{EXIT}$'),
        ],
    map_to_parent={
        EXIT: CANCEL
    },
    allow_reentry=True
)