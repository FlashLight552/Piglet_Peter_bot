import asyncio
from shazamio import Shazam
import json


async def main():
    shazam = Shazam()
    out = await shazam.recognize_song('downloads/voice_message/AwACAgIAAxkBAAILY2J2ZX-QpcaTb9hxbA-lcqKJ00QfAALRGQACZkmwS64BgrirRKCJJAQ.oga')

    lyrics= ''
    title = out['track']['title']
    subtitle = out['track']['subtitle']
    images = out['track']['images']['coverart']
    for item in out['track']['sections']:
        if item['type'] == 'LYRICS':
             for text in item['text']:
                 lyrics += f'{text}\n'
loop = asyncio.get_event_loop()
loop.run_until_complete(main())