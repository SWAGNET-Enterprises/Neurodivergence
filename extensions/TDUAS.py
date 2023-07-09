import discord
from discord.ext import commands
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse

print('Loading TDUAS...')

# Twilio API credentials
TWILIO_ACCOUNT_SID = 'sid'
TWILIO_AUTH_TOKEN = 'token'
TWILIO_PHONE_NUMBER = 'number'

# File containing the phone numbers
PHONE_NUMBER_FILE = 'extensions/TDUAS/numbers.txt'

# Initialize the Twilio client
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

class MessageListener(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        mentioned_users = message.mentions
        mentioned_user_ids = [str(user.id) for user in mentioned_users]

        if mentioned_user_ids:
            if "urgent" in message.content.lower():
                if isinstance(message.channel, discord.TextChannel):
                    # Get the content of the message
                    channel = message.channel
                    content = message.clean_content

                    # Get the phone numbers for mentioned users from the file
                    phone_numbers = self.get_phone_numbers()
                    mentioned_phone_numbers = {
                        user_id: phone_numbers.get(user_id)
                        for user_id in mentioned_user_ids
                    }

                for user_id, phone_number in mentioned_phone_numbers.items():
                    if phone_number:
                        # Send SMS using Twilio
                        self.send_sms(phone_number, channel, content, message.author.name)
                        await channel.send('TDUAS: SMS sent to user.')

    def get_phone_numbers(self):
        phone_numbers = {}
        with open(PHONE_NUMBER_FILE, 'r') as file:
            for line in file:
                user_id, phone_number = line.strip().split(':')
                phone_numbers[user_id] = phone_number
        return phone_numbers

    def send_sms(self, phone_number, channel, content, sender_name):
        message = f'TDUAS:\n{channel} - {sender_name}\n{content}'
        
        # Send an SMS using Twilio
        client.messages.create(
            body=message,
            from_=TWILIO_PHONE_NUMBER,
            to=phone_number
        )

async def setup(bot):
    await bot.add_cog(MessageListener(bot))