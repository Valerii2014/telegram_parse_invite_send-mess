import configparser
import json
from pathlib import Path
from telethon.sync import TelegramClient
from telethon.errors.rpcerrorlist import ChannelPrivateError


async def parser_channel():
    config = configparser.ConfigParser()
    config.read("Configs/config.ini")

    configWorker = configparser.ConfigParser()
    configWorker.read("Configs/sparserConfig.ini")

    api_id = configWorker["SparserWorker"]["api_id"]
    api_hash = configWorker["SparserWorker"]["api_hash"]

    # Введите путь к файлу сессии Telegram (для сохранения авторизационных данных)
    session_file = "Sessions/parser_session/undefined.session"

    group_id = input("Give me link to Telegram group: ")
    group_name = group_id.split("/")[-1]
    limit = int(input("How much messages i have check: "))
    group_names = config["Group_names"]

    names_array = [group_names[key] for key in group_names]

    def get_user_choice():
        choice = input("Do you want parse this group again ? (Y/N):")
        return choice

    # Создайте Telegram-клиента и подключитесь
    client = TelegramClient(session_file, api_id, api_hash)
    await client.connect()
    # Получите информацию о группе
    try:
        entity = await client.get_entity(group_id)
    except ValueError as e:
        print(f"Error: {str(e)}")
        entity = None

    if entity:
        # Обрезаем ссылку и сохраняем в файл INI
        if group_name not in names_array:
            config.set("Group_names", str(len(group_names) + 1), group_name)
            with open("Configs/config.ini", "w") as config_file:
                config.write(config_file)
        else:
            print(f"{group_name} has already been parsed !")
            answer_parse = get_user_choice()
            if answer_parse == "Y" or answer_parse == "y":
                file_path = Path(
                    f"jsonDB/archiveChekpoint/checkpointIS{group_name}.json"
                )
                # Проверяем, существует ли файл
                if file_path.exists():
                    # Удаляем файл
                    file_path.unlink()
                    print(f"\nFile succesfuly deleted: {file_path}\n")

                else:
                    print(f"\nFile not found: {file_path}\n")
            else:
                client.disconnect()
                return

        print("Getting messages...")
        messages = await client.get_messages(entity, limit=limit)
        print("Done!")

        # Создайте словарь для хранения данных
        users = {}
        unique_users = set()
        counter = 1
        for index, message in enumerate(messages, start=1):
            try:
                if (
                    message.sender_id not in unique_users
                    and message.sender_id is not None
                ):
                    unique_users.add(message.sender_id)
                    user = await client.get_entity(message.sender_id)
                    if user.username:
                        users[counter] = user.username
                        counter += 1
            except ChannelPrivateError as e:
                print(f"Error: {str(e)}. Skipping message {index}")

            # Display progress update
            print(f"Processed message {index}/{limit}", end="\r")

        # Print a new line after processing is complete
        print()

        # Сохраните словарь в файл JSON
        with open(f"jsonDB/sparsedChannelsUsers/{group_name}.json", "w") as file:
            json.dump(users, file)

        print(
            f"{len(users)} usernames were be succesfuly saved to jsonDB/sparsedChannelsUsers/{group_name}.json"
        )
    client.disconnect()
