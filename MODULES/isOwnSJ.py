import asyncio
import json
import datetime
from telethon.sync import TelegramClient
from telethon.tl.functions.account import UpdateStatusRequest
import configparser
from MODULES.invite_user import invite_users, send_users, invite_send_users
from MODULES.load_save_data import (
    load_data,
    load_list_data,
    load_invited_users,
    save_data,
    save_checkpoint,
    load_checkpoint,
)


async def inviteSJ(list_name, doing):
    configWorker = configparser.ConfigParser()
    configWorker.read("Configs/sessionConfig.ini")

    configProxy = configparser.ConfigParser()
    configProxy.read("Configs/ukrProxy.ini")

    config = configparser.ConfigParser()
    config.read("Configs/config.ini")

    # Параметры прокси
    proxy_host = configProxy["Proxy"]["proxy_host"]
    proxy_port = int(configProxy["Proxy"]["proxy_port"])
    proxy_username = configProxy["Proxy"]["proxy_username"]
    proxy_password = configProxy["Proxy"]["proxy_password"]

    json_name = list_name

    iteration_for_profile = int(config["Config"]["iteration_for_profile"])
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    excluded_sessions = []
    profiles_iteration = 0

    profile_count = len(configWorker.sections())
    if profile_count == 0:
        print(
            'You has no sessions file, start "Add new sess" or add session file to folder sessJson'
        )

    group_id = config["Config"]["group_that_id"]
    flood_rest = int(config["Config"]["flood_rest"])

    usernames = load_list_data(f"jsonDB/sparsedChannelsUsers/{json_name}.json")
    uninvited_users = load_data("jsonDB/sparsedChannelsUsers/uninvited_users.json")
    invited_users = load_invited_users("jsonDB/invited_users.json")
    flood_list = load_invited_users("jsonDB/flood_list.json")

    proxy = {
        "proxy_type": "socks5",  # (mandatory) protocol to use (see above)
        "addr": proxy_host,  # (mandatory) proxy IP address
        "port": proxy_port,  # (mandatory) proxy port number
        "username": proxy_username,  # (optional) username if the proxy requires auth
        "password": proxy_password,  # (optional) password if the proxy requires auth
        "rdns": True,  # (optional) whether to use remote or local resolve, default remote
    }

    profile_index = 0
    while profile_index < profile_count:
        profile = configWorker.sections()[profile_index]

        if profiles_iteration >= iteration_for_profile:
            print(f"All sessionss sent: {iteration_for_profile} invite ")
            return

        if len(excluded_sessions) >= profile_count:
            print("All sessions have a spam block =(")
            return

        print(f"Profile:  {profile}          [{profile_index + 1}/{profile_count}]")

        if profile in excluded_sessions:
            profile_index = (profile_index + 1) % profile_count
            continue

        found_flood_session = False
        for flood_session in flood_list:
            if flood_session[0] == profile:
                flood_timestamp = datetime.datetime.strptime(
                    flood_session[1], "%Y-%m-%d %H:%M:%S"
                )
                current_timestamp = datetime.datetime.now()
                time_diff = current_timestamp - flood_timestamp
                if time_diff < datetime.timedelta(hours=flood_rest):
                    waitTime = datetime.timedelta(hours=flood_rest) - time_diff
                    print(
                        f"{profile} will be unlocked through: - - - - - - - - - - - - - - - {waitTime}"
                    )
                    found_flood_session = True
                    break
                else:
                    print(f"{profile} is unlocked !")
                    flood_list.remove(flood_session)
                    save_data("jsonDB/flood_list.json", flood_list)

        if found_flood_session:
            excluded_sessions.append(profile)
            profile_index = (profile_index + 1) % profile_count
            continue

        session_data = load_data(f"Sessions/sessJson/{profile}.json")

        api_id = session_data["app_id"]
        api_hash = session_data["app_hash"]
        phone_number = session_data["phone"]
        password = "206473"
        device_model = session_data["sdk"]
        device_version = session_data["app_version"]
        system_lang = session_data["system_lang_pack"]

        session_file = f"Sessions/sessJson/{profile}.session"
        start_index, uninvited_local_users = load_checkpoint(
            f"jsonDB/archiveChekpoint/checkpointIS{json_name}.json"
        )

        client = TelegramClient(
            session_file,
            api_id,
            api_hash,
            proxy=proxy,
            device_model=device_model,
            app_version=device_version,
        )
        try:
            await client.connect()
            await client(UpdateStatusRequest(offline=False))
            if doing == "invite":
                (
                    remaining_usernames,
                    new_invited_users,
                    flood,
                    counter,
                ) = await invite_users(
                    client,
                    usernames,
                    start_index,
                    group_id,
                    profile,
                    profile_count,
                )
            elif doing == "send":
                (
                    remaining_usernames,
                    new_invited_users,
                    flood,
                    counter,
                ) = await send_users(
                    client,
                    usernames,
                    start_index,
                    group_id,
                    profile,
                    profile_count,
                )
            elif doing == "invite_send":
                (
                    remaining_usernames,
                    new_invited_users,
                    flood,
                    counter,
                ) = await invite_send_users(
                    client,
                    usernames,
                    start_index,
                    group_id,
                    profile,
                    profile_count,
                )
            else:
                print("ERROR not send, not invite, not invite_send!")

        except asyncio.IncompleteReadError as e:
            print("Error reading data: 0 bytes read out of expected 8 bytes.")
            print("Reason:", str(e))

        finally:
            await client(UpdateStatusRequest(offline=True))
            client.disconnect()

        if flood is True:
            flood_list.append(
                (profile, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            )
            with open("jsonDB/flood_list.json", "w") as file:
                json.dump(flood_list, file)
            excluded_sessions.append(profile)
            continue

        if remaining_usernames is not None:
            uninvited_users.extend(remaining_usernames)

        if new_invited_users is not None:
            invited_users.extend(new_invited_users)

        save_checkpoint(
            f"jsonDB/archiveChekpoint/checkpointIS{json_name}.json",
            (start_index + counter) % len(usernames),
            remaining_usernames,
        )

        if len(uninvited_users) > 0:
            with open("jsonDB/sparsedChannelsUsers/uninvited_users.json", "w") as file:
                json.dump(uninvited_users, file)

        # Сохранить приглашенных пользователей в отдельный JSON-файл
        if len(invited_users) > 0:
            save_data("jsonDB/invited_users.json", invited_users)

        profile_index = (
            profile_index + 1
        ) % profile_count  # Перейти к следующему профилю

        if (profile_index + 1) % profile_count == 0:
            profiles_iteration += 1  # Увеличиваем значение profiles_iteration при начале нового круга сесси
            print("All profiles have been processed. Starting from the first profile.")
