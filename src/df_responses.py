import os
from google.cloud import dialogflow_v2 as dialogflow
from telegram import Update
from telegram.ext import CallbackContext

from py_models import ResponseInfo
from logs import logger

# Установите переменные окружения
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/diana/Downloads/botdevs-6685c25ee41b.json"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/app/botdevs-6685c25ee41b.json"
PROJECT_ID = "botdevs"
SESSION_ID = "unique-session-id" # todo сделать генерацию
language_code = "ru"
# todo убрать переменные в .env и constants


def detect_intent(text):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(PROJECT_ID, SESSION_ID)

    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(session=session, query_input=query_input)
    logger.info(f"Dialoflow response {response.query_result} type {type(response)}")

    return response.query_result

def detect_intent_event(event):
    #неудачная попытка сделать переход в стейты через event
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(PROJECT_ID, SESSION_ID)

    event_input = dialogflow.EventInput(name=event, language_code=language_code)
    query_input = dialogflow.QueryInput(event=event_input)

    response = session_client.detect_intent(
        session=session, query_input=query_input
    )

    print(response.query_result)
    return response.query_result


def process_fulfillment_messages(update: Update, context: CallbackContext, fulfillment_messages) -> ResponseInfo:
    messages_info = []
    buttons_info = None

    for message in fulfillment_messages:
        if message.text:
            try:
                mes = message.text.text[0]
                if mes:
                    messages_info.append(mes)
            except:
                logger.exception("Empty text message")

        if message.payload:
            if "keyboard" in message.payload.keys():
                buttons_info = message.payload["keyboard"]
            if "go_to_state" in message.payload.keys():
                context.bot.send_message(chat_id=update.effective_chat.id,
                                         text=f'**TestMode: для перехода тык сюда> {message.payload["go_to_state"]}**')
                # неудачная попытка сделать переход в стейты через event

                # detect_intent_event(message.payload["go_to_state"])

    return ResponseInfo(messages=messages_info, buttons=buttons_info)
