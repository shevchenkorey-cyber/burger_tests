import os
import json
import random
import logging
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

USERS_FILE = os.path.join(os.path.dirname(__file__), "users_data.json")


# ─── Хранилище участников ─────────────────────────────────────────────────────

def load_users() -> dict:
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_users(data: dict) -> None:
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def register_user(chat_id: int, user, registered: bool = False) -> None:
    """Сохраняет пользователя в хранилище по chat_id."""
    data = load_users()
    key = str(chat_id)
    if key not in data:
        data[key] = {}
    uid = str(user.id)
    existing = data[key].get(uid, {})
    data[key][uid] = {
        "id": user.id,
        "first_name": user.first_name or "",
        "username": user.username or "",
        # Не снимаем флаг, если он уже был выставлен через /reg
        "registered": registered or existing.get("registered", False),
    }
    save_users(data)


def get_chat_users(chat_id: int) -> list:
    data = load_users()
    return list(data.get(str(chat_id), {}).values())


def get_registered_users(chat_id: int) -> list:
    """Возвращает только тех, кто явно зарегистрировался через /reg."""
    return [u for u in get_chat_users(chat_id) if u.get("registered")]


# ─── Клавиатуры ───────────────────────────────────────────────────────────────

def main_menu_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton("📋 О боте", callback_data="about")],
        [
            InlineKeyboardButton("⚙️ Настройки", callback_data="settings"),
            InlineKeyboardButton("❓ Помощь", callback_data="help"),
        ],
    ]
    return InlineKeyboardMarkup(buttons)


# ─── Команды ──────────────────────────────────────────────────────────────────

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    register_user(update.effective_chat.id, user)
    await update.message.reply_text(
        f"Привет, {user.first_name}! 👋\n\n"
        "Я бот с командами и меню. Выбери действие:",
        reply_markup=main_menu_keyboard(),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = (
        "📖 *Список команд:*\n\n"
        "/start — главное меню\n"
        "/help — эта справка\n"
        "/about — информация о боте\n"
        "/reg — зарегистрироваться для участия в /kpacaba\n"
        "/kpacaba — выбрать красавчика дня 👑\n"
    )
    await update.message.reply_text(text, parse_mode="Markdown")


async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "🤖 *О боте*\n\n"
        "Бот умеет выбирать красавчика дня в групповом чате.\n"
        "Напиши /kpacaba и узнаешь, кто сегодня красавчик!",
        parse_mode="Markdown",
    )


async def reg_command(update: Update, _context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    chat = update.effective_chat

    if user.is_bot:
        return

    register_user(chat.id, user, registered=True)

    mention = f"@{user.username}" if user.username else user.first_name
    await update.message.reply_text(
        f"✅ {mention}, ты зарегистрирован(а) как участник!\n"
        "Теперь тебя могут выбрать командой /kpacaba 👑"
    )


async def kpacaba_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat = update.effective_chat

    users = get_registered_users(chat.id)

    if not users:
        await update.message.reply_text(
            "😔 Никто ещё не зарегистрировался.\n"
            "Пусть участники напишут /reg — тогда смогу выбрать красавчика!"
        )
        return

    chosen = random.choice(users)

    # Формируем упоминание: @username или просто имя
    if chosen["username"]:
        mention = f"@{chosen['username']}"
    else:
        mention = chosen["first_name"]

    await update.message.reply_text(
        f"🌟 ВНИМАНИЕ! 🌟\n\n"
        f"СЕГОДНЯ ТЫ КРАСАВЧИК ДНЯ!\n\n"
        f"👑 {mention} 👑\n\n"
        f"Поздравляем! Ты лучший сегодня! 🎉"
    )


# ─── Обработчик кнопок ────────────────────────────────────────────────────────

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    responses = {
        "about": (
            "🤖 *О боте*\n\n"
            "Бот умеет выбирать красавчика дня в групповом чате.\n"
            "Напиши /kpacaba и узнаешь, кто сегодня красавчик!"
        ),
        "settings": "⚙️ *Настройки*\n\nЗдесь будут настройки.",
        "help": (
            "📖 *Список команд:*\n\n"
            "/start — главное меню\n"
            "/help — справка\n"
            "/about — о боте\n"
            "/reg — зарегистрироваться для /kpacaba\n"
            "/kpacaba — красавчик дня 👑"
        ),
    }

    text = responses.get(query.data, "Неизвестная команда.")
    await query.edit_message_text(
        text=text,
        parse_mode="Markdown",
        reply_markup=main_menu_keyboard(),
    )


# ─── Трекинг участников группы ────────────────────────────────────────────────

async def track_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Запоминает каждого, кто написал сообщение в чате."""
    user = update.effective_user
    chat = update.effective_chat
    if user and not user.is_bot:
        register_user(chat.id, user)

    # Эхо только в личных чатах
    if chat.type == "private":
        await update.message.reply_text(
            f"Ты написал: {update.message.text}\n\n"
            "Воспользуйся /start для открытия меню."
        )


# ─── Запуск ───────────────────────────────────────────────────────────────────

def main() -> None:
    if not TOKEN:
        raise ValueError("Не задан BOT_TOKEN в файле .env")

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("about", about_command))
    app.add_handler(CommandHandler("reg", reg_command))
    app.add_handler(CommandHandler("kpacaba", kpacaba_command))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, track_user))

    logger.info("Бот запущен")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
