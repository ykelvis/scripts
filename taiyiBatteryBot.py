# coding=utf-8
#!/usr/bin/python
import os,random
import sys
import time
import datetime
import json
import requests

def getMe(token):
    response = requests.post(
    url='https://api.telegram.org/bot' + token + "/" + method
).json()
    return response;

def getUpdates(token,offset):
    response = requests.post(
        url='https://api.telegram.org/bot' + token + "/getUpdates",
        data={'offset': offset}
).json()
    return response;

def sendMessage(token,chat_id,message_id,text):
    response = requests.post(
        url='https://api.telegram.org/bot' + token + "/sendMessage",
        data={'chat_id': chat_id,'reply_to_message_id': message_id, 'text': text}
).json()
    return response

def sendPhoto(token,chat_id,message_id,img):
    response = requests.post(
        url='https://api.telegram.org/bot' + token + "/sendPhoto",
        data={'chat_id': chat_id,'reply_to_message_id': message_id},
        files={'photo': img},
).json
    return response

def getImg(folder):
    a = [];
    for f in os.listdir(folder):
        if os.path.isfile(os.path.join(folder,f)):
            a.append(f);
    pic = random.choice(a);
    picLoc = os.path.join(folder,pic)
    img = open(picLoc,'rb')
    return img

def getReplyIDs(js,index):
    chat_id = js['result'][index]['message']['chat']['id']
    message_id = js['result'][index]['message']['message_id']
    return chat_id, message_id

def dice():
    text = response['result'][i]['message']['text']
    try:
        x,y,z = text.split(" ")
        if y < z:
            text = random.randrange(int(y),int(z))
            sendMessage(token,a,b,text)
        else:
            sendMessage(token,a,b,"（〃｀д´ )( ´ｪ`)")
    except:
        sendMessage(token,a,b,"/dice num1 num2\n//num1 < num2")

def choice():
    text = response['result'][i]['message']['text']
    if text == "/choice":
        reply = "/choice choice1 choice2 choice3 choice4 ..."
        sendMessage(token,a,b,reply)
    else:
        arr = text.split(" ")
        arr.pop(0)
        text = random.choice(arr)
        sendMessage(token,a,b,text)
    return 0

def calBattery():
    dateToday = datetime.date.today()
    timeEnds = datetime.time(21,50,00)
    timeStarts = datetime.time(9,00,00)
    batteryStarts = datetime.datetime.combine(dateToday,timeStarts)
    batteryEnds = datetime.datetime.combine(dateToday,timeEnds)
    batteryNow = datetime.datetime.now()
    result = float((batteryEnds - batteryNow).total_seconds())/float((batteryEnds - batteryStarts).total_seconds())
    return "{:.2%}".format(result)

if __name__ == "__main__":
    token = sys.argv[1]
    offset = sys.argv[2]
    folder = sys.argv[3]
    offset_old = 0
    while True:
        response = getUpdates(token,offset)
        offset = response['result'][-1]['update_id']
        if offset == offset_old:
            pass;
        else:
            print offset
            for i in range(1,len(response['result'])):
                a,b = getReplyIDs(response,i)
                text = calBattery()
                r = response['result'][i]['message']
                if r.has_key("text"):
                    if response['result'][i]['message']['text'] == "/batteryreport":
                        sendMessage(token,a,b,text)
                        print "sent battery report"
                    elif response['result'][i]['message']['text'] == "/leg":
                        img = getImg(folder)
                        sendPhoto(token,a,b,img)
                        print "sent photo"
                        #sendMessage(token,a,b,"（〃｀д´ )( ´ｪ`)")
                    elif response['result'][i]['message']['text'] == "/crossdressfubuki":
                        sendMessage(token,a,b,"🌚")
                        print "crossdress requested"
                    elif "/dice" in response['result'][i]['message']['text']:
                        dice();
                        print "dice"
                    elif "/choice" in response['result'][i]['message']['text']:
                        choice();
                        print "choice"
                    else:
                        sendMessage(token,a,b,"🍼")
                        print "whadafu!?"
        offset_old = offset 
        time.sleep(1);
