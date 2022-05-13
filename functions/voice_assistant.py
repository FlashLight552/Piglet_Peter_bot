import asyncio
import random

from aiogram.utils.markdown import hlink

from youtube_search import YoutubeSearch
from ytmusicapi import YTMusic
from googletrans import Translator
from pyowm import OWM

from functions.zenon import zenon
from config.config import OPEN_WEATHER_TOKEN, DISCORD_CHAT_ID
from functions.sql import Database



def get_weather(*args):
    if args[0][1:]:
        try:
            city = f'{args[0][1]}, {args[0][2]}'
        except:
            city = f'{args[0][1]}'
       
    owm = OWM(OPEN_WEATHER_TOKEN)
    mgr = owm.weather_manager()
    observation = mgr.weather_at_place(city)
    w = observation.weather
    location = observation.location.to_dict()
    g_translate = Translator()

    country_name = location['country']
    city_name = location['name']
    temp = (int(w.temperature('celsius')['temp']))
    temp_feels_like = (int(w.temperature('celsius')['feels_like']))
    wind_speed = float('{:.2f}'.format(w.wind('km_hour')['speed']))
    wind_gust = float('{:.2f}'.format(w.wind('km_hour')['gust']))
    press = (int(float(w.barometric_pressure()['press']) * 0.75006157584566))
    humidity = w.humidity
    weather_status = g_translate.translate(text=w.detailed_status,dest='ru',src='en').text

    weather =   f'{city_name},{country_name}\n'\
                f'{weather_status.title()}\n'\
                f'Температура:{temp}°C\nОщущается: {temp_feels_like}°C\n'\
                f'Скорость ветра: {wind_speed}km/h\nПорывы ветра: {wind_gust}km/h\n'\
                f'Давление: {press}mm\nВлажность: {humidity}%'

    return weather


def toss_coin(*args):
    coin = ('Орел','Решка')
    return (random.choice(coin))


def search_on_youtube_music(search):        
        ytmusic = YTMusic()
        search_result = ytmusic.search(search, filter='songs')
        url_list = list()
        for item in search_result:
            videoid = item['videoId']
            url = f'https://music.youtube.com/watch?v={videoid}'
            url_list.append(url)
        return url_list


def discord_youtube_music_song(*args):    
    if args[0][1:]:
        search = ''
        for item in args[0][1:]:
            search += f'{item} '

    result = search_on_youtube_music(search)[0]
    
    db = Database()
    token = db.user_data_request(args[0][0], 'ds_token')
    if token:
        client = zenon.Client(token)
        client.send_message(DISCORD_CHAT_ID, f'!! {result}')

        return search
    else:
        return 'Для начала добавь свой Discord token: \n/discord_token "TOKEN"'


def discord_youtube_music_playlist(*args):    
    if args[0][1:]:
        search = ''
        for item in args[0][1:]:
            search += f'{item} '
    result = search_on_youtube_music(search)
    
    db = Database()
    token = db.user_data_request(args[0][0], 'ds_token')
    if token:
        client = zenon.Client(token)
        for i in range(5):
            item = result[i]
            client.send_message(DISCORD_CHAT_ID, f'!! {item}')
            asyncio.sleep(1)
        return search
    else: 
        return 'Для начала добавь свой Discord token: \n/discord_token "TOKEN"'


def search_on_youtube(*args):
    if args[0][1:]:
        search = ''
        for item in args[0][1:]:
            search += f'{item} '
    
        search_result = YoutubeSearch(f'{search}', max_results=5).to_dict()
        result = ''
        i = 1

        for item in search_result:
            id = item['id']
            title = item['title']
            url = f'https://www.youtube.com/watch?v={id}'
            result += f'{i}. {hlink(title, url)}\n'
            i += 1
        return result


def execute_command(command_name: str, *args: list):
    for key in commands.keys():
        if command_name in key:
            return commands[key](*args)


commands = {
    ("video", "youtube", "ютуб", "видео", "відео"): search_on_youtube,
    ("песня", "song", "трек"): discord_youtube_music_song,
    ("плейлист", "playlist"): discord_youtube_music_playlist,
    ("weather", "forecast", "погода", "погода"): get_weather,
    ("toss", "мотенка", "монета", "подбрось", "монета", "підкинь", "подкинь"): toss_coin,
}


def assistant(user_id, voice_input:str):
    try:
        split_input = voice_input.split()
        command = split_input[0].lower()
        command_param = split_input[1:]
        command_param.insert(0, user_id)
        return execute_command(command, command_param)
    except:
        return execute_command(None, None)






    


