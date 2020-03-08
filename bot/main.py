from flask import Flask, request, abort
from bot import app
from bot.retrans import Retrans
from linebot import (
        LineBotApi, WebhookHandler
        )
from linebot.exceptions import (
        InvalidSignatureError
        )
from linebot.models import (
        MessageEvent, TextMessage, TextSendMessage
        )
import os

#環境変数取得
LINE_CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
LINE_CHANNEL_SECRET = os.environ["LINE_CHANNEL_SECRET"]

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent)
def handle_message(event):
    message = Retrans(text=event.message.text)
    message.set_level(10)
    message = message.retrans()
    message = message["retrans"]
    line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=message)
            )

if __name__ == "__main__":
    print("Please run run.py")
