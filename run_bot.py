import os
from bot.bot import Bot

def main():
    TOKEN = os.environ.get('TOKEN', None)
    DB = os.environ.get('DB', 'data.db')
    if TOKEN == None:
        print('Please set TOKEN as environment variable')
    else:
        obormot = Bot(TOKEN,DB)
        obormot.start()

if __name__ == '__main__':
    main()
