import json
import os

import telebot

from playlist_creator import PlaylistMaker
from config import Config

TG_TOKEN = Config.TG_TOKEN
VK_TOKEN = Config.VK_TOKEN
bot = telebot.TeleBot(TG_TOKEN)
HELP_TEXT = "Чтобы загрузить весь свой плейлист, напиши мне '/download VK_ID', где VK_ID - id твоей страницы " \
            "ВКонтакте. Аудиозаписи должны быть открыты."


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, HELP_TEXT)
    print(message,  end='\n\n')


@bot.message_handler(commands=['help'])
def show_help(message):
    bot.send_message(message.chat.id, HELP_TEXT)
    print(message, end='\n\n')


@bot.message_handler(commands=['download'])
def load_music(message):
    print(message, end='\n\n')
    if message.chat.type != 'private':
        bot.send_message(message.chat.id, 'Доступно только в приватном чате')
        return
    if len(message.text.split(' ')) != 2:
        bot.send_message(message.chat.id, 'Использование: /download VK_ID')
    else:
        try:
            id_ = int(message.text.split(' ')[1])
        except ValueError:
            bot.send_message(message.chat.id, 'id может быть только числом')
            return

        bot.send_message(message.chat.id, 'Загрузка плейлиста начата')
        pl_maker = PlaylistMaker()
        plist = pl_maker.create_playlist_file(id_)
        with open(plist) as json_file_playlist:
            playlist = json.loads(json_file_playlist.read())
            for song in playlist:
                if song['src'] and not song['is_blocked']:
                    try:
                        # Sync loading here to save order of music in bot dialog
                        bot.send_audio(message.chat.id, song['src'], caption=f"{song['author']} - {song['title']}",
                                       disable_notification=True)
                    except telebot.apihelper.ApiException:
                        bot.send_message(message.chat.id, f"Не удалось загрузить {song['author']} - {song['title']}")
                        continue
            bot.send_message(message.chat.id, 'Загрузка плейлиста окончена')


bot.polling(none_stop=True, interval=5)
