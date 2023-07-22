import asyncio
import re
import random
import telethon
from .random_number import get_random_number
from telethon.tl.functions.channels import InviteToChannelRequest

batch_size = 1


# Отправка приглашений в группу
async def invite_send_users(
    client, usernames, start_index, group_id, session, session_count
):
    uninvited_users = []
    invited_users = []
    flood = False
    sleeptime = get_random_number(session_count)
    counter = 1

    user_index = start_index + counter

    if user_index < len(usernames):
        username = usernames.get(str(user_index))

        if username is not None:
            try:
                user = await client.get_entity(username)
                await client(InviteToChannelRequest(channel=group_id, users=[user]))
                print(f"User {username} invited to the group. . . . . .user {start_index + counter} of {len(usernames)}")
                # Добавить пользователя в список приглашенных
                invited_users.append(username)
            except telethon.errors.UserAlreadyParticipantError:
                print(f"User {username} is already a member of the group")
            except Exception as e:
                print(f"Error inviting user {username}: {str(e)}")

                try:
                    await asyncio.sleep(random.random())
                    # Отправка приглашения в личные сообщения
                    await client.send_message(
                        user, f"You might be interested in: {group_id}"
                    )
                    invited_users.append(username)
                    print(f"User {username} received an invitation in direct messages")
                except telethon.errors.PeerFloodError as e:
                    counter = counter - 1
                    print(f"Error inviting user {username}: {str(e)}")
                    print(f"PeerFloodError. Session {session} excluded")
                    return uninvited_users, invited_users, True, counter
                except Exception as e:
                    print(
                        f"User {start_index + counter}/{len(usernames)} : {str(e)}"
                    )
    return (
        uninvited_users,
        invited_users,
        flood,
        counter,
    )  # Вернуть список неприглашенных пользователей и список приглашенных пользователей


# Отправка приглашений в группу
async def invite_users(
    client, usernames, start_index, group_id, session, session_count
):
    uninvited_users = []
    invited_users = []
    flood = False
    sleeptime = get_random_number(session_count)
    success_invite = False
    counter = 1

    # await asyncio.sleep(sleeptime)

    while (
        not success_invite and counter <= 6 and start_index + counter < len(usernames)
    ):
        username = usernames.get(str(start_index + counter))

        if username is not None:
            try:
                user = await client.get_entity(username)
                await client(InviteToChannelRequest(channel=group_id, users=[user]))
                print(
                    f"User {start_index + counter}/{len(usernames)}  with name - {username} invited to the group"
                )
                invited_users.append(username)
                success_invite = True
            except telethon.errors.PeerFloodError as e:
                print(f"User {start_index + counter}/{len(usernames)} : {str(e)}")
                counter = counter - 1
                flood = True
                print(f"XXXX_ Session {session} has been banned for flood, and excluded _XXXX")
                return uninvited_users, invited_users, flood, counter
            except telethon.errors.ChatWriteForbiddenError as e:
                print(f"User {start_index + counter}/{len(usernames)} : {str(e)}")
                return uninvited_users, invited_users, True, counter
            except Exception as e:
                string = str(e)
                if string.startswith("A wait of"):
                    # Используем регулярное выражение для поиска числа в секундах
                    match = re.search(r'A wait of (\d+) seconds', string)
                    if match:
                        seconds = int(match.group(1))
                        print(f"User {start_index + counter}/{len(usernames)} : session {session} will be able to invite after: {seconds} seconds")
                        counter = counter - 1
                        flood = seconds
                        return uninvited_users, invited_users, flood, counter
                    else:
                        print(f"User {start_index + counter}/{len(usernames)} : {string}")
                        await asyncio.sleep(random.random())
                        uninvited_users.append(username)
                        counter += 1
                else:
                    print(f"User {start_index + counter}/{len(usernames)} : {string}")
                    await asyncio.sleep(1 + random.random())
                    uninvited_users.append(username)
                    counter += 1
        else:
            break

    return (
        uninvited_users,
        invited_users,
        flood,
        counter,
    )  # Вернуть список неприглашенных пользователей и список приглашенных пользователей


async def send_users(client, usernames, start_index, group_id, session, session_count):
    uninvited_users = []
    invited_users = []
    flood = False
    sleeptime = get_random_number(session_count)
    counter = 1

    user_index = start_index + counter

    if user_index < len(usernames):
        username = usernames.get(str(user_index))

        if username is not None:
            user = await client.get_entity(username)
            try:
                # Sending invitation to direct messages
                await client.send_message(
                    user, f"You might be interested in: {group_id}"
                )
                invited_users.append(username)
                print(f"User {username} received an invitation in direct messages. . . . .user {start_index + counter} of {len(usernames)}")
            except telethon.errors.PeerFloodError as e:
                print(f"Error inviting user {username}{start_index + counter}/{len(usernames)} : {str(e)}")
                counter = counter - 1
                print(f"PeerFloodError. Session {session} excluded")
                return uninvited_users, invited_users, True, counter
            except telethon.errors.ChatWriteForbiddenError as e:
                print(f"User {start_index + counter}/{len(usernames)} : {str(e)}")
                return uninvited_users, invited_users, True, counter
            except Exception as e:
                print(
                    f"User {start_index + counter}/{len(usernames)} : {str(e)}"
    )
    return (
        uninvited_users,
        invited_users,
        flood,
        counter,
    )  # Вернуть список неприглашенных пользователей и список приглашенных пользователей
