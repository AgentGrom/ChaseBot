from telegram import error, Update, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, Message
from telegram.ext import (
    ContextTypes, 
)

from database_add_data import add_user

from main_vars import (
    EXIT, 
    NAME,
    EMAIL, 
    AGE, 
    GENDER,
    REVERT, 
    SKIP,
    MAN, 
    WOMAN,
    )

standart_buttons = [
    ['пропустить', 'назад'],
    ['отмена']
]

revert_button = InlineKeyboardButton(text='Назад', callback_data=REVERT)
skip_button = InlineKeyboardButton(text='Пропустить', callback_data=SKIP)
exit_button = InlineKeyboardButton(text='Отмена', callback_data=EXIT)

gender_keyboard = [
    InlineKeyboardButton(text='Мужчина', callback_data=MAN),
    InlineKeyboardButton(text='Женщина', callback_data=WOMAN)
]

async def registration_start_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = update

    return await registration_start(data, context)


async def registration_start_skip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = update.callback_query
    await data.answer()

    return await registration_start(data, context)


async def registration_start(data: Update| CallbackQuery, context: ContextTypes.DEFAULT_TYPE):

    keyboard = InlineKeyboardMarkup(
            [[skip_button],
            [exit_button]]
        )

    last_message: Message = context.user_data.get("last_message")

    if not last_message: return EXIT

    await last_message.edit_reply_markup(
        reply_markup=None
    )

    message = await data.message.reply_text(
            "Введите имя:",
            reply_markup=keyboard
        )
    
    context.user_data["last_message"] = message

    return NAME

async def registration_start_reverted(data: Update| CallbackQuery, context: ContextTypes.DEFAULT_TYPE):
    keyboard = InlineKeyboardMarkup(
            [[skip_button],
            [exit_button]]
        )

    last_message: Message = context.user_data.get("last_message")

    if not last_message: return EXIT

    await last_message.delete()

    message = await data.message.reply_text(
            "Введите имя:",
            reply_markup=keyboard
        )
    
    context.user_data["last_message"] = message

    return NAME

async def registration_name_skip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = update.callback_query
    text = data.from_user.full_name
    await data.answer()

    return await registration_name(data, context, text)


async def registration_name_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = update
    text = data.message.text

    return await registration_name(data, context, text)

    
async def registration_name(data: Update | CallbackQuery, context: ContextTypes.DEFAULT_TYPE, text: str):
    context.user_data["name"] = text

    keyboard = InlineKeyboardMarkup(
            [[revert_button],
            [exit_button]]
        )

    last_message: Message = context.user_data.get("last_message")

    if not last_message: return EXIT

    await last_message.edit_text(
        text=f"Ваше имя: {text}",
        reply_markup=None
    )

    message = await data.message.reply_text(
            "Введите почту:",
            reply_markup=keyboard
        )
    
    context.user_data["last_message"] = message

    return EMAIL


async def registration_name_reverted(data: Update | CallbackQuery, context: ContextTypes.DEFAULT_TYPE):
    keyboard = InlineKeyboardMarkup(
            [[revert_button],
            [exit_button]]
        )

    last_message: Message = context.user_data.get("last_message")

    if not last_message: return EXIT

    await last_message.delete()

    message = await data.message.reply_text(
            "Введите почту:",
            reply_markup=keyboard
        )
    
    context.user_data["last_message"] = message

    return EMAIL

async def registration_email_revert(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = update.callback_query
    await data.answer()

    return await registration_start_reverted(data, context)

async def registration_email_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = update
    text = data.message.text

    return await registration_email(data, context, text)


async def registration_email(data: Update|CallbackQuery, context: ContextTypes.DEFAULT_TYPE, text: str):
    if text.count('@') == 1:
        context.user_data["email"] = text

        keyboard = InlineKeyboardMarkup(
            [[skip_button, revert_button],
            [exit_button]]
        )

        last_message: Message = context.user_data.get("last_message")

        if not last_message: return EXIT

        await last_message.edit_text(
            text=f"Ваша почта: {text}",
            reply_markup=None
        )

        message = await data.message.reply_text(
                "Введите свой возраст:",
                reply_markup=keyboard
            )
        
        context.user_data["last_message"] = message
        
        return AGE
    else:
        keyboard = InlineKeyboardMarkup(
            [[revert_button],
            [exit_button]]
        )

        last_message: Message = context.user_data.get("last_message")

        if not last_message: return EXIT

        await last_message.edit_text(
            text=f"Неверно введена почта\nПопробуйте ещё раз",
            reply_markup=None
        )

        message = await data.message.reply_text(
            "Введите почту:",
            reply_markup=keyboard
        )
    
        context.user_data["last_message"] = message

        return EMAIL


async def registration_email_reverted(data: Update|CallbackQuery, context: ContextTypes.DEFAULT_TYPE):
    cancel_button = InlineKeyboardButton(text='Назад', callback_data=EMAIL)

    keyboard = InlineKeyboardMarkup(
        [[skip_button, cancel_button],
        [exit_button]]
    )

    last_message: Message = context.user_data.get("last_message")

    if not last_message: return EXIT

    await last_message.delete()

    message = await data.message.reply_text(
            "Введите свой возраст:",
            reply_markup=keyboard
        )
    
    context.user_data["last_message"] = message
    
    return AGE

async def registration_age_revert(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = update.callback_query
    await data.answer()

    return await registration_name_reverted(data, context)

async def registration_age_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = update
    text = data.message.text

    return await registration_age(data, context, text)


async def registration_age_skip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = update.callback_query
    text = None
    await data.answer()

    return await registration_age(data, context, text)


async def registration_age(data: Update|CallbackQuery, context: ContextTypes.DEFAULT_TYPE, text: str):
    if text is None or (text.isnumeric() and 0 <= int(text) <= 150):
        if text: context.user_data["age"] = int(text)

        keyboard = InlineKeyboardMarkup(
                [gender_keyboard,
                [skip_button, revert_button],
                [exit_button]]
            )
        
        last_message: Message = context.user_data.get("last_message")

        if not last_message: return EXIT

        await last_message.edit_text(
            text=(f"Ваш возраст: {text}" if text else 'Возраст не известен'),
            reply_markup=None
        )

        message = await data.message.reply_text(
                "Выберите пол:",
                reply_markup=keyboard
            )
        
        context.user_data["last_message"] = message

        return GENDER
    else:
        last_message: Message = context.user_data.get("last_message")

        if not last_message: return EXIT

        await last_message.edit_text(
            text=f"Неверно введён возраст\n(Число от 0 до 150)\nПопробуйте ещё раз",
            reply_markup=None
        )

        keyboard = InlineKeyboardMarkup(
            [[skip_button, revert_button],
            [exit_button]]
        )

        message = await data.message.reply_text(
                "Введите свой возраст:",
                reply_markup=keyboard
            )
        
        context.user_data["last_message"] = message

        return AGE

async def registration_gender_revert(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = update.callback_query
    await data.answer()

    return await registration_email_reverted(data, context)

async def registration_gender_man(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = update.callback_query
    await data.answer()

    text = 'man'
    value = 'Мужчина'

    return await registration_gender(data, context, text, value)

async def registration_gender_woman(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = update.callback_query
    await data.answer()

    text = 'woman'
    value = 'Женщина'

    return await registration_gender(data, context, text, value)

async def registration_gender_skip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = update.callback_query
    await data.answer()

    text = None
    value = None

    return await registration_gender(data, context, text, value)


async def registration_gender(data: Update|CallbackQuery, context: ContextTypes.DEFAULT_TYPE, text: str|None, value:str|None):

    context.user_data["gender"] = text

    last_message: Message = context.user_data.get("last_message")

    if not last_message: return EXIT

    await last_message.edit_text(
        text=(f"Ваш пол: {value}" if value else 'Пол не известен'),
        reply_markup=None
    )

    message = await data.message.reply_text(
            "Регистрация завершена!"
    )

    del context.user_data["last_message"]

    await registration_end(
        telegram_id=data.from_user.id, 
        name=context.user_data.get('name'), 
        email=context.user_data.get("email"),
        age=context.user_data.get('age'),
        gender=context.user_data.get('gender')
    )

    return EXIT
    

async def stop_under_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = update.callback_query
    await data.answer()

    return await stop_under(data, context)


async def stop_under_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = update

    return await stop_under(data, context)


async def stop_under(data: Update, context: ContextTypes.DEFAULT_TYPE):
    last_message: Message = context.user_data.get("last_message")

    try:
        await last_message.edit_text(
            text='Хорошо, увидимся в следующий раз!',
            reply_markup=None
        )
    except error.BadRequest:
        pass

    context.user_data.clear()

    return EXIT
    

async def registration_end(telegram_id, name, email, age, gender):
    await add_user(
        telegram_id=telegram_id, 
        name=name, 
        email=email, 
        age=age, 
        gender=gender
    )