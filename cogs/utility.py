import discord
from discord.ext import commands
from discord.ext.commands import Context
import aiohttp
from bs4 import BeautifulSoup
import re
import json
import base64
from PIL import Image
import io
import os
import random

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/114.0'}

auto1111_hosts = json.loads(os.environ['AUTO1111_HOSTS'])

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

        async with aiohttp.ClientSession() as session:
            url = f"http://www.bom.gov.au/{state}/forecasts/{town}.shtml"
            async with session.get(url, headers=headers) as response:
                if response.status != 200:
                    embed = discord.Embed(title="Weather", description="Failed to retrieve weather.")
                    await msg.edit(embed=embed)
                    return
                soup = BeautifulSoup(await response.text(), "html.parser")

                # Find the main weather div
                div_element = soup.find("div", class_="day main")
                if not div_element:
                    embed = discord.Embed(title="Weather", description="No weather information found for this location.")
                    await msg.edit(embed=embed)
                    return

                # Extract weather information
                summary = div_element.find('dd', class_="summary").text
                max_temp = div_element.find('em', class_="max").text
                rainfall_chance = div_element.find('em', class_="pop").text
                description = div_element.find('p').text

                # Create and send the embed with weather information
                embed = discord.Embed(title=f"BOM Weather - {town.capitalize()}")
                embed.add_field(name="Max Temp", value=f"{max_temp}°C", inline=True)
                embed.add_field(name="Chance of any rain", value=f"{rainfall_chance}", inline=True)
                embed.add_field(name=f"{summary}", value=f"{description}", inline=False)
                await msg.edit(embed=embed)

    @commands.hybrid_command(
        name="pl",
        description="Find contact details using Person Lookup (Australia)",
    )
    async def pl(self, ctx, query="", suburb="", state=""):
        embed = discord.Embed(title=f"Person Lookup - {query.capitalize()}", description="Please wait...")
        msg = await ctx.reply(embed=embed)

        async with aiohttp.ClientSession() as session:
            url = f"https://personlookup.com.au/search?page=1&q={query}&suburb={suburb}&state={state}"
            async with session.get(url, headers=headers) as response:
                if response.status != 200:
                    embed = discord.Embed(title=f"Person Lookup - {query.capitalize()}", description="Error fetching results.")
                    await msg.edit(embed=embed)
                    return
                soup = BeautifulSoup(await response.text(), "html.parser")

                # Find all profile divs
                profile_divs = soup.find("div", class_="col-12 col-md-8 order-first order-md-last mb-4 mb-md-0").find_all("div", class_="buttons-fix")
                if not profile_divs:
                    embed = discord.Embed(title=f"Person Lookup - {query.capitalize()}", description="No results found.")
                    await msg.edit(embed=embed)
                    return

                # Iterate over each profile div and extract the relevant information then add to embed
                embed = discord.Embed(title=f"Person Lookup - {query.capitalize()}")
                for profile in profile_divs:
                    name = profile.find("a", class_="stretched-link").text.strip()
                    address = profile.find("div", class_="col-12 col-sm-6 col-md-8 col-lg-9 col-xl-6 mb-2 mb-sm-0").text.strip()
                    phone = profile.find("div", class_="col-12 offset-0 col-sm-6 offset-sm-0 col-md-8 offset-md-4 col-lg-9 offset-lg-3 col-xl-3 offset-xl-0").text.strip()
                    embed.add_field(name=name, value=f"{address}\n{phone}", inline=False)
                await msg.edit(embed=embed)

    @commands.hybrid_command(
        name="fuel",
        description="Retrieve fuel prices (Australia)",
    )
    async def fuel(self, ctx, town="adelaide", state="sa"):
        embed = discord.Embed(title=f"Fuel Prices - {town.capitalize()}", description="Please wait...")
        msg = await ctx.reply(embed=embed)

        async with aiohttp.ClientSession() as session:
            url = f"https://fuelprice.io/{state}/{town}/"
            async with session.get(url, headers=headers) as response:
                if response.status != 200:
                    embed = discord.Embed(title=f"Fuel Prices - {town.capitalize()}", description="Error fetching fuel prices.")
                    await msg.edit(embed=embed)
                    return
            soup = BeautifulSoup(await response.text(), "html.parser")

            # Find all price divs
            results_box = soup.find("ul", class_="cheapest-stations")
            servo_divs = results_box.find_all("li")
            if not servo_divs:
                embed = discord.Embed(title=f"Fuel Prices - {town.capitalize()}", description="No results found.")
                await msg.edit(embed=embed)
                return

            # Iterate over each price div and extract the relevant information then add to embed
            embed = discord.Embed(title=f"Fuel Prices - {town.capitalize()}", description="low to high")
            for servo in servo_divs:
                name = servo.find("strong").text.strip()
                price_text = servo.get_text(strip=True)
                price = re.search(r'(\d+(?:\.\d+)?)', price_text).group()
                embed.add_field(name=name, value=price, inline=False)
            await msg.edit(embed=embed)

    @commands.hybrid_command(
        name="openports",
        description="Retrieve open ports on a host from Shodan",
    )
    async def openports(self, ctx, ip="168.138.9.168"):
        embed = discord.Embed(title=f"Open ports - {ip}", description="Please wait...")
        msg = await ctx.reply(embed=embed)

        async with aiohttp.ClientSession() as session:
            url = f"https://internetdb.shodan.io/{ip}"
            async with session.get(url) as response:
                if response.status == 404:
                    embed = discord.Embed(title=f"Open ports - {ip}", description="No information available for this IP address.")
                    await msg.edit(embed=embed)
                    return
                elif response.status != 200:
                    # Handle other potential errors
                    print(f"Error fetching Shodan data for {ip} (status code: {response.status})")
                    embed = discord.Embed(title=f"Open ports - {ip}", description="An error occurred while fetching data.")
                    await msg.edit(embed=embed)
                    return
                shodan_json = await response.json()

        if "detail" in shodan_json and shodan_json["detail"] == "No information available":
            embed = discord.Embed(title=f"Open ports - {ip}", description="No information available for this IP address.")
        else:
            embed = discord.Embed(title=f"Open ports - {ip}")
            embed.add_field(name="Hostnames", value=shodan_json["hostnames"], inline=False)
            embed.add_field(name="Open Ports", value=shodan_json["ports"], inline=False)
            embed.add_field(name="Tags", value=shodan_json["tags"], inline=False)
            embed.add_field(name="CPEs", value=shodan_json["cpes"], inline=False)
            embed.add_field(name="Vulns", value=shodan_json["vulns"], inline=False)
        await msg.edit(embed=embed)
    
    @commands.hybrid_command(
        name="metro",
        description="See departures on the Adelaide Metro network",
    )
    async def metro(self, ctx, stop="16490"):
        embed = discord.Embed(title=f"Adelaide Metro", description="Please wait...")
        msg = await ctx.reply(embed=embed)

        async with aiohttp.ClientSession() as session:
            # Get stop information
            async with session.get(f"https://www.adelaidemetro.com.au/search?f.Top%7Cadl-metro-stops=Stops&query={stop}", headers=headers) as response:
                if response.status != 200:
                    embed = discord.Embed(title=f"Adelaide Metro", description="Error fetching stop information.")
                    await msg.edit(embed=embed)
                    return
                soup = BeautifulSoup(await response.text(), "html.parser")

                # Find name & ID of stop
                stop_name = soup.find("span", class_="result-name").text.strip()
                stop_id = re.search(r'(\b\d{5}\b)', soup.find("p", class_="result-description").get_text(strip=True)).group()
                if not stop_id:
                    embed = discord.Embed(title=f"Adelaide Metro", description="Stop not found.")
                    await msg.edit(embed=embed)
                    return

            # Get departures using API
            async with session.get(f"https://api-cloudfront.adelaidemetro.com.au/stops/next-services?stop={stop_id}") as response:
                if response.status != 200:
                    embed = discord.Embed(title=f"Adelaide Metro", description="Error fetching departures.")
                    await msg.edit(embed=embed)
                    return
                services_json = await response.json()
                services = services_json['services']

        embed = discord.Embed(title=f"Adelaide Metro - {stop_name}", description="next services")
        for service in services:
            embed.add_field(name=service['id'], value=f"{service['min']} mins - {service['scheduled']}", inline=False)
        await msg.edit(embed=embed)
        
    @commands.hybrid_command(
        name="rego",
        description="Check a vehicles registration (South Australia)",
    )
    async def rego(self, ctx, plate="wgz422"):
        embed = discord.Embed(title=f"Check Registration - {plate}", description="Please wait...")
        msg = await ctx.reply(embed=embed)

        async with aiohttp.ClientSession() as session:
            url = "https://account.ezyreg.sa.gov.au/r/veh/an/checkRegistration"
            data = {"plateNumber": plate, "registrationType": "VEHICLE"}
            async with session.post(url, json=data) as response:
                if response.status != 200:
                    embed = discord.Embed(title=f"Check Registration - {plate}", description="No results found.")
                    await msg.edit(embed=embed)
                    return
                ezyreg_json = await response.json()

        embed = discord.Embed(title=f"Check Registration - {plate}")
        embed.add_field(name="Expiry Date", value=ezyreg_json["checkRegistrationDetails"][0]["expiryDate"], inline=False)
        embed.add_field(name="Make", value=ezyreg_json["checkRegistrationDetails"][0]["vehicleMake"], inline=False)
        embed.add_field(name="Body Type", value=ezyreg_json["checkRegistrationDetails"][0]["vehicleBodyType"], inline=False)
        embed.add_field(name="Primary Colour", value=ezyreg_json["checkRegistrationDetails"][0]["primaryColour"], inline=False)
        embed.add_field(name="CTP Insurer", value=ezyreg_json["checkRegistrationDetails"][0]["ctpInsurer"], inline=False)
        embed.add_field(name="CTP Ins. Premium Class", value=ezyreg_json["checkRegistrationDetails"][0]["insuranceClass"], inline=False)
        embed.add_field(name="VIN", value=ezyreg_json["checkRegistrationDetails"][0]["vinChassis"], inline=False)
        await msg.edit(embed=embed)

    @commands.hybrid_command(
        name="gemini",
        description="Talk to the Google Gemini AI",
    )
    async def gemini(self, ctx, prompt="Give me a short description of yourself."):
        embed = discord.Embed(title="Gemini", description="Please wait...")
        msg = await ctx.reply(embed=embed)

        async with aiohttp.ClientSession() as session:
            url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={os.getenv("GEMINI_KEY")}'
            data = {"contents": [{"parts": [{"text": prompt}]}]}
            async with session.post(url, json=data) as response:
                if response.status != 200:
                    embed = discord.Embed(title="Gemini", description="There was an error communicating with the Gemini API.")
                    await msg.edit(embed=embed)
                    return
                gemini_json = await response.json()

        embed = discord.Embed(title="Gemini", description=gemini_json["candidates"][0]["content"]["parts"][0]["text"])
        await msg.edit(embed=embed)

    @commands.hybrid_command(
        name="sd",
        description="Generate an image using Stable Diffusion",
    )
    async def sd(self, ctx, prompt="masterpiece, best_quality, 1male, solo, ((aisan, aiden)), hell_background, fire, membranous_wings, devil_horns <lora:y-aidenStrict:0.85>", neg_prompt="deformed_hands, (worst quality, low quality:1.4)", cfg="7", steps="35", sampler="Euler a", restore_faces="true"):
        random.shuffle(auto1111_hosts)
        embed = discord.Embed(title=f"Stable Diffusion - {prompt}", description="Please wait...")
        msg = await ctx.reply(embed=embed)

        async with aiohttp.ClientSession() as session:
            for host in auto1111_hosts:
                try:
                    async with session.post(url=f"{host}/sdapi/v1/txt2img", json={"prompt": prompt, "cfg_scale": cfg, "width": 672, "height": 672, "restore_faces": restore_faces, "negative_prompt": neg_prompt, "steps": steps, "sampler_index": sampler}) as response:
                        if response.status != 200:
                            return
                        sd_json = await response.json()
                except:
                    continue

                gen = f"{ctx.message.id}.jpg"
                with open(gen, "wb") as f:
                    f.write(base64.b64decode(sd_json['images'][0]))
                await ctx.reply(file=discord.File(gen))
                os.remove(gen)
                await msg.delete()
                break

        embed = discord.Embed(title=f"Stable Diffusion - {prompt}", description="All Stable Diffusion hosts are currently offline.")
        await msg.edit(embed=embed)       
            
async def setup(bot) -> None:
    await bot.add_cog(Utility(bot))