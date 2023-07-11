from discord.ext import commands
import openai

print('Loading ChatGPT...')

# OpenAI API credentials
openai.api_key = 'token'

messages = [ {"role": "system", "content": "You are a fun chatbot named Neurodivergence in a Discord server called The Drain."} ]

class MentionedBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        try:
            if message.author == self.bot.user:
                return

            if self.bot.user.mentioned_in(message):
                # Extract the mentioned user IDs
                mentioned_user_ids = [mention.id for mention in message.mentions]

                # Check if the bot's user ID is among the mentioned user IDs
                if self.bot.user.id in mentioned_user_ids:
                    # Remove the bot's mention from the message content
                    author_id = message.author.id
                    channel = message.channel
                    content = message.content.replace(f'<@!{self.bot.user.id}>', '').strip()

                    # Execute the Python code
                    messages.append(
                        {"role": "user", "content": content},
                    )
                    chat = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo", messages=messages
                    )
                    reply = chat.choices[0].message.content
                    await channel.send(reply)
                    messages.append({"role": "assistant", "content": reply})

        except Exception as e:
            await ctx.send(f'An error occurred: {str(e)}')

async def setup(bot):
    await bot.add_cog(MentionedBot(bot))