import discord
from discord.ext import commands
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import random
import re
import pyrandonaut
import requests

print('Loading fun...')

# List of attractions
attractions_list = [
    'attractions in Adelaide region',
    'trails in Adelaide region',
    'bars in Adelaide region',
    'restaurants in Adelaide region',
    'cafes in Adelaide region',
    'hikes in Adelaide region',
    'beaches in Adelaide region',
    'things to do in Adelaide region',
    'museums in Adelaide region',
    'outdoors activities in Adelaide region',
    'reserves in Adelaide region',
    'parks in Adelaide region',
    'lookouts in Adelaide region'
]

# List of insecam URLS
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

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/114.0',
}

API_KEY = "token"

my_latitude = -34.921230
my_longitude = 138.599503
radius = 65000

@commands.command()
async def hamburger(ctx):
    # Select a random URL from the list
    # Send the random URL as a message
    await ctx.reply(f"https://mfc.pw/dl/hamburger/hamburger{random.randint(1, 7)}.mp4")

@commands.command()
async def falcon(ctx):
    try:
        # Configure FirefoxOptions and WebDriver
        embed = discord.Embed()
        embed.add_field(name="Here, a falcon", value=f"Please wait...", inline=False)
        msg = await ctx.reply(embed=embed)
        options = Options()
        options.headless = True  # Run Firefox in headless mode
        driver = webdriver.Firefox(options=options)

        # Load the Facebook Marketplace page for Ford AU Falcon listings in Adelaide
        url = "https://www.facebook.com/marketplace/adelaide/search/?query=Ford%20Falcon"
        driver.get(url)

        # Wait for the page to load and extract its HTML content
        html_content = driver.page_source

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')

        # Find all the listing links on the page
        listing_links = soup.find_all('a', href=True)
        marketplace_links = [
            link['href']
            for link in listing_links
            if link['href'].startswith('/marketplace/item')
        ]
        if not marketplace_links:
            raise Exception('No listings found.')

        # Get a random listing link
        random_link = random.choice(marketplace_links)
        listing_url = f"https://www.facebook.com{random_link}"
        
        # Get the listing image
        url = listing_url
        driver.get(url)
        html_content = driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')
        pattern = re.compile(r'^Product photo of')
        listing_image = soup.find('img', alt=pattern)
        image_url = listing_image['src']

        # Send the link to the Discord channel
        embed = discord.Embed()
        embed.add_field(name="Here, a falcon", value=f"[You know you want it]({listing_url})", inline=False)
        embed.set_image(url=image_url)
        await msg.edit(embed=embed)

        # Quit the WebDriver
        driver.quit()

    except Exception as e:
        embed = discord.Embed(title="An error occurred", description=f"{str(e)}")
        await msg.edit(embed=embed)

@commands.command()
async def commodore(ctx):
    try:
        # Configure FirefoxOptions and WebDriver
        embed = discord.Embed()
        embed.add_field(name="A commodore, I guess...", value=f"Please wait...", inline=False)
        msg = await ctx.reply(embed=embed)
        options = Options()
        options.headless = True  # Run Firefox in headless mode
        driver = webdriver.Firefox(options=options)

        # Load the Facebook Marketplace page for Ford AU Falcon listings in Adelaide
        url = "https://www.facebook.com/marketplace/adelaide/search/?query=Holden%20Commodore"
        driver.get(url)

        # Wait for the page to load and extract its HTML content
        html_content = driver.page_source

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')

        # Find all the listing links on the page
        listing_links = soup.find_all('a', href=True)
        marketplace_links = [
            link['href']
            for link in listing_links
            if link['href'].startswith('/marketplace/item')
        ]
        if not marketplace_links:
            raise Exception('No listings found.')

        # Get a random listing link
        random_link = random.choice(marketplace_links)
        listing_url = f"https://www.facebook.com{random_link}"
        
        # Get the listing image
        url = listing_url
        driver.get(url)
        html_content = driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')
        pattern = re.compile(r'^Product photo of')
        listing_image = soup.find('img', alt=pattern)
        image_url = listing_image['src']

        # Send the link to the Discord channel
        embed = discord.Embed()
        embed.add_field(name="A commodore, I guess...", value=f"[Buy it if you really want it?]({listing_url})", inline=False)
        embed.set_image(url=image_url)
        await msg.edit(embed=embed)

        # Quit the WebDriver
        driver.quit()

    except Exception as e:
        embed = discord.Embed(title="An error occurred", description=f"{str(e)}")
        await msg.edit(embed=embed)

@commands.command()
async def randonautica(ctx):
    try:
        embed = discord.Embed(title="Randonautica", description="Please wait...")
        msg = await ctx.reply(embed=embed)
        result = pyrandonaut.get_coordinate(my_latitude, my_longitude, radius)
        gmaps_link = f"https://www.google.com/maps/search/?api=1&query={result}"
        embed = discord.Embed(title="Randonautica", description="Coordinates:")
        embed.add_field(name=f"{result}", value=f"[Google Maps link]({gmaps_link})", inline=False)
        await msg.edit(embed=embed)
    except Exception as e:
        embed = discord.Embed(title="An error occurred", description=f"{str(e)}")
        await msg.edit(embed=embed)

@commands.command()
async def attraction(ctx):
    embed = discord.Embed()
    embed.add_field(name="Random Attraction", value=f"Please wait...", inline=False)
    msg = await ctx.reply(embed=embed)
    # Search for attractions in Adelaide
    attraction_query = random.choice(attractions_list)
    url = f"https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {
        "key": API_KEY,
        "query": attraction_query,
        "region": "au"
    }

    response = requests.get(url, params=params)
    data = response.json()

    # Retrieve the list of attractions
    attractions = data.get("results", [])
    if not attractions:
        embed = discord.Embed(title="No attractions found...")
        await msg.edit(embed=embed)
        return

    # Choose a random attraction
    random_attraction = random.choice(attractions)

    # Extract the required information
    name = random_attraction.get("name", "Unknown Attraction")
    photos = random_attraction.get("photos", [])
    photo_url = photos[0]["photo_reference"] if photos else None
    location = random_attraction.get("geometry", {}).get("location", {})
    lat = location.get("lat", 0)
    lng = location.get("lng", 0)

    # Generate the Google Maps link
    maps_link = f"https://www.google.com/maps/place/{lat},{lng}"

    # Create an embed with the information
    embed = discord.Embed(title=name, url=maps_link)
    if photo_url:
        photo_link = f"https://maps.googleapis.com/maps/api/place/photo?key={API_KEY}&photoreference={photo_url}&maxwidth=800"
        embed.set_image(url=photo_link)

        # Send the message
        await msg.edit(embed=embed)

@commands.command()
async def wanted(ctx):
    embed = discord.Embed()
    embed = discord.Embed(title="Wanted Person", description="Please wait...")
    msg = await ctx.reply(embed=embed)
    random_number = random.randint(1, 16)
    url = f"https://crimestopperssa.com.au/unsolved-cases/?case-date_min-format=d%2Fm%2FY&case-date_max-format=d%2Fm%2FY&wpv_view_count=69&wpv_post_search=&reference-number=&case-date_min=&case-date_min-format=d%2Fm%2FY&case-date_max=&case-date_max-format=d%2Fm%2FY&wpv-case-type=0&wpv_paged={random_number}"

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    image_elements = soup.find_all('img')
    image_urls = [img["src"] for img in image_elements if "crimestoppers-no-photo" not in img["src"]]

    if image_urls:
        embed = discord.Embed(title="Wanted Person")
        random_image_url = random.choice(image_urls)
        embed.set_image(url=random_image_url)
        await msg.edit(embed=embed)
    else:
        embed = discord.Embed(title="Wanted Person", description="No images found.")
        await msg.edit(embed=embed)

@commands.command()
async def cctv(ctx):
    embed = discord.Embed()
    embed = discord.Embed(title="Random CCTV", description="Please wait...")
    msg = await ctx.reply(embed=embed)
    random_number = random.randint(1, 10)
    url = f"{random.choice(insecam_list)}{random_number}"

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    camera_elements = soup.find_all('img', class_="thumbnail-item__img img-responsive")
    camera_urls = [img["src"] for img in camera_elements]

    if camera_urls:
        embed = discord.Embed(title="Random CCTV")
        random_camera_url = random.choice(camera_urls)
        embed.set_image(url=random_camera_url)
        await msg.edit(embed=embed)
    else:
        embed = discord.Embed(title="Random CCTV", description="No cameras found.")
        await msg.edit(embed=embed)

@commands.command()
async def song(ctx):
    with open("extensions/fun/musiclist.txt", 'r') as file:
        lines = file.readlines()
    
    random_line = random.choice(lines)

    embed = discord.Embed(title="Song Suggestion", description=random_line.strip())
    await ctx.reply(embed=embed)

async def setup(bot):
    bot.add_command(hamburger)
    bot.add_command(falcon)
    bot.add_command(commodore)
    bot.add_command(randonautica)
    bot.add_command(attraction)
    bot.add_command(wanted)
    bot.add_command(cctv)
    bot.add_command(song)