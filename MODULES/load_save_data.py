import json


def convert_format(usernames):
    if isinstance(usernames, list):
        converted_usernames = {
            str(i + 1): username for i, username in enumerate(usernames)
        }
        return converted_usernames
    else:
        return usernames


# Загрузка информации о пользователях из JSON файла
def load_data(file_name):
    with open(file_name, "r") as file:
        usernames = json.load(file)
    return usernames


# Загрузка информации о пользователях из JSON файла
def load_list_data(file_name):
    with open(file_name, "r") as file:
        usernames = json.load(file)
        usernames = convert_format(usernames)
    return usernames


def load_invited_users(file_name):
    try:
        with open(file_name, "r") as file:
            invited_users = json.load(file)  ##### NYJNO IZMENIT INVITED NA DATA
    except FileNotFoundError:
        invited_users = []
    return invited_users


def save_data(path_name, data):
    with open(path_name, "w") as file:
        json.dump(data, file)


# Сохранение остановки выполнения и неприглашенных пользователей
def save_checkpoint(file_name, start_index, uninvited_users):
    data = {"start_index": start_index, "uninvited_users": uninvited_users}
    with open(file_name, "w") as file:
        json.dump(data, file)


# Загрузка остановки выполнения и неприглашенных пользователей
def load_checkpoint(file_name):
    try:
        with open(file_name, "r") as file:
            data = json.load(file)
            start_index = data["start_index"]
            uninvited_users = data["uninvited_users"]
    except FileNotFoundError:
        start_index = 0
        uninvited_users = []
    return start_index, uninvited_users
