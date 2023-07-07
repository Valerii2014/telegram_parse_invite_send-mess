import configparser


def update_config_value():
    config_file = "Configs/config.ini"
    config = configparser.ConfigParser()
    config.read(config_file)

    print("[Config]")
    num_config = 1
    for key in config["Config"]:
        print(f"{num_config}. {key} = {config['Config'][key]}")
        num_config += 1
    print()

    while True:
        try:
            field_num = int(input("Enter the field number to update (0 to exit): "))
            if field_num == 0:
                break
            elif 0 < field_num < len(config["Config"]):
                field_name = list(config["Config"].keys())[field_num - 1]
                new_value = input(f"Enter the new value for {field_name}: ")
                config["Config"][field_name] = new_value
                with open(config_file, "w") as f:
                    config.write(f)
                print("Value updated.")
            else:
                print("Invalid field number. Please try again.")
        except ValueError:
            print("Incorrect input. Enter a number.")