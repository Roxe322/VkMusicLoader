from downloader import Downloader
from playlist_creator import PlaylistMaker

pm = PlaylistMaker()

file_name = pm.create_playlist_file(9693122)


dl = Downloader('music', file_name, 30)

dl.run()
