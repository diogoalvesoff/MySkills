import os
from dotenv import load_dotenv
import discord
from discord import app_commands
from discord.ext import commands
from globals import *


load_dotenv()
TOKEN = os.getenv('TOKEN')


class Client (commands.Bot):
    async def on_ready(self):
        print(f'Logged on as {self.user}')
        try:
            synced = await self.tree.sync(guild=GUILD)
            print (f'Synced {len(synced)} commands to guild {GUILD_ID}')
        except Exception as e:
            print (f'Error syncing commands: {e}')

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            return
        print(f"E: '{ctx.command} failed: {error}")
        


intents = discord.Intents.default()
intents.message_content = True                              # lets see messages
intents.reactions = True                                    # lets see reactions
intents.guilds = True                                       # lets see specific guild info
intents.members = True                                      # lets assign roles to users

client = Client (command_prefix="!", intents=intents)


@client.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.MissingAnyRole):
        await interaction.response.send_message("You don't have perms to execute me", ephemeral=True)
        return
    print(f"E: '{interaction.command.name}' failed: {error}")
    if not interaction.response.is_done():
        await interaction.response.send_message(f"I think smth went wrong... role <@&{SECURITY_MANAGER_ROLE_ID}>")


async def ping_autocomplete (interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
    choices = []
    user_role_ids = [role.id for role in interaction.user.roles]
    for category in PING_CATEGORIES:
        if any(r_id in category["allowed_roles"] for r_id in user_role_ids):
            for opt in category["options"]:
                name = ROLES_NAME.get(opt)
                if name and current.lower() in name.lower():
                    choices.append(app_commands.Choice(name=name, value=opt))

    return choices[:25]

@app_commands.checks.has_any_role(*ROLES_WITH_PERMS_TO_USE_BOT)
@client.tree.command(name="ping", description="If you are a hoster or a premium hoster, use me to ping certain roles", guild=GUILD)
@app_commands.autocomplete(role=ping_autocomplete)
async def ping(interaction: discord.Interaction, role: str):
    role_key = role.lower()
    target_role_id = ROLES_ID.get(role_key)
    if not target_role_id:
        await interaction.response.send_message("That role doesn't exist", ephemeral=True)
        return

    user_role_ids = [r.id for r in interaction.user.roles]
    has_perms = False
    
    for category in PING_CATEGORIES:
        category_target_ids = [ROLES_ID[opt] for opt in category["options"]]
        
        if target_role_id in category_target_ids:
            if any(r_id in category["allowed_roles"] for r_id in user_role_ids):
                has_perms = True
            break
    
    if not has_perms:
        await interaction.response.send_message("You don't have perms to ping that role", ephemeral=True)
        return

    if target_role_id: 
        await interaction.response.send_message(f"<@&{target_role_id}>")

def main():
    if not TOKEN:
        print ("E: Token not found!")
        return
    print ("Starting!")
    client.run(TOKEN)

if __name__ == "__main__":
    main()