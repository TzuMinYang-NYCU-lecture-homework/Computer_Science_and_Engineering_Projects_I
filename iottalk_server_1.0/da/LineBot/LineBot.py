# -*- coding: UTF-8 -*-
import time, threading
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError 
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import DAI, config

line_bot_api = LineBotApi(config.ChannelAccessToken) #LineBot's Channel access token
handler = WebhookHandler(config.ChannelSecret)       #LineBot's Channel secret
user_id_set=set()                                    #LineBot's Friend's user id 
app = Flask(__name__)

def loadUserId():
    try:
        idFile = open(config.idfilePath, 'r')
        idList = idFile.readlines()
        idFile.close()
        idList = idList[0].split(';')
        idList.pop()
        return idList
    except Exception as e:
        print(e)
        return None


def saveUserId(userId):
        idFile = open(config.idfilePath, 'a')
        idFile.write(userId+';')
        idFile.close()


def pushLineMsg(pullDelay=10):
    while True:
        Msg = DAI.pull()
        if Msg:  
            print('PushMsg:{}'.format(Msg))
            for userId in user_id_set:
                try:
                    line_bot_api.push_message(userId, TextSendMessage(text=Msg))
                except Exception as e:
                    print(e)
        Msg=None
        time.sleep(pullDelay)


@app.route("/LineBotQ", methods=['GET'])
def hello():
    return "HTTPS Test OK."

@app.route("/LineBotQ", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']    # get X-Line-Signature header value
    body = request.get_data(as_text=True)              # get request body as text
    print("Request body: " + body, "Signature: " + signature)
    try:
        handler.handle(body, signature)                # handle webhook body
    except InvalidSignatureError:
        abort(400)
    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    Msg = event.message.text
    if Msg == 'Hello, world': return
    #msg = msg.encode('utf-8')
    print('GotMsg:{}'.format(Msg))
    DAI.push(Msg)

    if event.source.type == 'user':
        userId = event.source.user_id
    elif event.source.type == 'group':    
        userId = event.source.group_id
    else: userId = None

    if userId and (not userId in user_id_set):
        user_id_set.add(userId)
        saveUserId(userId)
   
    #line_bot_api.reply_message(event.reply_token,TextSendMessage(text="收到訊息!!"))   # reply api example


if __name__ == "__main__":

    idList = loadUserId()
    if idList: user_id_set = set(idList)
    
    pullThread = threading.Thread(target=pushLineMsg, args=(1,))
    pullThread.daemon = True
    pullThread.start()
    
    app.run('127.0.0.1', port=32768, threaded=True, use_reloader=False)

    
