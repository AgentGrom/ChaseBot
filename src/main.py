from telegram import Update
from telegram.ext import (
    ApplicationBuilder,  
    CommandHandler, 
    JobQueue,
    MessageHandler,
    filters
)

from warnings import filterwarnings
from telegram.warnings import PTBUserWarning

filterwarnings(action="ignore", message=r".*CallbackQueryHandler", category=PTBUserWarning)

from config import TOKEN

from main_funcs import clear_all_users
from main_handles import check_register_handle, set_registered_status_handle

async def beautiful_print(data, tabs=0):
    for key, val in data.items():
        if type(val) == dict: 
            print(' '*tabs + f'{key}:')
            await beautiful_print(val, tabs+2)
        else:
            print(' '*tabs + f'{key}: {val}')

async def test(update:Update, b):
    print(update.message.message_thread_id)
    # print(update.message.to_dict())
    await beautiful_print(update.message.to_dict())


def main() -> None:

    job_queue = JobQueue()
    application = ApplicationBuilder().token(TOKEN).job_queue(job_queue).build()

    # application.add_handlers(check_register_handle)

    # application.add_handler(set_registered_status_handle)
    # application.add_handler(CommandHandler('clear', clear_all_users))

    application.add_handler(MessageHandler(filters.TEXT, test))

    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()