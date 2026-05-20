"""Главный модуль Telegram-бота с рекомендательной системой."""

import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import TOKEN
from dataset import items_df, posters
from interactions import add_interaction
from recommender import get_recommendations
from db_funcs import init_db

init_db()

bot = telebot.TeleBot(TOKEN)
user_positions = {}


def main_menu() -> InlineKeyboardMarkup:
    """Создаёт главное меню."""
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("📚 Каталог", callback_data="catalog"),
        InlineKeyboardButton("⭐ Рекомендации", callback_data="recs")
    )
    return markup


@bot.message_handler(commands=['start'])
def start(message):
    """Обработчик команды /start."""
    text = (
        "Привет! 👋\n\n"
        "Я Telegram-бот с рекомендательной системой.\n"
        "Подбираю фильмы 🎬, книги 📚 и курсы 🎮.\n\n"
        "Нажми «Каталог», чтобы начать."
    )
    bot.send_message(message.chat.id, text, reply_markup=main_menu())


def send_item(chat_id: int, user_id: int) -> None:
    """Отправляет объект пользователю с картинкой (если есть)."""
    idx = user_positions.get(user_id, 0) % len(items_df)
    item = items_df.iloc[idx]

    text = f"📌 **{item.title}**\n\n**Описание:** {item.description}\n**Тип:** {item.domain}"

    markup = InlineKeyboardMarkup(row_width=3)
    markup.row(
        InlineKeyboardButton("⬅️", callback_data="prev"),
        InlineKeyboardButton("➡️", callback_data="next")
    )
    markup.row(
        InlineKeyboardButton("👁 Просмотр", callback_data=f"view_{item.item_id}"),
        InlineKeyboardButton("👍 Лайк", callback_data=f"like_{item.item_id}"),
        InlineKeyboardButton("❤️ Избранное", callback_data=f"fav_{item.item_id}")
    )
    markup.row(InlineKeyboardButton("⭐ Рекомендации", callback_data="recs"))

    # Путь к изображению
    poster_path = f"src/dataset/{posters.get(item.item_id)}"

    try:
        with open(poster_path, "rb") as photo:
            bot.send_photo(
                chat_id,
                photo,
                caption=text,
                parse_mode="Markdown",
                reply_markup=markup
            )
    except Exception:
        # Если картинка не найдена — отправляем только текст
        bot.send_message(
            chat_id,
            text,
            parse_mode="Markdown",
            reply_markup=markup
        )


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    """Обработчик нажатий на кнопки."""
    user_id = call.from_user.id

    if call.data == "catalog":
        user_positions[user_id] = 0
        send_item(call.message.chat.id, user_id)

    elif call.data in ["next", "prev"]:
        step = 1 if call.data == "next" else -1
        user_positions[user_id] = (user_positions.get(user_id, 0) + step) % len(items_df)
        send_item(call.message.chat.id, user_id)

    elif call.data.startswith(("view_", "like_", "fav_")):
        event, item_id = call.data.split("_")
        add_interaction(user_id, int(item_id), event)
        bot.answer_callback_query(call.id, "Сохранено ✔️")

    elif call.data == "recs":
        recs = get_recommendations(user_id)
        if recs.empty:
            bot.send_message(call.message.chat.id,
                             "Пока мало данных 🙂\nОцените несколько объектов из каталога.")
            return

        bot.send_message(call.message.chat.id, "⭐ **Ваши рекомендации:**\n")
        for _, row in recs.iterrows():
            bot.send_message(call.message.chat.id,
                             f"🔥 **{row.title}**\n{row.description}")


print("Бот успешно запущен...")
bot.polling(none_stop=True)
