from shared.hardcore_globals import ROLE_IDS
import re
import discord

"""
#################################################################################################################################
#                                                              CONFIGS                                                          #
#################################################################################################################################
"""

PS = "https://www.roblox.com/share?code=24f0174ac4601144ba68fa7999fbda3b&type=Server"
COOLDOWN = 2.0


"""
#################################################################################################################################
#                                                           COMMAND PERMS                                                       #
#################################################################################################################################
"""

ROLES_WITH_PERMS_TO_USE__PING = [
    ROLE_IDS["HOSTER_ROLE_ID"],
    ROLE_IDS["PREMIUM_HOSTER_ROLE_ID"],
    ROLE_IDS["SANTA_CLAUS_ROLE_ID"],
    ROLE_IDS["LEAK_PING_MANAGER_ROLE_ID"],
    ROLE_IDS["SHOP_RESET_MANAGER_ROLE_ID"],
    ROLE_IDS["TOURNAMENT_MANAGER_ROLE_ID"],
    ROLE_IDS["CHALLENGE_MANAGER_ROLE_ID"]
]
ROLES_WITH_PERMS_TO_PING__BADGES = [
    ROLE_IDS["HOSTER_ROLE_ID"],
    ROLE_IDS["PREMIUM_HOSTER_ROLE_ID"]
]
ROLES_WITH_PERMS_TO_PING__SHOP_RESET = [
    ROLE_IDS["SHOP_RESET_MANAGER_ROLE_ID"]
]
ROLES_WITH_PERMS_TO_PING__GIVEAWAY = [
    ROLE_IDS["SANTA_CLAUS_ROLE_ID"],
    ROLE_IDS["PREMIUM_HOSTER_ROLE_ID"]
]
ROLES_WITH_PERMS_TO_PING__LEAK = [
    ROLE_IDS["LEAK_PING_MANAGER_ROLE_ID"]
]
ROLES_WITH_PERMS_TO_PING__TOURNAMENT = [
    ROLE_IDS["TOURNAMENT_MANAGER_ROLE_ID"]
]

ROLES_WITH_PERMS_TO_USE__ACTIVITY = [
    ROLE_IDS["STAFF_TEAM_ROLE_ID"]
]


"""
#################################################################################################################################
#                                                           COMMAND CONST                                                       #
#################################################################################################################################
"""

PING_CATEGORIES = [
    {
        "allowed_roles": ROLES_WITH_PERMS_TO_PING__BADGES,
        "options": ["hh", "ahp", "a", "r", "h", "m", "o", "b", "bm", "d", "gs", "c", "th", "kg", "v"]
    },
    {
        "allowed_roles": ROLES_WITH_PERMS_TO_PING__SHOP_RESET,
        "options": ["sr"]
    },
    {
        "allowed_roles": ROLES_WITH_PERMS_TO_PING__GIVEAWAY,
        "options": ["g"]
    },
    {
        "allowed_roles": ROLES_WITH_PERMS_TO_PING__LEAK,
        "options": ["l"]
    },
    {
        "allowed_roles": ROLES_WITH_PERMS_TO_PING__TOURNAMENT,
        "options": ["t"]
    }
]


"""
#################################################################################################################################
#                                                           PERMS GAMBLE                                                        #
#################################################################################################################################
"""

_PERMS_GAMBLE_WORDS1 = ["admin", "administrator", "mod", "moderator", "perms", "permissions", "permes", "prems", "pers", "perm"]
_PERMS_GAMBLE_WORDS2 = ["make", "rn", "now", "right now", "please", "me", "i", "gimme", "gimmie", "give", "perms", "pass"]
PATTERN_W1 = re.compile(r'\b(?:' + '|'.join(map(re.escape, _PERMS_GAMBLE_WORDS1)) + r')\b', re.IGNORECASE)
PATTERN_W2 = re.compile(r'\b(?:' + '|'.join(map(re.escape, _PERMS_GAMBLE_WORDS2)) + r')\b', re.IGNORECASE)

"""
#################################################################################################################################
#                                                              BUTTONS                                                          #
#################################################################################################################################
"""

BUTTON_ACTIVITY_ACTIVE = {
    "label": "🔥Set active🔥",
    "style": discord.ButtonStyle.success,
    "cid": "btn_activity_active"
}
BUTTON_ACTIVITY_INACTIVE = {
    "label": "😴Set inactive😴",
    "style": discord.ButtonStyle.danger,
    "cid": "btn_activity_inactive"
}