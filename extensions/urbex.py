import discord
from discord.ext import commands
import random
import json
from pyproj import Proj, transform
from urllib.parse import urlencode

print('Loading urbex...')

# Google Maps API parameters
GOOGLE_MAPS_API_BASE_URL = 'https://www.google.com/maps/search/?'
GOOGLE_MAPS_API_PARAMS = {
    'api': 1,
    'query': ''
}

# GEOJson File Location
GEOJSON_FILE_PATH = 'extensions/urbex/WATER_Stormwater_GDA2020.geojson'

@commands.command()
async def bc(ctx):
    embed = discord.Embed(title="Random box culvert in South Australia", description="Please wait...")
    msg = await ctx.reply(embed=embed)
    with open(GEOJSON_FILE_PATH, 'r') as f:
        geojson_data = json.load(f)

    features = geojson_data['features']

    # Filter the features to find box culvert drains
    box_culvert_drains = [feature for feature in features if feature['properties'].get('COMMENTS') == 'Box Culvert']

    # Check if any box culvert drains were found
    if len(box_culvert_drains) == 0:
        embed = discord.Embed(title="Random box culvert in South Australia", description="No box culvert drains found in the dataset.")
        await msg.edit(embed=embed)
    else:
        # Select a random box culvert drain from the dataset
        random_box_culvert_drain = random.choice(box_culvert_drains)

        # Get the coordinates of the drain
        drain_coordinates = random_box_culvert_drain['geometry']['coordinates'][0]

        # Assuming the coordinates are in [longitude, latitude] format
        drain_longitude, drain_latitude = drain_coordinates[0], drain_coordinates[1]

        # Define the coordinate systems for conversion
        input_crs = Proj('EPSG:7844')  # GDA2020
        output_crs = Proj('EPSG:4326')  # WGS84

        # Convert coordinates to WGS84
        converted_longitude, converted_latitude = transform(input_crs, output_crs, drain_longitude, drain_latitude)

        # Generate Google Maps link
        google_maps_query = f"{converted_latitude},{converted_longitude}"
        google_maps_params = GOOGLE_MAPS_API_PARAMS.copy()
        google_maps_params['query'] = google_maps_query
        google_maps_link = GOOGLE_MAPS_API_BASE_URL + urlencode(google_maps_params)

        embed = discord.Embed(title="Random box culvert in South Australia", description="Coordinates:")
        embed.add_field(name=f"({converted_latitude}, {converted_longitude})", value=f"[Google Maps link]({google_maps_link})", inline=False)
        await msg.edit(embed=embed)

@commands.command()
async def rcp(ctx):
    embed = discord.Embed(title="Random RCP in South Australia", description="Please wait...")
    msg = await ctx.reply(embed=embed)
    with open(GEOJSON_FILE_PATH, 'r') as f:
        geojson_data = json.load(f)

    features = geojson_data['features']

    # Filter the features to find RCPs
    RCPs = [feature for feature in features if feature['properties'].get('COMMENTS') == 'Reinforced Concrete Pipe']

    # Check if any RCPs were found
    if len(RCPs) == 0:
        embed = discord.Embed(title="Random RCP in South Australia", description="No RCPs found in the dataset.")
        await msg.edit(embed=embed)
    else:
        # Select a random RCP from the dataset
        random_RCP = random.choice(RCPs)

        # Get the coordinates of the drain
        drain_coordinates = random_RCP['geometry']['coordinates'][0]

        # Assuming the coordinates are in [longitude, latitude] format
        drain_longitude, drain_latitude = drain_coordinates[0], drain_coordinates[1]

        # Define the coordinate systems for conversion
        input_crs = Proj('EPSG:7844')  # GDA2020
        output_crs = Proj('EPSG:4326')  # WGS84

        # Convert coordinates to WGS84
        converted_longitude, converted_latitude = transform(input_crs, output_crs, drain_longitude, drain_latitude)

        # Generate Google Maps link
        google_maps_query = f"{converted_latitude},{converted_longitude}"
        google_maps_params = GOOGLE_MAPS_API_PARAMS.copy()
        google_maps_params['query'] = google_maps_query
        google_maps_link = GOOGLE_MAPS_API_BASE_URL + urlencode(google_maps_params)

        embed = discord.Embed(title="Random RCP in South Australia", description="Coordinates:")
        embed.add_field(name=f"({converted_latitude}, {converted_longitude})", value=f"[Google Maps link]({google_maps_link})", inline=False)
        await msg.edit(embed=embed)

async def setup(bot):
    bot.add_command(bc)
    bot.add_command(rcp)