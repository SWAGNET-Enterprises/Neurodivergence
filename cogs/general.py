import discord
from discord.ext import commands
from discord.ext.commands import Context
import requests
from bs4 import BeautifulSoup
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/114.0',
}

class Utility(commands.Cog, name="utility"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.hybrid_command(
        name="weather",
        description="See the current weather (Australia)",
    )
    async def weather(self, ctx, town="adelaide", state="sa"):
        embed = discord.Embed(title=f"BOM Weather - {town.capitalize()}", description="Please wait...")
        msg = await ctx.send(embed=embed)

        response = requests.get(f"http://www.bom.gov.au/{state}/forecasts/{town}.shtml", headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")

        div_element = soup.find("div", class_="day main")
        summary = div_element.find('dd', class_="summary").text
        max_temp = div_element.find('em', class_="max").text
        min_temp = div_element.find('em', class_="min").text
        rainfall_chance = div_element.find('em', class_="pop").text
        description = div_element.find('p').text
    
        if div_element:
            embed = discord.Embed(title=f"BOM Weather - {town.capitalize()}")
            embed.add_field(name="Max Temp", value=f"{max_temp}°C", inline=True)
            embed.add_field(name="Min Temp", value=f"{min_temp}°C", inline=True)
            embed.add_field(name="Chance of any rain", value=f"{rainfall_chance}", inline=True)
            embed.add_field(name=f"{summary}", value=f"{description}", inline=False)
            await msg.edit(embed=embed)
        else:
            embed = discord.Embed(title="Weather", description="Failed to retreive weather.")
            await msg.edit(embed=embed)

    @commands.hybrid_command(
        name="pl",
        description="Find contact details using Person Lookup (Australia)",
    )
    async def pl(self, ctx, query="", suburb="", state=""):
        embed = discord.Embed(title=f"Person Lookup - {query.capitalize()}", description="Please wait...")
        msg = await ctx.reply(embed=embed)
        response = requests.get(f"https://personlookup.com.au/search?page=1&q={query}&suburb={suburb}&state={state}", headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")

        # Find all profile divs
        results_box = soup.find("div", class_="col-12 col-md-8 order-first order-md-last mb-4 mb-md-0")
        profile_divs = results_box.find_all("div", class_="buttons-fix")

        if not profile_divs:
            embed = discord.Embed(title=f"Person Lookup - {query.capitalize()}", description="No results found.")
            return

        # Create a new Discord embed
        embed = discord.Embed(title=f"Person Lookup - {query.capitalize()}")

        # Iterate over each profile div and extract the relevant information
        for profile in profile_divs:
            # Get the name from the profile
            name = profile.find("a", class_="stretched-link").text.strip()

            # Get the address from the profile
            address_div = profile.find("div", class_="col-12 col-sm-6 col-md-8 col-lg-9 col-xl-6 mb-2 mb-sm-0")
            address = address_div.text.strip()

            # Get the phone number from the profile
            phone_div = profile.find("div", class_="col-12 offset-0 col-sm-6 offset-sm-0 col-md-8 offset-md-4 col-lg-9 offset-lg-3 col-xl-3 offset-xl-0")
            phone = phone_div.text.strip()

            # Add the name, address, and phone number as fields in the embed
            embed.add_field(name=name, value=f"{address}\n{phone}", inline=False)

        # Send the embed to the Discord channel
        await msg.edit(embed=embed)

    @commands.hybrid_command(
        name="fuel",
        description="Retrieve fuel prices (Australia)",
    )
    async def fuel(self, ctx, town="adelaide", state="sa"):
        embed = discord.Embed(title=f"Fuel Prices - {town.capitalize()}", description="Please wait...")
        msg = await ctx.reply(embed=embed)

        response = requests.get(f"https://fuelprice.io/{state}/{town}/", headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")

        # Find all price divs
        results_box = soup.find("ul", class_="cheapest-stations")
        servo_divs = results_box.find_all("li")

        if not servo_divs:
            embed = discord.Embed(title=f"Fuel Prices - {town.capitalize()}", description="No results found.")
            return

        # Create a new Discord embed
        embed = discord.Embed(title=f"Fuel Prices - {town.capitalize()}", description="low to high")

        # Iterate over each price div and extract the relevant information
        for servo in servo_divs:
            # Get the servo name
            name = servo.find("strong").text.strip()

            # Get the fuel price
            price_text = servo.get_text(strip=True)
            price = re.search(r'(\d+(?:\.\d+)?)', price_text).group()

            # Add the name of the servo, and it's fuel price as fields in the embed
            embed.add_field(name=name, value=price, inline=False)

        # Send the embed to the Discord channel
        await msg.edit(embed=embed)

async def setup(bot) -> None:
    await bot.add_cog(Utility(bot))