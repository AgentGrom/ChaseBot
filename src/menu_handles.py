from telegram.ext import (
    MessageHandler, 
    filters, 
    ConversationHandler,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)

from telegram import Update

from database_add_data import all_forms_to_false
from menu_funcs import (
    accept_order_cost,
    all_forms_check,
    answer_to_exit,
    answer_to_start,
    answer_to_stop,
    cancel_order,
    cancel_order_cost,
    check_works_accept,
    check_works_denied,
    check_works_start,
    check_works_stop,
    clear_all_forms,
    clear_all_orders,
    confirm_order,
    confirm_order_finaly,
    confirm_order_pay,
    del_user,
    give_role,
    media_handler,
    pay_order_exit,
    pay_order_start,
    pay_order_stop,
    post_work_cancel_change_description,
    post_work_start_change_description,
    post_work_stop_change_description,
    send_works_admin_design,
    send_works_admin_dress,
    show_menu,
    show_channel_link,
    post_work_start,
    post_work_stop,
    post_work_stop_check,
    post_work_start_callback,
    post_work_send_form,
    post_work_start_change_photo,
    post_work_stop_change_photo,
    post_work_add_photos,
    show_menu_args,
    post_work_start_change_name,
    post_work_stop_change_name,
    post_work_cancel_change_photo,
    post_work_cancel_change_name,
    show_menu_args_cancel,
    show_menu_args_stop
)
from main_vars import (
    CANCEL_ORDER,
    CONFIRM_ORDER,
    CONFIRM_ORDER_FINALY,
    CONFIRM_PAY,
    MAKEORDER,
    CHATS,
    ORDERS,
    PAY_ACCEPT,
    PAY_CANCEL,
    PAY_ORDER,
    POSTWORK,
    EXIT,
    CANCEL,
    CHANGE_NAME,
    CHANGE_PHOTOS,
    WORK_MENU,
    WORK_EXIT,
    SEND_WORK_FORM,
    ADD_PHOTO,
    ANSWER_TO, 
    BUTTON_NAMES, 
    CHANGE_DESCRIPTION, 
    CHAT_WITH_MENU, 
    CHECK_MENU, 
    CHECKWORKS, 
    SEND_WORK_FORM_DESIGN, 
    SEND_WORK_FORM_DRESS
)

description_handle = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(post_work_start_change_description, pattern=f'{CHANGE_DESCRIPTION}'),
                ],
    states={
        CHANGE_DESCRIPTION:[]
    },
    fallbacks=[
        MessageHandler(filters.TEXT & ~filters.Regex('^Отмена$'), post_work_stop_change_description),
        MessageHandler(filters.Regex('^Отмена$'), post_work_cancel_change_description)
            ],
    map_to_parent={
        CANCEL: WORK_MENU
    },
) 

name_handle = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(post_work_start_change_name, pattern=f'{CHANGE_NAME}'),
                ],
    states={
        CHANGE_NAME:[]
    },
    fallbacks=[
        MessageHandler(filters.TEXT & ~filters.Regex('^Отмена$'), post_work_stop_change_name),
        MessageHandler(filters.Regex('^Отмена$'), post_work_cancel_change_name)
            ],
    map_to_parent={
        CANCEL: WORK_MENU
    },
) 

photo_handle = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(post_work_start_change_photo, pattern=f'{CHANGE_PHOTOS}'),
                ],
    states={
        ADD_PHOTO: 
        [
            MessageHandler(filters.PHOTO, post_work_add_photos)
        ],
    },
    fallbacks=[
        MessageHandler(filters.Regex('^Сохранить$'), post_work_stop_change_photo),
        MessageHandler(filters.Regex('^Отмена$'), post_work_cancel_change_photo)
            ],
    map_to_parent={
        CANCEL: WORK_MENU
    },
) 

post_work_handler = ConversationHandler(
    entry_points=[
        MessageHandler(filters.Regex(f'^{BUTTON_NAMES[POSTWORK]}$') , post_work_start),
                ],
    states={
        WORK_MENU: 
        [
            CallbackQueryHandler(post_work_start_callback, pattern=f'{WORK_MENU}'),
            CallbackQueryHandler(post_work_stop_check, pattern=f'{WORK_EXIT}'),
            CallbackQueryHandler(post_work_send_form, pattern=f'{SEND_WORK_FORM}'),
            CallbackQueryHandler(send_works_admin_design, pattern=f'{SEND_WORK_FORM_DESIGN}'),
            CallbackQueryHandler(send_works_admin_dress, pattern=f'{SEND_WORK_FORM_DRESS}'),
            name_handle,
            photo_handle,
            description_handle
        ],
    },
    fallbacks=[
        CallbackQueryHandler(post_work_stop, pattern=f'{EXIT}'),
        ],
    map_to_parent={
        EXIT: CANCEL
    },
)

check_work_handler = ConversationHandler(
    entry_points=[
        MessageHandler(filters.Regex(f'^{BUTTON_NAMES[CHECKWORKS]}$') , check_works_start),
                ],
    states={
        CHECK_MENU: 
        [
            MessageHandler(filters.Regex(f'^✅Принять$') , check_works_accept),
            MessageHandler(filters.Regex(f'^❌Отказать$') , check_works_denied),
            MessageHandler(filters.TEXT & ~(filters.Regex(f'^(✅Принять)|(❌Отказать)|(↩️Выйти)$') | filters.COMMAND), check_works_start)
        ],
    },
    fallbacks=[
        MessageHandler(filters.Regex(f'^↩️Выйти$') , check_works_stop),
        MessageHandler(filters.TEXT & ~(filters.Regex(f'^(✅Принять)|(❌Отказать)|(↩️Выйти)$') | filters.COMMAND), check_works_start)
        ],
    map_to_parent={
        EXIT: CANCEL
    },
)

chat_with_handler = ConversationHandler(
    entry_points=[
        CommandHandler(['start'], show_menu_args, has_args=True)
                ],
    states={
        CHAT_WITH_MENU: [
        ],
    },
    fallbacks=[
        MessageHandler(filters.Regex(f'^↩️Выйти$') , show_menu_args_cancel),
        MessageHandler(~filters.Regex(f'^↩️Выйти$') , show_menu_args_stop)
        ],
    map_to_parent={
        EXIT: CANCEL
    },
)

answer_to_handler = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(answer_to_start, pattern=f'{ANSWER_TO}.*')
                ],
    states={
        CHAT_WITH_MENU: [
        ],
    },
    fallbacks=[
        MessageHandler(filters.Regex(f'^↩️Выйти$') , answer_to_exit),
        MessageHandler(~filters.Regex(f'^↩️Выйти$') , answer_to_stop)
        ],
    map_to_parent={
        EXIT: CANCEL
    },allow_reentry=True
)

pay_order_handler = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(pay_order_start, pattern=f'{PAY_ORDER}.*'),
                ],
    states={
        CHAT_WITH_MENU: [
        ],
    },
    fallbacks=[
        MessageHandler(filters.Regex(f'^↩️Выйти$') , pay_order_exit),
        MessageHandler(~filters.Regex(f'^↩️Выйти$') , pay_order_stop)
        ],
    map_to_parent={
        EXIT: CANCEL
    },allow_reentry=True
)



menu_handle = [
    CommandHandler(['clear_orders'], clear_all_orders, has_args=False),
    CommandHandler(['clear_forms'], clear_all_forms, has_args=False),
    CommandHandler(['give_role'], give_role, has_args=True),
    CommandHandler(['all_forms_check'], all_forms_check, has_args=False),
    CommandHandler(['del_user'], del_user, has_args=True),
    chat_with_handler,
    CommandHandler(['start', 'help'], show_menu, has_args=False),
    MessageHandler(filters.Regex(f'^{BUTTON_NAMES[MAKEORDER]}$'), show_channel_link),
    answer_to_handler,
    pay_order_handler,
    CallbackQueryHandler(cancel_order, pattern=f'{CANCEL_ORDER}.*'),
    post_work_handler,
    check_work_handler,
    CallbackQueryHandler(accept_order_cost, pattern=f'{PAY_ACCEPT}.*'),
    CallbackQueryHandler(cancel_order_cost, pattern=f'{PAY_CANCEL}.*'),
    CallbackQueryHandler(confirm_order_pay, pattern=f'{CONFIRM_PAY}.*'),
    CallbackQueryHandler(confirm_order, pattern=f'{CONFIRM_ORDER}.*'),
    CallbackQueryHandler(confirm_order_finaly, pattern=f'{CONFIRM_ORDER_FINALY}.*')
]

# async def test(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     print(update.message)
#     print()
#     chat_id = -1002213633542
#     await context.bot.send_message(chat_id=chat_id,
#                              text=update.message.text,
#                              entities=update.message.entities)

# menu_handle = [
#     MessageHandler(filters.ALL, test)
# ]