from downloader import Downloader
from playlist_creator import PlaylistMaker


def main() -> None:
    pm = PlaylistMaker()

    user_id = input("Type your VK_ID. Audios shouldn't be private: ")

    try:
        user_id = int(user_id)
    except ValueError:
        print('Invalid VK_ID')
        return

    file_name = pm.create_playlist_file(user_id)

    dl = Downloader('music', file_name, 30)

    dl.run()


if __name__ == '__main__':
    main()
