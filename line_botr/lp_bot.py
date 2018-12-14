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
from line_botr.session import StatusSession

CHANNEL_ACCESS_TOKEN = os.getenv('CHANNEL_ACCESS_TOKEN')
CHANNEL_SECRET = os.getenv('CHANNEL_SECRET')

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

@app.route("/callback", methods=['POST'])
def callback():
    json = request.get_json()
    app.logger.info(json)
    user_resource = json['events'][0]
    user_id = user_resource['source']['userId']
    reply_token =  user_resource['replyToken']

    # session factory
    sess = logic.get_session(user_id)
    sess.print_session_vars()
    # print_variables(sess)

    input_msg = _get_message_text(user_resource)
    if logic.is_initialize(sess.user_id, input_msg):
        actm, output_msg = None, '初期化しました'
        send_msg(sess.user_id, reply_token, output_msg)
        return ""


    if sess.action_mode is None:
        input_msg = _get_message_text(user_resource)
        actm, output_msg = logic.select_1st_action(sess.user_id, input_msg)
        send_msg(sess.user_id, reply_token, output_msg)
        if actm is not None:
            sess.set_action_mode(actm)
            logic.set_session(sess)
        # drop_session(sess)
        return ""

    if sess.tr_name is None:
        try:
            actm, output_msg = logic.select_2nd_action(sess.user_id, sess.action_mode, user_resource)
        except Exception as e:
            app.logger.error(e)
            actm, output_msg = None, '正しく処理ができませんでした'
        send_msg(sess.user_id, reply_token, output_msg)
        if actm is not None:
            sess.set_tr_name(actm)
            sess.print_session_vars()
            logic.set_session(sess)
        return ""

    if sess.tr_strength is None:
        input_msg = _get_message_text(user_resource)
        output_msg = logic.select_3rd_action(sess.user_id, sess.tr_name, input_msg)
        send_msg(sess.user_id, reply_token, output_msg)
        # drop_session(user_id)
    return ''


def send_msg(user_id, reply_token, msg):
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
        return
    try:
        line_bot_api.reply_message(
            reply_token,
            TextSendMessage(text=msg))
    except Exception as e:
        app.logger.error(e)
        return

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))

def drop_session(sess):
    sess = None

def print_variables(sess):
    sess.print_session_vars()

def _get_message_text(user_resource):
    msg = user_resource.get('message')
    txt = msg.get('text') if msg is not None else None
    return txt
