#!/usr/local/bin/python3
# coding=utf-8
import telebot, logging, datetime, random, sys, time
from telebot import types

logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG) # Outputs debug messages to console.
token = sys.argv[1]
bot = telebot.AsyncTeleBot(token)
strip = lambda a:a.lstrip(a.split()[0]).lstrip().rstrip()

def calBattery():
    timeend = 78600
    timestart = 32400
    secnow = (time.time().__int__() - time.timezone) % 86400
    if secnow < timestart or secnow > timeend: 
        return "太医补魔中"
    else:
        diff = secnow - timestart
        bat = (46200 - diff * diff / 46200) / 46200
        return "太医电量剩余: {:.2%}".format(bat)

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
    a = random.randrange(1,100)
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

@bot.message_handler(commands=['rollit'])
def roll(message):
    text = strip(message.text)
    choice = list(set(text.split(",")))
    print(choice)
    r,res,winner = {},[],[]
    for i in choice:
        if i != '':
            name = i.strip()
            dice = random.choice(range(1,101))
            r[name] = dice
    values = list(r.values()).count(max(list(r.values())))
    for k,v in r.items():
        res.append("{} rolled: {}".format(k,v))
    r_sort = sorted(r.items(), key=lambda d: d[1],reverse=True)
    for i in range(values):
        winner.append("winner is {}: {}".format(r_sort[i][0],r_sort[i][1]))
    res = "\n".join(res) + "\n\n" + "\n".join(winner)
    bot.reply_to(message,res)

@bot.message_handler(commands=['test'])
def test(message):
    text = strip(message.text)
    bot.reply_to(message,text)

bot.polling()
