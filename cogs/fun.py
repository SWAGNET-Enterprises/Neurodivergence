import discord
from discord.ext import commands
from discord.ext.commands import Context
import aiohttp
import random
from random import choice
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/114.0',
}

insecam_list = [
    'http://insecam.org/en/bytype/AxisMkII/?page=',
    'http://insecam.org/en/bytype/Bosch/?page=',
    'http://insecam.org/en/bytype/Defeway/?page=',
    'http://insecam.org/en/bytype/Hi3516/?page=',
    'http://insecam.org/en/bytype/Fullhan/?page=',
    'http://insecam.org/en/bytype/Megapixel/?page=',
    'http://insecam.org/en/bytype/Panasonic/?page=',
    'http://insecam.org/en/bytype/PanasonicHD/?page=',
    'http://insecam.org/en/bytype/Sony/?page=',
    'http://insecam.org/en/bytype/StarDot/?page=',
    'http://insecam.org/en/bytype/SunellSecurity/?page=',
    'http://insecam.org/en/bytype/Vivotek/?page='
]

class Fun(commands.Cog, name="fun"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.hybrid_command(
        name="wanted",
        description="Retrieve a picture of a random wanted person (Crime Stoppers SA)",
    )
    async def wanted(self, ctx):
        embed = discord.Embed(title="Wanted Person - Crime Stoppers SA", description="Please wait...")
        msg = await ctx.reply(embed=embed)

        async with aiohttp.ClientSession() as session:
            # Construct the URL with a random page number
            page = random.randint(1, 16)
            url = f"https://crimestopperssa.com.au/unsolved-cases/?case-date_min-format=d%2Fm%2FY&case-date_max-format=d%2Fm%2FY&wpv_view_count=69&wpv_post_search=&reference-number=&case-date_min=&case-date_min-format=d%2Fm%2FY&case-date_max=&case-date_max-format=d%2Fm%2FY&wpv-case-type=0&wpv_paged={page}"

            async with session.get(url, headers=headers) as response:
                if response.status != 200:
                    embed = discord.Embed(title="Wanted Person - Crime Stoppers SA", description=f"Error retrieving image. {response.status}")
                    await msg.edit(embed=embed)
                    return
                soup = BeautifulSoup(await response.text(), "html.parser")

                # Find image elements and filter out default "no photo" images
                image_elements = soup.find_all('img', class_="attachment-thumb size-thumb wp-post-image")
                image_urls = [img["src"] for img in image_elements if "crimestoppers-no-photo" not in img["src"]]

                if image_urls:
                    # Choose a random image URL and set it as the embed image
                    embed = discord.Embed(title="Wanted Person - Crime Stoppers SA")
                    embed.set_image(url=random.choice(image_urls))
                    await msg.edit(embed=embed)
                else:
                    embed = discord.Embed(title="Wanted Person - Crime Stoppers SA", description="No images found on this page.")
                    await msg.edit(embed=embed)
            
    @commands.hybrid_command(
        name="cctv",
        description="Retrieve a stream from a random insecure CCTV camera",
    )
    async def cctv(self, ctx):
        embed = discord.Embed(title="Random CCTV", description="Please wait...")
        msg = await ctx.reply(embed=embed)

        async with aiohttp.ClientSession() as session:
            # Choose a random Insecam URL and a random camera number
            insecam_url = choice(insecam_list)
            camera_number = random.randint(1, 10)
            url = f"{insecam_url}{camera_number}"

            async with session.get(url, headers=headers) as response:
                if response.status != 200:
                    embed = discord.Embed(title="Random CCTV", description=f"Error retrieving stream. {response.status}")
                    await msg.edit(embed=embed)
                    return
                soup = BeautifulSoup(await response.text(), "html.parser")

                # Find camera elements and extract URLs
                camera_elements = soup.find_all('img', class_="thumbnail-item__img img-responsive")
                camera_urls = [img["src"] for img in camera_elements]

                if camera_urls:
                    embed = discord.Embed(title="Random CCTV")
                    embed.set_image(url=random.choice(camera_urls))
                    await msg.edit(embed=embed)
                else:
                    embed = discord.Embed(title="Random CCTV", description="No cameras found on this page.")
                    await msg.edit(embed=embed)

async def setup(bot) -> None:
    await bot.add_cog(Fun(bot))