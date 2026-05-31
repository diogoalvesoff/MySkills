import os
import re
import time
from dotenv import load_dotenv
import discord
from discord import app_commands
from discord.ext import commands

GUILD_ID = 1479320102745800838
GUILD = discord.Object(id=GUILD_ID)

ADMIN_ROLE_ID = 1483236165019631799
SECURITY_MANAGER_ROLE_ID = 1486549522803982396

HOSTER_ROLE_ID = 1480252394481910012
PREMIUM_HOSTER_ROLE_ID = 1497426112471367751
SANTA_CLAUS_ROLE_ID = 1508246646671016026
LEAK_PING_MANAGER_ROLE_ID = 1479949973947682826
SHOP_RESET_MANAGER_ROLE_ID = 1479949902657093842
TOURNAMENT_MANAGER_ROLE_ID = 1480030870822977638
CHALLENGE_MANAGER_ROLE_ID = 1480773783974449295

ROLES_WITH_PERMS_TO_USE_BOT = [
    HOSTER_ROLE_ID,
    PREMIUM_HOSTER_ROLE_ID,
    SANTA_CLAUS_ROLE_ID,
    LEAK_PING_MANAGER_ROLE_ID,
    SHOP_RESET_MANAGER_ROLE_ID,
    TOURNAMENT_MANAGER_ROLE_ID,
    CHALLENGE_MANAGER_ROLE_ID
]
ROLES_WITH_PERMS_TO_PING__BADGES = [
    HOSTER_ROLE_ID,
    PREMIUM_HOSTER_ROLE_ID
]
ROLES_WITH_PERMS_TO_PING__SHOP_RESET = [
    SHOP_RESET_MANAGER_ROLE_ID
]
ROLES_WITH_PERMS_TO_PING__GIVEAWAY = [
    SANTA_CLAUS_ROLE_ID
]
ROLES_WITH_PERMS_TO_PING__LEAK = [
    LEAK_PING_MANAGER_ROLE_ID
]
ROLES_WITH_PERMS_TO_PING__TOURNAMENT = [
    TOURNAMENT_MANAGER_ROLE_ID
]

ROLES_ID = {
    "hotel hell": 1480063127864475832, "hotelhell": 1480063127864475832, "hh": 1480063127864475832,
    "a hard place": 1480065104958455970, "ahardplace": 1480065104958455970, "ahp": 1480065104958455970,
    "a-1000": 1480065693973221489, "a1000": 1480065693973221489, "a 1000": 1480065693973221489, "a": 1480065693973221489,
    "rooms": 1480067095583789347, "r": 1480067095583789347,
    "hotel": 1480066879832850506, "h": 1480066879832850506,
    "mines": 1480066992806428734, "m": 1480066992806428734,
    "outdoors": 1480067153603596318, "o": 1480067153603596318,
    "backdoors": 1480067070245732352, "b": 1480067070245732352,
    "battle mode": 1480076512962281633, "battlemode": 1480076512962281633, "bm": 1480076512962281633,
    "donut": 1487301312998801408, "d": 1487301312998801408,
    "gween soda": 1487301509665394779, "gweensoda": 1487301509665394779, "gs": 1487301509665394779,
    "crucifix": 1480069665593102356, "c": 1480069665593102356,
    "tower heroes": 1480240740834607124, "towerheroes": 1480240740834607124, "th": 1480240740834607124,
    "knob grind": 1480403815898284124, "knobgrind": 1480403815898284124, "kg": 1480403815898284124,
    "visions": 1487304057193496656, "v": 1487304057193496656,
    "giveaway": 1480105656316072120, "g": 1480105656316072120,
    "leak": 1479922262407909660, "l": 1479922262407909660,
    "shop reset": 1479922359870947559, "shopreset": 1479922359870947559, "sr": 1479922359870947559,
    "tournament": 1480030682804650005, "t": 1480030682804650005
}

ROLES_NAME = {
    "hotel hell": "👹 | HH ᵖⁱⁿᵍ", "hotelhell": "👹 | HH ᵖⁱⁿᵍ", "hh": "👹 | HH ᵖⁱⁿᵍ",
    "a hard place": "🪨 | AHP ᵖⁱⁿᵍ", "ahardplace": "🪨 | AHP ᵖⁱⁿᵍ", "ahp": "🪨 | AHP ᵖⁱⁿᵍ",
    "a-1000": "🛑 | A-1000 ᵖⁱⁿᵍ", "a1000": "🛑 | A-1000 ᵖⁱⁿᵍ", "a 1000": "🛑 | A-1000 ᵖⁱⁿᵍ", "a": "🛑 | A-1000 ᵖⁱⁿᵍ",
    "rooms": "🔦 | Rooms ᵖⁱⁿᵍ", "r": "🔦 | Rooms ᵖⁱⁿᵍ",
    "hotel": "🚪 | Hotel ᵖⁱⁿᵍ", "h": "🚪 | Hotel ᵖⁱⁿᵍ",
    "mines": "⛏️ | Mines ᵖⁱⁿᵍ", "m": "⛏️ | Mines ᵖⁱⁿᵍ",
    "outdoors": "🌲 | Outdoors ᵖⁱⁿᵍ", "o": "🌲 | Outdoors ᵖⁱⁿᵍ",
    "backdoors": "🕰️ | Backdoors ᵖⁱⁿᵍ", "b": "🕰️ | Backdoors ᵖⁱⁿᵍ",
    "battle mode": "💣 | Battle Mode ᵖⁱⁿᵍ", "battlemode": "💣 | Battle Mode ᵖⁱⁿᵍ", "bm": "💣 | Battle Mode ᵖⁱⁿᵍ",
    "donut": "🍩 | Donut ᵖⁱⁿᵍ", "d": "🍩 | Donut ᵖⁱⁿᵍ",
    "gween soda": "🍹 | Gween Soda ᵖⁱⁿᵍ", "gweensoda": "🍹 | Gween Soda ᵖⁱⁿᵍ", "gs": "🍹 | Gween Soda ᵖⁱⁿᵍ",
    "crucifix": "✝️ | Crucifix ᵖⁱⁿᵍ", "c": "✝️ | Crucifix ᵖⁱⁿᵍ",
    "tower heroes": "🗼 | Tower heroes ᵖⁱⁿᵍ", "towerheroes": "🗼 | Tower heroes ᵖⁱⁿᵍ", "th": "🗼 | Tower heroes ᵖⁱⁿᵍ",
    "knob grind": "🪙 | Knob grind ᵖⁱⁿᵍ", "knobgrind": "🪙 | Knob grind ᵖⁱⁿᵍ", "kg": "🪙 | Knob grind ᵖⁱⁿᵍ",
    "visions": "👁️ | Visions ᵖⁱⁿᵍ", "v": "👁️ | Visions ᵖⁱⁿᵍ",
    "giveaway": "🎉 | Giveaway ᵖⁱⁿᵍ", "g": "🎉 | Giveaway ᵖⁱⁿᵍ",
    "leak": "👀 | Leak ᵖⁱⁿᵍ", "l": "👀 | Leak ᵖⁱⁿᵍ",
    "shop reset": "🛒 | Shop reset ᵖⁱⁿᵍ", "shopreset": "🛒 | Shop reset ᵖⁱⁿᵍ", "sr": "🛒 | Shop reset ᵖⁱⁿᵍ",
    "tournament": "⚔️ | Tournament ᵖⁱⁿᵍ", "t": "⚔️ | Tournament ᵖⁱⁿᵍ"
}

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


perms_gamble_words1 = ["admin", "administrator", "mod", "moderator", "perms", "permissions", "pass", "permes", "prems", "pers", "perm"]
perms_gamble_words2 = ["make", "rn", "now", "right now", "please", "me", "i", "gimme", "gimmie", "give", "perms", "pass"]
padrao_w1 = re.compile(r'\b(?:' + '|'.join(map(re.escape, perms_gamble_words1)) + r')\b', re.IGNORECASE)
padrao_w2 = re.compile(r'\b(?:' + '|'.join(map(re.escape, perms_gamble_words2)) + r')\b', re.IGNORECASE)

PS = "https://www.roblox.com/share?code=24f0174ac4601144ba68fa7999fbda3b&type=Server"

COOLDOWN = 2.0