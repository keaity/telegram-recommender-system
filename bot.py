import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import TOKEN
from dataset import items_df
from interactions import add_interaction
from recommender import get_recommendations

bot = telebot.TeleBot(TOKEN)

user_positions = {}

def main_menu():
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("📚 Каталог", callback_data="catalog"),
        InlineKeyboardButton("⭐ Рекомендации", callback_data="recs")
    )
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    text = (
        "Привет! 👋\n\n"
        "Я Telegram-бот с рекомендательной системой.\n"
        "Подбираю фильмы 🎬, книги 📚 и курсы 🎮.\n\n"
        "Как это работает:\n"
        "Вы листаете каталог и оцениваете объекты.\n"
        "Я запоминаю ваши действия и предлагаю рекомендации.\n\n"
        "Обозначения кнопок:\n"
        "👁 Просмотр — просто посмотрели\n"
        "👍 Лайк — понравилось\n"
        "❤️ Избранное — очень понравилось\n\n"
        "Нажмите «Каталог», чтобы начать."
    )

    bot.send_message(message.chat.id, text, reply_markup=main_menu())

def send_item(chat_id, user_id):
    idx = user_positions.get(user_id, 0)
    item = items_df.iloc[idx]

    text = f"📌 {item.title}\n{item.description}"

    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton("⬅️", callback_data="prev"),
        InlineKeyboardButton("➡️", callback_data="next")
    )
    markup.row(
        InlineKeyboardButton("👁 Просмотр", callback_data=f"view_{item.item_id}"),
        InlineKeyboardButton("👍 Лайк", callback_data=f"like_{item.item_id}"),
        InlineKeyboardButton("❤️ Избранное", callback_data=f"fav_{item.item_id}")
    )
    markup.row(
        InlineKeyboardButton("⭐ Рекомендации", callback_data="recs")
    )

    bot.send_message(chat_id, text, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
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
        event, item_id = call.data.split("_")
        add_interaction(user_id, int(item_id), event)
        bot.answer_callback_query(call.id, "Сохранено ✔️")

    elif call.data == "recs":
        recs = get_recommendations(user_id)

        if recs.empty:
            bot.send_message(call.message.chat.id,
                             "Пока мало данных 🙂 Оцените несколько объектов.")
            return

        bot.send_message(call.message.chat.id, "⭐ Ваши рекомендации:\n")

        for _, row in recs.iterrows():
            bot.send_message(call.message.chat.id,
                             f"🔥 {row.title}\n{row.description}")


print("Бот запущен...")
bot.polling(none_stop=True)