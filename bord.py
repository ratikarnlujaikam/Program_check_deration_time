from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

# ใส่ Channel Access Token และ Channel Secret ที่ได้จากการสร้าง Channel ใน Line Developers
CHANNEL_ACCESS_TOKEN = 'YOUR_CHANNEL_ACCESS_TOKEN'
CHANNEL_SECRET = 'YOUR_CHANNEL_SECRET'

app = Flask(__name__)
line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

@app.route("/callback", methods=['POST'])
def callback():
    # X-Line-Signature header จะถูกส่งมาพร้อมกับ request จาก Line
    signature = request.headers['X-Line-Signature']

    # จัดเก็บ body ของ request
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # รับข้อความจากผู้ใช้
    user_message = event.message.text

    # ตัวอย่างการประมวลผล: ส่งข้อความตอบกลับ
    reply_message = f'คุณพูดว่า: {user_message}'
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_message))

if __name__ == "__main__":
    app.run(debug=True)
