from time import sleep
from collections import OrderedDict
import json
from datetime import datetime
from typing import Union

import requests

# TODO Also save thumbnails of albums


class PlaylistMaker:

    def __init__(self, token: str) -> None:
        self.token = token

    @staticmethod
    def group(lst: list, n: int):
        """ Split provided lst to groups with n elements"""
        return [lst[i:i + n] for i in range(0, len(lst), n)]

    def create_playlist_file(self, user_id: Union[int, str]) -> str:
        # Probably it is better to separate it all to different methods

        all_music_link = f'https://api.vk.com/method/audio.get?owner_id={user_id}&access_token={self.token}&v=5.85'
        all_music = requests.get(all_music_link).json()['response']['items']
        song_ids = []

        # Create unique song ids
        for song in all_music:
            if not song.get('access_key'):
                continue
            access_key = song['access_key']
            song_id = song['id']
            song_ids.append(f'{user_id}_{song_id}_{access_key}')

        splited_song_ids = self.group(song_ids, 200)  # Grouping ids because of VK API limits for songs in one request

        result = OrderedDict()  # OrderedDict here and below is to specify order of songs like in a real playlist

        for chunk in splited_song_ids:
            # Making one request to get data for each 200 songs
            ids_for_request = ','.join(chunk)
            data = {'audios': ids_for_request, 'access_token': self.token, 'v': '5.85'}
            songs_with_urls = requests.post('https://api.vk.com/method/audio.getById', data=data).json()['response']

            sleep(0.5)  # Excepting VK API rate limit

            # Getting only needed data for each song to create a beautiful playlist file
            for song in songs_with_urls:
                id_ = song['id']
                author = song.get('artist')
                title = song.get('title')
                src = song.get('url')
                if not src:
                    is_blocked = True
                else:
                    is_blocked = False
                restricted_symbols = ['\\', '/', ':', '*', '"', '?', '<', '>', '|']
                for symbol in restricted_symbols:
                	author = author.replace(symbol, "")
                	title = title.replace(symbol, "")
                needed_data = OrderedDict(author=author, title=title, src=src, is_blocked=is_blocked)
                result[id_] = needed_data

        datetime_now = datetime.now()
        file_name = f"playlist_id{user_id}_({datetime_now.day}.{datetime_now.month}.{datetime_now.year}).json"
        with open(file_name, "w", encoding='UTF-8') as file:
            file.write(json.dumps(list(result.values()), indent=4, ensure_ascii=False))

        print('Playlist created')  # TODO change to logging
        return file_name
