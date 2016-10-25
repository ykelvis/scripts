#!/usr/local/bin/python3
# coding=utf-8
import logging
import sys
import random
import time
from uuid import uuid4
from telegram.ext import Updater, CommandHandler, InlineQueryHandler
from telegram import InlineQueryResultArticle, InputTextMessageContent

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
            c = calBattery()
            a = random.choice(emoji)
            c = c + ' ' + str(a)
            logging.info('battery now {}'.format(c))
            results.append(
                InlineQueryResultArticle(
                    id=uuid4(),
                    title=c,
                    input_message_content=InputTextMessageContent(c)))
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


def main(token):
    TOKEN = token
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('roll', roll))
    dp.add_handler(CommandHandler('taiyi', taiyi))
    dp.add_handler(CommandHandler('choice', choice))
    dp.add_handler(CommandHandler('say', say))
    dp.add_handler(CommandHandler('dice', dice))
    dp.add_handler(CommandHandler('test', test))

    dp.add_handler(InlineQueryHandler(inline_battery))

    #updater.start_polling()
    updater.start_webhook(listen="127.0.0.1",port=15000,url_path='taiyi')
    updater.bot.setWebhook("https://tg.libyk.so/taiyi")
    updater.idle()

if __name__ == "__main__":
    t = sys.argv[1]
    main(t)
