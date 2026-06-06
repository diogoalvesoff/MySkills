import discord
from shared.hardcore_globals import ROLE_IDS


"""
#################################################################################################################################
#                                                              CONFIGS                                                          #
#################################################################################################################################
"""

COOLDOWN = 2


"""
#################################################################################################################################
#                                                           COMMAND PERMS                                                       #
#################################################################################################################################
"""

ROLES_WITH_PERMS_TO__CLOSE_A_CHALLENGE_THREAD = [
    ROLE_IDS["ADMIN_ROLE_ID"],
    ROLE_IDS["LEADERBOARDS_MANAGER_ROLE_ID"]
]
ROLES_WITH_PERMS_TO__LOCK_A_CHALLENGE_THREAD = [
    ROLE_IDS["ADMIN_ROLE_ID"],
    ROLE_IDS["LEADERBOARDS_MANAGER_ROLE_ID"]
]
ROLES_WITH_PERMS_TO__UNLOCK_A_CHALLENGE_THREAD = [
    ROLE_IDS["ADMIN_ROLE_ID"],
    ROLE_IDS["LEADERBOARDS_MANAGER_ROLE_ID"]
]


"""
#################################################################################################################################
#                                                              BUTTONS                                                          #
#################################################################################################################################
"""

BUTTON_CHALLENGE_JOIN_THREAD = {
    "label": "🔥JOIN🔥",
    "style": discord.ButtonStyle.success,
    "cid": "btn_challenge_join"
}
BUTTON_CHALLENGE_CLOSE_THREAD = {
    "label": "✖️CLOSE✖️",
    "style": discord.ButtonStyle.danger,
    "cid": "btn_challenge_close_thread"
}
BUTTON_CHALLENGE_LOCK_THREAD = {
    "label": "🔒LOCK🔒",
    "style": discord.ButtonStyle.secondary,
    "cid": "btn_challenge_lock_thread"
}
BUTTON_CHALLENGE_UNLOCK_THREAD = {
    "label": "🔓UNLOCK🔓",
    "style": discord.ButtonStyle.success,
    "cid": "btn_challenge_unlock_thread"
}


"""
#################################################################################################################################
#                                                              EMBEDS                                                           #
#################################################################################################################################
"""

EMBED_CHALLENGE_THREAD = {
    "title" : "⚔️ Battle Session ⚔️",
    "description" : "Use this space to describe how the battle terms.\nTry to make it clear so all players understand the rules",
    "color" : 0xff5500
}