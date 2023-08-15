from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import openai
from linebot_project.settings import OPENAI_API_KEY

# 環境変数の設定
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(settings.LINE_CHANNEL_SECRET)
openai.api_key = OPENAI_API_KEY

@csrf_exempt
def callback(request):
    signature = request.headers['X-Line-Signature']
    body = request.body.decode('utf-8')

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        return HttpResponse(status=400)

    return HttpResponse(status=200)


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # GPT-3を使用してレスポンスを生成
    response = openai.Completion.create(
      engine="davinci",
      prompt=event.message.text,
      max_tokens=150,
      temperature=0
    )
    response_text = response.choices[0].text.strip()

    # LINE botがレスポンスを返す
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=response_text)
    )


#TODO ngrok動作確認用(最後に消す)
def index(request):
    return HttpResponse("Hello, LINE bot!")
