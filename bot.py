import os

import discord
from discord.ext import commands

# -------------------------------------------------
# Configuration
# -------------------------------------------------

# Either set the DISCORD_TOKEN environment variable,
# or replace the line below with your token string, e.g.
# TOKEN = "YOUR_BOT_TOKEN_HERE"

# Name of the channel where rules should be posted
RULES_CHANNEL_NAME = "rules"

# The actual rules text. Edit these to match your server.
# Each string is one rule (numbering is added automatically in the embed).
RULES = [
    "Do NOT post or do anything against Discord's Terms of Service.",
    "NO Doxxing (revealing personal information about someone).",
    "No NSFW, excessive gore, or otherwise inappropriate content.",
    "No spamming, advertising, or self-promotion without staff permission.",
    "NO Screeching/screaming in voice channels (mic spamming).",
    "Only open tickets for authentic problems.",
    "No hacking/scripting or use of 3rd party software (Crosshairs exempt).",
    "No EAC bans newer than 90 days. ALL gamebanned players MUST submit a ticket and show us all gamebanned accounts, and the alt you will be using to play.",
    "No ban evading.",
]

# Shown at the bottom of the rules embed.
RULES_FOOTER = "Breaking these rules may result in warnings, mutes, kicks, or bans at staff discretion."

# Accent color for the embed sidebar (Discord blurple). Use a hex int, e.g. 0x5865F2.
EMBED_COLOR = 0x5865F2


# -------------------------------------------------
# Bot Setup
# -------------------------------------------------

intents = discord.Intents.default()
intents.message_content = True  # Required for prefix commands

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("Bot is ready.")


@bot.command(name="rules", help="Post the server rules into the #rules channel.")
@commands.has_permissions(administrator=True)
async def send_rules(ctx: commands.Context):
    """Send the rules to the configured rules channel."""
    guild = ctx.guild

    if guild is None:
        await ctx.send("This command can only be used in a server.")
        return

    rules_channel = discord.utils.get(guild.text_channels, name=RULES_CHANNEL_NAME)

    if rules_channel is None:
        await ctx.send(f"Could not find a text channel named '{RULES_CHANNEL_NAME}'.")
        return

    embed = discord.Embed(
        title="📜 Server Rules",
        description=(
            "Please read and follow these rules. By participating in this server, "
            "you agree to abide by them.\n"
        ),
        color=EMBED_COLOR,
        timestamp=discord.utils.utcnow(),
    )
    embed.set_author(name=guild.name, icon_url=guild.icon.url if guild.icon else None)

    rules_body = "\n\n".join(f"**{i}.** {rule}" for i, rule in enumerate(RULES, 1))
    embed.add_field(name="Rules", value=rules_body, inline=False)
    embed.add_field(
        name="\u200b",
        value=f"*{RULES_FOOTER}*",
        inline=False,
    )
    embed.set_footer(text="Stay respectful and have fun.")

    await rules_channel.send(embed=embed)

    if ctx.channel != rules_channel:
        await ctx.send(f"Rules have been posted in {rules_channel.mention}.")


@send_rules.error
async def send_rules_error(ctx: commands.Context, error: commands.CommandError):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You need **Administrator** permissions to use this command.")
    else:
        # Re-raise other errors so they appear in the console
        raise error


def main():
    if not TOKEN:
        raise RuntimeError(
            "No bot token found. Set the DISCORD_TOKEN environment variable "
            "or hard-code your token into the TOKEN variable in bot.py."
        )

    bot.run(TOKEN)


if __name__ == "__main__":
    main()