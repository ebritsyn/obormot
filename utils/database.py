import sqlite3


class DbConnection:
    def __init__(self, database):
        self.connection = sqlite3.connect(database, check_same_thread=False)
        self.cursor = self.connection.cursor()
        self.connection.execute("PRAGMA foreign_keys=ON")

    def start(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                                id INTEGER PRIMARY KEY,
                                    user TEXT,
                                 name1 TEXT, name2 TEXT)''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS messages
                                (id INTEGER PRIMARY KEY,
                                 text TEXT, user_id INTEGER,
                                FOREIGN KEY(user_id) REFERENCES users(id))''')

    def add_user(self, username, name1, name2, chat_id):
        try:
            self.cursor.execute("INSERT INTO users VALUES (?,?,?,?)",
                                (int(chat_id), username,
                                 name1, name2))
        except (sqlite3.OperationalError, sqlite3.IntegrityError):
            print('user_already_in_base')

        self.connection.commit()

    def add_message(self, mess_id, text, chat_id):
        self.cursor.execute("INSERT INTO messages VALUES (?,?,?)",
                            (mess_id, text, chat_id))

        self.connection.commit()
