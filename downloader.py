import asyncio
import json
import os
from typing import List, Coroutine, Dict, Union

import tqdm
import aiohttp


class Downloader:

    def __init__(self, download_to_folder: str, playlist_file_name: str, thread_limit: int) -> None:
        self.folder = download_to_folder
        self.file = playlist_file_name
        self.semaphore = asyncio.BoundedSemaphore(thread_limit)
        with open(self.file, encoding='UTF-8') as json_file_playlist:
            self.playlist = json.loads(json_file_playlist.read())
        os.makedirs(self.folder, exist_ok=True)

    async def wait_with_progress(self, coros: List[Coroutine]):
        for song in tqdm.tqdm(asyncio.as_completed(coros), total=len(coros), desc="Songs"):
            await song

    async def download_file(self, song: Dict[str, Union[str, bool]]):
        async with aiohttp.ClientSession() as session:
            async with self.semaphore, session.get(song['src']) as response:
                song_bin = await response.read()
                with open(f"{self.folder}/{self.playlist.index(song)+1}. {song['author']} - {song['title']}.mp3",
                          "wb") as file:
                    file.write(song_bin)

    def run(self):
        loop = asyncio.get_event_loop()
        f = [self.download_file(song) for song in self.playlist if song['src'] is not None and not song['is_blocked']]

        f = self.wait_with_progress(f)
        loop.run_until_complete(f)
