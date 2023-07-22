import configparser
from telethon.sync import TelegramClient
from MODULES.load_save_data import load_data



def create_client (profile):

    # Параметры прокси
    configProxy = configparser.ConfigParser()
    configProxy.read("Configs/ukrProxy.ini")
    proxy_host = configProxy["Proxy"]["proxy_host"]
    proxy_port = int(configProxy["Proxy"]["proxy_port"])
    proxy_username = configProxy["Proxy"]["proxy_username"]
    proxy_password = configProxy["Proxy"]["proxy_password"]

    proxy = {
        "proxy_type": "socks5",  # (mandatory) protocol to use (see above)
        "addr": proxy_host,  # (mandatory) proxy IP address
        "port": proxy_port,  # (mandatory) proxy port number
        "username": proxy_username,  # (optional) username if the proxy requires auth
        "password": proxy_password,  # (optional) password if the proxy requires auth
        "rdns": True,  # (optional) whether to use remote or local resolve, default remote
    }


    session_file = f"Sessions/sessJson/{profile}.session"
    session_data = load_data(f"Sessions/sessJson/{profile}.json")


    api_id = session_data["app_id"]
    api_hash = session_data["app_hash"]
    phone_number = session_data["phone"]
    password = "206473"
    device_model = session_data["sdk"]
    device_version = session_data["app_version"]
    system_lang = session_data["system_lang_pack"]


    client = TelegramClient(
                session_file,
                api_id,
                api_hash,
                proxy=proxy,
                device_model=device_model,
                app_version=device_version,
            )
    
    return client