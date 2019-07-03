import discord, aiohttp, configparser, asyncio, json, datetime
from bs4 import BeautifulSoup as bs
from apscheduler.schedulers.asyncio import AsyncIOScheduler

dConfig = configparser.ConfigParser()
dConfig.read('discordconfig.ini')
birbConfig = configparser.ConfigParser()
birbConfig.read('birbconfig.ini')

debug = True

def openBirbDB():
    with open('birbforms.json', 'r') as birblines:
        return json.load(birblines)

birbDB = openBirbDB()

class discordClient(discord.Client):
    async def on_ready(self):
        print('Logged in as ', self.user)

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

async def birbCheck():
    global debug
    prettyBirb = birb()
    siteContent = await prettyBirb.getSiteContent()
    artisanForm = prettyBirb.checkForForm(siteContent)
    if artisanForm and not artisanForm in birbDB:
        birbDB.append(artisanForm)
        await client.get_channel(518088187789443072).send(content=f"<@&566828640759971860> **B I R B** {artisanForm}")
        with open('birbforms.json', 'w') as birbout:
            if debug:
                print(f"[{datetime.datetime.now()}] DEBUG BIRB FOUND")
            json.dump(birbDB, birbout)
    elif artisanForm and artisanForm in birbDB and debug:
            print(f"[{datetime.datetime.now()}] DEBUG old birb")
    else:
        if debug:
            print(f"[{datetime.datetime.now()}] DEBUG no birb")

sched = AsyncIOScheduler()
sched.add_job(birbCheck, 'interval', seconds=10)
sched.start()

client = discordClient()
client.run(dConfig['discord']['token'])
