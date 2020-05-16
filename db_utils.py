import sqlite3

__connection = None


def ensure_connection(function):
    def inner(*args, **kwargs):
        with sqlite3.connect('keys_storage.db') as conn:
            result = function(*args, conn=conn, **kwargs)
        return result

    return inner


@ensure_connection
def init_db(conn, force: bool = False):
    c = conn.cursor()

    if force:
        c.execute('DROP TABLE IF EXISTS valid_keys')

    c.execute('''
        CREATE TABLE IF NOT EXISTS valid_keys (
            id          INTEGER PRIMARY KEY,
            user_id     TEXT,
            key TEXT    NOT NULL
        )
    ''')

    conn.commit()


@ensure_connection
def add_key(conn, key: str):
    c = conn.cursor()
    c.execute('INSERT INTO valid_keys (user_id, key) VALUES (?, ?)', (None, key))
    conn.commit()


@ensure_connection
def return_key_by_id(conn, id: int):
    c = conn.cursor()
    c.execute('SELECT key FROM valid_keys WHERE id = ?', (id,))
    (res,) = c.fetchone()
    return res


@ensure_connection
def return_key_by_user_id(conn, user_id: int):
    c = conn.cursor()
    c.execute('SELECT key FROM valid_keys WHERE user_id = ?', (user_id,))
    (res,) = c.fetchone()
    return res


@ensure_connection
def count_keys(conn):
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM valid_keys')
    (res,) = c.fetchone()
    return res


@ensure_connection
def count_free_keys(conn):
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM valid_keys WHERE user_id is NULL')
    (res,) = c.fetchone()
    return res


@ensure_connection
def list_keys(conn):
    c = conn.cursor()
    c.execute('SELECT id, key FROM valid_keys')
    return c.fetchall()


@ensure_connection
def get_free_key_ids(conn):
    c = conn.cursor()
    c.execute('SELECT id FROM valid_keys WHERE user_id is NULL')
    raw_list = c.fetchall()
    keys_list = []
    for i in range(len(raw_list)):
        keys_list.append(raw_list[i][0])
    return keys_list


@ensure_connection
def book_free_key(conn, user_id: str, id: int):
    c = conn.cursor()
    c.execute('UPDATE valid_keys SET user_id = ? WHERE id = ?', (user_id, id))
    conn.commit()


@ensure_connection
def check_user_has_key(conn, user_id: str):
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM valid_keys WHERE user_id = ?', (user_id,))
    (res,) = c.fetchone()
    if res > 0:
        return True
    else:
        return False
