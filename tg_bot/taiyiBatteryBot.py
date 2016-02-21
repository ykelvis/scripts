#!/usr/local/bin/python3
# coding=utf-8

import telebot, logging, datetime, random
from telebot import types


logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG) # Outputs debug messages to console.

token = ""

bot = telebot.AsyncTeleBot(token)


def calBattery():
    dateToday = datetime.date.today()
    timeEnds = datetime.time(21,50,00)
    timeStarts = datetime.time(9,00,00)
    batteryStarts = datetime.datetime.combine(dateToday,timeStarts)
    batteryEnds = datetime.datetime.combine(dateToday,timeEnds)
    batteryNow = datetime.datetime.now()
    result = float((batteryEnds - batteryNow).total_seconds())/float((batteryEnds - batteryStarts).total_seconds())
    if result < 1 and result > 0: 
        return "{:.2%}".format(result)
    else:
        return "太医补魔中..."

@bot.inline_handler(lambda query: query.query == '')
def query_battery(inline_query):
    try:
        c = "taiyi: {}".format(calBattery())
        r = types.InlineQueryResultArticle('1', c, c)
        bot.answer_inline_query(inline_query.id, [r],cache_time=10)
    except Exception as e:
        print(e)

@bot.message_handler(commands=['taiyi'])
def taiyi(message):
    m = calBattery()
    bot.reply_to(message, m)

@bot.message_handler(commands=['dice'])
def dice(message):
    try:
        x,y = message.text.split(" ")[1].split(",")
        a,b = int(x),int(y)
        if a < b:
            b = b + 1
            r = random.randrange(a,b)
            bot.reply_to(message,r)
        else:
            bot.reply_to(message,"invalid")
    except:
        bot.reply_to(message,"usage: /dice 1,6")

@bot.message_handler(commands=['choice'])
def choice(message):
    try:
        a = message.text.split(" ")[1].split(",")
        r = random.choice(a)
        bot.reply_to(message,r)
    except:
        bot.reply_to(message,"usage: /choice c1,c2,c3")

@bot.message_handler(commands=['say'])
def say(message):
    try:
        x,y = message.text.split(" ")
        bot.reply_to(message,y)
    except:
        bot.reply_to(message,"usage: /say blabla")

@bot.message_handler(commands=['pm25'])
def pm25(message):
    from bs4 import BeautifulSoup as bs
    import requests
    try:
        x,y = message.text.split(" ")
        res = requests.get("http://www.stateair.net/web/rss/1/1.xml")
        res = bs(res,"lxml")
        print(res)
        r = res.findAll('item')[0]
        bot.reply_to(message,r)
    except:
        bot.reply_to(message,"usage: /pm25")


@bot.message_handler(commands=['test'])
def test(message):
    bot.reply_to(message,"message text is {}".format(message.text))
    bot.reply_to(message,"message id is {}".format(message.message_id))
    bot.reply_to(message,"chat id is {}".format(message.chat.id))

bot.polling()
