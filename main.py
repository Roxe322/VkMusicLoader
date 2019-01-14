from playlist_creator import PlaylistMaker
from downloader import Downloader
import requests

pm = PlaylistMaker('443da9309bc9d10369b77f5f02158c16663f6b00cdf6ee2c1176f1b1f71dc15d09115fa2dbdf7117949ba')

file_name = pm.create_playlist_file(9693122)


dl = Downloader('music', file_name, 30)

dl.run()