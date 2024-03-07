from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler

from telegram_responses import general


def main():
    updater = Updater("7064589166:AAExbxEcM9l06bWerw_HSer_0Cj2UcD0J9A", use_context=True)
    # todo убрать токен в .env
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", general))
    dp.add_handler(CallbackQueryHandler(general))
    dp.add_handler(MessageHandler(Filters.text | Filters.command, general))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
