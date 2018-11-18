import os
from flask import Flask, request, abort
from flaskr import app
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
CHANNEL_ACCESS_TOKEN = os.getenv('CHANNEL_ACCESS_TOKEN')
CHANNEL_SECRET = os.getenv('CHANNEL_SECRET')

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

ACTION_LIST = ['追加', '記録' , '削除']
action_mode = None
tr_name  = None
tr_strength = None

@app.route("/")
def hello_world():
    return "hello world!"

@app.route("/callback", methods=['POST'])
def callback():
    json = request.get_json()
    reply_token =  json['events'][0]['replyToken']
    input_msg = json['events'][0]['message']['text']

    global action_mode
    global tr_name
    global tr_strength

    if action_mode is None:
        output_msg = select_action_mode(input_msg)
        throw_msg(reply_token, output_msg)
        return "OK"

    if tr_name is None:
        output_msg = select_tr_name(input_msg)
        throw_msg(reply_token, output_msg)
        return "OK"

    if tr_strength is None:
        output_msg = select_tr_strength(input_msg)
        throw_msg(reply_token, output_msg)
        return "OK"

    return 'OK'

def throw_msg(reply_token, msg):
    try:
        line_bot_api.reply_message(
            reply_token,
            TextSendMessage(text=msg))
    except:
        pass


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))

def select_action_mode(msg):
    global action_mode
    if msg not in ACTION_LIST:
        return 'その操作はできません'
    action_mode = msg
    return str(msg) + ' ですね'

def select_tr_name(msg):
    global action_mode
    global tr_name
    tr_name = msg
    return tr_name + ' を' + action_mode + ' します'

def select_tr_strength(msg):
    global action_mode
    global tr_name
    global tr_strength
    # TODO: validate input
    tr_strength = msg
    # record
    initialize_valiables()
    return '頑張ってください'

def initialize_valiables():
    global action_mode
    global tr_name
    global tr_strength

    action_mode = None
    tr_name = None
    tr_strength = None
