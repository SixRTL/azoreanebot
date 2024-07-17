import os
import discord
from discord.ext import commands
import pymongo
import asyncio

# Initialize bot and set command prefix
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

# Fetch environment variables from Heroku
TOKEN = os.getenv('DISCORD_TOKEN')
MONGODB_URI = os.getenv('MONGODB_URI')

# Check if the environment variables are set
if not TOKEN or not MONGODB_URI:
    print("Environment variables not set correctly.")
    exit()

# MongoDB connection URI with database name specified
try:
    client = pymongo.MongoClient(MONGODB_URI, tls=True, tlsAllowInvalidCertificates=True)
    db = client.get_database('discord_bot')  # Connect to 'discord_bot' database
    collection = db['characters']  # Collection name for characters
    
    # Send a ping to confirm a successful connection
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")

except pymongo.errors.ConnectionFailure:
    print("Failed to connect to MongoDB. Check your connection URI or MongoDB deployment.")
    exit()

# Dictionary mapping Pokémon natures to D&D stats
pokemon_nature_stats = {
    "Adamant": {"name": "Physical Prowess & Strength", "modifier": {"ATK": 2, "DEF": -1}},
    "Bashful": {"name": "Charisma & Speechcraft", "modifier": {}},
    "Bold": {"name": "Foraging & Perception", "modifier": {"DEF": 2, "ATK": -1}},
    "Brave": {"name": "Physical Prowess & Strength", "modifier": {"ATK": 2, "SPE": -1}},
    "Calm": {"name": "Charisma & Speechcraft", "modifier": {"Sp_DEF": 2, "ATK": -1}},
    "Careful": {"name": "Charisma & Speechcraft", "modifier": {"Sp_DEF": 2, "Sp_ATK": -1}},
    "Docile": {"name": "Intelligence & Knowledge", "modifier": {}},
    "Gentle": {"name": "Charisma & Speechcraft", "modifier": {"Sp_DEF": 2, "DEF": -1}},
    "Hardy": {"name": "Foraging & Perception", "modifier": {}},
    "Hasty": {"name": "Acrobatics & Stealth", "modifier": {"SPE": 2, "DEF": -1}},
    "Impish": {"name": "Acrobatics & Stealth", "modifier": {"DEF": 2, "Sp_ATK": -1}},
    "Jolly": {"name": "Acrobatics & Stealth", "modifier": {"SPE": 2, "Sp_ATK": -1}},
    "Lax": {"name": "Foraging & Perception", "modifier": {"DEF": 2, "Sp_DEF": -1}},
    "Lonely": {"name": "Physical Prowess & Strength", "modifier": {"ATK": 2, "DEF": -1}},
    "Mild": {"name": "Intelligence & Knowledge", "modifier": {"Sp_ATK": 2, "DEF": -1}},
    "Modest": {"name": "Intelligence & Knowledge", "modifier": {"Sp_ATK": 2, "ATK": -1}},
    "Naive": {"name": "Charisma & Speechcraft", "modifier": {"SPE": 2, "Sp_DEF": -1}},
    "Naughty": {"name": "Physical Prowess & Strength", "modifier": {"ATK": 2, "Sp_DEF": -1}},
    "Quiet": {"name": "Charisma & Speechcraft", "modifier": {"Sp_ATK": 2, "SPE": -1}},
    "Quirky": {"name": "Charisma & Speechcraft", "modifier": {}},
    "Rash": {"name": "Foraging & Perception", "modifier": {"Sp_ATK": 2, "Sp_DEF": -1}},
    "Relaxed": {"name": "Acrobatics & Stealth", "modifier": {"DEF": 2, "SPE": -1}},
    "Sassy": {"name": "Charisma & Speechcraft", "modifier": {"Sp_DEF": 2, "SPE": -1}},
    "Serious": {"name": "Intelligence & Knowledge", "modifier": {}},
    "Timid": {"name": "Acrobatics & Stealth", "modifier": {"SPE": 2, "ATK": -1}}
}

# Emoji reactions for stat choices
emoji_mapping = {
    'ATK': '⚔️',   # Sword for Attack
    'Sp_ATK': '🔮',  # Crystal ball for Special Attack
    'DEF': '🛡️',   # Shield for Defense
    'Sp_DEF': '🔒',  # Locked for Special Defense
    'SPE': '⚡'     # Lightning bolt for Speed
}

# Command descriptions (can be modified as needed)
command_descriptions = {
    'register': 'Register your D&D character with a Pokémon nature and distribute 5 stat points.',
    'distribute_stats': 'Distribute additional stat points to your registered character using reactions.',
    'stats': 'View the stats of your registered character.',
    'delete': 'Delete your registered character.',
    'help_menu': 'Show this help menu.'
}

# Command to register a character with reaction-based stat distribution
@bot.command(name='register', help=command_descriptions['register'])
async def register_character(ctx, name: str, profession: str, nature: str):
    # Implementation remains unchanged as per the previous example
    pass

# Command to distribute additional stat points using reactions
@bot.command(name='distribute_stats', help=command_descriptions['distribute_stats'])
async def distribute_stats(ctx):
    # Implementation remains unchanged as per the previous example
    pass

# Command to view the stats of the registered character
@bot.command(name='stats', help=command_descriptions['stats'])
async def view_stats(ctx):
    # Implementation remains unchanged as per the previous example
    pass

# Command to delete the registered character
@bot.command(name='delete', help=command_descriptions['delete'])
async def delete_character(ctx):
    # Implementation remains unchanged as per the previous example
    pass

# Command to show help menu
@bot.command(name='help_menu', help=command_descriptions['help_menu'])
async def help_menu(ctx):
    # Prepare the help menu content
    help_embed = discord.Embed(title='Command Help Menu', description='List of available commands:')
    
    for command in bot.commands:
        help_embed.add_field(name=command.name, value=command_descriptions.get(command.name, 'No description provided'), inline=False)
    
    await ctx.send(embed=help_embed)

# Bot event for initialization confirmation
@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

# Run the bot with the token from Heroku environment variables
bot.run(TOKEN)
