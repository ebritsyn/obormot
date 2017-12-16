import sys
from bot.bot import Bot


def main():
    obormot = Bot(sys.argv[1])
    obormot.start()


if __name__ == '__main__':
    main()
