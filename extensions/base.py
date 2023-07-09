import discord
from discord.ext import commands

print('Loading base...')

@commands.command()
async def cmds(ctx):
    embed=discord.Embed(title="Neurodivergence", description="Commands")
    embed.add_field(name="Base", value=f">cmds - Command list\n>reload - Reload the bot (owner only)", inline=False)
    embed.add_field(name="Utility", value=f">bom - Sends a picture from the BOM Buckland Park radar\n>weather - Sends Adelaide weather information from BOM\n>pl - Search for people on Person Lookup\n>fuel - Sends a list of the cheapest servos to get fuel in Adelaide", inline=False)
    embed.add_field(name="Fun", value=f">hamburger - Sends a random yeehaw hamburger video\n>falcon - Sends a Facebook marketplace link to a random Ford Falcon in Adelaide\n>commodore - Sends a Facebook marketplace link to a random Holden Commodore in Adelaide\n>randonautica - Sends Randonautica coordinates in Adelaide\n>attraction - Sends a random attraction in Adelaide\n>wanted - Sends an image of someone wanted by SA Police\n>cctv - Sends an image from a random CCTV camera\n>song - Sends a song suggestion", inline=False)
    embed.add_field(name="URBEX", value=f">bc - Sends coordinates for a random box culvert drain in South Australia\n>rcp - Sends coordinates for a random RCP drain in South Australia", inline=False)
    embed.add_field(name="ChatGPT", value="Ping Neurodivergence and it will reply as ChatGPT.", inline=False)
    embed.add_field(name="TDUAS", value="Include the word urgent in your ping, and TDUAS will send your ping to that user as an SMS.", inline=False)
    await ctx.reply(embed=embed)

@commands.command()
async def reload(ctx):
    stop()
    
async def setup(bot):
    bot.add_command(cmds)
    bot.add_command(reload)