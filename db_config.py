import sqlite3

PATH = 'db/database.db'
connect = sqlite3.connect(PATH)
cursor = connect.cursor()

def create_table():
    cursor.execute('DROP TABLE IF EXISTS proceduri')
    cursor.execute('''CREATE TABLE IF NOT EXISTS worker (tg_id INTEGER PRIMARY KEY AUTOINCREMENT, list_photo VARCHAR, 
    list_video VARCHAR, list_docs VARCHAR, list_audio VARCHAR, list_voice VARCHAR)''')
    connect.commit()



def add_new_worker(new_worker: tuple):
    cursor.execute(
        '''INSERT INTO worker (tg_id, list_docs) VALUES (?, ?)
         ON CONFLICT (tg_id) DO UPDATE
                    SET 
                    list_docs=list_docs''', new_worker)
    connect.commit()

def get_list(tg_id:tuple, column:str):
    old_list = cursor.execute(f'SELECT {column} FROM worker WHERE tg_id=?', tg_id).fetchall()
    return old_list


def update_list(new_data: tuple, column:str):
    cursor.execute(f'UPDATE worker SET {column}=? WHERE tg_id=?', new_data)
    connect.commit()