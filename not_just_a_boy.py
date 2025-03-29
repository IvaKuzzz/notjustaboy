import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

API_TOKEN = '7980477563:AAGVkMNiTtauLiiOD4DFIshI7Pvjy1brJdQ'
CHANNEL_ID = '@notjustaboy'
DONATION_LINK = 'https://www.donationalerts.com/r/notjustaboy'

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def start(update: Update, context: CallbackContext):
    # Отправляем сообщение через context.bot 
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Привет, {update.effective_user.first_name}! Для начала подтверди, что ты не робот.",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("✅ Я не робот", callback_data='not_robot')]])
    )

def check_subscription(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    try:
        member = context.bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        if member.status not in ['left', 'kicked']:
            return True
        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"❌ Подпишись на канал {CHANNEL_ID}, чтобы продолжить!"
            )
            return False
    except Exception as e:
        logging.error(f"Ошибка проверки подписки: {str(e)}")
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="⚠️ Произошла ошибка. Попробуй позже!"
        )
        return False

def main_menu(update: Update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Приветик, сладкий! Вижу ты захотел моего контента побольше. Тогда выбирай:",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Приват фото/видео 📸", callback_data='private_photo')],
            [InlineKeyboardButton("Супер Приватик 🔥", callback_data='super_private')]
        ])
    )

def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    data = query.data

    if data == 'not_robot':
        if check_subscription(update, context):
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Подтверди, что тебе есть 18 лет:",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Мне 18+ 🔞", callback_data='age_confirm')]])
            )

    elif data == 'age_confirm':
        main_menu(update, context)

    elif data == 'private_photo':
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Выбери срок подписки:",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("1 месяц - 500₽", callback_data='month_1')],
                [InlineKeyboardButton("6 месяцев - 1500₽", callback_data='month_6')],
                [InlineKeyboardButton("Навсегда - 2000₽", callback_data='forever')],
                [InlineKeyboardButton("В начало ↩️", callback_data='restart')]
            ])
        )

    elif data == 'super_private':
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Супер Приватик включает эксклюзивные видео с лицом, где я кончаю, меня трахают и многое другое!",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Навсегда - 5000₽", callback_data='super_forever')],
                [InlineKeyboardButton("В начало ↩️", callback_data='restart')]
            ])
        )

    elif data in ['month_1', 'month_6', 'forever', 'super_forever']:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"💸 Оплати тут: {DONATION_LINK}\nПосле оплаты напиши мне скриншот перевода. Подожди немного, сладкий! 😘"
        )

    elif data == 'restart':
        # Полный сброс через отправку нового сообщения
        start(update, context)

def main():
    updater = Updater(API_TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CallbackQueryHandler(button_handler))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
