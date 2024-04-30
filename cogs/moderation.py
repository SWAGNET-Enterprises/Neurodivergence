import os
from datetime import datetime

import discord
from discord.ext import commands
from discord.ext.commands import Context


class Moderation(commands.Cog, name="moderation"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.hybrid_command(
        name="purge",
        description="Delete a number of messages.",
    )
    @commands.has_guild_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    async def purge(self, context: Context, amount: int) -> None:
        embed = discord.Embed(title="Deleting messages...", description="Please wait...")
        await context.reply(embed=embed)
        purged_messages = await context.channel.purge(limit=amount + 1)
        embed = discord.Embed(description=f"**{context.author}** cleared **{len(purged_messages)-1}** messages!")
        await context.channel.send(embed=embed)

    @commands.hybrid_command(
        name="preemptban",
        description="Pre-emptively bans a user before they join the server.",
    )
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def preemptban(self, context: Context, user_id: str, *, reason: str = "Not specified") -> None:
        try:
            await self.bot.http.ban(user_id, context.guild.id, reason=reason)
            user = self.bot.get_user(int(user_id)) or await self.bot.fetch_user(
                int(user_id)
            )
            embed = discord.Embed(description=f"**{user}** (ID: {user_id}) was banned by **{context.author}**!")
            embed.add_field(name="Reason:", value=reason)
            await context.reply(embed=embed)
        except Exception:
            embed = discord.Embed(description="An error occurred while trying to ban the user. Make sure ID is an existing ID that belongs to a user.")
            await context.reply(embed=embed)

    @commands.hybrid_command(
        name="archive",
        description="Archives in a text file the last messages with a chosen limit of messages.",
    )
    @commands.has_permissions(manage_messages=True)
    async def archive(self, context: Context, limit: int = 10) -> None:
        log_file = f"{context.channel.id}.log"
        with open(log_file, "w", encoding="UTF-8") as f:
            f.write(
                f'Archived messages from: #{context.channel} ({context.channel.id}) in the guild "{context.guild}" ({context.guild.id}) at {datetime.now().strftime("%d.%m.%Y %H:%M:%S")}\n'
            )
            async for message in context.channel.history(
                limit=limit, before=context.message
            ):
                attachments = []
                for attachment in message.attachments:
                    attachments.append(attachment.url)
                attachments_text = (
                    f"[Attached File{'s' if len(attachments) >= 2 else ''}: {', '.join(attachments)}]"
                    if len(attachments) >= 1
                    else ""
                )
                f.write(
                    f"{message.created_at.strftime('%d.%m.%Y %H:%M:%S')} {message.author} {message.id}: {message.clean_content} {attachments_text}\n"
                )
        f = discord.File(log_file)
        await context.reply(file=f)
        os.remove(log_file)

async def setup(bot) -> None:
    await bot.add_cog(Moderation(bot))
