import configparser


def change_proxy():
    # Чтение файла .ini
    config = configparser.ConfigParser()
    config.read("Configs/ukrProxy.ini")

    # Вывод содержимого файла .ini
    for section in config.sections():
        print(f"[{section}]")
        for key, value in config.items(section):
            print(f"{key} = {value}")
        print()

    answer = input("Do you want change proxy ? (Y/N):")
    if answer != "Y" or "y":
        return

    # Изменение данных
    # section_name = input("Введите название секции, которую хотите изменить: ")
    section_name = "Proxy"
    if section_name in config.sections():
        for key in config[section_name]:
            new_value = input(f"Enter new value for key '{key}': ")
            config.set(section_name, key, new_value)
    # Сохранение изменений в файл .ini
    with open("file.ini", "w") as config_file:
        config.write(config_file)

    print("\nConfig proxy succesfuly changed!\n")
    for section in config.sections():
        print(f"[{section}]")
        for key, value in config.items(section):
            print(f"{key} = {value}")
        print()
