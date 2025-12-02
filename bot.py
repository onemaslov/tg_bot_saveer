import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

from database import init_db, add_user, get_all_users
from config import BOT_TOKEN

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Unique command constant
DUMP_COMMAND = "134950"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Я бот-сохранитель участников. Добавьте меня в группу!")


async def dump_users(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    users = get_all_users()
    if not users:
        await update.message.reply_text("Пока что нет сохраненных пользователей.")
        return

    lines = [f"{user_id} — {username or 'N/A'}" for user_id, username in users]
    await update.message.reply_text("\n".join(lines))


async def handle_new_members(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message.new_chat_members:
        return
    for member in update.message.new_chat_members:
        add_user(member.id, member.username)
        logger.info("Saved user %s (%s)", member.id, member.username)


def main() -> None:
    """Запуск бота (синхронный, управляет event loop внутри run_polling)."""
    init_db()

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler(DUMP_COMMAND, dump_users))
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, handle_new_members))

    logger.info("Bot started.")
    app.run_polling()


if __name__ == "__main__":
    main()
