import configparser
import asyncio
from telethon.sync import TelegramClient
from telethon.tl.types import InputChannel
from telethon.tl.types import ChannelParticipantsAdmins
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.account import UpdateStatusRequest, UpdateProfileRequest
from MODULES.load_save_data import load_data


async def join_channel(sess_names, change_name_boolean):
    profile_count = len(sess_names)
    config = configparser.ConfigParser()
    config.read("Configs/config.ini")

    configWorker = configparser.ConfigParser()
    configWorker.read("Configs/ownWorkerConfig.ini")

    configProxy = configparser.ConfigParser()
    configProxy.read("Configs/ukrProxy.ini")

    # Параметры прокси
    proxy_host = configProxy["Proxy"]["proxy_host"]
    proxy_port = int(configProxy["Proxy"]["proxy_port"])
    proxy_username = configProxy["Proxy"]["proxy_username"]
    proxy_password = configProxy["Proxy"]["proxy_password"]
    group_id = config["Config"]["group_that_id"]

    proxy = {
        "proxy_type": "socks5",  # (mandatory) protocol to use (see above)
        "addr": proxy_host,  # (mandatory) proxy IP address
        "port": proxy_port,  # (mandatory) proxy port number
        "username": proxy_username,  # (optional) username if the proxy requires auth
        "password": proxy_password,  # (optional) password if the proxy requires auth
        "rdns": True,  # (optional) whether to use remote or local resolve, default remote
    }
    profile_index = 0
    for profile in sess_names:
        session_data = load_data(f"Sessions/sessJson/{profile}.json")

        api_id = session_data["app_id"]
        api_hash = session_data["app_hash"]
        device_model = session_data["sdk"]
        device_version = session_data["app_version"]

        session_file = f"Sessions/sessJson/{profile}.session"

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

            if change_name_boolean == True:
                new_name = input(f"New name for {profile}: ")
                try:
                    await client(
                        UpdateProfileRequest(first_name=new_name, last_name="")
                    )
                    print(f"Name successfully changed to: {new_name}")
                except asyncio.IncompleteReadError as e:
                    print("Error reading data: 0 bytes read out of expected 8 bytes.")
                except Exception as e:
                    print(f"Failed to change name. Error: {str(e)}")

            group_entity = await client.get_entity(group_id)
            result = await client(JoinChannelRequest(group_entity))
            print(f"Successfully joined the group in session: {profile}")
            # if isinstance(result, InputChannel) or isinstance(
            #     result, ChannelParticipantsAdmins
            # ):
            #     print(f"Successfully joined the group in session: {profile}")
            # else:
            #     print(f"Admin confirmation required in session: {profile}")
        except Exception as e:
            print(f"Failed to join the group in session: {profile}")
            print(f"Error: {str(e)}")
        await client(UpdateStatusRequest(offline=True))
        client.disconnect()
        profile_index += 1

        if profile_index == profile_count:
            print("All profiles added to group")
