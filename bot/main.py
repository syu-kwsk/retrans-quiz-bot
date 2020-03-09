from flask import Flask, request, abort
from bot import app, db
from bot.retrans import Retrans
from bot.models import Quiz
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
from random import randint

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
    messages = []
    quiz = Quiz.query.filter_by(id=randint(1, 1000)).first()
    trans_question = Retrans(text=quiz.question)
    trans_question.set_level(5)
    trans_question = trans_question.retrans()
    answer = quiz.answer
    true_question = quiz.question
    messages.append(TextSendMessage(text=trans_question["retrans"]))
    messages.append(TextSendMessage(text="答えは:"+answer))
    messages.append(TextSendMessage(text="以下、原文:\n"+true_question))
    line_bot_api.reply_message(
            event.reply_token,
            messages
            )

if __name__ == "__main__":
    print("Please run run.py")
