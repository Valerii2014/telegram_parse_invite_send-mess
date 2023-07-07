import configparser
import os
from .JCACI import join_channel


async def addNewSess():
    # Path to the folder containing the files
    folder_path = "Sessions/sessJson"

    # Initialize the configparser
    config = configparser.ConfigParser()

    # Check if sessionConfig.ini exists
    if os.path.exists("Configs/sessionConfig.ini"):
        # Read the existing config file
        config.read("Configs/sessionConfig.ini")

    # Get the existing section names
    existing_sections = set(config.sections())

    # Get the filenames in the folder
    filenames = os.listdir(folder_path)

    # Set to store unique section names
    unique_section_names = set()
    counter = 0

    new_sessions = []

    # Loop through the filenames and add sections to the config
    for filename in filenames:
        # Remove the file extension
        section_name = os.path.splitext(filename)[0]
        # Add the section name to the set if it's unique and not already in the existing sections
        if (
            section_name not in unique_section_names
            and section_name not in existing_sections
        ):
            unique_section_names.add(section_name)
            # Add the section to the config
            new_sessions.append(section_name)
            config.add_section(section_name)
            counter += 1

    change_name = input("Do you want channge name in session profiles ? (Y/N):")
    change_name_boolean = False

    if change_name == "Y" or change_name == "y":
        change_name_boolean = True

    await join_channel(new_sessions, change_name_boolean)

    # Save the config to the sessionConfig.ini file
    print(f"TOTAL NEW SESSIONS: {counter}")
    with open("Configs/sessionConfig.ini", "w") as config_file:
        config.write(config_file)
