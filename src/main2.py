from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from telegram.ext import (
    ApplicationBuilder,  
    CommandHandler, 
    JobQueue,
    MessageHandler,
    filters,
    ContextTypes
)

from warnings import filterwarnings
from telegram.warnings import PTBUserWarning

filterwarnings(action="ignore", message=r".*CallbackQueryHandler", category=PTBUserWarning)

from config import TOKEN

# from app.models import RoleNames
from keyboards import RoleKeyboard

from database_get_data import get_user_role_data
from menu_funcs import show_menu
from menu_handles import menu_handle
# from main_funcs import clear_all_users
# from main_handles import check_register_handle, set_registered_status_handle


def main() -> None:

    job_queue = JobQueue()
    application = ApplicationBuilder().token(TOKEN).job_queue(job_queue).build()

    application.add_handlers(menu_handle)

    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()