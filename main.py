import sys
import asyncio
import datetime
import configparser
from MODULES.isOwn2 import inviteMy
from MODULES.isOwnSJ import inviteSJ
from MODULES.sparser import parser_channel
from MODULES.change_proxy import change_proxy
from MODULES.addNewSessToConfig import addNewSess
from MODULES.screen_saver import disable_screen_saver
from MODULES.change_config import update_config_value

class Tee:
    def __init__(self, *files):
        self.files = files

    def write(self, text):
        for file in self.files:
            file.write(text)

    def flush(self):
        for file in self.files:
            file.flush()

config = configparser.ConfigParser()
config.read("./Configs/config.ini")

# Открытие файла для записи
logfilename = datetime.datetime.now().strftime("%Y-%m-%d %H_%M_%S")
logfilename = logfilename.replace(":", "_")  # Замена недопустимых символов
output_file = open(f"jsonDB/logs_data/{logfilename}.txt", "w")

def get_user_choice():
    choice = input("Your choise (get me variant number): ")
    return choice


def display_profile_names():
    profile_names = config["Profiles_for_application"]
    print("\nProfile Names:")
    for key, value in profile_names.items():
        print(f"{key}. {value}")
    print()
    return profile_names
        

def display_group_names():
    group_names = config["Group_names"]
    print("\nGroup Names:")
    for key, value in group_names.items():
        print(f"{key}. {value}")
    print()
    return group_names


async def main():
    # Перенаправление стандартного потока вывода на файл и консоль
    sys.stdout = Tee(sys.stdout, output_file)

    disable_screen_saver()

    profile = False
    while profile == False:
        profile_names = display_profile_names()
        profile_choice = get_user_choice()
        try:
            profile = profile_names[profile_choice]
        except:
            print('\nTry again!\n')
        
    while True:
        print(f"\n \nPROFILE: {profile}")
        print("\nMake your choise:\n")

        print("1. Parsing")
        print("2. Invite")
        print("3. Send messages")
        print("4. Invite + send messages")
        print("5. Add new sess")
        print("6. Change proxy")
        print("7. Change config")
        print("0. Exit\n")

        choice = get_user_choice()

        if choice == "1":
            print("\n")

            await parser_channel()

        elif choice == "2":
            group_names = display_group_names()
            group_choice = get_user_choice()
            print("\n1 - my session")
            print("2 - russ session\n")
            sessions_choise = get_user_choice()
            if group_choice in group_names:
                print("\nInviting Starting....\n")
                if sessions_choise == "1":
                    await inviteMy(group_names[group_choice])
                else:
                    await inviteSJ(group_names[group_choice], "invite", profile)
            else:
                print("Invalid group choice.")

        elif choice == "3":
            group_names = display_group_names()
            group_choice = get_user_choice()
            if group_choice in group_names:
                print("\nSend messages Starting....\n")
                await inviteSJ(group_names[group_choice], "send", profile)
            else:
                print("Invalid group choice.")

        elif choice == "4":
            group_names = display_group_names()
            group_choice = get_user_choice()
            if group_choice in group_names:
                print("\nInvite + send Starting....\n")
                await inviteSJ(group_names[group_choice], "invite_send", profile)
            else:
                print("Invalid group choice.")

        elif choice == "5":
            print("\nAdding new session....\n")
            await addNewSess(profile)

        elif choice == "6":
            print()
            change_proxy()

        elif choice == "7":
            print()
            update_config_value()

        elif choice == "0":
            print("\nThe programm is closed.")
            return

        else:
            print("Incorectly. Try again.")


if __name__ == "__main__":
    asyncio.run(main())

# Восстановление стандартного потока вывода
sys.stdout = sys.__stdout__
output_file.close()