import asyncio
import json
import datetime
from telethon.sync import TelegramClient
from telethon.tl.functions.account import UpdateStatusRequest
import configparser
from MODULES.invite_user import invite_users, send_users, invite_send_users
from MODULES.client_create import create_client
from MODULES.load_save_data import (
    load_data,
    load_list_data,
    load_invited_users,
    save_data,
    save_checkpoint,
    load_checkpoint,
)

async def inviteSJ(list_name, doing, application_profile):
   
    config = configparser.ConfigParser()
    configWorker = configparser.ConfigParser()

    config.read("Configs/config.ini")
    configWorker.read("Configs/sessionConfig.ini")

    flood_rest = int(config["Config"]["flood_rest"])
    group_id = config["Link_for_profiles"][application_profile]
    iteration_for_profile = int(config["Config"]["iteration_for_profile"])

    profile_count = len(configWorker.sections())
    if profile_count == 0:
        print(
            'You has no sessions file, start "Add new sess" or add session file to folder sessJson'
        )
        
    flood_list = load_invited_users("jsonDB/flood_list.json")
    usernames = load_list_data(f"jsonDB/sparsedChannelsUsers/{list_name}.json")
    uninvited_users = load_data(f"jsonDB/profiles_data/{application_profile}/uninvited_users_{application_profile}.json")
    invited_users = load_invited_users(f"jsonDB/profiles_data/{application_profile}/invited_users_{application_profile}.json")

    profile_index = 0
    profiles_iteration = 0
    excluded_sessions = []

    while profile_index < profile_count:
        profile = configWorker.sections()[profile_index]

        if profiles_iteration >= iteration_for_profile:
            print(f"\nAll sessionss sent: {iteration_for_profile} invite ")
            return

        if len(excluded_sessions) >= profile_count:
            print("\nAll sessions have a spam block =(")
            return

        print(f"\nProfile:  {profile}          [{profile_index + 1}/{profile_count}]")

        if profile in excluded_sessions:
            profile_index = (profile_index + 1) % profile_count
            print("This profile excluded for these iterations")
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
                    
                    hours = waitTime.seconds // 3600
                    minutes = (waitTime.seconds // 60) % 60
                    seconds = waitTime.seconds % 60
                    waitTime_str = f"{hours:02}:{minutes:02}:{seconds:02}"
                    
                    found_flood_session = True
                    print(
                        f"{profile} will be unlocked through: - - - - - - - - - - - - - - - {waitTime_str}"
                    )
                    break
                else:
                    print(f"{profile} is unlocked !")
                    flood_list.remove(flood_session)
                    save_data("jsonDB/flood_list.json", flood_list)

        if found_flood_session:
            excluded_sessions.append(profile)
            profile_index = (profile_index + 1) % profile_count
            continue

        start_index, uninvited_local_users = load_checkpoint(
            f"jsonDB/profiles_data/{application_profile}/archiveChekpoint/CP_{list_name}_for_{application_profile}.json"
        )

        client = create_client(profile)
       
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
                print("ERROR 3th argument may be only - send / invite / invite_send")

        except asyncio.IncompleteReadError as e:
            print("Error reading data: 0 bytes read out of expected 8 bytes.")
            print("Reason:", str(e))
        except Exception as e:
            excluded_sessions.append(profile)
            profile_index = (profile_index + 1) % profile_count
            remaining_usernames = []
            new_invited_users = []
            flood = True
            counter = 0
        finally:
            try:
                await client(UpdateStatusRequest(offline=True))
                client.disconnect()
            except:
                print('May be session is dead')


        if isinstance(flood, bool) == False:
            flood_list.append(
                (
                    profile,
                    (datetime.datetime.now() - datetime.timedelta(hours=flood_rest) +
                    datetime.timedelta(seconds=flood)).strftime("%Y-%m-%d %H:%M:%S")
                )
            )
            with open("jsonDB/flood_list.json", "w") as file:
                json.dump(flood_list, file)
            continue

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
            f"jsonDB/profiles_data/{application_profile}/archiveChekpoint/CP_{list_name}_for_{application_profile}.json",
            (start_index + counter) % len(usernames),
            remaining_usernames,
        )

        if len(uninvited_users) > 0:
            with open(f"jsonDB/profiles_data/{application_profile}/uninvited_users_{application_profile}.json", "w") as file:
                json.dump(uninvited_users, file)

        # Сохранить приглашенных пользователей в отдельный JSON-файл
        if len(invited_users) > 0:
            save_data(f"jsonDB/profiles_data/{application_profile}/invited_users_{application_profile}.json", invited_users)

        if (profile_index + 1) == profile_count:
            profiles_iteration += 1
            profile_index = 0
            print("All profiles have been processed. Starting from the first profile.")
        else:
            profile_index += 1