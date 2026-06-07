import discord
from shared.hardcore_globals import ROLE_IDS


"""
#################################################################################################################################
#                                                              CONFIGS                                                          #
#################################################################################################################################
"""

COOLDOWN = 2
DELAY_BEFORE_DELETING_MESSAGE = 10


"""
#################################################################################################################################
#                                                           COMMAND PERMS                                                       #
#################################################################################################################################
"""

ROLES_WITH_PERMS_TO__CLOSE_A_BATTLE_THREAD = [
    ROLE_IDS["ADMIN_ROLE_ID"],
    ROLE_IDS["LEADERBOARDS_MANAGER_ROLE_ID"]
]
ROLES_WITH_PERMS_TO__LOCK_A_BATTLE_THREAD = [
    ROLE_IDS["ADMIN_ROLE_ID"],
    ROLE_IDS["LEADERBOARDS_MANAGER_ROLE_ID"]
]
ROLES_WITH_PERMS_TO__UNLOCK_A_BATTLE_THREAD = [
    ROLE_IDS["ADMIN_ROLE_ID"],
    ROLE_IDS["LEADERBOARDS_MANAGER_ROLE_ID"]
]

ROLES_WITH_PERMS_TO__TALK_IN_BATTLE_CHANNEL = [
    ROLE_IDS["ADMIN_ROLE_ID"],
    ROLE_IDS["LEADERBOARDS_MANAGER_ROLE_ID"],
    ROLE_IDS["HEAD_MOD_ROLE_ID"],
    ROLE_IDS["MOD_ROLE_ID"]
]


"""
#################################################################################################################################
#                                                              BUTTONS                                                          #
#################################################################################################################################
"""

BUTTON_BATTLE_JOIN_THREAD = {
    "label": "🔥JOIN🔥",
    "style": discord.ButtonStyle.success,
    "cid": "btn_battle_join"
}
BUTTON_BATTLE_CLOSE_THREAD = {
    "label": "✖️CLOSE✖️",
    "style": discord.ButtonStyle.danger,
    "cid": "btn_battle_close_thread"
}
BUTTON_BATTLE_LOCK_THREAD = {
    "label": "🔒LOCK🔒",
    "style": discord.ButtonStyle.secondary,
    "cid": "btn_battle_lock_thread"
}
BUTTON_BATTLE_UNLOCK_THREAD = {
    "label": "🔓UNLOCK🔓",
    "style": discord.ButtonStyle.success,
    "cid": "btn_battle_unlock_thread"
}


"""
#################################################################################################################################
#                                                              EMBEDS                                                           #
#################################################################################################################################
"""

EMBED_BATTLE_THREAD = {
    "title" : "⚔️ Battle Session ⚔️",
    "description" : "Use this space to describe the battle terms.\nTry to make it clear so all players understand the rules",
    "color" : 0xff5500
}