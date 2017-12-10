import sqlite3


def add_item(update):
    # print(update)
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    try:
        cursor.execute('''CREATE TABLE users (chat_id, mess_id, text, user, name1, name2)''')
    except sqlite3.OperationalError:
        pass
    mess = update.message
    chat_id = mess.chat.id
    # print('chat_id:',chat_id)
    mess_id = mess.message_id
    # print('mess_id:',mess_id)
    text = mess.text
    # print('text:',text)
    username = mess.chat.username
    # print('user:',username)
    name1 = mess.chat.first_name
    # print('1name:',name1)
    name2 = mess.chat.last_name
    # print('2name:',name2)
    cursor.execute("INSERT INTO users VALUES (?,?,?,?,?,?)", (chat_id, mess_id, text, username, name1, name2))
    conn.commit()
    conn.close()
