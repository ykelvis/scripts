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
    print pic,
    return img

def getReplyIDs(js,index):
    chat_id = js['result'][index]['message']['chat']['id']
    message_id = js['result'][index]['message']['message_id']
    return chat_id, message_id

def dice():
    text = response['result'][i]['message']['text']
    try:
        x,y,z = text.split(" ")
        if int(y) < int(z):
            text = random.randrange(int(y),int(z))
            sendMessage(token,a,b,text)
        else:
            sendMessage(token,a,b,"（〃｀д´ )( ´ｪ`)")
    except:
        sendMessage(token,a,b,"/dice num1 num2\n//num1 < num2")

def choice():
    text = response['result'][i]['message']['text']
    if text.split("@",1)[0] == "/choice":
        reply = "/choice choice1 choice2 choice3 choice4 ..."
        sendMessage(token,a,b,reply)
    else:
        arr = text.split(" ")
        arr.pop(0)
        text = random.choice(arr)
        sendMessage(token,a,b,text)
    return 0

def printLog(requestName):
    firstName = response['result'][i]['message']['from']['first_name']
    chat = response['result'] [i]['message']['chat']['id']
    print datetime.datetime.now(), offset, firstName, requestName, chat

def calBattery():
    dateToday = datetime.date.today()
    timeEnds = datetime.time(21,50,00)
    timeStarts = datetime.time(9,00,00)
    batteryStarts = datetime.datetime.combine(dateToday,timeStarts)
    batteryEnds = datetime.datetime.combine(dateToday,timeEnds)
    batteryNow = datetime.datetime.now()
    result = float((batteryEnds - batteryNow).total_seconds())/float((batteryEnds - batteryStarts).total_seconds())
    if result <= 0:
        return "((((；ﾟДﾟ)))))))))))"
    else:
        return "{:.2%}".format(result)
    return r;
if __name__ == "__main__":
    token = sys.argv[1]
    offset = sys.argv[2]
    folder = sys.argv[3]
    offset_old = 0
    rate = []
    while True:
        response = getUpdates(token,offset)
        offset = response['result'][-1]['update_id']
        randReply = ["🌚","🍼","GTMDFBK","GTMDSRR","GTMDYK","GTMDSORA","（〃｀д´ )( ´ｪ`)","辣鸡。","朕知道了。"]
        if offset == offset_old:
            pass;
        else:
            for i in range(1,len(response['result'])):
                a,b = getReplyIDs(response,i)
                res = response['result'][i]['message']
                if res.has_key("text"):
                    t = res['text'].split("@",1)[0]
                    if t == "/batteryreport":
                        text = calBattery()
                        sendMessage(token,a,b,text)
                        printLog("bat")
                    elif t == "/leg":
                        if a < 0:
                            rate.append(time.time())
                            if len(rate) > 5 and (rate[-1] - rate[0] > 600):
                                rate = []
                                img = getImg(folder)
                                sendPhoto(token,a,b,img)
                                printLog('leg')
                            elif len(rate) <= 5:
                                img = getImg(folder)
                                sendPhoto(token,a,b,img)
                                print "sent photo"
                                printLog('leg')
                            else:
                                sec = int(rate[-1] - rate[0])
                                text = "（〃｀д´ )( ´ｪ`) wait, " + str(600 - sec) + " seconds..."
                                #sendMessage(token,a,b,text)
                                print text
                        else:
                            img = getImg(folder)
                            sendPhoto(token,a,b,img)
                            print "sent photo",
                            printLog('leg')

                    elif t == "/crossdressfubuki":
                        sendMessage(token,a,b,"🌚")
                        printLog('cross')
                    elif t.split(" ",1)[0] == "/dice":
                        dice();
                        printLog('dice')
                    elif t.split(" ",1)[0] == "/choice":
                        choice();
                        printLog('choice')
                    else:
                        reply = random.choice(randReply);
                        sendMessage(token,a,b,reply)
                        printLog('whadafu!?')
        offset_old = offset 
        time.sleep(1);
