import os 
import re
import logging

import discord

from utils import utils

USER_ID = os.environ["USER_ID"]
CLIENT_TOKEN = os.environ["CLIENT_TOKEN"]

# SETTING LOGGING
logger = logging.getLogger("sora")
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
logger.addHandler(ch)

# # TWEETS
# reaction_keys = list(tweets.keys())
# regex_patterns = "|".join(reaction_keys)

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    logger.info(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    logger.info(message.content)
    if message.content == USER_ID:
        """
        メンションを飛ばされた場合は過去10件のメッセージ履歴をさかのぼって最新のリンクを参照
        """
        messages = [m.content async for m in message.channel.history(limit=10) if m.author != client.user]
        logger.info(messages)

        urls = [m for m in messages if "https://" in m]
        if urls:
            target_message = urls[0]
            logger.info(target_message)
            await utils.generate_vxlink(message, target_message)
        else:
            await message.channel.send("関係のないことで呼び出さないでください！")

    else:
        """
        メンションを飛ばされていない場合は直近のメッセージのprefixを参照
        """
        if "https://" in message.content:
            target_message = message.content
            await utils.generate_vxlink(message, target_message)
        else:
            pass


client.run(CLIENT_TOKEN)
