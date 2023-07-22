import random
import asyncio
import configparser
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.account import UpdateStatusRequest, UpdateProfileRequest
from MODULES.load_save_data import load_data
from MODULES.client_create import create_client



async def join_channel(sess_names, change_name_boolean, application_profile):

    config = configparser.ConfigParser()
    config.read("Configs/config.ini")


    session_index = 0
    session_count = len(sess_names)
    group_id = config["Link_for_profiles"][application_profile]

    first_names_list = load_data("jsonDB/profileNames/firstNames.json")
    second_names_list = load_data("jsonDB/profileNames/secondNames.json")


    def name_generator():
        first_index = random.randint(1, (len(first_names_list) - 1))
        second_index = random.randint(1, (len(second_names_list) - 1))
        return first_names_list[first_index], second_names_list[second_index]


    for session in sess_names:        
         
        print(f'{session}')
        session_index += 1

        client = create_client(session)

        try:
            await client.connect()
            await client(UpdateStatusRequest(offline=False))

            if change_name_boolean == True:
                # new_name = input(f"New name for {session}: ")
                first_name, second_name = name_generator()
                try:
                    await client(
                        UpdateProfileRequest(first_name=first_name, last_name=second_name)
                    )
                    print(f"Name successfully changed to: {first_name} {second_name}")
                except asyncio.IncompleteReadError as e:
                    print("Error reading data: 0 bytes read out of expected 8 bytes.")
                except Exception as e:
                    print(f"Failed to change name. Error: {str(e)}")

            group_entity = await client.get_entity(group_id)
            result = await client(JoinChannelRequest(group_entity))
            print(f"Successfully joined the group in session: {session}")
            await client(UpdateStatusRequest(offline=True))

        except Exception as e:
            print(f"Failed to join the group in session: {session}")
            print(f"Error: {str(e)}")

        client.disconnect()
        print('\n')

        if session_index == session_count:
            print("\nAll sessions added to group")
