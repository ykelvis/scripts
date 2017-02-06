#!/usr/local/bin/python3
# coding=utf-8
import os
import re
import logging
import sys
import random
import time
import requests
from uuid import uuid4
from telegram.ext import Updater, CommandHandler, InlineQueryHandler, Filters, MessageHandler
from telegram import InlineQueryResultArticle, InputTextMessageContent, ParseMode
from roll import *
from currency import *

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)
strip = lambda a: a.lstrip(a.split()[0]).lstrip().rstrip()


def wrapper(*args, **kwargs):
    def w(fn):
        def ww(bot, update):
            logging.info(
                'user: {} command: {}'.format(
                    update.message.from_user.username,
                    update.message.text))
            text = fn(bot, update)
            logging.info('response: {}'.format(text))
            if kwargs.get('reply_to', None):
                kwargs['reply_to'] = update.message.message_id
            bot.sendMessage(
                update.message.chat_id,
                reply_to_message_id=kwargs['reply_to'],
                text=text,
                parse_mode=kwargs.get(
                    'parse_mode',
                    None),
                disable_web_page_preview=kwargs.get(
                    'disable_preview',
                    None))
            return 0
        return ww
    return w

timeend = 21 * 60 * 60 + 50 * 60
timestart = 9 * 60 * 60
emoji = ['( ´_ゝ`)',
         '（〃｀д´ )( ´ｪ`)',
         '（〃｀д´ ) 🍼',
         '（〃｀д´ ) ☔️',
         '( ･ั﹏･ั )',
         '( ´∀｀ )',
         '( ﾟдﾟ )',
         '(・Д・)ノ',
         '(^o^)丿',
         '(๑´•.̫ • `๑)',
         '(゜-゜)',
         '(｡ŏ﹏ŏ)',
         '（ ・∀・）',
         '✌(´◓ｑ◔｀)✌﻿',
         '_:(´ཀ`」 ∠):_',
         '（￣へ￣）',
         '(｡•ˇ‸ˇ•｡)﻿',
         '(　д ) ﾟ ﾟ',
         '((((；ﾟДﾟ)))))))',
         '(ﾟДﾟ≡ﾟДﾟ)',
         'Σ(っ°Д°;)っ',
         ' ༼ つ ◕_◕ ༽つ',
         '(;´༎ຶД༎ຶ`)',
         '｡･ﾟ･(ﾉД`)･ﾟ･｡',
         'ヽ(；▽；)ノ',
         '_(:3」 ∠)_',
         '( ´◔ ‸◔`)﻿',
         '╮( ๑╹,◡╹ ๑ ) ╭',
         '(つд⊂)',
         '( ´∀`)σ)Д` )',
         '(╯°Д°)╯',
         '( ͡° ͜ʖ ͡° )',
         '¯\_(ツ)_/¯']


def calBattery():
    global timeend, timesatart
    d = timeend - timestart
    secnow = (time.time().__int__() - time.timezone) % 86400
    if secnow < timestart or secnow > timeend:
        return "太医补魔中"
    else:
        diff = secnow - timestart
        bat = (d - diff * diff / d) / d
        return "太医电量剩余: {:.2%}".format(bat)

def count_down(ts):
    starter = int(ts[0:2]) * 3600 + int(ts[2:4]) * 60 + int(ts[4:6])
    curr = (time.time().__int__() - time.timezone) % 86400
    if curr > starter:
        ret = 86400 - curr + starter
        result, sec = divmod(ret, 60)
        hour = result // 60
        minute = result % 60
    elif curr < starter:
        ret = starter - curr 
        result, sec = divmod(ret, 60)
        hour = result // 60
        minute = result % 60
    else:
        hour = 0
        minute = 0
        sec = 0
    return "距离{}还剩: {:02}:{:02}:{:02}".format(ts.rsplit('00')[0], hour, minute, sec)


def inline_charge():
    global timeend
    timeend += 1
    hour = (timeend / 3600).__int__()
    minute = (timeend % 3600 / 60).__int__()
    second = (timeend % 3600 % 60).__int__()
    text = '续1s, 太医没电时间: {:02}:{:02}:{:02}'.format(hour, minute, second)
    return text


def inline_battery(bot, update):
    global emoji
    query = update.inline_query.query
    results = list()
    logging.info(
        'inline {} from {}'.format(
            'no content'
            if query == '' else query,
            update.inline_query.from_user.username))
    if query == '':
        try:
            c = calBattery() + ' ' + str(random.choice(emoji))
            d = count_down('053000') + ' ' + str(random.choice(emoji))
            logging.info('battery now {}'.format(c))
            results.append(
                InlineQueryResultArticle(
                    id=uuid4(),
                    title=c,
                    input_message_content=InputTextMessageContent(c)))
            results.append(
                InlineQueryResultArticle(
                    id=uuid4(),
                    title=d,
                    input_message_content=InputTextMessageContent(d)))
            results.append(
                InlineQueryResultArticle(
                    id=uuid4(),
                    title='特工电量剩余：+∞',
                    input_message_content=InputTextMessageContent('特工电量剩余：+∞')))
            [results.append
             (
                 InlineQueryResultArticle(id=uuid4(), title=x,
                                          input_message_content=InputTextMessageContent(x)))
             for x in emoji]
            logging.info('battery now {}'.format(c))
            bot.answerInlineQuery(
                update.inline_query.id,
                results=results,
                cache_time=5)
            logging.info('return succ, {}'.format(c))
        except Exception as e:
            print(e)
    elif query == '+1s':
        ret = inline_charge()
        results = [
            InlineQueryResultArticle(
                id=1,
                title=ret,
                input_message_content=InputTextMessageContent(ret))]
        bot.answerInlineQuery(
            update.inline_query.id,
            results=results,
            cache_time=1)
    elif query.startswith('kuro'):
        query = query.replace('kuro', '').replace(" ","")
        if query == '':
            return 0
        _ret = requests.get("https://utils.libyk.so/kurorekishi/keyword/" + query, proxies=None).text
        try:
            _ret = json.loads(_ret)
            ret = {}
            if _ret['results'] == []:
                ret[1] = "nothing found"
            else:
                j = 1
                for i in _ret['results']:
                    ret[j] = i['text']
                    j += 1
        except:
            ret = {1: "json parse error"}
        results = [
            InlineQueryResultArticle(
                id=k,
                title=v,
                input_message_content=InputTextMessageContent(v)) for k,v in ret.items()]
        bot.answerInlineQuery(
            update.inline_query.id,
            results=results,
            cache_time=1)
    else:
        q = query
        ret = ''
        c = [' ', '']
        for i in q:
            ret = ret + i + random.choice(c)
        logger.info('return: {}'.format(ret))
        results.append(
            InlineQueryResultArticle(
                id=1,
                title=ret,
                input_message_content=InputTextMessageContent(ret)))
        bot.answerInlineQuery(
            update.inline_query.id,
            results=results,
            cache_time=1)


@wrapper(disable_preview=True, parse_mode=None, reply_to=True)
def taiyi(bot, update):
    m = calBattery()
    return m


@wrapper(disable_preview=True, parse_mode=None, reply_to=True)
def roll(bot, update):
    a = random.randrange(1, 101)
    return a


@wrapper(disable_preview=True, parse_mode=None, reply_to=True)
def dice(bot, update):
    text = strip(update.message.text)
    try:
        text = text.replace(" ", "")
        x, y = text.split(",")
        a, b = int(x), int(y)
        if a < b:
            b = b + 1
            r = random.randrange(a, b)
            return r
        else:
            return "usage: /dice 1,6"
    except:
        return "usage: /dice 1,6"


@wrapper(disable_preview=True, parse_mode=None, reply_to=True)
def choice(bot, update):
    text = strip(update.message.text)
    if text == '':
        return 'usage: /choice a,b,c,d'
    else:
        a = text.split(",")
        r = random.choice(a)
        return r


@wrapper(disable_preview=True, parse_mode=None, reply_to=True)
def say(bot, update):
    text = strip(update.message.text)
    if text == '':
        return 'usage: /say blabla'
    else:
        return text


@wrapper(disable_preview=True, parse_mode=None, reply_to=True)
def test(bot, update):
    return str(update)

def logg(bot, update):
    update.message.reply_text(update.message.text)

@wrapper(disable_preview=True, parse_mode=ParseMode.MARKDOWN, reply_to=True)
def rollstart(bot, update):
    return startroll(update)


@wrapper(disable_preview=True, parse_mode=ParseMode.MARKDOWN, reply_to=True)
def rolljoin(bot, update):
    return joinroll(update)


@wrapper(disable_preview=True, parse_mode=ParseMode.MARKDOWN, reply_to=False)
def rollquit(bot, update):
    return quitroll(update)


@wrapper(disable_preview=True, parse_mode=ParseMode.MARKDOWN, reply_to=False)
def rolllists(bot, update):
    return listsroll(update)


@wrapper(disable_preview=True, parse_mode=ParseMode.MARKDOWN, reply_to=False)
def rollnow(bot, update):
    return nowroll(update)


@wrapper(disable_preview=True, parse_mode=ParseMode.MARKDOWN, reply_to=True)
def rollkick(bot, update):
    return kickroll(update)

@wrapper(disable_preview=True, parse_mode=None, reply_to=False)
def kuro(bot, update):
    chanid = update.message.chat.id
    if chanid != -961315:
        return 'hello'
    ret = requests.get("https://utils.libyk.so/kurorekishi/random", proxies=None).text
    try:
        ret = json.loads(ret)
        return ret['text']
    except:
        return "json parse error"

@wrapper(disable_preview=True, parse_mode=None, reply_to=False)
def curr(bot, update):
    chanid = update.message.chat.id
    text = strip(update.message.text)
    command = re.match('(\d+)\s+?(\w+)\s+(?:to)\s+(\w+)', text)
    if not command:
        return "Bad request."
    try:
        amount = int(command.group(1))
        return get_currency(command.group(2), command.group(3), amount)
    except:
        return "Bad request."

def main(token, url, path):
    TOKEN = token
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('roll', roll))
    dp.add_handler(CommandHandler('taiyi', taiyi))
    dp.add_handler(CommandHandler('choice', choice))
    dp.add_handler(CommandHandler('say', say))
    dp.add_handler(CommandHandler('dice', dice))
    dp.add_handler(CommandHandler('test', test))

    dp.add_handler(CommandHandler('rollstart', rollstart))
    dp.add_handler(CommandHandler('rolljoin', rolljoin))
    dp.add_handler(CommandHandler('rolllists', rolllists))
    dp.add_handler(CommandHandler('rollnow', rollnow))
    dp.add_handler(CommandHandler('rollquit', rollquit))
    dp.add_handler(CommandHandler('rollkick', rollkick))

    dp.add_handler(CommandHandler('currency', curr))
    dp.add_handler(CommandHandler('kuro', kuro))

    dp.add_handler(InlineQueryHandler(inline_battery))
    # dp.add_handler(MessageHandler(Filters.text, logg))

    #updater.start_polling()
    updater.start_webhook(listen="0.0.0.0",port=15000,url_path=path)
    updater.bot.setWebhook("https://{}/{}".format(url, path))
    updater.idle()

if __name__ == "__main__":
    t = os.getenv('TG_TOKEN')
    url = os.getenv('TG_URL')
    path = os.getenv('TG_PATH')
    main(t, url, path)
