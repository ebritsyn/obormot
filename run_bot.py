import os
from bot.bot import Bot


def main():
    token = os.environ.get('TOKEN', None)
    dbase = os.environ.get('DB', 'data.db')
    if token is None:
        print('Please set TOKEN as environment variable')
    else:
        obormot = Bot(token, dbase)
        obormot.start()


if __name__ == '__main__':
    main()
