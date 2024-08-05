from telegram import error, Update, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, Message
from telegram.ext import (
    ContextTypes, 
)

from database_get_data import check_registered_user
from database_create import clear_users

from menu_funcs import menu_start

from main_vars import REG_TRUE, REG_FALSE, CANCEL, EXIT, START_REG

async def get_data(update: Update):
    if update.callback_query: 
        data = update.callback_query
        await data.answer()
    else: 
        data = update
    
    return data

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    last_message: Message = context.user_data.get("last_message")

    try:
        await last_message.edit_text(
            text='Хорошо, увидимся в следующий раз!',
            reply_markup=None
        )
    except (error.BadRequest, AttributeError):
        pass

    context.user_data.clear()

    return CANCEL

async def registration_false(data: CallbackQuery|Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = InlineKeyboardMarkup(
        [
            [
            InlineKeyboardButton(text='Начать', callback_data=START_REG), 
            InlineKeyboardButton(text='Отмена', callback_data=EXIT)
            ]
        ]
    )

    message = await data.message.reply_text(
            "Пожалуйста зарегистрируйтесь!",
            reply_markup=keyboard
        )
    
    context.user_data["last_message"] = message

    return REG_FALSE


async def registration_true(data: CallbackQuery|Update, context: ContextTypes.DEFAULT_TYPE):   
    context.user_data['registraion'] = True 
    await menu_start(data, context)

    return REG_TRUE


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = await get_data(update)

    telegram_id = data.message.from_user.id

    last_message: Message = context.user_data.get("last_message")

    try:
        if last_message: 
            await last_message.delete()
    except error.BadRequest:
        pass

    context.user_data.clear()

    if await check_registered_user(telegram_id): 
        return await registration_true(data, context)
    return await registration_false(data, context)

async def clear_all_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await clear_users()
    await update.message.reply_text(
            "Все очищены!"
        )
    
async def set_registered_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get('registraion') is None:
        context.user_data['registraion'] = bool(await check_registered_user(update.message.from_user.id)) 