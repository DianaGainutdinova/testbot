from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

from py_models import ResponseInfo
from df_responses import process_fulfillment_messages, detect_intent
from logs import logger


def general(update: Update, context: CallbackContext) -> None:
    if update.callback_query:
        response_info = button_click(update, context)
    else:
        response_info = handle_message(update, context)
    send_response(update, context, response_info)


def handle_message(update: Update, context: CallbackContext, ) -> ResponseInfo:
    # для обработка сообщений
    user_input = update.message.text

    # обращаемся к DF
    df_response = detect_intent(user_input)

    logger.info(f"DF response from message {dir(df_response.fulfillment_messages)}")
    return process_fulfillment_messages(update, context, df_response.fulfillment_messages)


def button_click(update: Update, context: CallbackContext, ) -> ResponseInfo:
    # для обработки кликов на кнопки
    query = update.callback_query
    data = query.data
    query.answer()
    query.edit_message_text(text=f"{data}")
    df_response = detect_intent(data)
    logger.info(f"DF response from click {dir(df_response.fulfillment_messages)}")
    return process_fulfillment_messages(update, context, df_response.fulfillment_messages)


def send_response(update: Update, context: CallbackContext, response_info: ResponseInfo) -> None:
    # для отправки сообщений без кнопок и с кнопками
    if response_info.messages:
        print(response_info.messages)
        if response_info.buttons:
            response_with_inline_keyboard(update, context, response_info)
        else:

            for message_info in response_info.messages:
                if update.callback_query:
                    context.bot.send_message(chat_id=update.effective_chat.id, text=message_info)
                else:
                    update.message.reply_text(message_info)
    else:
        pass
#     todo здесь должна быть описана логика перехода по "go_to_state"


def response_with_inline_keyboard(update: Update, context: CallbackContext, response_info: ResponseInfo) -> None:
    try:
        keyboard = [
            [InlineKeyboardButton(button, callback_data=button) for button in response_info.buttons]]
        reply_markup = InlineKeyboardMarkup(keyboard)
    except Exception as e:
        logger.exception(f"Error sending inline keyboard: {e}")
        reply_markup = None

    for ind, message_text in enumerate(response_info.messages):
        # добавляем к последнему сообщению кнопки
        if ind != len(response_info.messages) - 1:
            if update.callback_query:
                context.bot.send_message(chat_id=update.effective_chat.id, text=message_text)
            else:
                update.message.reply_text(message_text)
        else:
            if update.callback_query:
                context.bot.send_message(chat_id=update.effective_chat.id, text=message_text, reply_markup=reply_markup)
            else:
                update.message.reply_text(message_text, reply_markup=reply_markup)
