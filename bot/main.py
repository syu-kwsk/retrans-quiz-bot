from flask import Flask, request, abort
from bot import app, db
from bot.retrans import Retrans
from bot.models import Quiz, User
from linebot import (
        LineBotApi, WebhookHandler
        )
from linebot.exceptions import (
        InvalidSignatureError
        )
from linebot.models import (
        MessageEvent, TextMessage, TextSendMessage,
        FollowEvent
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
    user = User.query.filter_by(user_id=event.source.user_id).first()
    print(line_bot_api.get_profile(user.user_id).display_name)
    if user.status == "normal":
        if event.message.text == "クイズ":
            quiz = Quiz.query.filter_by(id=randint(1, 1000)).first()
            user.status = quiz.question
            db.session.add(user)
            db.session.commit()
            trans_question = Retrans(text=quiz.question)
            trans_question.set_level(2)
            quiz = trans_question.retrans()["retrans"]
            messages.append(TextSendMessage(text=quiz))

        else:
            messages.append(TextSendMessage(text="「クイズ」でランダムに選んだクイズを再翻訳して出題します。"))
    else:
        quiz = Quiz.query.filter_by(question=user.status).first()
        message = "………"
        if quiz.answer == event.message.text:
            message+="正解！\nすごいね"
        else:
            message+="残念！\n正解は「"+quiz.answer+"」"
        
        messages.append(TextSendMessage(text=message))
        messages.append(TextSendMessage(text="以下、原文:\n"+quiz.question))
        user.status = "normal"
        db.session.add(user)
        db.session.commit()

    line_bot_api.reply_message(
            event.reply_token,
            messages
            )

@handler.add(FollowEvent)
def handle_follow(event):
    user_id = event.source.user_id
    user = User.query.filter_by(user_id=user_id).first()

    if user is None:
        user = User(user_id=user_id, status="normal")
        db.session.add(user)
        db.session.commit()

    else :
        user.status = "normal"
        db.session.add(user)

    messages = []
    messages.append(TextSendMessage(text="こんにちは、"+line_bot_api.get_profile(user_id).display_name+"さん"))
    messages.append(TextSendMessage(text="「クイズ」でランダムに選んだクイズを再翻訳して出題します。"))
    line_bot_api.reply_message(
            event.reply_token,
            messages
            )

if __name__ == "__main__":
    print("Please run run.py")
