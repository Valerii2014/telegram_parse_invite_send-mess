import asyncio
import random
import telethon
from .random_number import get_random_number
from telethon.tl.functions.channels import InviteToChannelRequest

batch_size = 1


# Отправка приглашений в группу
async def invite_send_users(
    client, usernames, start_index, group_id, profile, profile_count
):
    uninvited_users = []
    invited_users = []
    flood = False
    sleeptime = get_random_number(profile_count)
    counter = 1

    user_index = start_index + counter

    if user_index < len(usernames):
        username = usernames.get(str(user_index))

        if username is not None:
            try:
                user = await client.get_entity(username)
                await client(InviteToChannelRequest(channel=group_id, users=[user]))
                print(f"User {username} invited to the group")
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
                    uninvited_users.append(username)
                    counter = counter - 1
                    print(f"Error inviting user {username}: {str(e)}")
                    print(f"PeerFloodError. Session {profile} excluded")
                    return uninvited_users, invited_users, True, counter
                except Exception as e:
                    uninvited_users.append(username)
                    print(
                        f"Error sending invitation to {username} in direct messages: {str(e)}"
                    )
    return (
        uninvited_users,
        invited_users,
        flood,
        counter,
    )  # Вернуть список неприглашенных пользователей и список приглашенных пользователей


# Отправка приглашений в группу
async def invite_users(
    client, usernames, start_index, group_id, profile, profile_count
):
    uninvited_users = []
    invited_users = []
    flood = False
    sleeptime = get_random_number(profile_count)
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
                    f"User {username} invited to the group     user {start_index} of {len(usernames)}"
                )
                invited_users.append(username)
                success_invite = True
            except telethon.errors.UserAlreadyParticipantError:
                print(f"User {username} is already a member of the group")
                counter += 1
            except telethon.errors.PeerFloodError as e:
                counter = counter - 1
                print(f"Error inviting user {username}: {str(e)}")
                print(f"PeerFloodError. Session {profile} excluded")
                return uninvited_users, invited_users, True, counter
            except Exception as e:
                counter += 1
                uninvited_users.append(username)
                print(f"Error inviting user {username}: {str(e)}")
                await asyncio.sleep(3 + random.random())
        else:
            break

    return (
        uninvited_users,
        invited_users,
        flood,
        counter,
    )  # Вернуть список неприглашенных пользователей и список приглашенных пользователей


async def send_users(client, usernames, start_index, group_id, profile, profile_count):
    uninvited_users = []
    invited_users = []
    flood = False
    sleeptime = get_random_number(profile_count)
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
                print(f"User {username} received an invitation in direct messages")
            except telethon.errors.PeerFloodError as e:
                uninvited_users.append(username)
                counter = counter - 1
                print(f"Error inviting user {username}: {str(e)}")
                print(f"PeerFloodError. Session {profile} excluded")
                return uninvited_users, invited_users, True, counter
            except Exception as e:
                uninvited_users.append(username)
                print(
                    f"Error sending invitation to {username} in direct messages: {str(e)}"
    )
    return (
        uninvited_users,
        invited_users,
        flood,
        counter,
    )  # Вернуть список неприглашенных пользователей и список приглашенных пользователей
