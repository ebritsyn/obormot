import sys
from bot.bot import Bot


if __name__ == '__main__':
    obormot = Bot(sys.argv[1])
    obormot.start()
