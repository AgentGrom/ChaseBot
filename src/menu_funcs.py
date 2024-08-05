from telegram import (
    InputMedia,
    InputMediaDocument,
    InputMediaPhoto,
    KeyboardButton,
    LinkPreviewOptions,
    MessageEntity,
    ReplyKeyboardMarkup,
    Update, 
    InlineKeyboardButton, 
    InlineKeyboardMarkup,
    ReplyKeyboardRemove,
    Message,
    error
)

from telegram.ext import (
    ContextTypes
)

from database_create import clear_forms, clear_orders, clear_users
from database_add_data import add_check_works, add_create_order, add_form_status_return, add_new_user_role, add_user, all_forms_to_false, order_set_cost, order_set_status
from app.models import Order, OrderStatuses, RoleNames, WorkPostForm

from main_vars import (
    ANSWER_TO,
    BANK_CARD_CONST,
    BANK_NAME_CONST,
    CANCEL,
    CANCEL_ORDER,
    CARD_OWNER_CONST,
    CHANGE_DESCRIPTION,
    CHANGE_NAME,
    CHAT_WITH_MENU,
    CHECK_MENU,
    CONFIRM_ORDER,
    CONFIRM_ORDER_FINALY,
    CONFIRM_PAY,
    PAY_ACCEPT,
    PAY_CANCEL,
    PAY_ORDER,
    PROCENT_CONST,
    SUMM_CONST,
    WORK_MENU,
    EXIT,
    WORK_EXIT,
    ADD_PHOTO,
    GROUP_ID
)

from database_get_data import get_check_works, get_order, get_order_by_id, get_user_account_data, get_user_id_data, get_user_role_data, get_user_telegram_id_data

from keyboards import (
    ChangeNameKeyboard,
    CheckWorksKeyboard,
    PostWorkAdminKeyboard,
    RoleKeyboard, 
    PostWorkKeyboard, 
    PostWorkKeyboardExit, 
    ChangePhotosKeyboard,
    ChangePhotosStartKeyboard
)

def js_len(stroke: str) -> int:
    return len(stroke.encode('utf_16_le'))//2

def final_sum(summ):
    new_summ = summ * (1 + PROCENT_CONST)
    new_summ += SUMM_CONST

    new_summ = new_summ//10*10

    if new_summ < summ: new_summ = (summ + 10) // 10 * 10

    return int(new_summ)


def data_to_post_form(owner_id:int, 
                      name:str, 
                      description:str, 
                      photo1:str,
                      photo2:str|bool,
                      photo3:str|bool
                      ) -> tuple[int, list[InputMediaPhoto], str, list[MessageEntity]]:
    
    caption = f'{name}\n\n{description}\n\nЗаказать'

    caption_entities = [
        MessageEntity(
            MessageEntity.BOLD, 
            offset=0, 
            length=js_len(name)
        ),
        MessageEntity(
            MessageEntity.TEXT_LINK, 
            offset=js_len(name)+js_len(description)+4, 
            length=len('Заказать'),
            url=f't.me/Chase_Market_Bot?start={owner_id}'
        )
    ]

    media = [InputMediaPhoto(photo1)]
    if photo2: media.append(InputMediaPhoto(photo2))
    if photo3: media.append(InputMediaPhoto(photo3))

    chat_id=GROUP_ID

    return chat_id, media, caption, caption_entities

def message_check(func):
    async def wrapper(*args, **kwargs):
        update: Update = args[0]
        context: ContextTypes.DEFAULT_TYPE = args[1]

        if update.message.chat.type != 'private': return

        telegram_id = update.message.from_user.id
        print(telegram_id)
        permission = await get_user_role_data(telegram_id)

        if not permission: 
            await add_user(telegram_id, update.message.from_user.full_name)
            permission = await get_user_role_data(telegram_id)
        
        context.user_data['permission'] = permission

        return await func(*args, **kwargs)
    return wrapper

def callback_message_check(func):
    async def wrapper(*args, **kwargs):
        update: Update = args[0]
        context: ContextTypes.DEFAULT_TYPE = args[1]

        if update.callback_query.message.chat.type != 'private': return

        telegram_id = update.callback_query.message.chat.id
        print(telegram_id)
        permission = await get_user_role_data(telegram_id)

        context.user_data['permission'] = permission  

        return await func(*args, **kwargs)
    return wrapper

async def beautiful_print(data, tabs=0):
    for key, val in data.items():
        if type(val) == dict: 
            print(' '*tabs + f'{key}:')
            await beautiful_print(val, tabs+2)
        else:
            print(' '*tabs + f'{key}: {val}')

async def log_message(context:ContextTypes.DEFAULT_TYPE, from_user:int, to_user:int, order_id:int):

    chat_id = -1002213633542

    from_user_id = await context.bot.get_chat(int(await get_user_telegram_id_data(from_user)))
    to_user_id = await context.bot.get_chat(int(await get_user_telegram_id_data(to_user)))

    # print(from_user_id.username)
    # print(to_user_id.username)

    if context.user_data.get('media_group'):
        media_group = [x.copy() for x in context.user_data.get('media_group')]

        if media_group[0][1] is None: media_group[0][1] = ''
        media_group[0][1] += f'\n\n@{from_user_id.username} -> @{to_user_id.username}\n#Заказ_{order_id}'
        media_group = [InputMediaPhoto(photo, caption) for photo, caption in media_group]

        await context.bot.send_media_group(chat_id=chat_id,
                                        media=media_group)
        return
    
    if context.user_data.get('documents'):
        documents = [x.copy() for x in context.user_data.get('documents')]

        if documents[0][1] is None: documents[0][1] = ''
        caption = documents[0][1] + f'\n\n@{from_user_id.username} -> @{to_user_id.username}\n#Заказ_{order_id}'

        new_documents = [InputMediaDocument(document, None) for document, _ in documents[:-1:]]
        new_documents.append(InputMediaDocument(documents[-1][0], caption))

        await context.bot.send_media_group(chat_id=chat_id,
                                        media=new_documents)
        return
    
    text = context.user_data.get('text')
    if text is None: text = ''

    text += f'\n\n@{from_user_id.username} -> @{to_user_id.username}\n#Заказ_{order_id}'
    await context.bot.send_message(chat_id=chat_id,
                                   text=text)

@message_check
async def clear_all_orders(update: Update, context: ContextTypes.DEFAULT_TYPE):
    permission = context.user_data['permission']
    if permission != RoleNames.administrator: return

    await clear_orders()

    await update.message.reply_text(
        f'Все заказы удалены из базы данных'
    )

@message_check
async def clear_all_forms(update: Update, context: ContextTypes.DEFAULT_TYPE):
    permission = context.user_data['permission']
    if permission != RoleNames.administrator: return

    await clear_forms()

    await update.message.reply_text(
        f'Все посты удалены из базы данных'
    )

@message_check
async def give_role(update: Update, context: ContextTypes.DEFAULT_TYPE):
    permission = context.user_data['permission']
    if permission != RoleNames.administrator and update.message.chat.id != 907106596: return
    if len(context.args) != 2: return

    telegram_id = int(context.args[0])
    new_role = int(context.args[1])

    ## Может сломаться при добавлении ролей!
    if new_role < 0 or new_role > len(list(RoleNames))-1: return

    await add_new_user_role(telegram_id, new_role+1)

    await update.message.reply_text(
        f'Пользователю {telegram_id} выдана роль {list(RoleNames)[new_role].name}'
    )

@message_check
async def all_forms_check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    permission = context.user_data['permission']
    if permission != RoleNames.administrator: return

    await all_forms_to_false()

    await update.message.reply_text(
        f'Все посты обновлены'
    )

@message_check
async def del_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    permission = context.user_data['permission']
    if permission != RoleNames.administrator: return

    for id in context.args:
        await clear_users(int(id))

        await update.message.reply_text(
            f'Пользователь {id} удалён'
        )

@message_check
async def show_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    permission = context.user_data['permission']

    # await add_new_user_role(907106596, 5)
    # await beautiful_print(update.to_dict())

    await update.message.reply_text(
        'Выберете пункт меню',
        reply_markup=RoleKeyboard[permission]
    )

@message_check
async def show_menu_args(update: Update, context: ContextTypes.DEFAULT_TYPE):
    permission = context.user_data['permission']
    
    # await beautiful_print(update.to_dict())

    from_user = int(await get_user_id_data(update.message.from_user.id))
    to_user = int(context.args[0])

    role = await get_user_role_data(int(await get_user_telegram_id_data(to_user)))

    if from_user == to_user:
        await update.message.reply_text(
            f'Вы не можете заказать у себя самого', 
        )
        return await show_menu_args_cancel(update, context)
    
    if role == RoleNames.basic: 
        await update.message.reply_text(
            f'Данный пользователь больше не выполняет услуги. '
            'Попоробуйте сделать заказ у кого-то ещё', 
        )
        return await show_menu_args_cancel(update, context)
    
    if (order:=await get_order(from_user, to_user, statuses=[OrderStatuses.new, OrderStatuses.on_payment])) != None:
        kb = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(text=f'Ответить по Заказу {order[0].id}', callback_data=f'{ANSWER_TO}.{order[0].id}')
                ],
                [
                    InlineKeyboardButton(text=f'Отменить Заказ {order[0].id}', callback_data=f'{CANCEL_ORDER}.{order[0].id}')
                ]
            ]
        )

        await update.message.reply_text(
            f'Вы не можете создать новый заказ у этого '
            f'пользователя, не завершив предыдущий:\n'
            f'#Заказ_{order[0].id}', 
            reply_markup=kb
        )
        return await show_menu_args_cancel(update, context)
        
    kb  = ReplyKeyboardMarkup(
        [
            [
                KeyboardButton('↩️Выйти')
            ],
        ], resize_keyboard=True, one_time_keyboard=True
    )

    await update.message.reply_text(
        'Одним сообщением, максимально опишите свой заказ. '
        'Прикрепите изображения, укажите размеры, '
        'цветовую палитру, материал, личные предпочтения. ', 
        reply_markup=kb
    )

    context.user_data['to_user'] = to_user

    return CHAT_WITH_MENU

@message_check
async def show_menu_args_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get('to_user'): del context.user_data['to_user']

    await show_menu(update, context)

    return EXIT

@message_check
async def show_menu_args_stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if 'media_group' not in context.user_data: context.user_data['media_group'] = []
    if 'documents' not in context.user_data: context.user_data['documents'] = []
    try:
        await context.bot.edit_message_text(text=' ', chat_id=update.message.chat.id, message_id=update.message.message_id + 1)
    except error.BadRequest as exc:
            if (exc.message != "Message must be non-empty" and
                    exc.message != "Message to edit not found"):
                if update.message.photo and len(context.user_data['media_group']) < 10: 
                    context.user_data['media_group'].append([update.message.photo[0].file_id, update.message.caption])
                if update.message.document and len(context.user_data['documents']) < 10: 
                    context.user_data['documents'].append([update.message.document.file_id, update.message.caption])
                return CHAT_WITH_MENU

    from_user = int(await get_user_id_data(update.message.from_user.id))
    to_user = context.user_data['to_user']

    await add_create_order(from_user, to_user)

    order_id = int((await get_order(from_user, to_user, [OrderStatuses.new]))[0].id)

    if update.message.photo and len(context.user_data['media_group']) < 10:
        context.user_data['media_group'].append([update.message.photo[0].file_id, update.message.caption])
    elif update.message.document and len(context.user_data['documents']) < 10: 
        context.user_data['documents'].append([update.message.document.file_id, update.message.caption])
    else:
        context.user_data['text'] = update.message.text

    await log_message(context, from_user, to_user, order_id)

    await answer_to(context, from_user, to_user, order_id)

    await update.message.reply_text(
        'Заказ отправлен! Ожидайте ответа',
    )

    if context.user_data.get('text'): del context.user_data['text']
    if context.user_data.get('media_group'): del context.user_data['media_group']
    if context.user_data.get('documents'): del context.user_data['documents']
    if context.user_data.get('to_user'): del context.user_data['to_user']
    
    await show_menu(update, context)

    return EXIT

@message_check
async def show_menu_args_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get('to_user'): del context.user_data['to_user']

    await show_menu(update, context)

    return EXIT

@callback_message_check
async def cancel_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    order_id = int(update.callback_query.data.split('.')[-1])

    order = await get_order_by_id(order_id)
    await update.callback_query.answer()

    if order.status == OrderStatuses.in_progress: 
        await update.callback_query.message.reply_text(
            text=f'Нельзя отменить заказ в процессе его выполнения'
        ) 
        return
    if order.status == OrderStatuses.on_payment: 
        await update.callback_query.message.reply_text(
            text=f'Нельзя отменить заказ в процессе его оплаты'
        ) 
        return
    if order.status != OrderStatuses.new: 
        await update.callback_query.message.reply_text(
            text=f'Заказ уже завершён'
        ) 
        return

    await order_set_status(order_id, OrderStatuses.canceled)
    
    from_user = int(await get_user_id_data(update.callback_query.from_user.id))

    if from_user == order.buyer_id: to_user = order.contractor_id
    else:                           to_user = order.buyer_id

    await update.callback_query.message.reply_text(
        text=f'#Заказ_{order_id} отменён по вашему запросу'
    ) 

    await context.bot.send_message(chat_id=int(await get_user_telegram_id_data(to_user)), 
                                   text=f'#Заказ_{order_id} отменён по решению другой стороны')

@message_check
async def show_channel_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        'Для оформлени заказа перейди в наш канал (Кнопка снизу), выбери раздел Дизаны или Работы, а после нажми "Заказать" под понравившейся работой',
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(text='Вперёд', url='t.me/chase_clth')]]
        )
    )

@message_check
async def media_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.media_group_id is None or update.message.caption: return
    if func:=context.user_data['media_group_do']: await func[0](*func[1:], update.message)

@message_check
async def post_work_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    permission = context.user_data['permission']

    if permission == RoleNames.basic: return CANCEL

    message = await update.message.reply_text(
        '.',
        reply_markup=ReplyKeyboardRemove()
    )

    await message.delete()

    name = context.user_data.get('name')
    if name is None: name = '**Название**'

    description = context.user_data.get('description')
    if description is None: description = '**Описание**'

    caption = f"""{name}"""

    entity = [MessageEntity(
        MessageEntity.BOLD, 
        offset=0, 
        length=js_len(caption)
    )]


    caption += f"""\n\n{description}"""

    telegram_id = update.message.from_user.id


    entity += [MessageEntity(
        MessageEntity.TEXT_LINK, 
        offset=js_len(caption)+2, 
        length=8,
        url=f't.me/Chase_Market_Bot?start={telegram_id}'
    )]
    
    caption += """\n\nЗаказать"""


    if context.user_data.get('photos'):
        message = await update.message.reply_media_group(
            media=[InputMediaPhoto(x) for x in context.user_data.get('photos')],
            caption=caption,
            caption_entities=[MessageEntity(
                MessageEntity.BOLD, 
                offset=0, 
                length=js_len(name)
            )]
        )
    else:
        message = await update.message.reply_text(
            caption,
            link_preview_options=LinkPreviewOptions(is_disabled=True),
            entities=[MessageEntity(
                MessageEntity.BOLD, 
                offset=0, 
                length=js_len(name)
            )]
        )
    reply_markup=PostWorkKeyboard
    if permission == RoleNames.administrator: reply_markup=PostWorkAdminKeyboard

    await update.message.reply_text(
        'Выберете действие:',
        reply_markup=reply_markup,
    )

    return WORK_MENU

@callback_message_check
async def post_work_start_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    permission = context.user_data['permission']

    if permission == RoleNames.basic: return CANCEL

    await update.callback_query.answer()

    message: Message = update.callback_query.message

    await message.edit_text(
        'Ваше сообщение:',
        reply_markup=PostWorkKeyboard
    )

    if context.user_data.get('photos'):

        await message.edit_media(
            media=InputMedia(
                type='photo',
                media=context.user_data['photos'][0].file_id
                )
            )

    return WORK_MENU

@callback_message_check
async def post_work_stop_check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    permission = context.user_data['permission']

    if permission == RoleNames.basic: return EXIT

    await update.callback_query.answer(
        text='Данные будут не сохранены!',
        show_alert=True
    )

    message: Message = update.callback_query.message

    await message.edit_text(
        'Вы уверены?',
        reply_markup=PostWorkKeyboardExit
    )

    return WORK_MENU

@callback_message_check
async def post_work_stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    permission = context.user_data['permission']

    if permission == RoleNames.basic: return EXIT

    await update.callback_query.answer()

    message: Message = update.callback_query.message

    await message.reply_text(
        'Запись удалена',
        reply_markup=RoleKeyboard[permission]
    )

    await message.delete()

    if context.user_data.get('photos'): del context.user_data['photos']
    if context.user_data.get('name'): del context.user_data['name']
    if context.user_data.get('description'): del context.user_data['description']

    return EXIT


@callback_message_check
async def post_work_send_form(update: Update, context: ContextTypes.DEFAULT_TYPE):
    permission = context.user_data['permission']

    if permission == RoleNames.basic: return EXIT

    message: Message = update.callback_query.message

    name = context.user_data.get('name')
    description = context.user_data.get('description')
    photos = context.user_data.get('photos')

    if name is None or description is None or photos is None:
        await update.callback_query.answer(
            'Заполните форму полность!',
            show_alert=True
        )

        return WORK_MENU
    
    await update.callback_query.answer()

    await message.reply_text(
        'Отправлено',
        reply_markup=RoleKeyboard[permission]
    )

    await message.delete()

    await add_check_works(update.callback_query.from_user.id, name, description, *photos)

    await context.bot.send_message(chat_id=-1002213633542, text=f'🆕 Появилась новая работа на модерацию')
    
    del context.user_data['photos']
    del context.user_data['name']
    del context.user_data['description']

    return EXIT

@message_check
async def post_work_stop_change_description(update: Update, context: ContextTypes.DEFAULT_TYPE):
    permission = context.user_data['permission']

    if permission == RoleNames.basic: return EXIT

    message: Message = update.message

    context.user_data['description'] = message.text

    await post_work_start(update, context)

    return CANCEL

@message_check
async def post_work_cancel_change_description(update: Update, context: ContextTypes.DEFAULT_TYPE):
    permission = context.user_data['permission']

    if permission == RoleNames.basic: return EXIT

    await post_work_start(update, context)

    return CANCEL

@callback_message_check
async def post_work_start_change_description(update: Update, context: ContextTypes.DEFAULT_TYPE):
    permission = context.user_data['permission']

    if permission == RoleNames.basic: return EXIT

    await update.callback_query.answer()

    message: Message = update.callback_query.message

    await message.reply_text(
        'Введите новое описание',
        reply_markup=ChangeNameKeyboard
    )

    await message.delete()

    return CHANGE_DESCRIPTION

@message_check
async def post_work_stop_change_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    permission = context.user_data['permission']

    if permission == RoleNames.basic: return EXIT

    message: Message = update.message

    context.user_data['name'] = message.text

    await post_work_start(update, context)

    return CANCEL

@message_check
async def post_work_cancel_change_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    permission = context.user_data['permission']

    if permission == RoleNames.basic: return EXIT

    await post_work_start(update, context)

    return CANCEL

@callback_message_check
async def post_work_start_change_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    permission = context.user_data['permission']

    if permission == RoleNames.basic: return EXIT

    await update.callback_query.answer()

    message: Message = update.callback_query.message


    await message.reply_text(
        'Введите новое название',
        reply_markup=ChangeNameKeyboard
    )

    await message.delete()

    return CHANGE_NAME


@callback_message_check
async def post_work_start_change_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    permission = context.user_data['permission']

    if permission == RoleNames.basic: return EXIT

    await update.callback_query.answer()

    message: Message = update.callback_query.message

    context.user_data['new_photos'] = []

    await message.reply_text(
        'Отправляйте фото\n(3 максимум)',
        reply_markup=ChangePhotosStartKeyboard
    )

    await message.delete()

    return ADD_PHOTO

@message_check
async def post_work_stop_change_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['photos'] = context.user_data['new_photos']
    del context.user_data['new_photos']

    await post_work_start(update, context)

    return CANCEL

@message_check
async def post_work_cancel_change_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    del context.user_data['new_photos']

    await post_work_start(update, context)

    return CANCEL


@message_check
async def post_work_add_photos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    permission = context.user_data['permission']

    if permission == RoleNames.basic: return EXIT

    message: Message = update.message
    
    context.user_data['new_photos'].append(message.photo[-1].file_id)

    if len(context.user_data["new_photos"]) == 3: 

        return await post_work_stop_change_photo(update, context)

    await message.reply_text(
        f'Добавлено фото { len(context.user_data["new_photos"]) }|3\n',
        reply_markup=ChangePhotosKeyboard
    )

    return ADD_PHOTO

@message_check
async def check_works_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    permission = context.user_data['permission']

    if permission != RoleNames.administrator: return EXIT

    form = await get_check_works()

    if form is None:
        await update.message.reply_text(
            'Форм для рассмотрения нет!',
            reply_markup=RoleKeyboard[permission]
        )

        return EXIT

    owner_id = form.owner_id
    name = form.name
    description = form.description
    photos = [form.photo1, form.photo2, form.photo3]

    tg_owner_id = await get_user_telegram_id_data(owner_id)
    owner_chat = await context.bot.get_chat(tg_owner_id)

    role = await get_user_role_data(tg_owner_id)

    _, media, caption, caption_entities = data_to_post_form(owner_id, name, description, *photos)

    context.user_data['form_owner_id'] = owner_id
    context.user_data['form'] = form
    context.user_data['form_role'] = role

    
    await update.message.reply_media_group(
            media=media,
            caption=caption,
            caption_entities=caption_entities[:-1:]
        )
    if role == RoleNames.designer: 
        text = f'Работа от Дизайнера @{owner_chat.username}'
    elif role == RoleNames.dressmaker:    
        text = f'Работа от Швеи @{owner_chat.username}'
    else:
        text = f'Работа от Админа @{owner_chat.username}'

    await update.message.reply_text(
            # 'Для отмены с комментарием, напишите его следующим сообщением',
            text,
            reply_markup=CheckWorksKeyboard
        )

    return CHECK_MENU

@message_check
async def check_works_accept(update: Update, context: ContextTypes.DEFAULT_TYPE):
    permission = context.user_data['permission']

    if permission == RoleNames.basic: return EXIT

    await send_form_to_topic(update, context)
    return await check_works_start(update, context)

@callback_message_check
async def send_works_admin_design(update: Update, context: ContextTypes.DEFAULT_TYPE):
    permission = context.user_data['permission']

    if permission == RoleNames.basic: return EXIT

    message: Message = update.callback_query.message

    name = context.user_data.get('name')
    description = context.user_data.get('description')
    photos = context.user_data.get('photos')

    if name is None or description is None or photos is None:
        await update.callback_query.answer(
            'Заполните форму полность!',
            show_alert=True
        )

        return WORK_MENU
    
    await update.callback_query.answer()

    await message.reply_text(
        'Отправлено',
        reply_markup=RoleKeyboard[permission]
    )

    await message.delete()

    photos += [None]*(3-len(photos))

    await add_check_works(update.callback_query.from_user.id, name, description, *photos, True)

    owner_id = int(await get_user_id_data(update.callback_query.from_user.id))

    form = WorkPostForm(owner_id=owner_id, 
                            name=name, 
                            description=description, 
                            photo1=photos[0], 
                            photo2=photos[1], 
                            photo3=photos[2])

    context.user_data['form_owner_id'] = owner_id
    context.user_data['form'] = form

    await send_form_to_topic(update, context, 23)

    del context.user_data['photos']
    del context.user_data['name']
    del context.user_data['description']
    del context.user_data['form_owner_id']
    del context.user_data['form']

    return EXIT

@callback_message_check
async def send_works_admin_dress(update: Update, context: ContextTypes.DEFAULT_TYPE):
    permission = context.user_data['permission']

    if permission == RoleNames.basic: return EXIT

    message: Message = update.callback_query.message

    name = context.user_data.get('name')
    description = context.user_data.get('description')
    photos = context.user_data.get('photos')

    if name is None or description is None or photos is None:
        await update.callback_query.answer(
            'Заполните форму полность!',
            show_alert=True
        )

        return WORK_MENU
    
    await update.callback_query.answer()

    await message.reply_text(
        'Отправлено',
        reply_markup=RoleKeyboard[permission]
    )

    await message.delete()

    photos += [None]*(3-len(photos))

    await add_check_works(update.callback_query.from_user.id, name, description, *photos, True)

    owner_id = int(await get_user_id_data(update.callback_query.from_user.id))

    form = WorkPostForm(owner_id=owner_id, 
                            name=name, 
                            description=description, 
                            photo1=photos[0], 
                            photo2=photos[1], 
                            photo3=photos[2])

    context.user_data['form_owner_id'] = owner_id
    context.user_data['form'] = form

    await send_form_to_topic(update, context, 135)

    del context.user_data['photos']
    del context.user_data['name']
    del context.user_data['description']
    del context.user_data['form_owner_id']
    del context.user_data['form']

    return EXIT

async def send_form_to_topic(update: Update, context: ContextTypes.DEFAULT_TYPE, message_thread_id=None):

    owner_id = context.user_data['form_owner_id']
    
    form = context.user_data['form']

    name = form.name
    description = form.description
    photos = [form.photo1, form.photo2, form.photo3]

    chat_id, media, caption, caption_entities = data_to_post_form(owner_id, name, description, *photos)

    if message_thread_id is None and context.user_data['form_role'] == RoleNames.designer: message_thread_id = 23
    elif message_thread_id is None and context.user_data['form_role'] == RoleNames.dressmaker: message_thread_id = 135

    await context.bot.send_media_group(chat_id=chat_id,
                                message_thread_id=message_thread_id,
                                media=media,
                                caption=caption,
                                caption_entities=caption_entities
                                )

@message_check
async def check_works_denied(update: Update, context: ContextTypes.DEFAULT_TYPE):
    permission = context.user_data['permission']

    if permission == RoleNames.basic: return EXIT

    return await check_works_start(update, context)
    

@message_check
async def check_works_stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    permission = context.user_data['permission']

    if permission == RoleNames.basic: return EXIT

    await update.message.reply_text(
            'Выберете пункт меню',
            reply_markup=RoleKeyboard[permission]
        )

    await add_form_status_return(context.user_data['form'].id)

    del context.user_data['form_owner_id']
    del context.user_data['form']

    return EXIT

async def answer_to(context: ContextTypes.DEFAULT_TYPE, from_user: int, to_user: int, order_id: int):

    to_user_id = int(await get_user_telegram_id_data(to_user))

    # print(from_user_id.username)
    # print(to_user_id.username)

    if context.user_data.get('media_group'):
        media_group = [x.copy() for x in context.user_data.get('media_group')]

        if media_group[0][1] is None: media_group[0][1] = ''
        media_group[0][1] += f'\n\n#Заказ_{order_id}'

        media_group = [InputMediaPhoto(photo, caption) for photo, caption in media_group]

        await context.bot.send_media_group(chat_id=to_user_id,
                                        media=media_group)
    elif context.user_data.get('documents'):
        documents = [x.copy() for x in context.user_data.get('documents')]

        if documents[0][1] is None: documents[0][1] = ''
        caption = documents[0][1] + f'\n\n#Заказ_{order_id}'


        new_documents = [InputMediaDocument(document, None) for document, _ in documents[:-1:]]
        new_documents.append(InputMediaDocument(documents[-1][0], caption))

        await context.bot.send_media_group(chat_id=to_user_id,
                                        media=new_documents)
    else:
        text = context.user_data.get('text')
        if text is None: text = ''

        text += f'\n\n#Заказ_{order_id}'

        await context.bot.send_message(chat_id=to_user_id,
                                    text=text)
    
    order = await get_order_by_id(order_id)
    btns = [[InlineKeyboardButton(text=f'Ответить', callback_data=f'{ANSWER_TO}.{order_id}')]]
    if order.status == OrderStatuses.new:
        btns.append([InlineKeyboardButton(text=f'Отменить Заказ', callback_data=f'{CANCEL_ORDER}.{order_id}')])
        if order.contractor_id == to_user: btns.append([InlineKeyboardButton(text=f'Запросить Оплату', callback_data=f'{PAY_ORDER}.{order_id}')])
    if order.status == OrderStatuses.in_progress and order.buyer_id == to_user:
        btns.append([InlineKeyboardButton(text=f'Подтвердить выполнение заказа', callback_data=f'{CONFIRM_ORDER_FINALY}.{order_id}')])


    kb = InlineKeyboardMarkup(btns)
    
    await context.bot.send_message(chat_id=to_user_id,
                                   text=f'⬆️ Новое сообщение ⬆️ \nПо заказу №{order_id}', 
                                   reply_markup=kb)

@callback_message_check
async def answer_to_start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    message: Message = update.callback_query.message

    order_id = int(update.callback_query.data.split('.')[-1])

    order = await get_order_by_id(order_id)
    await update.callback_query.answer()

    if order.status in [OrderStatuses.canceled, OrderStatuses.finished]: 
        await update.callback_query.message.reply_text(
            text=f'Заказ уже завершён'
        ) 
        return EXIT

    context.user_data['order_id'] = order_id

    kb = ReplyKeyboardMarkup(
        [
            [
                KeyboardButton('↩️Выйти')
            ],
        ], resize_keyboard=True, one_time_keyboard=True
    )

    await update.callback_query.answer()
    await message.reply_text('Введите ответ :', reply_markup=kb)
    return CHAT_WITH_MENU

@message_check    
async def answer_to_stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if 'media_group' not in context.user_data: context.user_data['media_group'] = []
    if 'documents' not in context.user_data: context.user_data['documents'] = []
    
    try:
        await context.bot.edit_message_text(text=' ', chat_id=update.message.chat.id, message_id=update.message.message_id + 1)
    except error.BadRequest as exc:
            if (exc.message != "Message must be non-empty" and
                    exc.message != "Message to edit not found"):
                if update.message.photo and len(context.user_data['media_group']) < 10: 
                    context.user_data['media_group'].append([update.message.photo[0].file_id, update.message.caption])
                if update.message.document and len(context.user_data['documents']) < 10: 
                    context.user_data['documents'].append([update.message.document.file_id, update.message.caption])
                return CHAT_WITH_MENU

    from_user = int(await get_user_id_data(update.message.from_user.id))
    order_id = context.user_data['order_id']

    order = await get_order_by_id(order_id)

    to_user = int(order.buyer_id if order.contractor_id == from_user else order.contractor_id)

    if update.message.photo and len(context.user_data['media_group']) < 10:
        context.user_data['media_group'].append([update.message.photo[0].file_id, update.message.caption])
    elif update.message.document and len(context.user_data['documents']) < 10:
        context.user_data['documents'].append([update.message.document.file_id, update.message.caption])
    else:
        context.user_data['text'] = update.message.text

    await answer_to(context, from_user, to_user, order_id)

    await log_message(context, from_user, to_user, order_id)

    await update.message.reply_text(
        'Ответ отправлен!',
    )
    
    await show_menu(update, context)

    if context.user_data.get('text'): del context.user_data['text']
    if context.user_data.get('media_group'): del context.user_data['media_group']
    if context.user_data.get('documents'): del context.user_data['documents']
    if context.user_data.get('order_id'): del context.user_data['order_id']

    return EXIT
    
@message_check    
async def answer_to_exit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get('order_id'): del context.user_data['order_id']

    await show_menu(update, context)

    return EXIT

@callback_message_check
async def pay_order_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    order_id = int(update.callback_query.data.split('.')[-1])

    order = await get_order_by_id(order_id)
    await update.callback_query.answer()

    if order.status == OrderStatuses.on_payment: 
        await update.callback_query.message.reply_text(
            text=f'Запрос уже отправлен'
        ) 
        return EXIT
    
    if order.status == OrderStatuses.in_progress: 
        await update.callback_query.message.reply_text(
            text=f'Заказ уже в работе'
        ) 
        return EXIT
    
    if order.status != OrderStatuses.new: 
        await update.callback_query.message.reply_text(
            text=f'Заказ уже завершён'
        ) 
        return EXIT

    context.user_data['pay_order_id'] = order_id

    kb = ReplyKeyboardMarkup(
        [
            [
                KeyboardButton('↩️Выйти')
            ],
        ], resize_keyboard=True, one_time_keyboard=True
    )

    await update.callback_query.message.reply_text(
        text=f'Введите сумму на оплату',
        reply_markup=kb
    ) 

    return CHAT_WITH_MENU

@message_check     
async def pay_order_stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    summ = update.message.text

    kb = ReplyKeyboardMarkup(
        [
            [
                KeyboardButton('↩️Выйти')
            ],
        ], resize_keyboard=True, one_time_keyboard=True
    )

    if not summ.isdigit(): 
        await update.message.reply_text(
        text=f'Введите число',
        reply_markup=kb
    ) 
        return CHAT_WITH_MENU

    summ = int(summ)
    
    new_summ = final_sum(summ)

    order_id = context.user_data.get('pay_order_id')

    order = await get_order_by_id(order_id)

    await order_set_status(order_id, OrderStatuses.on_payment)

    await order_set_cost(order_id, summ)
    
    from_user = int(await get_user_id_data(update.message.from_user.id))

    if from_user == order.buyer_id: to_user = order.contractor_id
    else:                           to_user = order.buyer_id

    await update.message.reply_text(
        text=f'По #Заказ_{order_id} отправлен запрос оплаты на сумму {summ} рублей ({new_summ} с учётом комиссии)' 
    ) 

    btns = [
        [
            InlineKeyboardButton(text=f'Согласиться', callback_data=f'{PAY_ACCEPT}.{order_id}'),
            InlineKeyboardButton(text=f'Отказаться', callback_data=f'{PAY_CANCEL}.{order_id}')
        ]
    ]

    kb = InlineKeyboardMarkup(btns)

    text = f"""
Вам пришёл счёт на оплату по #Заказ_{order_id} 
на сумму {new_summ} рублей. 
Согласитесь с этой суммой или откажитесь
"""

    await context.bot.send_message(chat_id=int(await get_user_telegram_id_data(to_user)), 
                                    text=text, 
                                    reply_markup=kb)
    
    await show_menu(update, context)
    return EXIT    
    

@message_check 
async def pay_order_exit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await show_menu(update, context)

    return EXIT

@callback_message_check 
async def cancel_order_cost(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()

    order_id = int(update.callback_query.data.split('.')[-1])
    order = await get_order_by_id(order_id)

    await order_set_status(order_id, OrderStatuses.new)
    
    from_user = int(await get_user_id_data(update.callback_query.message.chat.id))

    if from_user == order.buyer_id: to_user = order.contractor_id
    else:                           to_user = order.buyer_id

    btns = [[InlineKeyboardButton(text=f'Ответить', callback_data=f'{ANSWER_TO}.{order_id}')]]
    btns.append([InlineKeyboardButton(text=f'Отменить Заказ', callback_data=f'{CANCEL_ORDER}.{order_id}')])

    kb = InlineKeyboardMarkup(btns)

    await update.callback_query.message.reply_text(
        text=f'По #Заказ_{order_id} было отказано в оплате',
        reply_markup=kb
    ) 

    await update.callback_query.message.edit_reply_markup(
        reply_markup=None
    )

    btns.append([InlineKeyboardButton(text=f'Запросить Оплату', callback_data=f'{PAY_ORDER}.{order_id}')])
    kb = InlineKeyboardMarkup(btns)

    await context.bot.send_message(chat_id=int(await get_user_telegram_id_data(to_user)), 
                                    text=f'По #Заказ_{order_id} было отказано в оплате',
                                    reply_markup=kb)

@callback_message_check 
async def accept_order_cost(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()

    order_id = int(update.callback_query.data.split('.')[-1])
    order = await get_order_by_id(order_id)

    summ = order.cost

    new_summ = final_sum(summ)

    await order_set_status(order_id, OrderStatuses.in_progress)
    
    text = f"""Пожалуйста отправте {new_summ} руб. на карту
\n{BANK_NAME_CONST}
{BANK_CARD_CONST}
{CARD_OWNER_CONST}\n
После чего нажмите на кнопку подтверждения оплаты"""

    kb = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton('Подтвердить оплату', callback_data=f'{CONFIRM_PAY}.{order_id}')
            ]
        ]
    )

    await update.callback_query.message.edit_reply_markup(
        reply_markup=None
    )

    await update.callback_query.message.reply_text(
        text=text,
        reply_markup=kb
    ) 


@callback_message_check 
async def confirm_order_pay(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()

    order_id = int(update.callback_query.data.split('.')[-1])
    order = await get_order_by_id(order_id)

    new_summ = final_sum(order.cost)
    
    from_user = int(await get_user_id_data(update.callback_query.message.chat.id))

    if from_user == order.buyer_id: to_user = order.contractor_id
    else:                           to_user = order.buyer_id

    await update.callback_query.message.edit_reply_markup(
        reply_markup=None
    )

    btns = [[InlineKeyboardButton(text=f'Ответить', callback_data=f'{ANSWER_TO}.{order_id}')]]

    kb = InlineKeyboardMarkup(btns)

    await update.callback_query.message.reply_text(
        text=f'По #Заказ_{order_id} была принята сумма.'
        'Ожидайте подтверждение оплаты от модераторов',
        reply_markup=kb
    )

    await context.bot.send_message(chat_id=int(await get_user_telegram_id_data(to_user)), 
                                    text=f'По #Заказ_{order_id} была принята сумма.' 
                                    'Ожидайте подтверждение оплаты от модераторов',
                                    reply_markup=kb)
    
    chat_id = -1002213633542

    from_user_id = update.callback_query.message.chat
    to_user_id = await context.bot.get_chat(int(await get_user_telegram_id_data(to_user)))
    
    text = f'Подтвердите оплату на сумму {new_summ}'

    kb = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton('Подтвердить оплату', callback_data=f'{CONFIRM_ORDER}.{order_id}')
            ]
        ]
    )

    text += f'\n\n@{to_user_id.username} -> @{from_user_id.username}\n#Заказ_{order_id}'
    message = await context.bot.send_message(chat_id=chat_id,
                                   text=text,
                                   reply_markup=kb)
    await message.pin()

async def confirm_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()

    order_id = int(update.callback_query.data.split('.')[-1])
    order = await get_order_by_id(order_id)
    
    buyer_id = order.buyer_id
    contractor_id = order.contractor_id

    contractor_role = await get_user_role_data(await get_user_telegram_id_data(contractor_id))

    btns = [[InlineKeyboardButton(text=f'Ответить', callback_data=f'{ANSWER_TO}.{order_id}')]]

    kb = InlineKeyboardMarkup(btns)

    await context.bot.send_message(chat_id=int(await get_user_telegram_id_data(contractor_id)), 
                                text=f'Оплата по #Заказ_{order_id} подтверждена',
                                reply_markup=kb)

    btns.append([InlineKeyboardButton(text=f'Подтвердить выполнение заказа', callback_data=f'{CONFIRM_ORDER_FINALY}.{order_id}')])
    kb = InlineKeyboardMarkup(btns)

    await context.bot.send_message(chat_id=int(await get_user_telegram_id_data(buyer_id)), 
                                    text=f'Оплата по #Заказ_{order_id} подтверждена',
                                    reply_markup=kb)
        
    if contractor_role == RoleNames.dressmaker:
        await context.bot.send_message(chat_id=int(await get_user_telegram_id_data(buyer_id)), 
                                        text=f'Для дальнейшего оформления доставки напишите @chase_bot_support')

    
    message:Message = update.callback_query.message

    await message.edit_text(
        text=f'Оплата по #Заказ_{order_id} подтверждена',
        reply_markup=None
    )


@callback_message_check 
async def confirm_order_finaly(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()

    order_id = int(update.callback_query.data.split('.')[-1])
    order = await get_order_by_id(order_id)

    summ = order.cost
    new_summ = final_sum(summ)

    await order_set_status(order_id, OrderStatuses.finished)
    
    from_user = int(await get_user_id_data(update.callback_query.message.chat.id))

    if from_user == order.buyer_id: to_user = order.contractor_id
    else:                           to_user = order.buyer_id

    await update.callback_query.message.edit_reply_markup(
        reply_markup=None
    )

    await update.callback_query.message.reply_text(
        text=f'Выполение #Заказ_{order_id} было подтверждено. ' 
        'Спасибо, что были с нами. Ждём вас ещё!',
    )

    await context.bot.send_message(chat_id=int(await get_user_telegram_id_data(to_user)), 
                                    text=f'Выполение #Заказ_{order_id} было подтверждено')

    chat_id = -1002213633542

    from_user_id = update.callback_query.message.chat
    to_user_id = await context.bot.get_chat(int(await get_user_telegram_id_data(to_user)))

    text = f'Выполние заказа на сумму {new_summ} ({summ} для исполнителя) подтверждено!'
    text += f'\n\n@{from_user_id.username} -> @{to_user_id.username}\n#Заказ_{order_id}'
    await context.bot.send_message(chat_id=chat_id,
                                   text=text)