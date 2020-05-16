# coding=utf-8
import random
from db_utils import get_free_key_ids, add_key


def log_error(f):
    def inner(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            print(f'Ошибка: {e}')
            raise e

    return inner


def get_random_free_id():
    ids_list = get_free_key_ids()
    random.shuffle(ids_list)
    return ids_list[0]


def fill_db():
    file = open('keys_to_add.txt', encoding='utf-8')
    for line in file.read().split("\n"):
        if line != '':
            add_key(key=line)
