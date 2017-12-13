import sqlite3


class DbConnection:
    def __init__(self, database):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()
        self.connection.execute("PRAGMA foreign_keys=ON")

    def add_user(self, update):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                                id INTEGER PRIMARY KEY,
                                    user TEXT,
                                 name1 TEXT, name2 TEXT)''')

        mess = update.message
        username = mess.chat.username
        name1 = mess.chat.first_name
        name2 = mess.chat.last_name
        chat_id = mess.chat.id
        try:
            self.cursor.execute("INSERT INTO users VALUES (?,?,?,?)",
                                (int(chat_id), str(username),
                                 str(name1), str(name2)))
        except (sqlite3.OperationalError, sqlite3.IntegrityError):
            print('user_already_in_base')

        self.connection.commit()

    def add_message(self, update):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS messages
                                (id INTEGER PRIMARY KEY,
                                 text TEXT, user_id INTEGER,
                                FOREIGN KEY(user_id) REFERENCES users(id))''')

        mess = update.message
        mess_id = mess.message_id
        text = mess.text
        chat_id = mess.chat.id

        self.cursor.execute("INSERT INTO messages VALUES (?,?,?)",
                            (mess_id, text, chat_id))

        self.connection.commit()
