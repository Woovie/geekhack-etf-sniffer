import discord, aiohttp, configparser, asyncio
from bs4 import BeautifulSoup as bs

dConfig = configparser.ConfigParser()
dConfig.read('discordconfig.ini')

class discordClient(discord.Client):
    async def on_ready(self):
        print('Logged in as ', self.user)

    async def on_message(self, message):
        if message.author != self.user and message.content == 'birb!tweet':
            await message.channel.send(content="**SQUAK!**")

async def getPkContent():
    async with aiohttp.ClientSession() as session:
        async with session.get('https://geekhack.org/index.php?topic=79513.0') as r:
            if r.status == 200:
                text = await r.read()
    return bs(text.decode('utf-8'), 'html.parser')

client = discordClient()

client.run(dConfig['discord']['token'])
