import discord
from discord.ext import commands
from discord.ext.commands import Context

class General(commands.Cog, name="general"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.hybrid_command(
        name="cmds",
        description="List all commands"
    )
    async def cmds(self, ctx):
        embed = discord.Embed(title="Neurodivergence - Help", description="List of all available commands:")
        for i in self.bot.cogs:
            if i == "owner" and not (await self.bot.is_owner(ctx.author)):
                continue
            cog = self.bot.get_cog(i.lower())
            commands = cog.get_commands()
            data = []
            for command in commands:
                description = command.description.partition("\n")[0]
                data.append(f"{command.name} - {description}")
            help_text = "\n".join(data)
            embed.add_field(
                name=i.capitalize(), value=f"```{help_text}```", inline=False
            )
        await ctx.reply(embed=embed)

async def setup(bot) -> None:
    await bot.add_cog(General(bot))