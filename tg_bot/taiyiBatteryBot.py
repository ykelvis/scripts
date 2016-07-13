#!/usr/local/bin/python3
# coding=utf-8
import telebot, logging, datetime, random, sys, time
from telebot import types

logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG) # Outputs debug messages to console.
token = sys.argv[1]
bot = telebot.AsyncTeleBot(token)
strip = lambda a:a.lstrip(a.split()[0]).lstrip().rstrip()

timeend = 78600
timestart = 32400

def calBattery():
    global timeend,timesatart
    d = timeend - timestart
    secnow = (time.time().__int__() - time.timezone) % 86400
    if secnow < timestart or secnow > timeend: 
        return "太医补魔中"
    else:
        diff = secnow - timestart
        bat = (d - diff * diff / d) / d
        return "太医电量剩余: {:.2%}".format(bat)

@bot.inline_handler(lambda query: query.query == '+1s')
def query_charge(inline_query):
    global timeend
    timeend +=1
    hour = (timeend / 3600).__int__()
    minute = (timeend % 3600 / 60).__int__()
    second = (timeend % 3600 % 60).__int__()
    text = '续1s, 太医没电时间: {:02}:{:02}:{:02}'.format(hour,minute,second)
    r1 = types.InlineQueryResultArticle('taiyi', text, text)
    bot.answer_inline_query(inline_query.id, [r1],cache_time=1)

@bot.inline_handler(lambda query: query.query == '')
def query_battery(inline_query):
    try:
        emoji = ['( ´_ゝ`)','（〃｀д´ )( ´ｪ`)','（〃｀д´ ) 🍼','（〃｀д´ ) ☔️','( ･ั﹏･ั )','( ´∀｀ )','( ﾟдﾟ )','(・Д・)ノ','(^o^)丿','(๑´•.̫ • `๑)','(゜-゜)','(｡ŏ﹏ŏ)','（ ・∀・）','✌(´◓ｑ◔｀)✌﻿','_:(´ཀ`」 ∠):_','（￣へ￣）','(｡•ˇ‸ˇ•｡)﻿','(　д ) ﾟ ﾟ','((((；ﾟДﾟ)))))))','(ﾟДﾟ≡ﾟДﾟ)','Σ(っ°Д°;)っ',' ༼ つ ◕_◕ ༽つ','(;´༎ຶД༎ຶ`)','｡･ﾟ･(ﾉД`)･ﾟ･｡','ヽ(；▽；)ノ','_(:3」 ∠)_','( ´◔ ‸◔`)﻿','╮( ๑╹,◡╹ ๑ ) ╭','(つд⊂)','( ´∀`)σ)Д` )','(╯°Д°)╯','( ͡° ͜ʖ ͡° )','¯\_(ツ)_/¯']
        c = calBattery()
        a = random.choice(emoji)
        c = c + ' ' + str(a)
        r1 = types.InlineQueryResultArticle('taiyi', c, c)
        r2 = types.InlineQueryResultArticle('agent','特工电量剩余：+∞', '特工电量剩余：+∞')
        r = [r1,r2]
        j = 0
        for i in emoji:
            r.append(types.InlineQueryResultArticle(str(j),i,i))
            j+=1
        bot.answer_inline_query(inline_query.id, r,cache_time=5)
    except Exception as e:
        print(e)

@bot.message_handler(commands=['taiyi'])
def taiyi(message):
    m = calBattery()
    bot.reply_to(message, m)

@bot.message_handler(commands=['roll'])
def roll(message):
    a = random.randrange(1,101)
    bot.reply_to(message,a)

@bot.message_handler(commands=['dice'])
def dice(message):
    text = strip(message.text)
    try:
        text = text.replace(" ","")
        x,y = text.split(",")
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
    text = strip(message.text)
    try:
        a = text.split(",")
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

@bot.message_handler(commands=['test'])
def test(message):
    text = strip(message.text)
    bot.reply_to(message,text)

bot.polling()
