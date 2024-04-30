import discord
from discord.ext import commands
from discord.ext.commands import Context
import requests
from bs4 import BeautifulSoup
import re
import json

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
        rainfall_chance = div_element.find('em', class_="pop").text
        description = div_element.find('p').text
    
        if soup.find("div", class_="day main"):
            embed = discord.Embed(title=f"BOM Weather - {town.capitalize()}")
            embed.add_field(name="Max Temp", value=f"{max_temp}°C", inline=True)
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
        profile_divs = soup.find("div", class_="col-12 col-md-8 order-first order-md-last mb-4 mb-md-0").find_all("div", class_="buttons-fix")
        if not profile_divs:
            embed = discord.Embed(title=f"Person Lookup - {query.capitalize()}", description="No results found.")
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
        response = requests.get(f"https://fuelprice.io/{state}/{town}/", headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")

        # Find all price divs
        results_box = soup.find("ul", class_="cheapest-stations")
        servo_divs = results_box.find_all("li")
        if not servo_divs:
            embed = discord.Embed(title=f"Fuel Prices - {town.capitalize()}", description="No results found.")
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
    async def openports(self, ctx, ip=""):
        embed = discord.Embed(title=f"Open ports - {ip}", description="Please wait...")
        msg = await ctx.reply(embed=embed)
        shodan_json = json.loads(requests.get("https://internetdb.shodan.io/" + ip).content)

        if("detail" in shodan_json and shodan_json["detail"] == "No information available"):
            embed = discord.Embed(title=f"Open ports - {ip}", description="No information available for this IP address.")
            await msg.edit(embed=embed)
        else:
            embed=discord.Embed(title=f"Open ports - {ip}")
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
        response = requests.get(f"https://www.adelaidemetro.com.au/search?f.Top%7Cadl-metro-stops=Stops&query={stop}", headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")

        # Find name & ID of stop
        stop_name = soup.find("span", class_="result-name").text.strip()
        stop_id = re.search(r'(\b\d{5}\b)', soup.find("p", class_="result-description").get_text(strip=True)).group()
        if not stop_id:
            embed = discord.Embed(title=f"Adelaide Metro", description="Stop not found.")
            return
        
        # Get departures from API and add them to embed
        embed = discord.Embed(title=f"Adelaide Metro - {stop_name}", description="next services")
        services = json.loads(requests.get(f"https://api-cloudfront.adelaidemetro.com.au/stops/next-services?stop={stop_id}").content)['services']
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
        
        # Get registration info from EzyReg API and add them to embed
        ezyreg_json = json.loads(requests.post("https://account.ezyreg.sa.gov.au/r/veh/an/checkRegistration", json={'plateNumber': plate, 'registrationType': 'VEHICLE'}).content)
        if("description" in ezyreg_json):
            embed = discord.Embed(title=f"Check Registration - {plate}", description="The plate number entered is not currently assigned to a vehicle. ")
            await msg.edit(embed=embed)
            return
        embed = discord.Embed(title=f"Check Registration - {plate}")
        embed.add_field(name="Expiry Date", value=ezyreg_json["checkRegistrationDetails"][0]["expiryDate"], inline=False)
        embed.add_field(name="Make", value=ezyreg_json["checkRegistrationDetails"][0]["vehicleMake"], inline=False)
        embed.add_field(name="Body Type", value=ezyreg_json["checkRegistrationDetails"][0]["vehicleBodyType"], inline=False)
        embed.add_field(name="Primary Colour", value=ezyreg_json["checkRegistrationDetails"][0]["primaryColour"], inline=False)
        embed.add_field(name="CTP Insurer", value=ezyreg_json["checkRegistrationDetails"][0]["ctpInsurer"], inline=False)
        embed.add_field(name="CTP Ins. Premium Class", value=ezyreg_json["checkRegistrationDetails"][0]["insuranceClass"], inline=False)
        embed.add_field(name="VIN", value=ezyreg_json["checkRegistrationDetails"][0]["vinChassis"], inline=False)
        await msg.edit(embed=embed)

async def setup(bot) -> None:
    await bot.add_cog(Utility(bot))