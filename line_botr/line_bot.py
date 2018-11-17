from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, FollowEvent, PostbackEvent,
    MessageEvent, TextMessage, TextSendMessage,
    FlexSendMessage, FollowEvent, PostbackEvent,
    SourceUser, SourceGroup, SourceRoom,
    QuickReply, QuickReplyButton,
    MessageAction, CameraAction, LocationAction, PostbackAction, CarouselContainer
)

import os, time, random, json
from .reply_handler import Reply_handler
from .push_handler import Push_handler
from .MODE import MODE
from flaskr import app
from jinja2 import Environment, FileSystemLoader, select_autoescape

#環境変数取得
if not "YOUR_CHANNEL_ACCESS_TOKEN" in os.environ.keys():
    YOUR_CHANNEL_ACCESS_TOKEN = "test_token"
else:
    YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
if not "YOUR_CHANNEL_SECRET" in os.environ.keys():
    YOUR_CHANNEL_SECRET = "test_secret"
else:
    YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]

YOUR_CHANNEL_ACCESS_TOKEN = "QBaWtYKxqLQN04fMAHqv06JG76wWzHFef0iI4K5w7stYgOSIbwGCxQPnqmyt9pwOTtgTgmblZVow63Yhy/J2bhSnerlmncJl8tM+tCQs0cTp1W3nHM559i/+5KcDCUC3g2xwdwOeWA3YSFPr5cySIQdB04t89/1O/w1cDnyilFU="
YOUR_CHANNEL_SECRET = "27e9418cc7a19e398846c2ea6e3bec42"

global line_bot_api
line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

print(1)
from .onboarding import handle_follow_event
print(2)
from .reply_handler import Reply_handler
from .push_handler import Push_handler
from .MODE import MODE, Session_interface
print(3)
from flaskr import app
print(4)

@app.route("/testl")
def hello():
    import socket, os
    html = "<h3>Hello {name}!</h3>" \
           "<b>Hostname:</b> {hostname}<br/>" \
           "<b>Visits:</b> {visits}"
    return html.format(name=os.getenv("NAME", "line-bot"), hostname=socket.gethostname(), visits=9999)

@app.route("/test_hayate")
def test_hayate():
    _text = "テストテストテストテストテストテストテストテストテストテストテストテストテストテスト"
    line_bot_api.push_message("857NDKF8TISbbga5LxRWkA", TextSendMessage(text=_text))

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']


    # get request body as text
    body = request.get_data(as_text=True)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    rh = Reply_handler(event.message.text, event=event, line_bot_api=line_bot_api)
    rh.get_message()

@handler.add(PostbackEvent)
def handle_postback(event):
    # TODO: postback_handlerを作る？
    rh = Reply_handler(event.postback.data, event=event, line_bot_api=line_bot_api)
    reply_text = rh.get_message()
    if reply_text:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))

# 友達追加時の動作=オンボーディング
@handler.add(FollowEvent)
def handle_message(event):
    # 万が一にもユーザーがオンボーディング起動用の文字列を入力しないように、
    #   SHA-256で「ONBOARDING」をハッシュ化したものを使用
    rh = Reply_handler(MODE.ONBOARDING.hash, event=event, line_bot_api=line_bot_api)
    reply_text = rh.get_message()
    if reply_text:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))

    # 一つの長文メッセージを送るのではなく、連続して複数のメッセージを送る
    if isinstance(event.source, SourceUser):
        handle_follow_event(event, line_bot_api)

    # TODO: 以前一度使ってたことある人で、再度友達登録した場合のメッセージに分岐する

    return 'OK'

# pushメッセージ
@app.route("/send_customer", methods=["GET"])
def push_send_customer():
    '''送客ロジックが走る
    '''
    Session_interface.set_waiting_mode(user_id=user_id, mode=MODE.START_SEND_CUSTOMER)
    ph = Push_handler(MODE.START_SEND_CUSTOMER)
    text = ph.get_message()
    to = ph.to
    line_bot_api.push_message(to, TextSendMessage(text=text))
    return 'OK'

@app.route("/push_ask", methods=["GET"])
def push_test():
    '''何時にジムに行くか聞くプッシュ送信を毎朝7時に定期実行する
    '''
    ph = Push_handler(MODE.PUSH_ASK)
    text = ph.get_message()
    to = ph.to
    line_bot_api.push_message(to, TextSendMessage(text=text))
    return 'OK'

@app.route("/push_holiday", methods=["GET"])
def push_golds_gym_monthly_holiday():
    '''ジムの定休日をアナウンスするプッシュ送信を毎月第一月曜日と、第二月曜日とその前日・前々日に定期実行する
    '''
    ph = Push_handler(MODE.PUSH_HOLIDAY)
    text = ph.get_message()
    to = ph.to
    line_bot_api.push_message(to, TextSendMessage(text=text))
    return 'OK'

@app.route("/push_off_rate", methods=["GET"])
def push_off_rate():
    '''myproteinの割引率をスクレイプして一日一回通知する
    '''
    ph = Push_handler(MODE.PUSH_OFF_RATE)
    text = ph.get_message()
    to = ph.to
    line_bot_api.push_message(to, TextSendMessage(text=text))
    return 'OK'

def push_message(user_id, text):
    """外のモジュールからlineのbotにテキストを返させるメソッド"""
    print('user_id: {}'.format(user_id))
    print('text: {}'.format(text))
    line_bot_api.push_message(user_id, TextSendMessage(text=text))

def push_carousel_message(user_id, data):
    """外のモジュールからlineのbotにFlexメッセージを返させるメソッド"""
    print('user_id: {}'.format(user_id))
    print('data: {}'.format(json.loads(data)))
    line_bot_api.push_message(user_id,
        FlexSendMessage(
            alt_text="items",
            contents=CarouselContainer.new_from_json_dict(json.loads(data))
        )
    )

if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
