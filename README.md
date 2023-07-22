<<<<<<< HEAD
=======
# telegram_parse_invite_send-mess

>>>>>>> ab345250353928dfa04fc4ab22d7f2b7f0d3a0dc
This is an application for collecting user usernames, inviting them, and sending messages.

1. It can collect members of Telegram groups and store them in JSON files.
  
2. It works with Telegram session files (sess + json).
   You simply need to place the session files in a folder, and the program will add them to your group.

3.There are three invitation options to choose from:
  a) Group invitations: Each session will invite people from the previously collected lists. 
     If the privacy settings of the invited user prohibit this, the session will move on to the next user until a successful invitation to the group is made.
  b) Direct message broadcasting to your lists.
  c) Invitations + Broadcasting: If a user cannot be invited due to privacy settings, 
    an invitation will be sent to their direct messages. This ensures the most effective invitations.

4. When a spam block is encountered, the session takes a break for the duration specified by you.

5. Checkpoints are saved for all user lists, meaning the invitation process continues from where it left off.

6. Proxy support is available.
