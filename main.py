from discord.ext import commands

Token = ""

client = commands.Bot(command_prefix='.')


@client.event
async def on_ready():
    print("Running")

client.load_extension('cogs.bot')

client.run(Token)
print(client.user.name)
