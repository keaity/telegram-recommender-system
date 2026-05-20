import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import TOKEN
from dataset import items_df
from interactions import add_interaction
from recommender import get_recommendations
from db_funcs import init_db

# Инициализация базы данных при запуске бота
init_db()

bot = telebot.TeleBot(TOKEN)
user_positions = {}  # Словарь для хранения текущей позиции каждого пользователя


def main_menu():
    """Создаёт главное меню с кнопками 'Каталог' и 'Рекомендации'."""
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton(
            "📚 Каталог",
            callback_data="catalog"
        ),
        InlineKeyboardButton(
            "⭐ Рекомендации",
            callback_data="recs"
        )
    )
    return markup


@bot.message_handler(commands=['start'])
def start(message):
    """Обработчик команды /start — приветственное сообщение."""
    text = (
        "Привет! 👋\n\n"
        "Я Telegram-бот с рекомендательной системой.\n"
        "Подбираю фильмы 🎬, книги 📚 и курсы 🎓.\n\n"
        "Как это работает:\n"
        "• Листай каталог и оценивай объекты\n"
        "• Я запоминаю твои предпочтения\n"
        "• Получай персональные рекомендации\n\n"
        "Нажми «Каталог», чтобы начать."
    )
    bot.send_message(message.chat.id, text, reply_markup=main_menu())


def send_item(chat_id, user_id):
    """Отправляет пользователю один объект из каталога(с попыткой отправить картинку)"""
    idx = user_positions.get(user_id, 0)
    item = items_df.iloc[idx]

    poster_path = f"src/dataset/images/{item.item_id}.jpg"

    text = f"📌 {item.title}\n\nОписание: {item.description}\nТип: {item.domain}"

    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton("⬅️", callback_data="prev"),
        InlineKeyboardButton("➡️", callback_data="next")
    )
    markup.row(
        InlineKeyboardButton(
            "👁 Просмотр",
            callback_data=f"view_{item.item_id}"
        ),
        InlineKeyboardButton(
            "👍 Лайк",
            callback_data=f"like_{item.item_id}"
        ),
        InlineKeyboardButton(
            "❤️ Избранное",
            callback_data=f"fav_{item.item_id}"
        )
    )
    markup.row(
        InlineKeyboardButton(
            "⭐ Рекомендации",
            callback_data="recs"
        )
    )

    try:
        # Пытаемся отправить фото + текст
        with open(poster_path, "rb") as photo:
            bot.send_photo(chat_id, photo, caption=text, reply_markup=markup)
    except Exception:
        # Если фото нет — отправляем только текст
        bot.send_message(chat_id, text, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    """Главный обработчик всех нажатий на inline-кнопки."""
    user_id = call.from_user.id

    if call.data == "catalog":
        user_positions[user_id] = 0
        send_item(call.message.chat.id, user_id)

    elif call.data == "next":
        user_positions[user_id] = (user_positions.get(user_id, 0) + 1) % len(items_df)
        send_item(call.message.chat.id, user_id)

    elif call.data == "prev":
        user_positions[user_id] = (user_positions.get(user_id, 0) - 1) % len(items_df)
        send_item(call.message.chat.id, user_id)

    elif call.data.startswith(("view_", "like_", "fav_")):
        # Сохранение взаимодействия пользователя (просмотр, лайк, избранное)
        event, item_id = call.data.split("_")
        add_interaction(user_id, int(item_id), event)
        bot.answer_callback_query(call.id, "Сохранено ✔️")

    elif call.data == "recs":
        # Выдача персональных рекомендаций
        recs = get_recommendations(user_id)
        if recs.empty:
            bot.send_message(call.message.chat.id,
                             "Пока мало данных 🙂 Оцените несколько объектов.")
            return

        bot.send_message(call.message.chat.id, "⭐ Ваши рекомендации:")
        for _, row in recs.iterrows():
            bot.send_message(
                call.message.chat.id,
                f"🔥 {row.title}\n{row.description}"
            )


print("Бот запущен...")
bot.polling(none_stop=True)
