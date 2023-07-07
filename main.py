import asyncio
import configparser
from MODULES.sparser import parser_channel
from MODULES.isOwnSJ import inviteSJ
from MODULES.isOwn2 import inviteMy
from MODULES.addNewSessToConfig import addNewSess
from MODULES.screen_saver import disable_screen_saver
from MODULES.change_proxy import change_proxy
from MODULES.change_config import update_config_value


def get_user_choice():
    choice = input("Your choise (get me variant number): ")
    return choice


def display_group_names():
    config = configparser.ConfigParser()
    config.read("./Configs/config.ini")
    group_names = config["Group_names"]
    print("\nGroup Names:")
    for key, value in group_names.items():
        print(f"{key}. {value}")
    print()
    return group_names


async def main():
    disable_screen_saver()
    while True:
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
            print("\nParsing Starting....\n")

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
                    await inviteSJ(group_names[group_choice], "invite")
            else:
                print("Invalid group choice.")

        elif choice == "3":
            group_names = display_group_names()
            group_choice = get_user_choice()
            if group_choice in group_names:
                print("\nSend messages Starting....\n")
                await inviteSJ(group_names[group_choice], "send")
            else:
                print("Invalid group choice.")

        elif choice == "4":
            group_names = display_group_names()
            group_choice = get_user_choice()
            if group_choice in group_names:
                print("\nInvite + send Starting....\n")
                await inviteSJ(group_names[group_choice], "invite_send")
            else:
                print("Invalid group choice.")

        elif choice == "5":
            print("\nAdding new session....\n")
            await addNewSess()

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
