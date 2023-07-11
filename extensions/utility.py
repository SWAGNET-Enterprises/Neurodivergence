from discord.ext import commands
import discord
import os
import urllib.request
import requests
from bs4 import BeautifulSoup
import re

print('Loading utility...')

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/114.0',
}

@commands.command()
async def bom(ctx):
    # Radar file details
    radar_url = "ftp://ftp.bom.gov.au/anon/gen/radar/IDR644.gif"

    try:
        # Download the radar file
        local_filename = "IDR644.gif"
        urllib.request.urlretrieve(radar_url, local_filename)

        # Send the radar image as a regular attachment
        await ctx.reply(file=discord.File(local_filename))

        # Delete the downloaded radar file
        os.remove(local_filename)

    except Exception as e:
        # Handle any exceptions or errors that occur during file downloading
        await ctx.send(f"An error occurred: {str(e)}")

@commands.command()
async def weather(ctx, query=None):
    embed = discord.Embed()
    embed = discord.Embed(title="Weather", description="Please wait...")
    msg = await ctx.reply(embed=embed)

    if query is None:
        url = f"http://www.bom.gov.au/sa/forecasts/adelaide.shtml"
    else:
        url = f"http://www.bom.gov.au/sa/forecasts/{query}.shtml"

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    div_element = soup.find("div", class_="day main")
    summary = div_element.find('dd', class_="summary").text
    temp = div_element.find('em', class_="max").text
    #rainfall = div_element.find('em', class_="rain").text
    rainfall_chance = div_element.find('em', class_="pop").text
    description = div_element.find('p').text
    
    if div_element:
        embed = discord.Embed(title="Weather")
        embed.add_field(name="Temperature", value=f"{temp}°C", inline=True)
        #embed.add_field(name="Possible rainfall", value=f"{rainfall}", inline=True)
        embed.add_field(name="Chance of any rain", value=f"{rainfall_chance}", inline=True)
        embed.add_field(name=f"{summary}", value=f"{description}", inline=False)
        await msg.edit(embed=embed)
    else:
        embed = discord.Embed(title="Weather", description="Failed to retreive weather.")
        await msg.edit(embed=embed)

@commands.command()
async def pl(ctx, query, suburb, state):
    embed = discord.Embed()
    embed = discord.Embed(title="Person Lookup", description="Please wait...")
    msg = await ctx.reply(embed=embed)
    url = f"https://personlookup.com.au/search?page=1&q={query}&suburb={suburb}&state={state}"

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    # Find all profile divs
    results_box = soup.find("div", class_="col-12 col-md-8 order-first order-md-last mb-4 mb-md-0")
    profile_divs = results_box.find_all("div", class_="buttons-fix")

    if not profile_divs:
        embed = discord.Embed(title="Person Lookup", description="No results found.")
        return

    # Create a new Discord embed
    embed = discord.Embed(title="Person Lookup")

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

@commands.command()
async def fuel(ctx, query=None):
    embed = discord.Embed()
    embed = discord.Embed(title="Fuel Prices", description="Please wait...")
    msg = await ctx.reply(embed=embed)

    if query is None:
        url = f"https://fuelprice.io/sa/adelaide/"
    else:
        url = f"https://fuelprice.io/sa/{query}/"

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    # Find all profile divs
    results_box = soup.find("ul", class_="cheapest-stations")
    profile_divs = results_box.find_all("li")

    if not profile_divs:
        embed = discord.Embed(title="Fuel Prices", description="No results found.")
        return

    # Create a new Discord embed
    embed = discord.Embed(title="Fuel Prices", description="low to high")

    # Iterate over each profile div and extract the relevant information
    for profile in profile_divs:
        # Get the name from the profile
        name = profile.find("strong").text.strip()

        # Get the address from the profile
        number_text = profile.get_text(strip=True)
        number = re.search(r'(\d+(?:\.\d+)?)', number_text).group()

        # Add the name, address, and phone number as fields in the embed
        embed.add_field(name=name, value=number, inline=False)

    # Send the embed to the Discord channel
    await msg.edit(embed=embed)

async def setup(bot):
    bot.add_command(bom)
    bot.add_command(weather)
    bot.add_command(pl)
    bot.add_command(fuel)