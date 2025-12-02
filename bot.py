import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

from database import init_db, add_user, get_users, record_message
from config import BOT_TOKEN

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Unique command constant
DUMP_COMMAND = "134950"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Я бот-сохранитель участников. Добавьте меня в группу!")


async def dump_users(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    users = get_users(chat_id)
    if not users:
        await update.message.reply_text("Пока что нет сохраненных пользователей.")
        return

    lines = [
        f"{user_id} — {username or 'N/A'} — {count} сообщений"
        for user_id, username, count in users
    ]
    await update.message.reply_text("\n".join(lines))


async def handle_new_members(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message.new_chat_members:
        return
    for member in update.message.new_chat_members:
        add_user(update.effective_chat.id, member.id, member.username)
        logger.info("Saved user %s (%s)", member.id, member.username)


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Запись сообщения пользователя и увеличение счётчика."""
    chat_id = update.effective_chat.id
    user = update.effective_user
    record_message(chat_id, user.id, user.username)


def main() -> None:
    """Запуск бота (синхронный, управляет event loop внутри run_polling)."""
    init_db()

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler(DUMP_COMMAND, dump_users))
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, handle_new_members))
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text)
    )

    logger.info("Bot started.")
    app.run_polling()


if __name__ == "__main__":
    main()
