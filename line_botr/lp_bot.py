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
from line_botr import carousel_creater as cc, logic


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
    return msg

def select_tr_name(user_id, msg):
    global action_mode
    global tr_name
    tr_name = msg

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
    reply_msg = "{0} {1} \n登録完了".format(tr_name, tr_strength)
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
