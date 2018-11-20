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
from line_botr import carousel_creater as cc

CHANNEL_ACCESS_TOKEN = os.getenv('CHANNEL_ACCESS_TOKEN')
CHANNEL_SECRET = os.getenv('CHANNEL_SECRET')

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)
from line_botr import repository
repository.create_table()

ACTION_LIST = ['追加', '記録' , '削除', '参照']
action_mode = None
tr_name  = None
tr_strength = None

@app.route("/")
def hello_world():
    return "hello world!"

@app.route("/callback", methods=['POST'])
def callback():
    global action_mode
    global tr_name
    global tr_strength
    # log_global_variables()
    json = request.get_json()
    app.logger.info(json)
    user_resource = json['events'][0]
    user_id = user_resource['source']['userId']


    json = request.get_json()
    reply_token =  user_resource['replyToken']
    if action_mode is None:
        input_msg = user_resource['message']['text']
        output_msg = select_action_mode(reply_token, input_msg)
        if output_msg is None:
            throw_msg(reply_token, 'その操作はできません')
            return ""
        elif output_msg == '追加':
            data = cc.get_carousel_json()
            throw_carousel(reply_token, data)
            return ""
        elif output_msg == '参照':
            data = repository.get_records(user_id)
            output_msg = beautify_records(data)
            throw_msg(reply_token, output_msg)
            action_mode = None
            return ""

    if tr_name is None:
        if 'message' not in user_resource.keys():
            return ""
        input_msg = user_resource['message']['text']
        output_msg = select_tr_name(reply_token, input_msg)
        throw_msg(reply_token, output_msg)
        return ""

    if tr_strength is None:
        input_msg = user_resource['message']['text']
        output_msg = select_tr_strength(reply_token, input_msg)
        throw_msg(reply_token, output_msg)
        return ""

    return ''

def throw_msg(reply_token, msg):
    try:
        line_bot_api.reply_message(
            reply_token,
            TextSendMessage(text=msg))
    except:
        pass

def throw_carousel(reply_token, data):
    line_bot_api.reply_message(
        reply_token,
        FlexSendMessage(
            alt_text="trainings",
            contents=CarouselContainer.new_from_json_dict(json.loads(data))
        )
    )

    try:
        line_bot_api.reply_message(
            reply_token,
            FlexSendMessage(
                alt_text="trainings",
                contents=CarouselContainer.new_from_json_dict(json.loads(data))
            )
        )
    except:
        pass

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))

def create_carousel(category):
    if category == 'workout':
        item_dict = item_stub.get_videos()
        items = [VideoItem(k, v) for k,v in item_dict.items()]
    elif category == 'recipie':
        item_dict = item_stub.get_recipies()
        items = [VideoItem(k, v) for k,v in item_dict.items()]
    return items

def select_action_mode(user_id, msg):
    global action_mode
    if msg not in ACTION_LIST:
        return None
    action_mode = msg
    print(msg + 'ですね')
    return msg

def select_tr_name(user_id, msg):
    global action_mode
    global tr_name
    tr_name = msg
    format_request_msg = '[回数] [セット数] [重さ(kg)]　の形式で入力してください'
    return format_request_msg

def select_tr_strength(user_id, msg):
    global action_mode
    global tr_name
    global tr_strength
    # TODO: validate input
    if is_invalid(msg):
        return "入力の形式が正しくありません"

    tr_strength = beautify(msg)
    repository.insert_record(user_id, tr_name, msg)

    # record
    reply_msg = "{0} {1} -登録完了".format(tr_name, tr_strength)
    initialize_valiables()
    return reply_msg

def initialize_valiables():
    global action_mode
    global tr_name
    global tr_strength

    action_mode = None
    tr_name = None
    tr_strength = None

def log_global_variables():
    global action_mode
    global tr_name
    global tr_strength

    am = action_mode if action_mode is not None else 'none'
    tn = tr_name if tr_name is not None else 'none'
    ts = tr_strength if tr_strength is not None else 'none'
    app.logger.info('{} {} {}'.format(am,  tn, ts))

def is_invalid(msg):
    ary = msg.split(' ')
    if len(ary) < 2 or 3 < len(ary):
        return True
    not_digits = [x for x in ary if not x.isdigit()]
    if 0 < len(not_digits):
        return True
    return False

def beautify(msg):
    ary = msg.split(' ')
    if len(ary) == 2:
        str = '{}rep {}set'.format(ary[0], ary[1])
    if len(ary) == 3:
        str = '{}rep {}set {}Kg'.format(ary[0], ary[1], ary[2])
    return str

def beautify_records(msg):
    li = [' '.join(x) for x in msg]
    return ' '.join(li)
