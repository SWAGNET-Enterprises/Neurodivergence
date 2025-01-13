import discord
from discord.ext import commands
from discord.ext.commands import Context
import aiohttp
import os
import io

class Sidepipe(commands.Cog, name="sidepipe"):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.whitelisted_guilds = [
            discord.Object(id=1161606292541014056)
        ]

    async def cog_check(self, ctx: commands.Context) -> bool:
        if ctx.guild.id in [guild.id for guild in self.whitelisted_guilds]:
            return True
        else:
            await ctx.reply("This command can only be used inside The Sidepipe.")
            return False
    
    @commands.hybrid_command(
        name="cctvselfie",
        description="Take a selfie using my CCTV cameras",
    )
    async def cctvselfie(self, ctx, camera="2"):
        embed = discord.Embed(title=f"CCTV Selfie - Camera {camera}", description=f"Please wait...")
        msg = await ctx.reply(embed=embed)

        async with aiohttp.ClientSession() as session:
                url = os.getenv("HASS_URL")
                headers = {'Authorization': f'Bearer {os.getenv("HASS_TOKEN")}'}
                async with session.get(url=f"{url}/api/camera_proxy/camera.{camera}", headers=headers) as response:
                    if response.status != 200:
                        embed = discord.Embed(title=f"CCTV Selfie - Camera {camera}", description=f"Error fetching image.")
                        await msg.edit(embed=embed)
                        return
                    image_data = io.BytesIO(await response.read())
                    await ctx.reply(file=discord.File(image_data, filename=f"{ctx.message.id}.jpg"))
                    await msg.delete()

async def setup(bot) -> None:
    await bot.add_cog(Sidepipe(bot))