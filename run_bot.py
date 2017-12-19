import os
from bot.bot import Bot

def main():
    token = os.environ.get('TOKEN', None)
    db = os.environ.get('DB', 'data.db')
    if token is None:
        print('Please set TOKEN as environment variable')
    else:
        obormot = Bot(token, db)
        obormot.start()

if __name__ == '__main__':
    main()
