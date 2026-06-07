import os
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

from shared.hardcore_globals import GUILD_INFO, ROLE_IDS, CHANNEL_IDS
from leaderboards.leaderboards_constants import (
    COOLDOWN, DELAY_BEFORE_DELETING_MESSAGE,
    ROLES_WITH_PERMS_TO__CLOSE_A_BATTLE_THREAD, ROLES_WITH_PERMS_TO__LOCK_A_BATTLE_THREAD, ROLES_WITH_PERMS_TO__UNLOCK_A_BATTLE_THREAD, ROLES_WITH_PERMS_TO__TALK_IN_BATTLE_CHANNEL,
    BUTTON_BATTLE_JOIN_THREAD, BUTTON_BATTLE_CLOSE_THREAD, BUTTON_BATTLE_LOCK_THREAD, BUTTON_BATTLE_UNLOCK_THREAD,
    EMBED_BATTLE_THREAD
)

load_dotenv()
TOKEN = os.getenv('TOKEN')



class Client (commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.reactions = True                                    # lets see reactions
        intents.guilds = True                                       # lets see specific guild info
        intents.members = True                                      # lets assign roles to users~
        super().__init__(command_prefix="!", intents=intents)
        self.cooldown = commands.CooldownMapping.from_cooldown(1, COOLDOWN, commands.BucketType.user)

    async def setup_hook(self) -> None:
        self.add_view(ChallengeView())
        self.add_view(CloseThreadView())

    async def on_ready(self):
        print(f'Logged on as {self.user}')
        try:
            synced = await self.tree.sync(guild=GUILD_INFO["GUILD"])
            print (f'Synced {len(synced)} commands to guild {GUILD_INFO["GUILD_ID"]}')
        except Exception as e:
            print (f'Error syncing commands: {e}')

    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        bucket = self.cooldown.get_bucket(message)
        retry_after = bucket.update_rate_limit()
        if retry_after:
            print(f"Rate limit catch. {message.author.name} gotta wait more {retry_after:.2f}s")
            return
        
        await self.process_commands(message)

        battle_channel = CHANNEL_IDS.get("BATTLE_CHANNEL")
        if not battle_channel:
            print("[BOT] - Err: Battle channel not found")
        elif message.channel.id == battle_channel:
            have_permission = any(role.id in ROLES_WITH_PERMS_TO__TALK_IN_BATTLE_CHANNEL for role in message.author.roles)
            if not have_permission:
                try:
                    await message.delete()
                    await message.channel.send(f"⚠️ {message.author.mention}, This channel is fight only. Use /battle to fight others warriors", delete_after=DELAY_BEFORE_DELETING_MESSAGE)
                except discord.Forbidden:
                    print("[BOT] - E: I don't have perms to delete messages")
                except Exception as e:
                    print(f"[BOT] - E: Something wrong happened: {e}")

        # content = message.content

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            return
        print(f"E: '{ctx.command} failed: {error}")

client = Client()

@client.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.MissingAnyRole):
        await interaction.response.send_message("You don't have perms to execute me", ephemeral=True)
        return
    print(f"E: '{interaction.command.name}' failed: {error}")
    if not interaction.response.is_done():
        await interaction.response.send_message(f"I think smth went wrong... role <@&{ROLE_IDS.get('ADMIN_ROLE_ID')}>")


"""
#################################################################################################################################
#                                                               COMANDOS                                                        #
#################################################################################################################################

1. /battle
"""

"""
#################################################################################################################################
#                                                               BATTLE                                                          #
#################################################################################################################################
"""

class ChallengeView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label=BUTTON_BATTLE_JOIN_THREAD["label"], style=BUTTON_BATTLE_JOIN_THREAD["style"], custom_id=BUTTON_BATTLE_JOIN_THREAD["cid"])
    async def btn_challenge_join(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not interaction.message.embeds:
            await interaction.response.send_message("❌ Coudn't read message embed")
            print ("Err: Coudn't read battle embed to extract thread id")
            return
        embed = interaction.message.embeds[0]
        try:
            thread_id_str = embed.footer.text.split("Thread: ")[1]
            thread_id = int(thread_id_str)
        except (IndexError, ValueError, AttributeError) as e:
            await interaction.response.send_message("Err: Coudn't find thread ID. Technical detail", ephemeral=True)
            print(f"Err: Coudnt't extract thread ID from embed: {e}")
            return

        thread = interaction.guild.get_thread(thread_id)
        if not thread:
            await interaction.response.send_message("❌ This thread doesn't exist.", ephemeral=True)
            return
        
        if thread.archived:
            await interaction.response.send_message("❌ Too late! This challenge is over.", ephemeral=True)
            return
        await thread.add_user(interaction.user)
        await interaction.response.send_message(f"✅ You joined {thread.mention}! Good luck!.", ephemeral=True)

class CloseThreadView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    # close
    @discord.ui.button(label = BUTTON_BATTLE_CLOSE_THREAD["label"], style=BUTTON_BATTLE_CLOSE_THREAD["style"], custom_id=BUTTON_BATTLE_CLOSE_THREAD["cid"])
    async def btn_battle_close_thread(self, interaction: discord.Interaction, button: discord.ui.Button):
        thread = interaction.channel

        has_permission = any(role.id in ROLES_WITH_PERMS_TO__CLOSE_A_BATTLE_THREAD for role in interaction.user.roles)
        if not has_permission:
            await interaction.response.send_message("❌ You can't close this thread.", ephemeral=True)
            return

        await interaction.response.send_message("🏁 Arena closed 🏁")
        await thread.edit(archived=True, locked=True)

    # lock
    @discord.ui.button(label = BUTTON_BATTLE_LOCK_THREAD["label"], style=BUTTON_BATTLE_LOCK_THREAD["style"], custom_id=BUTTON_BATTLE_LOCK_THREAD["cid"])
    async def btn_battle_lock_thread(self, interaction: discord.Interaction, button: discord.ui.Button):
        thread = interaction.channel

        has_permission = any(role.id in ROLES_WITH_PERMS_TO__LOCK_A_BATTLE_THREAD for role in interaction.user.roles)
        if not has_permission:
            await interaction.response.send_message("❌ You can't lock this thread.", ephemeral=True)
            return

        await interaction.response.send_message("🔒 Arena Locked 🔒")
        await thread.edit(locked=True)

    # unlock
    @discord.ui.button(label = BUTTON_BATTLE_UNLOCK_THREAD["label"], style=BUTTON_BATTLE_UNLOCK_THREAD["style"], custom_id=BUTTON_BATTLE_UNLOCK_THREAD["cid"])
    async def btn_battle_unlock_thread(self, interaction: discord.Interaction, button: discord.ui.Button):
        thread = interaction.channel

        has_permission = any(role.id in ROLES_WITH_PERMS_TO__UNLOCK_A_BATTLE_THREAD for role in interaction.user.roles)
        if not has_permission:
            await interaction.response.send_message("❌ You can't unlock this thread.", ephemeral=True)
            return

        await interaction.response.send_message("🔓 Arena Unlocked 🔓")
        await thread.edit(locked=False)

@client.tree.command(name="battle", description="Hello warrior. Use me to fight 1 or more warriors in an organized battle field", guild=GUILD_INFO["GUILD"])
async def battle(interaction: discord.Interaction, title: str, description: str = None):
    if interaction.channel.id != CHANNEL_IDS.get("BATTLE_CHANNEL"):
        battle_channel = interaction.guild.get_channel(CHANNEL_IDS.get("BATTLE_CHANNEL"))
        if not battle_channel:
            print("Err: Battle channel doesn't exist")
            return
        await interaction.response.send_message(f"❌ I'm only only executable in {battle_channel.mention}", ephemeral=True)
        return

    await interaction.response.defer()
    try:
        thread = await interaction.channel.create_thread(
            name = f"⚔️ Battle: {title[:40]} - {interaction.user.display_name} ⚔️",
            type = discord.ChannelType.private_thread,
            invitable=False
        )
    except discord.Forbidden as e:
        await interaction.followup.send("❌ I don't have perms create private threads in this channel")
        print(f"Err: Missing Access - {e}")
        return
    except discord.HTTPException as e:
        await interaction.followup.send("❌ An error occurred while communicating with discord", ephemeral=True)
        print(f"Err: HTTP Exception - {e}")
        return
    except Exception as e:
        await interaction.followup.send("❌ Something wrong happened")
        print(f"Err: Something wrong happened - {e}")
        return

    embed_main = discord.Embed(
        title=f"⚔️ Battle {title} ⚔️",
        description=description.capitalize() if description and description.strip() else "Join to compete!",
        color=discord.Color.dark_purple()
    )
    embed_main.set_author(name=interaction.user.display_name, icon_url=interaction.user.display_avatar.url)
    embed_main.set_footer(text=f"Created by {interaction.user.display_name} | Thread: {thread.id}")

    await interaction.followup.send(embed=embed_main, view=ChallengeView())

    embed_thread = discord.Embed(
        title=EMBED_BATTLE_THREAD["title"],
        description=EMBED_BATTLE_THREAD["description"],
        color=EMBED_BATTLE_THREAD["color"]
    )
    embed_thread.set_footer(text=f"AuthorID: {interaction.user.id}")
    
    await thread.send(f"{interaction.user.mention}, the arena is ready!", embed=embed_thread, view=CloseThreadView())


def main():
    if not TOKEN:
        print ("E: Token not found!")
        return
    print ("Starting!")
    client.run(TOKEN)

if __name__ == "__main__":
    main()




    