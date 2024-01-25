import re
import logging

# SETTING LOGGING
logger = logging.getLogger("utils")
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
logger.addHandler(ch)


async def generate_vxlink(message_obj, url_message):
    """
    urlのprefixによって
    - https://twitter.com or https://x.com
        - vxリンクで投稿しなおし
    - https://nico.ms or https://www.nicovideo.jp
        - 恥ずかしい
    - それ以外
        - pass
    """
    if ("https://twitter.com" in url_message):
        twitter_url = re.search(r"https://twitter.com/.*", url_message).group()
        edited_url = twitter_url.replace("https://twitter.com", "https://vxtwitter.com")
        logger.info(f"edited url: {edited_url}")

        await message_obj.channel.send(edited_url)

    elif ("https://x.com" in url_message):
        twitter_url = re.search(r"https://x.com/.*", url_message).group()
        edited_url = twitter_url.replace("https://x.com", "https://vxtwitter.com")
        logger.info(f"edited url: {edited_url}")

        await message_obj.channel.send(edited_url)

    # nico
    elif ("https://nico.ms" in url_message) or ("https://www.nicovideo.jp" in url_message):
        await message_obj.channel.send('淫夢は恥ずかしいですよ！')

    else:
        pass

    return None