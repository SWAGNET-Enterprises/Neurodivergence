from discord.ext import commands
import openai

print('Loading ChatGPT...')

# OpenAI API credentials
openai.api_key = 'token'

messages = [ {"role": "system", "content": "You are a fun chatbot named Neurodivergence in a Discord server called The Drain."} ]
persona_programmer = [ {"role": "system", "content": "In all my following prompts I want you to act as my personal programming tutor"} ]
persona_chef = [ {"role": "system", "content": "I require someone who can suggest delicious recipes that includes foods which are nutritionally beneficial but also easy & not time consuming enough therefore suitable for busy people like us among other factors such as cost effectiveness so overall dish ends up being healthy yet economical at same time!"} ]
persona_mechanic = [ {"role": "system", "content": "Need somebody with expertise on automobiles regarding troubleshooting solutions like; diagnosing problems/errors present both visually & within engine parts in order to figure out what's causing them (like lack of oil or power issues) & suggest required replacements while recording down details such fuel consumption type etc."} ]

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

@commands.command()
async def mechanic(ctx, *, user_input):
    def construct_response():
        gpt3_response = openai.ChatCompletion.create(
                          model="gpt-4", # can change to 'text-davinci-002' if you prefer
                          messages=[
                                    {
                                        "role": "system",
                                        "content": "Need somebody with expertise on automobiles regarding troubleshooting solutions like; diagnosing problems/errors present both visually & within engine parts in order to figure out what's causing them (like lack of oil or power issues) & suggest required replacements while recording down details such fuel consumption type etc."
                                    },
                                    {
                                        "role": "user",
                                        "content": user_input
                                    }
                                 ])
        return gpt3_response.choices[0].message['content']

    response = construct_response()
    await ctx.send(response)

async def setup(bot):
    await bot.add_cog(MentionedBot(bot))
    bot.add_command(mechanic)