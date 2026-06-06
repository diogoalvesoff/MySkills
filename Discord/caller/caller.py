from globals import *


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
        self.gamble_cooldown = commands.CooldownMapping.from_cooldown(1, COOLDOWN, commands.BucketType.user)

    async def on_ready(self):
        print(f'Logged on as {self.user}')
        try:
            synced = await self.tree.sync(guild=GUILD)
            print (f'Synced {len(synced)} commands to guild {GUILD_ID}')
        except Exception as e:
            print (f'Error syncing commands: {e}')

    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        bucket = self.gamble_cooldown.get_bucket(message)
        retry_after = bucket.update_rate_limit()
        if retry_after:
            print(f"Rate limit catch. {message.author.name} gotta wait more {retry_after:.2f}s")
            return
        
        await self.process_commands(message)

        content = message.content
        num_words = len(re.findall(r'\w+', content))
            
        if num_words == 0:
            return

        # 3. Lógica principal
        perms_channel = message.author.guild.get_channel(1510644799311450152)
        if num_words == 1:
            # Regra: Se tem 1 palavra, tem de estar na words1
            if padrao_w1.search(content):
                print(f"{message.author.mention} asked for perms: {content}")
                await message.delete()
                if perms_channel:
                    await perms_channel.send(f"{message.author.mention} asked for perms!\nGambling ......\nNo")
                else:
                    print("E: No perms_channel")
                    
        elif num_words > 1:
            # Regra: Se tem > 1 palavra, precisa de uma da words1 E uma da words2
            if padrao_w1.search(content) and padrao_w2.search(content):
                print(f"{message.author.mention} asked for perms: {content}")
                await message.delete()
                if perms_channel:
                    await perms_channel.send(f"{message.author.mention} asked for perms!\nGambling ......\nNo")
                else:
                    print("E: No perms_channel")

        if content.startswith("1/10"):
            if perms_channel:
                await perms_channel.send(f"True")
            else:
                print("E: No perms_channel")

        if content.startswith("ps"):
            await message.reply(PS)

        if message.mentions:
            if not message.guild:
                return

            if message.channel.id != VOUCHES_CHANNEL:
                resting_role = message.guild.get_role(RESTING_ROLE_ID)
                if not resting_role:
                    print("Err: No resting role")
                    return
                mentioned_inactives = []
                for user in message.mentions:
                    if isinstance(user, discord.Member) and resting_role in user.roles:
                        mentioned_inactives.append(user.display_name)
                if len(mentioned_inactives) == 1:
                    await message.reply(f"**Shhh, {mentioned_inactives[0]} is inactive 😴!**\nPlease, avoid pinging inactive users and contact someone else if needed.")
                elif len(mentioned_inactives) > 1:
                    names = ", ".join(mentioned_inactives[:-1]) + f" and {mentioned_inactives[-1]}"
                    await message.reply(f"**Shhh, {names} are inactive 😴!**\nPlease, avoid pinging inactive users and contact someone else if needed.")

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


"""
#################################################################################################################################
#                                                               COMANDOS                                                        #
#################################################################################################################################

1. /ping
2. /set active
2. /set inactive

"""

"""
#################################################################################################################################
#                                                                PING                                                           #
#################################################################################################################################
"""

@app_commands.checks.has_any_role(*ROLES_WITH_PERMS_TO_USE__PING)
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
        print(f"{interaction.user.name} used /ping")


"""
#################################################################################################################################
#                                                             ACTIVITY                                                          #
#################################################################################################################################
"""

class SetActivity(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=60)

    @discord.ui.button(label=BUTTON_ACTIVITY_ACTIVE_LABEL, style=BUTTON_ACTIVITY_ACTIVE_STYLE, custom_id=BUTTON_ACTIVITY_ACTIVE_CUSTOM_ID)
    async def btn_activity_active(self, interaction: discord.Interaction, button: discord.ui.Button):
        resting_role = interaction.guild.get_role(RESTING_ROLE_ID)
        if not resting_role:
            print("Err: No resting role")
            return
        if resting_role in interaction.user.roles:
            await interaction.user.remove_roles(resting_role)

        for child in self.children:
            child.disabled = True

        await interaction.response.edit_message(
            content = f"✅ Done. You're active",
            view=self
        )

        staff_chat = interaction.guild.get_channel(STAFF_CHANNEL)
        if staff_chat:
            await staff_chat.send(f"{interaction.user.mention} is active")

    @discord.ui.button(label=BUTTON_ACTIVITY_INACTIVE_LABEL, style=BUTTON_ACTIVITY_INACTIVE_STYLE, custom_id=BUTTON_ACTIVITY_INACTIVE_CUSTOM_ID)
    async def btn_activity_inactive(self, interaction: discord.Interaction, button: discord.ui.Button):
        resting_role = interaction.guild.get_role(RESTING_ROLE_ID)
        if not resting_role:
            print("Err: No resting role")
            return
        if resting_role not in interaction.user.roles:
            await interaction.user.add_roles(resting_role)

        for child in self.children:
            child.disabled = True

        await interaction.response.edit_message(
            content = f"✅ Done. You're inactive",
            view=self
        )

        staff_chat = interaction.guild.get_channel(STAFF_CHANNEL)
        if staff_chat:
            await staff_chat.send(f"{interaction.user.mention} is inactive")

@app_commands.checks.has_any_role(*ROLES_WITH_PERMS_TO_USE__ACTIVITY)
@client.tree.command(name="activity", description="If you are a staff member, use me to declare yourself active or inactive", guild=GUILD)
async def activity (interaction: discord.Interaction):
    view = SetActivity()
    await interaction.response.send_message(f"Press the button that best suits your purpose", view=view, ephemeral=True)

def main():
    if not TOKEN:
        print ("E: Token not found!")
        return
    print ("Starting!")
    client.run(TOKEN)

if __name__ == "__main__":
    main()