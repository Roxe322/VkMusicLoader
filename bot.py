import json

import telebot

from playlist_creator import PlaylistMaker

TG_TOKEN = '649956076:AAE7NKOUQDuBogSAidSkhGZpfqYF1yfdXfM'
VK_TOKEN = '443da9309bc9d10369b77f5f02158c16663f6b00cdf6ee2c1176f1b1f71dc15d09115fa2dbdf7117949ba'
bot = telebot.TeleBot(TG_TOKEN)
HELP_TEXT = "Чтобы загрузить весь свой плейлист, напиши мне '/download VK_ID', где VK_ID - id твоей страницы " \
            "ВКонтакте. Аудиозаписи должны быть открыты."


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, HELP_TEXT)
    print(message)
    print()


@bot.message_handler(commands=['help'])
def show_help(message):
    bot.send_message(message.chat.id, HELP_TEXT)
    print(message)
    print()


@bot.message_handler(commands=['download'])
def load_music(message):
    print(message)
    print()
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
        pl_maker = PlaylistMaker(VK_TOKEN)
        plist = pl_maker.create_playlist_file(id_)
        with open(plist) as json_file_playlist:
            playlist = json.loads(json_file_playlist.read())
            for song in playlist:
                if song['src'] and not song['is_blocked']:
                    try:
                        bot.send_audio(message.chat.id, song['src'], caption=f"{song['author']} - {song['title']}",
                                       disable_notification=True)
                    except telebot.apihelper.ApiException:
                        bot.send_message(message.chat.id, f"Не удалось загрузить {song['author']} - {song['title']}")
                        continue
            bot.send_message(message.chat.id, 'Загрузка плейлиста окончена')


bot.polling(none_stop=True, interval=5)