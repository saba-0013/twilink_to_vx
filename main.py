import os 
import re
import logging

import discord

USER_ID = os.environ["USER_ID"]
CLIENT_TOKEN = os.environ["CLIENT_TOKEN"]

# SETTING LOGGING
logger = logging.getLogger("sora")
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
logger.addHandler(ch)

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    logger.info(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.content == USER_ID:
        messages = [m.content async for m in message.channel.history(limit=10) if m.author != client.user]
        logger.info(messages)

        urls = [m for m in messages if "https://" in m]
        target_message = urls[0]
        logger.info(target_message)

        if ("https://twitter.com" in target_message):
            twitter_url = re.search(r"https://twitter.com/.*", target_message).group()
            edited_url = twitter_url.replace("https://twitter.com", "https://vxtwitter.com")
            logger.info(f"edited url: {edited_url}")

            await message.channel.send(edited_url)
        elif ("https://x.com" in target_message):
            twitter_url = re.search(r"https://x.com/.*", target_message).group()
            edited_url = twitter_url.replace("https://x.com", "https://vxtwitter.com")
            logger.info(f"edited url: {edited_url}")

            await message.channel.send(edited_url)
        # nico
        elif ("https://nico.ms" in target_message) or ("https://www.nicovideo.jp" in target_message):
            await message.channel.send('淫夢は恥ずかしいですよ！')
        else:
            await message.channel.send("関係のないことで呼び出さないでください！")
    else:
        pass

client.run(CLIENT_TOKEN)
