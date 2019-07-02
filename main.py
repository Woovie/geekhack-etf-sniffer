import discord, aiohttp, configparser, asyncio, re
from bs4 import BeautifulSoup as bs

dConfig = configparser.ConfigParser()
dConfig.read('discordconfig.ini')

class discordClient(discord.Client):
    async def on_ready(self):
        print('Logged in as ', self.user)

    async def on_message(self, message):
        if message.author != self.user and message.content == 'birb!getsite':
            prettyBirb = birb()
            siteContent = await prettyBirb.getSiteContent()
            artisanForm = prettyBirb.checkForForm(siteContent)
            if artisanForm:
                await message.channel.send(content=f"<dawawd@&566828640759971860> **B I R B** {artisanForm}")

class birb():
    async def getSiteContent(a):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://geekhack.org/index.php?topic=79513.0') as r:
                if r.status == 200:
                    text = await r.read()
        return bs(text.decode('utf-8'), 'html.parser')
    def checkForForm(a, siteContent):
        div = siteContent.find(id="msg_2048390")
        for link in div.find_all('a'):
            href = link.get('href')
            if 'forms' in href:
                return href

client = discordClient()
client.run(dConfig['discord']['token'])
