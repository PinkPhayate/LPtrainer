import os, json
from flask import Flask, request, abort
from flaskr import app
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, FlexSendMessage, CarouselContainer,
)
from line_botr import logic


CHANNEL_ACCESS_TOKEN = os.getenv('CHANNEL_ACCESS_TOKEN')
CHANNEL_SECRET = os.getenv('CHANNEL_SECRET')

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)


@app.route("/callback", methods=['POST'])
def callback():
    global action_mode
    global tr_name
    global tr_strength
    json = request.get_json()
    app.logger.info(json)
    user_resource = json['events'][0]
    user_id = user_resource['source']['userId']


    json = request.get_json()
    reply_token =  user_resource['replyToken']
    if action_mode is None:
        input_msg = user_resource['message']['text']
        actm, output_msg = logic.select_1st_action(user_id, input_msg)
        send_msg(reply_token, output_msg)
        if actm is None:
            initialize_valiables()
        else:
            action_mode = actm
        return ""


    if tr_name is None:
        try:
            actm, output_msg = logic.select_2nd_action(user_id, action_mode, user_resource)
        except Exception as e:
            print(e)
            actm, output_msg = None, '正しく処理ができませんでした'
        send_msg(reply_token, output_msg)
        if actm is None:
            initialize_valiables()
        else:
            tr_name = actm
        return ""

    if tr_strength is None:
        input_msg = user_resource['message']['text']
        output_msg = logic. select_3rd_action(user_id, tr_name, input_msg)
        send_msg(reply_token, output_msg)
        initialize_valiables()
    return ''


def send_msg(reply_token, msg):
    try:
        line_bot_api.reply_message(
            reply_token,
            FlexSendMessage(
                alt_text="trainings",
                contents=CarouselContainer.new_from_json_dict(json.loads(msg))
            )
        )
        return
    except json.decoder.JSONDecodeError:
        pass
    except Exception as e:
        app.logger.error(e)
        initialize_valiables()
        return
    try:
        line_bot_api.reply_message(
            reply_token,
            TextSendMessage(text=msg))
    except Exception as e:
        app.logger.error(e)
        initialize_valiables()
        return


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))

def initialize_valiables():
    global action_mode
    global tr_name
    global tr_strength

    action_mode = None
    tr_name = None
    tr_strength = None
initialize_valiables()
